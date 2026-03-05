# -*- coding: utf-8 -*-
"""엑셀 수신번호 양식 휴대폰 열에 60,000건 채우기"""
import random
import openpyxl

def generate_korean_mobile():
    middle = random.randint(1000, 9999)
    last = random.randint(1000, 9999)
    return f"010{middle:04d}{last:04d}"

xlsx_path = r"c:\Users\ibank\Desktop\spec\수신번호_업로드_양식 (1).xlsx"
out_path = r"c:\Users\ibank\Desktop\spec\수신번호_업로드_양식_60000명.xlsx"

phones = [generate_korean_mobile() for _ in range(60000)]

wb = openpyxl.load_workbook(xlsx_path)
ws = wb.active
col_phone = 2  # 휴대폰 = B열
for row, num in enumerate(phones, start=2):
    ws.cell(row=row, column=col_phone, value=num)

wb.save(out_path)
print(f"완료: 휴대폰 열에 60,000건 채움 → {out_path}")
