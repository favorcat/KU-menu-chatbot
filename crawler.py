from selenium import webdriver  # 웹수집 자동화를 위한 크롬 드라이버 호출
from selenium.webdriver.common.by import By
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)  # 크롬 드라이버 경로 설정

driver.get("https://www.korea.ac.kr/user/restaurantMenuAllList.do?siteId=university&id=university_050402000000")

today = datetime.today().weekday()
path = f'/html/body/div[4]/div[2]/div[2]/div[2]/div/ul/li[2]/ol[{today+1}]/li/div'

menulist = driver.find_element(By.XPATH,path).text.split('[')
student_menu = menulist[1].split('▶')
staff_menu = menulist[2].split('▶')

date = datetime.today().strftime("%m월 %d일 식단표")
sendText = '❤️' + date + '❤️\n\n'

#학생식당
for i in range(1, len(student_menu)):
  a = student_menu[i]
  s = a.split(':',1)
  if '조식' in a:
    sendText += '1️⃣ 조식\n'
    if '운영없음' in a:
      sendText += '천원의 아침밥 - '
    else:
      sendText += '[운영시간 08:00~09:30]\n천원의 아침밥 - 🪪학생증 지참\n🍴'
  elif '중식' in a:
    sendText += '=\n2️⃣ 중식\n'
    if '운영없음' in a:
      sendText += '👩🏻‍🎓 학생식당 - '
    else:
      sendText += '👩🏻‍🎓 학생식당 - 💰5,000원\n[운영시간 11:00 ~ 13:30]\n🍴'
  else:
    break
  sendText += s[1] + '\n'

#교직원식당
for i in range(1, len(staff_menu)):
  a = staff_menu[i]
  s = a.split(':',1)
  if '중식' in a:
    if '운영없음' in a:
      sendText += '💁 교직원식당 - '
    else:
      sendText += '💁 교직원식당 - 💰6,500원\n[운영시간 11:00 ~ 14:00]\n🍴'
  elif '석식' in a:
    sendText += '=\n3️⃣ 석식\n'
    if '운영없음' in a:
      print("석식운영없음")
      sendText += '💁 교직원식당 - '
    else:
      sendText += '💁 교직원식당 - 💰6,500원\n[운영시간 17:30~19:00]\n🍴'
  sendText += s[1] + '\n'
print(sendText)