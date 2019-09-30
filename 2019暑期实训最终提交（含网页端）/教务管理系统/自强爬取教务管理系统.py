# -*- coding: utf-8 -*-

import logging

from django.utils import timezone
import datetime
from django.conf import settings
from rest_framework import serializers

from lib.rest_framework import validators
from lib.education import login_new as education_login
from lib.education.exceptions import EducationCrash, EducationPasswordError, EducationCaptchaError
from lib.information import login_information as information_login
from lib.information.exceptions import InformationCrash, InformationPasswordError
from lib.library import login as library_login
from lib.library.exceptions import LibraryCrash, LibraryPasswordError
from app.wifi.tasks import ruijie_get_status_task  # 此处违反了APP的依赖原则，日后再改（如果你不幸看到了这句话，那么加油吧骚年，快去改╮(╯▽╰)╭）
from lib.wifi.exceptions import (
    RuijieUserDoesNotExistOrPasswordError, RuijieCaptchaError, RuijieSessionExpired, RuijieCrash, RuijieUnknownError
)
from lib.wifi import STATUS_RESUME, STATUS_SUSPEND, STATUS_UNKNOWN
from lib.sport import login as sport_login
from lib.sport.exceptions import SportCrash, SportPasswordError
from system.authtoken.models import Token
from system.authtoken.utils import Permission, check_wifi_status
from system.user.models import WhuUser

logger = logging.getLogger(__name__)


