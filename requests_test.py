import requests
# r=requests.get("https://baidu.com")
# print(r.content.decode(r.apparent_encoding))
#
# r = requests.post('http://httpbin.org/post', data={'key':'value'})
# print(r.content.decode(r.apparent_encoding))

header1={
    "X-Service-Id": "userauth",
    "client_id": "eplus_app",
    "User-Agent": "SmartOffice/2.6.0 (MuMu;Android6.0.1);",
    "Connection": "close,",
    "user_id":"",
    "Authorization":"",
    "Content-Type": "application/json;charset=UTF-8",
    "Content-Length": "70",
    "Host": "v2-app.delicloud.com",
    "Accept-Encoding": "gzip"

}

header2={
    "X-Service-Id": "device",
    "client_id": "eplus_app",
    "User-Agent": "SmartOffice/2.6.0 (MuMu;Android6.0.1);",
    "Content-Type": "application/json;charset=UTF-8",
    "Connection": "close",
    "user_id": "551093014559797248",
    "Authorization": "dfcf8d75b777c98516d3f2a29778e55e551143751caa4868e860b7ff7aa38981",
    "Host": "v2-app.delicloud.com",
    "Accept-Encoding": "gzip",
    "If-Modified-Since": "Thu, 09 Mar 2023 12:13:09 GMT"

}

r1 = requests.post("https://v2-app.delicloud.com/api/v2.0/auth/loginMobile HTTP/1.1", headers=header1, data={"password":"1fd918bcc22af079a9a4c1eb61d72305","mobile":"13774182093"})
# print(r.text)
# print(r.content.decode(r.apparent_encoding))
r2 = requests.get("https://v2-app.delicloud.com/api/v2.0/product/group/findAllProductDirectory HTTP/1.1", headers=header2)
print(r2.text)
print(r2.content.decode(r2.apparent_encoding))
