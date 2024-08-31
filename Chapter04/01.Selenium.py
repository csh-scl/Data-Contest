from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

time.sleep(2)  # 페이지 로드 대기

# 버튼 클릭
try:
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._targetBanner_button_1u8dJ._targetBanner_close_2F4H0'))
    )
    close_button.click()
except Exception as e:
    print(f"버튼 클릭 오류: {e}")

# 드라이버 종료
time.sleep(10)

