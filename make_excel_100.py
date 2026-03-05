# -*- coding: utf-8 -*-
"""수신번호 업로드 양식 100명 - 이름, 휴대폰, 변수1, 변수2, 변수3 모두 채움"""
import random
import openpyxl
from datetime import datetime, timedelta

# 한글 이름 (성 + 이름 조합)
LAST = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍"]
FIRST1 = ["민", "준", "서", "도", "시", "재", "지", "현", "수", "성", "예", "하", "우", "진", "영", "수", "은", "지", "유", "다"]
FIRST2 = ["준", "우", "현", "영", "호", "수", "민", "진", "희", "성", "윤", "아", "연", "정", "원", "빈", "율", "서", "인", "후"]

# 변수1: 지역/주소 스타일
ADDRS = [
    "서울시 강남구", "서울시 서초구", "서울시 송파구", "서울시 마포구", "서울시 영등포구",
    "부산시 해운대구", "부산시 수영구", "부산시 남구", "인천시 남동구", "인천시 부평구",
    "대구시 수성구", "대구시 달서구", "광주시 서구", "대전시 서구", "울산시 남구",
    "세종시 나성동", "경기도 성남시", "경기도 수원시", "경기도 고양시", "경기도 용인시",
    "강원도 춘천시", "충청북도 청주시", "충청남도 천안시", "전북 전주시", "전남 목포시",
    "경북 포항시", "경남 창원시", "제주시 연동"
]

# 변수2: 등급/구분
GRADES = ["VIP", "일반", "우수", "골드", "실버", "프리미엄", "스탠다드"]

def random_name():
    last = random.choice(LAST)
    if random.random() < 0.5:
        first = random.choice(FIRST1) + random.choice(FIRST2)
    else:
        first = random.choice(FIRST1) + random.choice(FIRST2)
    return last + first

def random_phone():
    return "010" + f"{random.randint(1000,9999)}{random.randint(1000,9999)}"

def random_date():
    d = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 400))
    return d.strftime("%Y-%m-%d")

out_path = r"c:\Users\ibank\Desktop\spec\수신번호_업로드_100명.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "수신번호"

# 헤더
ws.append(["이름", "휴대폰", "변수1", "변수2", "변수3"])

# 100명 데이터 (이름 중복 방지 위해 set 사용)
seen_phones = set()
for _ in range(100):
    while True:
        phone = random_phone()
        if phone not in seen_phones:
            seen_phones.add(phone)
            break
    row = [
        random_name(),
        phone,
        random.choice(ADDRS),
        random.choice(GRADES),
        random_date()
    ]
    ws.append(row)

wb.save(out_path)
print(f"완료: 100명 데이터(이름·휴대폰·변수1·변수2·변수3) → {out_path}")
