# -*- coding: utf-8 -*-
"""수신번호 업로드 양식에 N명 랜덤 데이터 생성 (기본 200명)"""
import openpyxl
import random
import sys
from datetime import datetime, timedelta

# 한국 성씨 (자주 쓰이는 것)
SURNAMES = [
    "김", "이", "박", "최", "정", "강", "조", "윤", "장", "임",
    "한", "오", "서", "신", "권", "황", "안", "송", "류", "전",
    "홍", "고", "문", "양", "손", "배", "백", "허", "유", "남",
    "심", "노", "정", "하", "곽", "성", "차", "주", "우", "구",
    "라", "진", "마", "탁", "위", "길", "연", "표", "제", "함"
]

# 이름 글자 (남녀 혼합)
NAME_CHARS = [
    "민", "준", "서", "윤", "도", "예", "지", "현", "수", "진",
    "영", "호", "성", "재", "민", "지", "수", "현", "정", "미",
    "철", "영", "희", "수", "동", "경", "선", "혜", "은", "아",
    "태", "형", "우", "진", "석", "민", "지", "유", "나", "하"
]

# 지역 (시/구)
CITIES = [
    "서울시 강남구", "서울시 서초구", "서울시 송파구", "서울시 마포구", "서울시 영등포구",
    "서울시 강서구", "서울시 양천구", "서울시 구로구", "서울시 금천구", "서울시 동작구",
    "부산시 해운대구", "부산시 수영구", "부산시 남구", "부산시 동구", "부산시 중구",
    "대구시 수성구", "대구시 달서구", "대구시 북구", "인천시 연수구", "인천시 남동구",
    "광주시 서구", "광주시 북구", "대전시 유성구", "대전시 서구", "대전시 중구",
    "울산시 남구", "세종시", "경기도 수원시", "경기도 성남시", "경기도 고양시",
    "경기도 용인시", "경기도 부천시", "경기도 안양시", "경기도 안산시", "경기도 화성시",
    "강원도 춘천시", "강원도 원주시", "충청북도 청주시", "충청남도 천안시", "전라북도 전주시",
    "전라남도 목포시", "경상북도 포항시", "경상남도 창원시", "제주시", "제주시 서귀포시"
]

# 등급
GRADES = ["VIP", "프리미엄", "일반", "신규", "골드"]

def random_name():
    """랜덤 한국 이름 생성 (2~3글자)"""
    surname = random.choice(SURNAMES)
    length = random.choice([2, 3])
    name = "".join(random.choices(NAME_CHARS, k=length))
    return surname + name

def random_phone(existing):
    """중복 없는 010-XXXX-XXXX 형식 번호 (저장은 010XXXXXXXX)"""
    while True:
        mid = random.randint(1000, 9999)
        end = random.randint(1000, 9999)
        num = f"010{mid}{end}"
        if num not in existing:
            existing.add(num)
            return num

def random_date():
    """2023~2025 사이 랜덤 날짜"""
    start = datetime(2023, 1, 1)
    end = datetime(2025, 2, 5)
    delta = (end - start).days
    d = start + timedelta(days=random.randint(0, delta))
    return d.strftime("%Y-%m-%d")

def main():
    n = 200
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            n = 200
    wb = openpyxl.load_workbook("수신번호_업로드_양식 (1).xlsx")
    ws = wb.active
    while ws.max_row > 1:
        ws.delete_rows(2)
    used_phones = set()
    for i in range(n):
        row = [
            random_name(),
            random_phone(used_phones),
            random.choice(CITIES),
            random.choice(GRADES),
            random_date()
        ]
        ws.append(row)
    out_path = f"수신번호_업로드_{n}명.xlsx"
    wb.save(out_path)
    print(f"저장 완료: {out_path} ({n}명)")

if __name__ == "__main__":
    main()
