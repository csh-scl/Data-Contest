# 공감대별 연예뉴스를 분석하는 서비스
**네이버 뉴스를 분석해 워드클라우드 제작 (GUI 활용)**

## 설계 구조
1. **데이터 수집**: 네이버 뉴스 API를 통해 연예뉴스 데이터를 수집합니다.
2. **전처리**: 수집된 데이터에서 불필요한 정보를 제거한 후 필요한 데이터만 액셀 파일로 저장합니다.
3. **GUI 구현**: 그래픽 인터페이스(GUI)를 활용해 사용자들이 보고 싶은 연예뉴스 카테고리를 입력받습니다. 
4. **결과 시각화**: 텍스트 데이터를 기반으로 단어 빈도를 계산하고, 이를 시각화하여 워드클라우드를 생성합니다.

## 실행 과정
### **1. 보고싶은 연예뉴스 카테고리 선택**
<img width=500px src=https://github.com/user-attachments/assets/7652b784-7aa5-4b7b-8b36-ed4b56f1bf34/>


### **2. 보고싶은 연예뉴스 카테고리 선택**
마우스 호버 기능 제공 마우스 올릴 시 빨간색 버튼색 변경이 됩니다.
<br>
이번 테스트 : 놀라워요 선택!
<br>
<img width=405px src=https://github.com/user-attachments/assets/6d6a2c53-0c3d-4e9f-b8cc-fa4ca23369ff/>

### **3. 해당 카테고리의 연예기사 액셀 파일로 저장**
<img src=https://github.com/user-attachments/assets/1811f0b3-b903-40e2-b235-f02555dab5bb/>

### **4. 이를 바탕으로 워드클라우드 제작**
<img src=https://github.com/user-attachments/assets/c46e9289-48a9-4253-a5bd-e560afa5dbda/>

## 사용한 기술
- **프로그래밍 언어**: Python
- **라이브러리**:
  - **BeautifulSoup**: 웹 크롤링 및 데이터 수집
  - **Pandas**: 데이터 처리 및 분석
  - **NLTK / KoNLPy**: 자연어 처리 및 텍스트 분석
  - **WordCloud**: 워드클라우드 생성
  - **Matplotlib**: 데이터 시각화
  - **Tkinter / PyQt**: GUI 구현
- **API**: 네이버 뉴스 API
- **기타 도구**: Vs Code (개발 및 테스트)

이 서비스를 통해 사용자는 실시간 연예뉴스를 공감대별 키워드로 쉽게 파악하고, 이를 워드클라우드로 시각화하여 한눈에 확인할 수 있습니다.
