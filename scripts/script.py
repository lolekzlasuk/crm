import requests
import json
import os
image_path = os.path.join(os.getcwd(),'dino.jpg')
# print(image_path)



AUTH_ENDPOINT ="http://localhost:8080/accounts/api/jwt/"
# REFRESH_ENDPOINT ="http://localhost:8080/auth/refresh/"
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT"
    }

data = {
    'username': '3',
    'password': 'Maniek007'
}

# r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
r = requests.post(AUTH_ENDPOINT,json.dumps(data), headers=headers)
# print(r.content)
token = r.json()['token']
headers2 = {
    "Authorization": "JWT " + token,
    "Content-Type": 'application/json'
    # "Content-Type" :"multipart/form-data; boundary=&"
    }
# print(token)
# with open(image_path, 'rb') as r:
#     files = {'file': r}
data2 = {

         'day':'2020-07-08',
         'title':'tesdddt',
         'description':'test'

}

# with open(image_path, 'rb') as image:
#     file_data = {
#     'file': image,
#     }
#     ENDPOINT = "http://localhost:8080/news/api/uploaddocfile/"
#     r2 = requests.post(ENDPOINT,data2, files = file_data, headers=headers2)
#     token2 = r2.json()#['token']
#     print(token2)
ENDPOINT = "http://localhost:8080/news/api/news/12/"
r2 = requests.get(ENDPOINT, headers=headers2)
token2 = r2.json()
print(token2)


#     'token':token
# }
# new_response = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_data), headers=headers)
# new_token = new_response.json()['token']
#
# print(new_token)


# headers = {
#     #'Content-Type': "application/json",
#     "Authorization": "JWT " + token,
# }
# with open(image_path, 'rb') as image:
#             file_data = {
#             'image':image
#             }
#             post_data = {} #json.dumps({"content": ""})
#             posted_response = requests.post(ENDPOINT, data=post_data, headers=headers, files=file_data)
#             print(posted_response.text)


#
# get_endpoint = ENDPOINT + str(12)
#
#
#
# r = requests.get(get_endpoint)
# print(r.text)
#
# r2 = requests.get(ENDPOINT)
# print(r2.status_code)
#
# post_headers = {
#     'content-type': 'application/json'
# }
# post_response = requests.post(ENDPOINT, data=post_data, headers=post_headers)
#
#
# print(post_response.text)













#
# def do_img(method='get',data={}, is_json=True, img_path = None):
#     headers = {}
#     if is_json:
#         headers['content-type'] = 'application/json'
#         data = json.dumps(data)
#     if img_path is not None:
#         with open(image_path, 'rb') as image:
#             file_data = {
#             'image':image
#             }
#             r = requests.request(method, ENDPOINT, data=data , files=file_data, headers=headers)
#     else:
#         r = requests.request(method, ENDPOINT, data=data, headers=headers)
#     print(r.text)
#     print(r.status_code)
#     return r
#
# do_img(method='post', data={'user':1, "content": ""}, is_json=False, img_path = image_path)
#
# def do(method='get',data={}, is_json=True):
#     headers = {}
#     if is_json:
#         headers['content-type'] = 'application/json'
#         data = json.dumps(data)
#     r = requests.request(method, ENDPOINT, data=data, headers=headers)
#     print(r.text)
#     print(r.status_code)
#     return r
#



# do(data={'id':10})
#
# do(method='delete', data={'id':11})
# do(method='put', data={'id':10,"content":"Some new cool content",'user':1})
# do(method='post', data={"content":"Some new cool content",'user':1})
