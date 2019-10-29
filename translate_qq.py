import json
import urllib.request
import urllib.parse
import time
time_chuo=str(int(time.time()*1000))
zzz=input('请输入中文:')
data={
    "source": "auto",
    "target": "en",
    "sourceText": zzz,
    "qtv": "fb7019db18d2efd2",
    "qtk": "tMDoh4iZnYF7a6MshJPtOvA7vXOMj0j+MUFcj6Ogl94MkIim6UUYl/KC4sv03GvVBnb2t6BbmOnew9ASvvKDh+sjJh7tOjLhy1W1M/S/xofJ469ZnMym2es4NJ2Ux8q3pZ0r/RCLPOPc15BSupGOcQ==",
    "sessionUuid": "translate_uuid" + time_chuo
}
headers={
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "fanyi.qq.com",
    "Origin": "https://fanyi.qq.com",
    "Referer": "https://fanyi.qq.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    # 请求体的长度
    "Content-Length": "288",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "fy_guid=1ebf7009-a752-4e96-9c00-6f1716ff5feb; pgv_info=ssid=s2052501920; ts_refer=www.baidu.com/link; pgv_pvid=6854096010; ts_uid=4010684990; gr_user_id=0d431726-9e54-48b8-9a03-ef467bab3c4f; grwng_uid=42c02436-79da-49fe-b367-4f577cfe293f; 9c118ce09a6fa3f4_gr_session_id=3eed6036-7a72-4c3d-8307-f49cc268ffd1; qtv=fb7019db18d2efd2; qtk=tMDoh4iZnYF7a6MshJPtOvA7vXOMj0j+MUFcj6Ogl94MkIim6UUYl/KC4sv03GvVBnb2t6BbmOnew9ASvvKDh+sjJh7tOjLhy1W1M/S/xofJ469ZnMym2es4NJ2Ux8q3pZ0r/RCLPOPc15BSupGOcQ==; ts_last=fanyi.qq.com/; openCount=2; 9c118ce09a6fa3f4_gr_session_id_3eed6036-7a72-4c3d-8307-f49cc268ffd1=true"
}
data_from=urllib.parse.urlencode(data).encode('utf-8')
headers['Content-Length'] = len(data_from)
request1=urllib.request.Request('https://fanyi.qq.com/api/translate',data=data_from,headers=headers)
response=urllib.request.urlopen(request1)
# 从响应中提取翻译后的结果
json_data = json.loads(response.read())
result = json_data['translate']['records'][0]['targetText']
print(result)

