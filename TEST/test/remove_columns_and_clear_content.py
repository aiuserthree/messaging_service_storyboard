#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 담당자, 수정방향, 우선순위 열 삭제
PASS/FAIL, 오류내용 열 내용 비우기
"""

import re

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {filepath} - {e}")
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {filepath} - {e}")
        return False

def process_table_columns(content):
    """테이블 열 삭제 및 내용 비우기"""
    
    lines = content.split('\n')
    new_lines = []
    
    # 열 인덱스 찾기 (헤더 기준)
    # 순번 | 테스트ID | 순서 | 테스트케이스명 | 페이지/팝업 | 단계별 작업 수행내용 | 테스트 데이터 | 예상 결과 | 테스트 담당자 | PASS/FAIL | 오류내용 | 수정방향 | 수정/오류 | 우선순위 | ...
    
    for line in lines:
        # 테이블 헤더 라인 찾기
        if re.match(r'^\|\s*순번\s*\|', line):
            # 헤더에서 열 인덱스 확인
            parts = [p.strip() for p in line.split('|')]
            
            # 열 인덱스 찾기
            try:
                test_manager_idx = parts.index('테스트 담당자')
                pass_fail_idx = parts.index('PASS/FAIL')
                error_content_idx = parts.index('오류내용')
                fix_direction_idx = parts.index('수정방향')
                priority_idx = parts.index('우선순위')
            except ValueError:
                # 이미 처리된 경우
                new_lines.append(line)
                continue
            
            # 헤더에서 열 제거
            new_parts = []
            for i, part in enumerate(parts):
                if i == 0:  # 첫 번째 빈 열
                    new_parts.append('')
                elif i in [test_manager_idx, fix_direction_idx, priority_idx]:
                    continue  # 삭제할 열
                else:
                    new_parts.append(part)
            
            new_lines.append('|' + '|'.join(new_parts) + '|')
            continue
        
        # 구분선 라인
        if re.match(r'^\|\s*---', line):
            parts = [p.strip() for p in line.split('|')]
            # 삭제할 열 인덱스는 헤더에서 찾은 것 사용
            try:
                test_manager_idx = -1
                pass_fail_idx = -1
                error_content_idx = -1
                fix_direction_idx = -1
                priority_idx = -1
                
                # 헤더 라인을 다시 찾아서 인덱스 확인
                for prev_line in reversed(new_lines):
                    if re.match(r'^\|\s*순번\s*\|', prev_line):
                        prev_parts = [p.strip() for p in prev_line.split('|')]
                        try:
                            test_manager_idx = prev_parts.index('테스트 담당자')
                            pass_fail_idx = prev_parts.index('PASS/FAIL')
                            error_content_idx = prev_parts.index('오류내용')
                            fix_direction_idx = prev_parts.index('수정방향')
                            priority_idx = prev_parts.index('우선순위')
                        except ValueError:
                            pass
                        break
                
                if test_manager_idx >= 0:
                    new_parts = []
                    for i, part in enumerate(parts):
                        if i == 0:
                            new_parts.append('')
                        elif i in [test_manager_idx, fix_direction_idx, priority_idx]:
                            continue
                        else:
                            new_parts.append('---')
                    new_lines.append('|' + '|'.join(new_parts) + '|')
                else:
                    new_lines.append(line)
            except:
                new_lines.append(line)
            continue
        
        # 데이터 행 처리
        if re.match(r'^\|', line) and not re.match(r'^\|\s*---', line):
            parts = [p.strip() for p in line.split('|')]
            
            if len(parts) < 10:
                # 이미 처리된 행이거나 형식이 다른 경우
                new_lines.append(line)
                continue
            
            # 헤더에서 인덱스 찾기 (이전 헤더 라인 참조)
            test_manager_idx = -1
            pass_fail_idx = -1
            error_content_idx = -1
            fix_direction_idx = -1
            priority_idx = -1
            
            for prev_line in reversed(new_lines):
                if re.match(r'^\|\s*순번\s*\|', prev_line):
                    prev_parts = [p.strip() for p in prev_line.split('|')]
                    try:
                        test_manager_idx = prev_parts.index('테스트 담당자')
                        pass_fail_idx = prev_parts.index('PASS/FAIL')
                        error_content_idx = prev_parts.index('오류내용')
                        fix_direction_idx = prev_parts.index('수정방향')
                        priority_idx = prev_parts.index('우선순위')
                    except ValueError:
                        # 이미 처리된 헤더
                        # 열 개수로 추정
                        if len(prev_parts) < len(parts):
                            # 이미 일부 열이 삭제된 상태
                            # 원본 열 구조 추정
                            # 순번(0) | 테스트ID(1) | 순서(2) | 테스트케이스명(3) | 페이지/팝업(4) | 단계별 작업 수행내용(5) | 테스트 데이터(6) | 예상 결과(7) | 테스트 담당자(8) | PASS/FAIL(9) | 오류내용(10) | 수정방향(11) | 수정/오류(12) | 우선순위(13) | ...
                            if len(parts) >= 14:
                                test_manager_idx = 8
                                pass_fail_idx = 9
                                error_content_idx = 10
                                fix_direction_idx = 11
                                priority_idx = 13
                    break
            
            # 인덱스를 찾지 못한 경우 기본값 사용
            if test_manager_idx < 0 and len(parts) >= 14:
                test_manager_idx = 8
                pass_fail_idx = 9
                error_content_idx = 10
                fix_direction_idx = 11
                priority_idx = 13
            
            if test_manager_idx >= 0 and len(parts) > max(test_manager_idx, pass_fail_idx, error_content_idx, fix_direction_idx, priority_idx):
                # 열 삭제 및 내용 비우기
                new_parts = []
                for i, part in enumerate(parts):
                    if i == 0:  # 첫 번째 빈 열
                        new_parts.append('')
                    elif i == test_manager_idx or i == fix_direction_idx or i == priority_idx:
                        continue  # 삭제할 열
                    elif i == pass_fail_idx or i == error_content_idx:
                        new_parts.append('')  # 내용 비우기
                    else:
                        new_parts.append(part)
                
                new_lines.append('|' + '|'.join(new_parts) + '|')
            else:
                # 이미 처리된 행
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_columns'
    
    print("=" * 80)
    print("테스트 담당자, 수정방향, 우선순위 열 삭제")
    print("PASS/FAIL, 오류내용 열 내용 비우기")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 테이블 열 처리
    print("\n[1] 테이블 열 삭제 및 내용 비우기 중...")
    content = process_table_columns(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
