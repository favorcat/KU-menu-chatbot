# 식단표 크롤링
from selenium import webdriver  # 웹수집 자동화를 위한 크롬 드라이버 호출
from selenium.webdriver.common.by import By
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome()  # 크롬 드라이버 경로 설정

driver.get("https://www.korea.ac.kr/user/restaurantMenuAllList.do?siteId=university&id=university_050402000000")

today = datetime.today().weekday()
path = f'/html/body/div[4]/div[2]/div[2]/div[2]/div/ul/li[2]/ol[{today+1}]/li/div'

menulist = driver.find_element(By.XPATH,path).text.split('[')
studnet_menu = menulist[1].split('▶')
staff_menu = menulist[2].split('▶')

#학생식당
student_menulist = '[학생식당] - 5,000원\n'
for i in range(1, len(studnet_menu)):
  student_menulist += "\n▶" + studnet_menu[i]

#교직원식당
staff_menulist = '[교직원식당]\n'
for i in range(1, len(staff_menu)):
  staff_menulist += "\n▶" + staff_menu[i]

sendText = student_menulist + "\n" + staff_menulist

# 카카오톡
import requests
import json

access_token = "REST API 키"

# 친구 목록 불러오기
url = "https://kapi.kakao.com/v1/api/talk/friends"
header = {"Authorization": 'Bearer ' + access_token}
result = json.loads(requests.get(url, headers=header).text)
friends_list = result.get("elements")
for i in range(len(friends_list)):
  friend_id = friends_list[i].get("uuid")

  # 채팅 보내기
  url = 'https://kapi.kakao.com/v1/api/talk/friends/message/default/send'
  headers = {
      # 엑세스 토큰
      "Authorization": "Bearer " + access_token
  }
  data = {
  'receiver_uuids': '["{}"]'.format(friend_id),
      "template_object": json.dumps({
          "object_type":"text",
          "text":"오늘의 식단표\n" + sendText,
          "link":{
              "web_url" : "https://www.korea.ac.kr/user/restaurantMenuAllList.do?siteId=university&id=university_050402000000",
              "mobile_web_url" : "https://www.korea.ac.kr/user/restaurantMenuAllList.do?siteId=university&id=university_050402000000"
          },
          "button_title": "식단표"
      })
  }
  response = requests.post(url, headers=header, data=data)