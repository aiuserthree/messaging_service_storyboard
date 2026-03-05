# -*- coding: utf-8 -*-
"""수신번호_업로드_50명.xlsx 양식처럼 10만 건 생성"""
import openpyxl
import random
from datetime import datetime, timedelta

SURNAMES = [
    "김", "이", "박", "최", "정", "강", "조", "윤", "장", "임",
    "한", "오", "서", "신", "권", "황", "안", "송", "류", "전",
    "홍", "고", "문", "양", "손", "배", "백", "허", "유", "남",
    "심", "노", "정", "하", "곽", "성", "차", "주", "우", "구",
    "라", "진", "마", "탁", "위", "길", "연", "표", "제", "함"
]
NAME_CHARS = [
    "민", "준", "서", "윤", "도", "예", "지", "현", "수", "진",
    "영", "호", "성", "재", "민", "지", "수", "현", "정", "미",
    "철", "영", "희", "수", "동", "경", "선", "혜", "은", "아",
    "태", "형", "우", "진", "석", "민", "지", "유", "나", "하"
]
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
GRADES = ["VIP", "프리미엄", "일반", "신규", "골드"]

def random_name():
    surname = random.choice(SURNAMES)
    length = random.choice([2, 3])
    name = "".join(random.choices(NAME_CHARS, k=length))
    return surname + name

def random_phone(used):
    while True:
        mid = random.randint(1000, 9999)
        end = random.randint(1000, 9999)
        num = f"010{mid:04d}{end:04d}"
        if num not in used:
            used.add(num)
            return num

def random_date():
    start = datetime(2023, 1, 1)
    end = datetime(2025, 2, 11)
    delta = (end - start).days
    d = start + timedelta(days=random.randint(0, delta))
    return d.strftime("%Y-%m-%d")

def main():
    template_path = r"c:\Users\ibank\Desktop\spec\수신번호_업로드_50명.xlsx"
    out_path = r"c:\Users\ibank\Desktop\spec\수신번호_업로드_100000명.xlsx"
    n = 100000

    print("양식 로드 중...")
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # 헤더(1행) 유지, 2행부터 데이터 제거
    while ws.max_row > 1:
        ws.delete_rows(2)

    print(f"{n:,}건 생성 중...")
    used_phones = set()
    batch = 10000
    for i in range(n):
        row = [
            random_name(),
            random_phone(used_phones),
            random.choice(CITIES),
            random.choice(GRADES),
            random_date()
        ]
        ws.append(row)
        if (i + 1) % batch == 0:
            print(f"  {i + 1:,} / {n:,}")

    wb.save(out_path)
    print(f"완료: {out_path} ({n:,}건)")

if __name__ == "__main__":
    main()
