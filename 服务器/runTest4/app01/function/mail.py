import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from app01.function.verification_code import generate_verification_code

def mail(receiver):
    sender = '1791781644@qq.com'  # 发件人邮箱账号
    # TODO 上传代码时要记得把授权码删除
    pass_code = ''  # 发件人邮箱授权码
    verification_code = generate_verification_code()
    try:
        content = '欢迎您使用“大学公共课程共享资源管理平台”，您本次的验证码为%s。使用该服务时还请遵守相关法律法规。\n如果不是本人操作请忽略这封电子邮件。谢谢!' %verification_code
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = formataddr(["一个苦命的码农", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["可爱的你", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "欢迎您使用大学公共课程共享资源管理平台"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(sender, pass_code)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的返回False
        return False
    return verification_code  # 正确执行就返回验证码
