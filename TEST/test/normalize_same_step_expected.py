#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단계별 작업 수행내용과 예상 결과가 동일한 행에서,
예상 결과(6번째 컬럼)를 검증 문구(~되는지 확인)로 바꿉니다.
"""
import re

FP = r"c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md"

def has_jong(s):
    """한글 마지막 글자 받침 여부"""
    if not s or not s.strip():
        return False
    c = s.strip()[-1]
    if not ('\uac00' <= c <= '\ud7a3'):
        return False
    return (ord(c) - 0xAC00) % 28 != 0

def josa_iga(lead):
    return "이" if has_jong(lead) else "가"

def to_verify(exp):
    """예상결과 문구를 검증문구로 변환"""
    if not exp or not exp.strip():
        return exp
    s = exp.strip()

    # 완전 일치 치환 (자주 나오는 구문)
    full_map = {
        "상담 신청 취소 및 모달 닫기": "모달이 닫히고 입력 내용이 초기화되는지 확인",
        "모달 닫기": "모달이 닫히는지 확인",
        "입력된 수신번호를 메인 테이블에 추가": "입력된 수신번호가 메인 테이블에 추가되는지 확인",
        "주소록에 데이터 추가": "주소록에 데이터가 추가되는지 확인",
        "최종 발송 실행": "최종 발송이 정상 실행되는지 확인",
        "검색 조건으로 목록 조회": "검색 조건에 따라 목록이 조회되는지 확인",
        "템플릿 삭제 실행": "템플릿이 삭제되는지 확인",
        "그룹명 저장": "그룹명이 저장되는지 확인",
        "수신거부 삭제 실행": "수신거부 번호가 삭제되는지 확인",
        "예약 취소 확정": "예약이 취소되는지 확인",
        "세금계산서 발행 최종 신청": "세금계산서 발행이 정상 신청되는지 확인",
        "최신 서비스 공지사항 빠른 확인": "최신 서비스 공지사항을 빠르게 확인할 수 있는지 확인",
    }
    if s in full_map:
        return full_map[s]

    # 접미사별 변환 (앞부분 + 조사 + " ~되는지 확인"). tail이 공백으로 시작하면 조사(이/가) 붙임.
    def ro_uro(lead):
        return "으로" if has_jong(lead) else "로"

    suffix_rules = [
        (" 표시", " 표시되는지 확인"),
        (" 제공", " 제공되는지 확인"),
        (" 접근", "에 접근 가능한지 확인"),
        (" 유도", " 유도 영역이 표시되고 동작하는지 확인"),
        (" 노출", " 노출되는지 확인"),
        (" 확인", " 확인되는지 확인"),
        (" 이동", None),  # 별도: lead + ro_uro(lead) + " 이동되는지 확인"
        (" 소개", " 소개·표시되는지 확인"),
        (" 해결", " 해결되는지 확인"),
        (" 영역", " 영역이 표시되는지 확인"),
        (" 다운로드", " 다운로드되는지 확인"),
        (" 폼", " 폼이 표시되는지 확인"),
        (" 입력", " 입력이 가능한지 확인"),
        (" 선택", " 선택되는지 확인"),
        (" 제출", " 정상 제출되는지 확인"),
        (" 실행", " 정상 실행되는지 확인"),
        (" 전환", " 전환되는지 확인"),
        (" 저장", " 저장되는지 확인"),
        (" 업로드", " 업로드되는지 확인"),
        (" 추가", " 추가되는지 확인"),
        (" 삭제", " 삭제되는지 확인"),
        (" 수집", " 입력이 가능한지 확인"),
        (" 형성", " 형성 영역이 표시되는지 확인"),
        (" 전달", " 전달·표시되는지 확인"),
        (" 홍보", " 표시되는지 확인"),
        (" 동의", " 동의 항목이 표시되는지 확인"),
    ]
    for suffix, tail in suffix_rules:
        if not s.endswith(suffix):
            continue
        lead = s[: -len(suffix)].strip() or "해당 내용"
        if suffix == " 이동":
            if lead.endswith("으로") or lead.endswith("로"):
                return lead + " 이동되는지 확인"
            return lead + ro_uro(lead) + " 이동되는지 확인"
        if tail is None:
            continue
        # " 유도"," 형성"," 영역"," 폼"," 동의"," 입력"은 lead+tail만 (조사 없음)
        if suffix in (" 유도", " 형성", " 영역", " 폼", " 동의", " 입력"):
            return lead + tail
        if tail.startswith(" "):
            return lead + josa_iga(lead) + tail
        if tail.startswith("에 "):
            return lead + tail
        return lead + tail

    # 그 외: 공통 검증문
    return "해당 기능이 정상 표시·동작하는지 확인"

def step_first_bullet(step_col):
    """단계별 작업의 첫 번째 불릿 내용만 추출 (예: '- 서비스 전역...' -> '서비스 전역...')"""
    t = (step_col or "").replace("<br>", "\n")
    for line in t.split("\n"):
        m = re.match(r"^\s*[-•]\s*(.+)$", line.strip())
        if m:
            return m.group(1).strip()[:120]
    t = re.sub(r"[\s\-]+", " ", (step_col or "").replace("<br>", " ")).strip()
    return t[:120]

def exp_trim(exp_col):
    return (exp_col or "").replace("<br>", " ").replace("\n", " ").strip()

def is_same_step_and_expected(step_col, exp_col):
    """단계 첫 불릿과 예상결과가 동일하면 True"""
    first = step_first_bullet(step_col)
    exp = exp_trim(exp_col)
    if not first or not exp or len(exp) < 2:
        return False
    # 첫 불릿과 예상결과가 같거나, 첫 불릿이 예상결과로 시작하면 동일로 간주
    return first == exp or (len(exp) >= 3 and first.startswith(exp))

def process_line(line):
    if not line.strip().startswith("|") or "TS-" not in line or line.strip().startswith("| ---"):
        return line
    parts = line.split(" | ", 6)
    if len(parts) < 6:
        return line
    step_col = (parts[4] or "").strip()
    exp_col = (parts[5] or "").strip()
    if not is_same_step_and_expected(step_col, exp_col):
        return line
    new_exp = to_verify(exp_col)
    parts[5] = new_exp
    return " | ".join(parts[:6]) + (" | " + parts[6] if len(parts) > 6 else "")

def main():
    with open(FP, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out = [process_line(ln) for ln in lines]
    with open(FP, "w", encoding="utf-8") as f:
        f.writelines(out)
    print("단계=예상결과 행의 예상결과를 검증문구로 정리해 저장했습니다.")

if __name__ == "__main__":
    main()
