# 🤖 My GPT

Django와 Hugging Face Transformers를 활용한 AI 웹 서비스입니다.

## 📌 프로젝트 소개

Hugging Face 모델을 이용하여 다음 기능을 제공합니다.

- 😊 감정 분석 (Sentiment Analysis)
- 📝 문서 요약 (Text Summarization)
- 🚨 유해 표현 분석 (Content Moderation)
- 🔍 복합 분석 (감정 분석 + 유해 표현 분석 + 문서 요약)

로그인한 사용자는 최근 분석 기록을 확인할 수 있습니다.

---

## 🛠️ 기술 스택

- Python 3
- Django
- Hugging Face Transformers
- PyTorch
- HTML
- CSS
- JavaScript (Fetch API)

---

## 📂 프로젝트 구조

```
my_gpt/
├── services/
│   ├── sentiment.py
│   ├── summarize.py
│   ├── moderate.py
│   ├── combo.py
│   └── common.py
├── static/
│   ├── css/
│   └── js/
├── templates/
├── models.py
├── views.py
└── urls.py
```

---

## 🚀 실행 방법

### 1. 가상환경 생성

```bash
python -m venv .venv
```

### 2. 가상환경 활성화

Windows

```bash
.venv\Scripts\activate
```

macOS / Linux

```bash
source .venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 마이그레이션

```bash
python manage.py migrate
```

### 5. 서버 실행

```bash
python manage.py runserver
```

---

## ✨ 주요 기능

### 😊 감정 분석

- 영어 문장 감정 분석
- 긍정 / 중립 / 부정 분류
- 신뢰도 제공

### 📝 문서 요약

- 긴 영어 문서 자동 요약
- 원문 길이
- 요약 길이
- 압축률 제공

### 🚨 유해 표현 분석

- Toxic BERT 모델 사용
- 가장 높은 유해 항목 출력
- 모든 항목의 점수 제공

### 🔍 복합 분석

한 번의 요청으로

- 감정 분석
- 유해 표현 분석
- 문서 요약

을 함께 수행합니다.

---

## 👤 로그인 기능

로그인한 사용자는

- 최근 분석 기록 저장
- 최근 5개 기록 조회

기능을 사용할 수 있습니다.

---

## 📷 사용 모델

| 기능           | 모델                                             |
| -------------- | ------------------------------------------------ |
| 감정 분석      | cardiffnlp/twitter-roberta-base-sentiment-latest |
| 문서 요약      | sshleifer/distilbart-cnn-6-6                     |
| 유해 표현 분석 | unitary/toxic-bert                               |