class GetAuthTokenSerializer(serializers.Serializer):
    default_error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid'
    }

    sid = serializers.CharField(
        error_messages=default_error_messages,
        validators=[validators.StudentID()]
    )
    binding_type = serializers.IntegerField(
        error_messages=default_error_messages,
        validators=[validators.NumericList('binding type', [x[0] for x in WhuUser.TYPE])]
    )
    device_iden = serializers.CharField(
        validators=[validators.MaxLength('device identifier', settings.DEVICE_IDEN_MAX_LEN)],
        required=False,
    )
    pwd_edu = serializers.CharField(
        validators=[validators.MaxLength('educational password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_info = serializers.CharField(
        validators=[validators.MaxLength('information password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_lib = serializers.CharField(
        validators=[validators.MaxLength('library password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_wifi = serializers.CharField(
        validators=[validators.MaxLength('wifi password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_sport = serializers.CharField(
        validators=[validators.MaxLength('sport password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    check = serializers.IntegerField(
        validators=[validators.NumericList('check flag', [0, 1, 2])],
        default=1
    )

    def validate(self, data):
        sid = data.get('sid')
        binding_type = data.get('binding_type')
        device_iden = data.get('device_iden')
        pwd_edu = data.get('pwd_edu')
        pwd_info = data.get('pwd_info')
        pwd_lib = data.get('pwd_lib')
        pwd_wifi = data.get('pwd_wifi')
        pwd_sport = data.get('pwd_sport')
        check = data.get('check')

        if not pwd_edu and not pwd_info and not pwd_lib and not pwd_wifi and not pwd_sport:
            raise serializers.ValidationError('must provide at least one password')
        if binding_type in [WhuUser.TYPE_APP_ANDROID, WhuUser.TYPE_APP_IOS]:
            if not device_iden:  # 移动端设备必须提供设备标识符
                raise serializers.ValidationError('mobile device must provide device identifier')
        else:
            device_iden = None

        validation_messages = []
        if check == 0:
            user = WhuUser.manager.get(sid=sid, binding_type=binding_type, device_iden=device_iden)
            if not user:
                raise serializers.ValidationError('the user you requested does not exist, you need to bind it first')

            if user.pwd_edu and pwd_edu and pwd_edu != user.pwd_edu:
                validation_messages.append('education password error')
            elif not user.pwd_edu and pwd_edu:
                validation_messages.append('the user\'s educational system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_info and pwd_info and pwd_info != user.pwd_info:
                validation_messages.append('information password error')
            elif not user.pwd_info and pwd_info:
                validation_messages.append('the user\'s information system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_lib and pwd_lib and pwd_lib != user.pwd_lib:
                validation_messages.append('library password error')
            elif not user.pwd_lib and pwd_lib:
                validation_messages.append('the user\'s library system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_sport and pwd_sport and pwd_sport != user.pwd_sport:
                validation_messages.append('sport password error')
            elif not user.pwd_sport and pwd_sport:
                validation_messages.append('the user\'s sport system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_wifi and pwd_wifi and pwd_wifi != user.pwd_wifi:
                validation_messages.append('wifi password error')
            elif not user.pwd_wifi and pwd_wifi:
                validation_messages.append('the user\'s wifi system password is not stored in the system, you '
                                           'need to bind it first')

            if validation_messages:
                raise serializers.ValidationError(validation_messages)
        elif check == 1:
            if pwd_edu:  # 验证教务密码
                try:
                    education_login(sid=sid, pwd=pwd_edu, use_cache=False)
                except EducationPasswordError:
                    validation_messages.append('education password error')
                except EducationCaptchaError:
                    validation_messages.append('education captcha error, please try again')
                except EducationCrash:
                    validation_messages.append('education system is not available now')
            if pwd_info:  # 验证信息门户密码
                try:
                    information_login(sid=sid, pwd=pwd_info)
                except InformationPasswordError:
                    validation_messages.append('information password error')
                except InformationCrash:
                    validation_messages.append('information system is not available now')
            if pwd_lib:  # 验证图书馆密码
                try:
                    library_login(sid=sid, pwd=pwd_lib)
                except LibraryPasswordError:
                    validation_messages.append('library password error')
                except LibraryCrash:
                    validation_messages.append('library system is not available now')
            if pwd_wifi:  # 验证校园网密码
                status, reason = check_wifi_status(sid=sid, pwd=pwd_wifi)
                if status is False:
                    validation_messages.append(reason)
            if pwd_sport:  # 验证体育部密码
                try:
                    sport_login(sid=sid, pwd=pwd_sport)
                except SportPasswordError:
                    validation_messages.append('sport password error')
                except SportCrash:
                    validation_messages.append('sport system is not available now')

            if validation_messages:
                raise serializers.ValidationError(validation_messages)

            # 将已通过验证的密码更新现有密码
            user = WhuUser.manager.add_or_update(
                sid=sid,
                binding_type=binding_type,
                device_iden=device_iden,
                pwd_edu=pwd_edu,
                pwd_info=pwd_info,
                pwd_lib=pwd_lib,
                pwd_wifi=pwd_wifi,
                pwd_sport=pwd_sport,
            )
        else:
            # 不做任何检查，直接更新
            user = WhuUser.manager.add_or_update(
                sid=sid,
                binding_type=binding_type,
                device_iden=device_iden,
                pwd_edu=pwd_edu,
                pwd_info=pwd_info,
                pwd_lib=pwd_lib,
                pwd_wifi=pwd_wifi,
                pwd_sport=pwd_sport,
            )

        permission = Permission.make_permission(
            pwd_edu=pwd_edu,
            pwd_info=pwd_info,
            pwd_lib=pwd_lib,
            pwd_wifi=pwd_wifi,
            pwd_sport=pwd_sport,
        )
        data['user'] = user, permission

        return data


class RefreshAuthTokenSerializer(serializers.Serializer):
    default_error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid'
    }

    token = serializers.CharField()
    refresh_token = serializers.CharField()

    def validate(self, data):
        token = data.get('token')
        refresh_token = data.get('refresh_token')

        token = Token.manager.get(key=token)
        utc_now = timezone.now()
        if not token:
            token = data.get('token')
            token = Token.manager.get(cache_key=token)
            if not token:
                raise serializers.ValidationError('invalid token')
            if token.created < utc_now - datetime.timedelta(seconds=30):
                raise serializers.ValidationError('invalid token')
            if refresh_token != token.cache_rkey:
                raise serializers.ValidationError('invalid refresh token')
            data['use_rkey'] = True
        else:
            if refresh_token != token.rkey:
                raise serializers.ValidationError('invalid refresh token')
            if token.created < utc_now - datetime.timedelta(seconds=30):
                data['use_rkey'] = False
            else:
                data['use_rkey'] = True

        data['token'] = token
        return data


class TokenUpdatePermissionsSerializer(serializers.Serializer):
    default_error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid'
    }

    token = serializers.CharField()
    refresh_token = serializers.CharField()
    pwd_edu = serializers.CharField(
        validators=[validators.MaxLength('educational password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_info = serializers.CharField(
        validators=[validators.MaxLength('information password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_lib = serializers.CharField(
        validators=[validators.MaxLength('library password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_wifi = serializers.CharField(
        validators=[validators.MaxLength('wifi password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    pwd_sport = serializers.CharField(
        validators=[validators.MaxLength('sport password', settings.PASSWORD_MAX_LEN)],
        required=False
    )
    check = serializers.IntegerField(
        validators=[validators.NumericList('check flag', [0, 1, 2])]
    )

    def validate(self, data):
        token = data.get('token')
        refresh_token = data.get('refresh_token')
        pwd_edu = data.get('pwd_edu')
        pwd_info = data.get('pwd_info')
        pwd_lib = data.get('pwd_lib')
        pwd_wifi = data.get('pwd_wifi')
        pwd_sport = data.get('pwd_sport')
        check = data.get('check')

        token = Token.manager.get(key=token)
        if not token:
            raise serializers.ValidationError('invalid token')
        if refresh_token != token.rkey:
            raise serializers.ValidationError('invalid refresh token')
        user = token.user
        sid = user.sid

        validation_messages = []
        if check == 1:
            if pwd_edu:  # 验证教务密码
                try:
                    education_login(sid=sid, pwd=pwd_edu, use_cache=False)
                except EducationPasswordError:
                    validation_messages.append('education password error')
                except EducationCaptchaError:
                    validation_messages.append('education captcha error, please try again')
                except EducationCrash:
                    validation_messages.append('education system is not available now')
            if pwd_info:  # 验证信息门户密码
                try:
                    information_login(sid=sid, pwd=pwd_info)
                except InformationPasswordError:
                    validation_messages.append('information password error')
                except InformationCrash:
                    validation_messages.append('information system is not available now')
            if pwd_lib:  # 验证图书馆密码
                try:
                    library_login(sid=sid, pwd=pwd_lib)
                except LibraryPasswordError:
                    validation_messages.append('library password error')
                except LibraryCrash:
                    validation_messages.append('library system is not available now')
            if pwd_wifi:  # 验证校园网密码
                status, reason = check_wifi_status(sid=sid, pwd=pwd_wifi)
                if status is False:
                    validation_messages.append(reason)
            if pwd_sport:
                try:
                    sport_login(sid=sid, pwd=pwd_sport)
                except SportPasswordError:
                    validation_messages.append('sport password error')
                except SportCrash:
                    validation_messages.append('sport system is not available now')

            if validation_messages:
                raise serializers.ValidationError(validation_messages)
        elif check == 0:
            if user.pwd_edu and pwd_edu and pwd_edu != user.pwd_edu:
                validation_messages.append('education password error')
            elif not user.pwd_edu and pwd_edu:
                validation_messages.append('the user\'s educational system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_info and pwd_info and pwd_info != user.pwd_info:
                validation_messages.append('information password error')
            elif not user.pwd_info and pwd_info:
                validation_messages.append('the user\'s information system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_lib and pwd_lib and pwd_lib != user.pwd_lib:
                validation_messages.append('library password error')
            elif not user.pwd_lib and pwd_lib:
                validation_messages.append('the user\'s library system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_wifi and pwd_wifi and pwd_wifi != user.pwd_wifi:
                validation_messages.append('wifi password error')
            elif not user.pwd_wifi and pwd_wifi:
                validation_messages.append('the user\'s wifi system password is not stored in the system, you '
                                           'need to bind it first')

            if user.pwd_sport and pwd_sport and pwd_sport != user.pwd_sport:
                validation_messages.append('sport password error')
            elif not user.pwd_sport and pwd_sport:
                validation_messages.append('the user\'s sport system password is not stored in the system, you '
                                           'need to bind it first')

            if validation_messages:
                raise serializers.ValidationError(validation_messages)

        data['token_model'] = token  # 在 validated_data 中导入 Token model 实例，避免在 views 中重复查询
        return data


class TokenDeletePermissionsSerializer(serializers.Serializer):
    default_error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid'
    }

    token = serializers.CharField()
    refresh_token = serializers.CharField()
    system_abbr = serializers.CharField(
        validators=[validators.MaxLength('system name abbreviation', settings.SYSTEM_NAME_ABBR_MAX_LEN)],
    )

    def validate_system_abbr(self, value):
        """
        验证系统名称缩写词的字符串并返回处理好的列表
        :param value: str object
        :return: list object
        """
        available_abbr = ['edu', 'info', 'lib', 'wifi']
        abbr_list = value.split(',')
        for index, abbr in enumerate(abbr_list):
            abbr_list[index] = abbr.strip()
        for abbr in abbr_list:
            if abbr and abbr not in available_abbr:
                raise serializers.ValidationError(self.error_messages['invalid'])
        return filter(None, abbr_list)

    def validate(self, data):
        token = data.get('token')
        refresh_token = data.get('refresh_token')

        token = Token.manager.get(key=token)
        if not token:
            raise serializers.ValidationError('invalid token')
        if refresh_token != token.rkey:
            raise serializers.ValidationError('invalid refresh token')

        data['token_model'] = token  # 在 validated_data 中导入 Token model 实例，避免在 views 中重复查询
        return data
