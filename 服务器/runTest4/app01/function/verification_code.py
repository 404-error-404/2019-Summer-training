# -*- coding: utf-8 -*-
import random
def generate_verification_code():
    ''' 随机生成6位的验证码 '''
    code_list = []
    for i in range(6):
        random_num = random.randint(0, 9)  # 随机生成0-9的数字
        code_list.append(str(random_num))
        verification_code = ''.join(code_list)
    return verification_code