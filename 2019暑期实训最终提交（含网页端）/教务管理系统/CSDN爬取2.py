import requests
url = 'http://2547m30z96.wicp.vip:26056/add_course/'
d = {'title': "4", 'school' : 232, 'content': 3, 'img':32,'type': 23, 'course_type' : 23, 'teacher_name':23, 'teacher_avatar':23}


url = 'http://2547m30z96.wicp.vip:26056/course_advise/'
d = {'courseID':4}

r = requests.post(url, data=d)
print(r.text)
