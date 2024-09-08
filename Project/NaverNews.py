import pyautogui
import pandas as pd
import datetime
from pytz import timezone
import re
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from urllib.request import urlopen
from bs4 import BeautifulSoup

# 데이터프레임 생성
data = pd.DataFrame(columns=['순위','공감종류','기사제목','기사링크','기사내용','공감수','수집일자'])

# 네이버 연예 공감별 랭크 뉴스 URL 준비
url_list = ['', '/cheer', '/congrats', '/expect', '/surprise', '/sad']

# 공감별 url 주소 조합
for n in range(len(url_list)):
    url = 'https://entertain.naver.com/ranking/sympathy' + url_list[n]
    sympathy = 'like' if url_list[n] == '' else url_list[n].replace('/', '')

    # html 가져오기
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # 뉴스 정보 가져오기
    li = soup.find_all('li', {'class': '_inc_news_lst3_rank_reply'})

    for index_l in range(len(li)):
        rank = li[index_l].find('em', {'class': 'blind'}).text
        title = li[index_l].find('a', {'class': 'tit'}).text
        summary = li[index_l].find('p', {'class': 'summary'}).text
        link = li[index_l].find('a', {'class': 'tit'}).attrs['href']
        temp_cnt = li[index_l].find('a', {'class': 'likeitnews_item_likeit'}).text
        cnt = re.sub('[^0-9]', '', temp_cnt)

        # 데이터 프레임에 저장
        temp_df = pd.DataFrame({'순위': rank,
                                '공감종류': sympathy,
                                '기사제목': title,
                                '기사링크': link,
                                '기사내용': summary,
                                '공감수': cnt,
                                '수집일자': datetime.datetime.now(timezone('Asia/Seoul'))},
                               index=[0])

        data = pd.concat([data, temp_df], ignore_index=True)

# 공감 종류 선택
# 공감 종류 매핑
sympathy_mapping = {
    'like': '좋아요',
    'cheer': '응원해요',
    'congrats': '축하해요',
    'expect': '기대해요',
    'surprise': '놀라워요',
    'sad': '슬퍼요'
}

# 공감 종류 선택
sympathy_options = data['공감종류'].unique().tolist()
sympathy_options_korean = [sympathy_mapping[sympathy] for sympathy in sympathy_options]

# 사용자에게 공감 종류 선택
choice_korean = pyautogui.confirm('보고 싶은 랭킹 뉴스를 선택하세요:', buttons=sympathy_options_korean)

# 선택한 한국어를 영어로 변환
choice_english = next(key for key, value in sympathy_mapping.items() if value == choice_korean)

# 선택한 공감 뉴스 제목만 텍스트로 만들기
text = ' '.join(li for li in data[data['공감종류'] == choice_english].기사내용.astype(str))


font_path = r'C:\Users\82104\Desktop\Py_workspace\Project\BMDOHYEON_ttf.ttf'
heart_mask = np.array(Image.open('heart_mask.png'))  # 마스크 이미지 파일

wc = WordCloud(width=1000, height=700, background_color='white', font_path=font_path).generate(text)

plt.axis('off')
plt.imshow(wc, interpolation='bilinear')
plt.show()
