# 传输用户的手机号和密码所需的Header信息
headerLogin={
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

# 为获得 Organization ID 所需的Header信息 eg.5G联创实验室的ID
headerOrgId={
    "X-Service-Id": "organization",
    "client_id": "eplus_app",
    "User-Agent": "SmartOffice/2.6.0 (MuMu;Android6.0.1);",
    "Content-Type": "application/json;charset=UTF-8",
    "Connection": "close",
    "Host":"v2-app.delicloud.com",
    "Accept-Encoding":"gzip"
}

# 为获得用户的原始ID所需的Header信息
headerOriginId={
    "client_id": "eplus_app",
    "Content-Type": "application/json;charset=UTF-8",
    "X-Service-Id": "organization",
    "User-Agent": "SmartOffice/2.6.0 (MuMu;Android6.0.1);",
    "Connection": "close",
    "Host": "v2-app.delicloud.com",
    "Accept-Encoding": "gzip"
}


# 获得所需网址
headerGoal = {
    "client_type": "eplus_app",
    "Content-Type": "application/json",
    "Host": "kq.delicloud.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.11.0"
}