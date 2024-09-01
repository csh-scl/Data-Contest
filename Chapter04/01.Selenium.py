from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pyautogui

#검색하고 싶은 내용 입력받기
keyword = pyautogui.prompt("검색어를 입력하세요 : ")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Chrome 드라이버 초기화
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.naver.com')

driver.implicitly_wait(10)  # 10초 대기
shortcut_items = driver.find_elements(By.CLASS_NAME, 'shortcut_item')

# 네 번째 요소 선택 (인덱스는 0부터 시작하므로 3)
fourth_item = shortcut_items[3]
fourth_item.find_element(By.CLASS_NAME, 'link_service').click()

# 창 전환
main = driver.window_handles
driver.switch_to.window(main[1])  # 여기가 수정된 부분입니다. 새 창으로 전환해야 합니다.

time.sleep(1)  # 페이지 로드 대기

# 버튼 클릭
try:
    time.sleep(1)
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._targetBanner_button_1u8dJ._targetBanner_close_2F4H0'))
    )
    close_button.click()
except Exception as e:
    print(f"버튼 클릭 오류: {e}")

# 검색하고 싶은 데이터 입력받기
# time.sleep(2)
# driver.find_element(By.CLASS_NAME, "_combineHeader_expansion_search_button_u3JIl N=a:gnb.schopen").click()

# Class를 선택할 때 띄어쓰기가 들어있는 경우, CSS SELECTOR로 선택해주어야 한다.
try:
    time.sleep(1)
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._combineHeader_expansion_search_button_u3JIl'))
    )
    search_button.click()
except Exception as e:
    print(f"버튼 클릭 오류: {e}")
    
try:
    time.sleep(1)
    InputText = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, 'input_text'))
    )
    # 검색어 넣기
    InputText.send_keys(keyword)
    # 검색
    InputText.send_keys(Keys.ENTER)
    
except Exception as e:
    print("검색 실패 에러 발생")

# 스크롤 전 높이
before_h = driver.execute_script("return window.scrollY")

#무한 스크롤
while True:
    # 맨 아래로 스크롤을 내린다.
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    
    #스크롤 사이 페이지 로딩 시간 추가
    time.sleep(0.5)
    
    #스크롤 이후 높이
    after_h = driver.execute_script("return window.scrollY")
    
    if before_h == after_h:
        break 
    before_h = after_h
    
#상품 정보 div
items = driver.find_elements(By.CLASS_NAME, 'product_info_main__piyRs')
print(f'검색 결과 : {len(items)}개')
