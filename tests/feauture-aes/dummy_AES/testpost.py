import requests

url = 'http://127.0.0.1:2342/passwd_correct'

data = input('data>>>')
post_json = {'data':data}

r_post = requests.post(url, json=post_json)
print(r_post.text)
