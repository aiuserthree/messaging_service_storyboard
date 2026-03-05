# -*- coding: utf-8 -*-
"""10,000개의 임의 한국 휴대폰 번호(010-XXXX-XXXX) 생성"""
import random

def generate_korean_mobile():
    """010 + 8자리 랜덤 숫자 생성 (중복 가능, 임의 데이터용)"""
    middle = random.randint(1000, 9999)
    last = random.randint(1000, 9999)
    return f"010-{middle}-{last}"

count = 60000
numbers = [generate_korean_mobile() for _ in range(count)]

with open("phone_numbers_60000.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(numbers))

print(f"생성 완료: {count}건 → phone_numbers_60000.txt")
