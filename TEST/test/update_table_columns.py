# -*- coding: utf-8 -*-
"""데이터 행에서 수정/오류 열(8번째) 제거"""
import re

path = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
for line in lines:
    # 테이블 데이터 행: | n | TS-xxx | ... 형태이고, 14개 컬럼이면 8번째(수정/오류) 제거
    if re.match(r"^\|\s*\d+\s*\|\s*TS-", line.strip()):
        parts = line.split(" | ", 8)  # 최대 8번 분리 → 9개 부분 (1~7, 8번째, 9번째~끝)
        if len(parts) >= 9:
            # 8번째(parts[7]) 제거 → 1~7열 + 9~끝
            new_line = " | ".join(parts[:7]) + " | " + parts[8]
            out.append(new_line)
        elif len(parts) == 8:
            rest_after_8 = parts[7].split(" | ", 1)[1] if " | " in parts[7] else ""
            new_line = " | ".join(parts[:7]) + (" | " + rest_after_8 if rest_after_8 else "")
            out.append(new_line)
        else:
            out.append(line)
    else:
        out.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(out)

print("Done: 수정/오류 column removed from data rows.")
