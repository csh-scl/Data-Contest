import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QDesktopWidget  # QDesktopWidget를 여기서 가져옵니다.
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 폰트 파일 경로 설정
        font_path = r'C:\Users\82104\Desktop\Py_workspace\Project\BMDOHYEON_ttf.ttf'
        QFontDatabase.addApplicationFont(font_path)  # 폰트 추가

        # 윈도우 설정
        self.setWindowTitle("보고 싶은 랭킹 뉴스를 선택하세요")
        self.setGeometry(0, 0, 450, 300)  # 초기 위치를 (0, 0)으로 설정
        self.setStyleSheet("background-color: white;")  # 배경색 설정

        # 레이아웃 설정 (GridLayout 사용)
        layout = QGridLayout()

        # 버튼 생성
        sympathy_options_korean = ['좋아요', '응원해요', '축하해요', '기대해요', '놀라워요', '슬퍼요']
        background_colors = ['#FFCCCC', '#FFCC99', '#FFFF99', '#CCFF99', '#99FFCC', '#99CCFF']  # 각 버튼의 배경색

        # 3x2 그리드 좌표
        positions = [(i, j) for i in range(2) for j in range(3)]

        for position, (option, bg_color) in zip(positions, zip(sympathy_options_korean, background_colors)):
            button = QPushButton(option, self)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    border: none;  /* 테두리 제거 */
                    border-radius: 50px;
                    font-size: 16px;
                    padding: 15px 20px;  /* 패딩을 늘려 버튼이 더 커지도록 */
                    color: black;
                    font-weight: bold;  
                    font-family: 'BMDOHYEON';  /* 추가한 폰트 적용 */
                }}
                QPushButton:hover {{
                    background-color: #ff6666;
                }}
            """)  # 각 버튼마다 다른 배경색을 설정
            button.setFixedSize(120, 120)  # 버튼 크기를 더 크게 설정 (동그랗게 보이도록)
            layout.addWidget(button, *position, alignment=Qt.AlignCenter)

        # 레이아웃을 위젯에 설정
        self.setLayout(layout)

        # 화면 중앙에 위치시키기
        self.center()

    def center(self):
        qr = self.frameGeometry()  # 현재 창의 크기
        cp = QDesktopWidget().availableGeometry().center()  # 화면 중앙 좌표
        qr.moveCenter(cp)  # 현재 창을 화면 중앙으로 이동
        self.move(qr.topLeft())  # 좌상단 이동

# PyQt 앱 실행
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
