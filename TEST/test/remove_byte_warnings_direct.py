#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
바이트 초과 경고 메시지 관련 시나리오 직접 제거
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

def remove_byte_warning_scenarios(content):
    """바이트 초과 경고 메시지 관련 시나리오 제거"""
    
    lines = content.split('\n')
    new_lines = []
    removed_count = 0
    removed_ids = []
    
    for line in lines:
        original_line = line
        
        # 바이트 초과 경고 메시지 패턴
        warning_patterns = [
            r'입력 가능한 글자수.*초과했습니다',
            r'메시지가 최대 바이트를 초과했습니다',
            r'제목이.*바이트를 초과했습니다',
            r'.*바이트를 초과했습니다',
            r'글자수가 초과되었습니다',
        ]
        
        # 바이트 초과 경고만 다루는 시나리오인지 확인
        is_warning_only = False
        if re.match(r'^\|', line) and 'TS-' in line:
            has_warning = False
            for pattern in warning_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    has_warning = True
                    break
            
            if has_warning:
                # 다른 중요한 기능이 있는지 확인
                functional_keywords = [
                    r'입력.*확인', r'선택.*확인', r'저장', r'삭제', r'수정',
                    r'발송.*확인', r'등록.*확인', r'검색', r'표시.*확인',
                ]
                
                has_other_function = False
                for keyword in functional_keywords:
                    if re.search(keyword, line, re.IGNORECASE):
                        # 경고 메시지 부분만 제거하고 유지
                        for pattern in warning_patterns:
                            line = re.sub(pattern, '', line, flags=re.IGNORECASE)
                        line = re.sub(r'<br>.*?경고\s*메시지.*?확인[^<]*', '', line, flags=re.IGNORECASE)
                        line = re.sub(r'<br>.*?오류\s*메시지.*?확인[^<]*', '', line, flags=re.IGNORECASE)
                        has_other_function = True
                        break
                
                if not has_other_function:
                    # 경고 메시지만 다루는 시나리오 제거
                    is_warning_only = True
                    parts = line.split('|')
                    if len(parts) > 2:
                        test_id = parts[1].strip()
                        removed_ids.append(test_id)
                    removed_count += 1
        
        # 경고 메시지 관련 내용 제거 (라인 내에서)
        if not is_warning_only:
            for pattern in warning_patterns:
                line = re.sub(pattern, '', line, flags=re.IGNORECASE)
            
            line = re.sub(r'<br>.*?경고\s*메시지.*?표시[^<]*', '', line, flags=re.IGNORECASE)
            line = re.sub(r'<br>.*?오류\s*메시지.*?표시[^<]*', '', line, flags=re.IGNORECASE)
            line = re.sub(r'경고\s*메시지가\s*표시되는지\s*확인', '', line, flags=re.IGNORECASE)
            line = re.sub(r'오류\s*메시지가\s*표시되는지\s*확인', '', line, flags=re.IGNORECASE)
            line = re.sub(r'초과된\s*부분은\s*입력되지\s*않는지\s*확인', '', line, flags=re.IGNORECASE)
            line = re.sub(r'초과된\s*부분은\s*자동으로\s*잘리는지\s*확인', '', line, flags=re.IGNORECASE)
            
            # 빈 <br> 태그 정리
            line = re.sub(r'<br>\s*<br>', '<br>', line)
            line = re.sub(r'<br>\s*$', '', line)
            line = re.sub(r'^\s*<br>', '', line)
            line = re.sub(r'\s+', ' ', line).strip()
        
        if not is_warning_only:
            new_lines.append(line)
    
    return '\n'.join(new_lines), removed_count, removed_ids

def main():
    file_path = r'c:\Users\ibank\Desktop\spec\TEST\test\FO_테스트시나리오_상세.md'
    backup_path = file_path + '.backup_remove_warnings_direct'
    
    print("=" * 80)
    print("바이트 초과 경고 메시지 관련 시나리오 직접 제거")
    print("=" * 80)
    
    content = read_file(file_path)
    if not content:
        print("파일을 읽을 수 없습니다.")
        return
    
    if write_file(backup_path, content):
        print(f"\n백업 파일 생성: {backup_path}")
    
    original_content = content
    
    # 바이트 초과 경고 메시지 제거
    print("\n바이트 초과 경고 메시지 제거 중...")
    content, removed_count, removed_ids = remove_byte_warning_scenarios(content)
    
    if content != original_content:
        if write_file(file_path, content):
            print(f"\n✓ 파일 수정 완료: {file_path}")
            print(f"  백업 파일: {backup_path}")
            print(f"  제거된 시나리오: {removed_count}건")
            if removed_ids:
                print(f"\n제거된 테스트 ID:")
                for test_id in removed_ids[:20]:
                    print(f"  - {test_id}")
                if len(removed_ids) > 20:
                    print(f"  ... 외 {len(removed_ids) - 20}개")
        else:
            print("\n✗ 파일 저장 실패")
    else:
        print("\n변경사항 없음")

if __name__ == '__main__':
    main()
