from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)  # 옵션 추가
driver.get('https://www.naver.com')

driver.implicitly_wait(10)  # 10초 대기
shortcut_items = driver.find_elements(By.CLASS_NAME, 'shortcut_item')

# 네 번째 요소 선택 (인덱스는 0부터 시작하므로 3)
fourth_item = shortcut_items[3]
fourth_item.find_element(By.CLASS_NAME, 'link_service').click()

try:
    continue_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="gnb-header"]/div/div[4]/div/div/button[2]'))
    )

    continue_button.click()  # 버튼 클릭하여 광고 닫기
except Exception as e:
    print(f"요소를 찾을 수 없습니다: {e}")
