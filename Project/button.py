import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QIcon
import pandas as pd
import datetime
from pytz import timezone
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from wordcloud import WordCloud
from urllib.request import urlopen
from bs4 import BeautifulSoup

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        icon_path = r'C:\Users\82104\Desktop\Py_workspace\Project\ThemeImg.jpg'
        self.setWindowIcon(QIcon(icon_path))
        
        # 폰트 파일 경로 설정
        font_path = r'C:\Users\82104\Desktop\Py_workspace\Project\SUIT-Variable.ttf'
        QFontDatabase.addApplicationFont(font_path)

        # 윈도우 설정
        self.setWindowTitle("보고 싶은 랭킹 뉴스를 선택하세요")
        self.setGeometry(0, 0, 450, 300)
        self.setStyleSheet("background-color: white;")

        # 레이아웃 설정 (GridLayout 사용)
        layout = QGridLayout()

        # 버튼 생성
        sympathy_options_korean = ['좋아요', '응원해요', '축하해요', '기대해요', '놀라워요', '슬퍼요']
        background_colors = ['#FFCCCC', '#FFCC99', '#FFFF99', '#CCFF99', '#99FFCC', '#99CCFF']

        positions = [(i, j) for i in range(2) for j in range(3)]

        for position, (option, bg_color) in zip(positions, zip(sympathy_options_korean, background_colors)):
            button = QPushButton(option, self)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    border: none;  
                    border-radius: 50px;
                    font-size: 16px;
                    padding: 15px 20px;
                    color: black;
                    font-weight: bold;  
                    font-family: 'SUIT-Variable';
                }}
                QPushButton:hover {{
                    background-color: #ff6666;
                }}
            """)
            button.setFixedSize(120, 120)
            button.clicked.connect(lambda checked, option=option: self.fetch_news(option))
            layout.addWidget(button, *position, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fetch_news(self, option):
        # 창 닫기
        self.close()

        sympathy_mapping = {
            '좋아요': 'like',
            '응원해요': 'cheer',
            '축하해요': 'congrats',
            '기대해요': 'expect',
            '놀라워요': 'surprise',
            '슬퍼요': 'sad'
        }

        # URL 준비
        url = f'https://entertain.naver.com/ranking/sympathy/{sympathy_mapping[option]}'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

        # 뉴스 정보 가져오기
        li = soup.find_all('li', {'class': '_inc_news_lst3_rank_reply'})
        data = pd.DataFrame(columns=['순위', '공감종류', '기사제목', '기사링크', '기사내용', '공감수', '수집일자'])

        for index_l in range(len(li)):
            rank = li[index_l].find('em', {'class': 'blind'}).text
            title = li[index_l].find('a', {'class': 'tit'}).text
            summary = li[index_l].find('p', {'class': 'summary'}).text
            link = li[index_l].find('a', {'class': 'tit'}).attrs['href']
            temp_cnt = li[index_l].find('a', {'class': 'likeitnews_item_likeit'}).text
            cnt = re.sub('[^0-9]', '', temp_cnt)

            temp_df = pd.DataFrame({'순위': rank,
                                    '공감종류': sympathy_mapping[option],
                                    '기사제목': title,
                                    '기사링크': link,
                                    '기사내용': summary,
                                    '공감수': cnt,
                                    '수집일자': datetime.datetime.now(timezone('Asia/Seoul'))},
                                   index=[0])

            data = pd.concat([data, temp_df], ignore_index=True)
        
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        formatted_date = now.strftime('%Y%m%d_%H%M')  # 'YYYYMMDD_HHMM' 형식으로 포맷팅
        # 파일명 생성
        file_name = f'네이버_연예공감별_랭킹뉴스_{sympathy_mapping[option]}_{formatted_date}.csv'

        # CSV 파일로 저장
        data.to_csv(file_name, encoding='utf-8-sig', index=False)

        print(f"데이터가 {file_name}에 저장되었습니다.")
       
        
        # 워드 클라우드 생성
        text = ' '.join(data['기사내용'].astype(str))

        font_path = r'C:\Users\82104\Desktop\Py_workspace\Project\BMDOHYEON_ttf.ttf'
        wc = WordCloud(width=1500, height=1000, background_color='white', font_path=font_path).generate(text)

        # Matplotlib Figure 생성
        self.figure = plt.figure(figsize=(10, 7))
        self.canvas = FigureCanvas(self.figure)

        # 워드 클라우드 이미지 출력
        plt.axis('off')
        plt.imshow(wc, interpolation='bilinear')

        # 마우스 휠 이벤트 연결
        self.figure.canvas.mpl_connect('scroll_event', self.on_scroll)

        
        
        # 이미지 표시
        plt.show()

    def on_scroll(self, event):
        ax = self.figure.axes[0]
        
        # 현재 중심점을 기준으로 줌
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # 줌 인/아웃 비율 설정
        scale_factor = 1.1 if event.button == 'up' else 0.9
        
        # 중심점 계산
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        
        # 새로운 x, y 범위 설정
        new_xlim = [(x_center - (x_center - x) / scale_factor) for x in xlim]
        new_ylim = [(y_center - (y_center - y) / scale_factor) for y in ylim]
        
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        
        self.figure.canvas.draw()

# PyQt 앱 실행
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
