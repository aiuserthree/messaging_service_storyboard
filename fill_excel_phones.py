# -*- coding: utf-8 -*-
"""엑셀 수신번호 양식의 휴대폰 열에 phone_numbers_50000.txt 데이터 채우기"""
import openpyxl

xlsx_path = r"c:\Users\ibank\Downloads\수신번호_업로드_양식 (1).xlsx"
out_path = r"c:\Users\ibank\Downloads\수신번호_업로드_양식_50000명.xlsx"
txt_path = r"c:\Users\ibank\Desktop\spec\phone_numbers_50000.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.read().strip().splitlines()

# 50,000개 번호 (하이픈 제거하여 시트 기존 형식 01012345678 맞춤)
phones = [line.replace("-", "") for line in lines if line]
assert len(phones) == 50000, f"Expected 50000 numbers, got {len(phones)}"

wb = openpyxl.load_workbook(xlsx_path)
ws = wb.active  # 시트: 수신번호
# 1행: 헤더 [이름, 휴대폰, 변수1, 변수2, 변수3] -> 휴대폰 = B열 = col 2
col_phone = 2
for row, num in enumerate(phones, start=2):
    ws.cell(row=row, column=col_phone, value=num)

wb.save(out_path)
print(f"완료: 휴대폰 열에 50,000건 채움 → {out_path}")
