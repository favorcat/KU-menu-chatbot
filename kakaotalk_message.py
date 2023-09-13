import requests
import json

# 저장된 refresh_token 불러와서 엑세스 토큰 갱신하기
with open("kakao_code.json", "r",encoding="utf-8") as fp:
    json_data = json.load(fp)
    refresh_token = json_data['refresh_token']
url = "https://kauth.kakao.com/oauth/token"
header = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "refresh_token",
    "client_id": "REST API 키",
    "refresh_token": refresh_token
}
response = requests.post(url, headers=header, data=data)
tokens = response.json()
# 갱신한 엑세스 토큰 저장하기
json_data['access_token'] = tokens['access_token']
with open("kakao_code.json", "w") as fp:
    json.dump(json_data, fp)
access_token = tokens['access_token']

# 친구 목록 불러오기
with open("uuid.json", "r") as fl:
  friends_list = json.load(fl)

# 친구들에게 카톡 메세지 보내기
for i in range(1,len(friends_list)):
  friend_id = friends_list[i]["uuid"]
  url = 'https://kapi.kakao.com/v1/api/talk/friends/message/default/send'
  header = {
      # 엑세스 토큰
      "Authorization": "Bearer " + access_token
  }
  data = {
  'receiver_uuids': '["{}"]'.format(friend_id),
      "template_object": json.dumps({
          "object_type":"text",
          "text":"보낼 메세지",
          "link":{
              "web_url" : "https://www.korea.ac.kr/user/restaurantMenuAllList.do?siteId=university&id=university_050402000000",
              "mobile_web_url" : "https://www.korea.ac.kr/user/restaurantMenuAllList.do?siteId=university&id=university_050402000000"
          },
          "button_title": "식단표"
      })
  }
  response = requests.post(url, headers=header, data=data)