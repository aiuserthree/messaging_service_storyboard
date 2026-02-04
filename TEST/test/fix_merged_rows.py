# -*- coding: utf-8 -*-
"""붙어버린 테이블 행을 다시 줄 단위로 복구"""
import re

path = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# " ... | | | | | | | | || 2 | TS-01-002 | ..." 처럼 붙은 것을 " ... | | | | | | | | |\n| 2 | TS-01-002 | ..." 로 분리
content = re.sub(r"\|\|\s*(\d+)\s*\|\s*", r"|\n| \1 | ", content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Merged rows fixed.")
