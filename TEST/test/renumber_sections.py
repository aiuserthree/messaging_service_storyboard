# -*- coding: utf-8 -*-
"""섹션별 순번·테스트ID를 1,2,3... 연속으로 재정렬"""
import re

path = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 테이블 데이터 행: | 순번 | 테스트ID | ... 형식 (앞뒤 공백 있을 수 있음)
row_pattern = re.compile(r'^(\|\s*)(\d+)(\s*\|\s*)(TS-[0-9\-]+)(\s*\|.*)$', re.MULTILINE)

def replacer(m):
    # 각 매치는 섹션 단위가 아니라 전체 파일에 대해 한 번에 적용되므로,
    # 순번/ID만 바꿀 수 없음. 대신 섹션별로 나눠서 처리해야 함.
    return m.group(0)  # no-op in re.sub, we do section-based edit

# 섹션 단위로 자른 뒤, 각 블록에서 데이터 행만 모아서 1,2,3 & TS-XX-001,002,003 으로 치환
parts = re.split(r'(^## \d+(?:\.\d+)*\..*$)', content, flags=re.MULTILINE)
out_lines = []
i = 0
while i < len(parts):
    block = parts[i]
    # 섹션 헤더가면 (## N. 제목) 다음 블록이 해당 섹션 본문
    if re.match(r'^## \d+(?:\.\d+)*\..*', block.strip()):
        out_lines.append(block)
        i += 1
        if i >= len(parts):
            break
        body = parts[i]
        # 본문에서 테이블 헤더/구분선 다음에 오는 데이터 행만 수집
        lines = body.split("\n")
        new_lines = []
        in_table = False
        datarows = []  # (line, line_idx in new_lines placeholder)
        for L in lines:
            if "| 순번 | 테스트ID |" in L or "| --- | --- |" in L:
                in_table = True
                new_lines.append(L)
                continue
            if in_table and re.match(r'^\|\s*\d+\s*\|\s*TS-', L):
                datarows.append(L)
                new_lines.append(None)  # placeholder
                continue
            if in_table and L.strip() == "":
                new_lines.append(L)
                continue
            in_table = False
            new_lines.append(L)

        # datarows 를 순번 1,2,3 / 테스트ID prefix+001,002,003 으로 변경
        if datarows:
            first_id = re.search(r'TS-[0-9\-]+', datarows[0])
            if first_id:
                tid = first_id.group(0)
                # TS-04-033 -> prefix "TS-04-",  TS-01-01-001 -> "TS-01-01-"
                suffix = re.search(r'-[0-9]+\s*\|', datarows[0])
                if suffix:
                    prefix = tid.rsplit("-", 1)[0] + "-"
                else:
                    prefix = tid.rsplit("-", 1)[0] + "-"
                idx = 0
                for j, ln in enumerate(new_lines):
                    if ln is None:
                        old_line = datarows[idx]
                        mo = row_pattern.match(old_line)
                        if mo:
                            new_seq = idx + 1
                            new_id = f"{prefix}{new_seq:03d}"
                            new_line = f"{mo.group(1)}{new_seq}{mo.group(3)}{new_id}{mo.group(5)}"
                            new_lines[j] = new_line
                        else:
                            new_lines[j] = old_line
                        idx += 1
            else:
                for j, ln in enumerate(new_lines):
                    if ln is None:
                        new_lines[j] = datarows.pop(0)
        else:
            for j, ln in enumerate(new_lines):
                if ln is None:
                    raise SystemExit("placeholder left without datarow")

        out_lines.append("\n".join(new_lines))
        i += 1
    else:
        out_lines.append(block)
        i += 1

result = "".join(out_lines)
with open(path, "w", encoding="utf-8") as f:
    f.write(result)
print("Done. 순번·테스트ID 연속 재정렬 완료.")
