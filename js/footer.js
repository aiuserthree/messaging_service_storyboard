// 공통 푸터 생성 함수
function createFooter() {
    return `
        <footer class="footer">
            <div class="footer-top-row">
                <a href="support-center.html" class="footer-top-link">고객센터</a>
                <a href="support-notice.html" class="footer-top-link">공지사항</a>
                <a href="javascript:void(0)" class="footer-top-link" onclick="event.preventDefault(); openPolicyModal('terms')">이용약관</a>
                <a href="javascript:void(0)" class="footer-top-link" onclick="event.preventDefault(); openPolicyModal('privacy')">개인정보처리방침</a>
                <a href="javascript:void(0)" class="footer-top-link" onclick="event.preventDefault(); openPolicyModal('spam')">스팸방지정책</a>
                <a href="javascript:void(0)" class="footer-top-link" onclick="event.preventDefault(); openPolicyModal('company')">회사소개</a>
            </div>
            <div class="footer-content">
                <div class="footer-section footer-company">
                    <h4 class="footer-title">회사정보</h4>
                    <div class="footer-logo-wrap">
                        <img src="img/logo/logo.png" alt="ibank" class="footer-logo" />
                    </div>
                    <div class="footer-info">
                        <p class="footer-text">상호 : (주)아이뱅크</p>
                        <p class="footer-text">대표자: 정용관</p>
                        <p class="footer-text">사업자등록번호: 116-81-68774</p>
                        <p class="footer-text">통신판매업신고번호: 제2025-서울강서-0365호</p>
                        <p class="footer-text">특수부가통신사업등록번호: 제 3-01-25-0037 호</p>
                        <p class="footer-text">사업장 주소: 서울 강서구 마곡동 779번지 보타닉게이트 10층</p>
                        <p class="footer-text">호스팅제공사: iwinv</p>
                    </div>
                </div>
                <div class="footer-section footer-contact">
                    <h4 class="footer-title">고객지원</h4>
                    <div class="footer-info">
                        <p class="footer-text"><a href="support-faq.html" class="footer-inline-link">FAQ</a> · <a href="support-inquiry.html" class="footer-inline-link">1:1문의</a> · <span>실시간채팅(카카오상담톡)</span></p>
                        <p class="footer-text">전화번호: 02-6951-0035</p>
                        <p class="footer-text">상담시간: 평일 10시~17시 / 점심 11시30분~13시</p>
                        <p class="footer-text">대표이메일: <a href="mailto:tokbell@ibank.co.kr" class="footer-inline-link">tokbell@ibank.co.kr</a></p>
                        <p class="footer-text">기업견적문의 담당이메일: <a href="mailto:msg@ibank.co.kr" class="footer-inline-link">msg@ibank.co.kr</a></p>
                    </div>
                    <div class="footer-cert-logos">
                        <img src="img/logo/vntr_mark_signature02%201-Photoroom.png" alt="벤처확인기업" class="footer-cert-logo" />
                        <img src="img/logo/기술혁신형중소기업_국문로고%201.png" alt="기술혁신형중소기업" class="footer-cert-logo" />
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p class="footer-copyright">© 2025 Tokbell. All rights reserved.</p>
            </div>
        </footer>
        <style>
            .footer {
                background-color: var(--text-primary);
                color: var(--surface-color);
                padding: 40px 24px 24px;
                margin-top: 64px;
            }
            .footer-top-row {
                max-width: 1400px;
                margin: 0 auto 32px;
                display: flex;
                flex-wrap: wrap;
                gap: 8px 24px;
                padding-bottom: 24px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.15);
            }
            .footer-top-link {
                font-size: 14px;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.9);
                text-decoration: none;
                transition: color 0.2s;
            }
            .footer-top-link:hover {
                color: var(--surface-color);
                text-decoration: underline;
            }
            .footer-content {
                max-width: 1400px;
                margin: 0 auto;
                margin-bottom: 32px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 48px;
            }
            .footer-section {
                display: flex;
                flex-direction: column;
            }
            .footer-company { grid-column: 1; }
            .footer-contact { grid-column: 2; }
            .footer-title {
                font-size: 15px;
                font-weight: 600;
                margin-bottom: 14px;
                color: var(--surface-color);
            }
            .footer-info {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .footer-text {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.6;
                margin: 0;
            }
            .footer-inline-link {
                color: rgba(255, 255, 255, 0.9);
                text-decoration: none;
            }
            .footer-inline-link:hover {
                color: var(--surface-color);
                text-decoration: underline;
            }
            .footer-logo-wrap {
                margin-top: 0;
                margin-bottom: 16px;
            }
            .footer-logo {
                height: 28px;
                width: auto;
                max-width: 80px;
                display: block;
                object-fit: contain;
                opacity: 0.95;
            }
            .footer-bottom {
                max-width: 1400px;
                margin: 0 auto;
                padding-top: 24px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
            }
            .footer-cert-logos {
                margin-top: 20px;
                display: flex;
                align-items: center;
                justify-content: flex-start;
                gap: 16px;
                flex-wrap: wrap;
            }
            .footer-cert-logo {
                height: 30px;
                width: auto;
                max-width: 120px;
                object-fit: contain;
                opacity: 0.9;
            }
            .footer-copyright {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.6);
                margin: 0;
            }
            @media (max-width: 768px) {
                .footer {
                    padding: 28px 16px 20px;
                }
                .footer-top-row {
                    margin-bottom: 24px;
                    padding-bottom: 20px;
                }
                .footer-content {
                    grid-template-columns: 1fr;
                    gap: 28px;
                }
                .footer-company { grid-column: auto; }
                .footer-contact { grid-column: auto; }
            }
        </style>
    `;
}

// 모달 열기 함수
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// 모달 닫기 함수
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// 정책 모달 열기 함수
function openPolicyModal(type) {
    const modalId = 'policyModal';
    let modal = document.getElementById(modalId);
    
    if (!modal) {
        modal = document.createElement('div');
        modal.id = modalId;
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal" style="max-width: 800px; max-height: 90vh; overflow-y: auto;">
                <div class="modal-header">
                    <h3 class="modal-title" id="policyModalTitle">정책</h3>
                    <button class="modal-close" onclick="closeModal('policyModal')">&times;</button>
                </div>
                <div class="modal-body" id="policyModalBody">
                    <p>내용을 불러오는 중...</p>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-outline" onclick="closeModal('policyModal')">닫기</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        // 모달 외부 클릭 시 닫기
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal(modalId);
            }
        });
    }
    
    const titleMap = {
        'company': '회사소개',
        'service': '서비스 소개',
        'terms': '이용약관',
        'privacy': '개인정보처리방침',
        'spam': '스팸방지정책',
        'refund': '환불정책'
    };
    
    const contentMap = {
        'company': `
            <div style="line-height: 1.8; color: var(--text-primary);">
                <p style="margin-bottom: 24px;">
                    <strong>주식회사 아이뱅크</strong>는 기업과 개인을 위한 차세대 메시징 서비스 플랫폼 <strong>톡벨(TalkBell)</strong>을 운영하는 전문 기업입니다.
                    고객과의 소통을 혁신하고, 비즈니스 성장을 지원하는 신뢰할 수 있는 파트너로서 최고의 메시징 솔루션을 제공합니다.
                </p>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">회사 정보</h4>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600; width: 140px;">상호명</td>
                        <td style="padding: 12px 0;">주식회사 아이뱅크</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">서비스명</td>
                        <td style="padding: 12px 0;">톡벨(TalkBell)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">대표자</td>
                        <td style="padding: 12px 0;">정용관</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">사업자등록번호</td>
                        <td style="padding: 12px 0;">116-81-68774</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">통신판매업신고</td>
                        <td style="padding: 12px 0;">제2025-서울강서-0365호</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">특수부가통신사업등록번호</td>
                        <td style="padding: 12px 0;">제 3-01-25-0037 호</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">사업장 주소</td>
                        <td style="padding: 12px 0;">서울 강서구 마곡동 779번지 보타닉게이트 10층</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">호스팅제공사</td>
                        <td style="padding: 12px 0;">iwinv</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">대표전화</td>
                        <td style="padding: 12px 0;">02-6951-0035</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">대표이메일</td>
                        <td style="padding: 12px 0;">tokbell@ibank.co.kr</td>
                    </tr>
                </table>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">핵심 가치</h4>
                <ul style="padding-left: 20px; margin-bottom: 16px;">
                    <li style="margin-bottom: 8px;"><strong>신뢰성</strong>: 안정적인 인프라와 99.9% 이상의 발송 성공률 보장</li>
                    <li style="margin-bottom: 8px;"><strong>혁신성</strong>: 최신 기술을 활용한 사용자 친화적인 플랫폼 제공</li>
                    <li style="margin-bottom: 8px;"><strong>고객 중심</strong>: 고객의 니즈를 반영한 지속적인 서비스 개선</li>
                    <li style="margin-bottom: 8px;"><strong>법적 준수</strong>: 정보통신망법, 개인정보보호법 등 관련 법규 준수</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">미션 & 비전</h4>
                <p style="margin-bottom: 16px;">
                    톡벨은 고객과의 소통을 더욱 쉽고 효율적으로 만들어가는 것을 핵심 미션으로 합니다.
                    기업의 마케팅, 고객 관리, 공지사항 전달 등 다양한 비즈니스 니즈를 충족시키는 
                    종합 메시징 솔루션을 제공하여 고객의 성공을 함께 만들어갑니다.
                </p>
                <p>
                    국내 최고의 메시징 서비스 플랫폼으로 성장하여, 
                    모든 기업과 개인이 쉽고 편리하게 메시지를 발송할 수 있는 생태계를 구축하겠습니다.
                </p>
            </div>
        `,
        'service': `
            <div style="line-height: 1.8; color: var(--text-primary);">
                <p style="margin-bottom: 24px;">
                    <strong>톡벨(TalkBell)</strong>은 인터넷 문자 발송 및 카카오톡 비즈메시지를 통합 제공하는 메시징 플랫폼입니다.
                    개인 회원부터 사업자 회원, 선거 회원까지 다양한 고객층에 맞춤형 서비스를 제공합니다.
                </p>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">📱 문자 발송 서비스</h4>
                <ul style="padding-left: 20px; margin-bottom: 24px;">
                    <li style="margin-bottom: 8px;"><strong>SMS (단문 메시지)</strong>: 최대 90바이트(한글 45자)까지 발송 가능</li>
                    <li style="margin-bottom: 8px;"><strong>LMS (장문 메시지)</strong>: 최대 2,000바이트(한글 1,000자)까지 발송 가능</li>
                    <li style="margin-bottom: 8px;"><strong>MMS (멀티미디어 메시지)</strong>: 이미지 첨부 가능, 최대 2,000바이트</li>
                    <li style="margin-bottom: 8px;"><strong>발송 한도</strong>: 개인 회원 1일 500건, 사업자 회원 1회 최대 1,000,000건</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">💬 카카오톡 비즈메시지</h4>
                <ul style="padding-left: 20px; margin-bottom: 24px;">
                    <li style="margin-bottom: 8px;"><strong>알림톡</strong>: 정보성 메시지 발송 (주문확인, 배송안내, 예약확인 등)</li>
                    <li style="margin-bottom: 8px;"><strong>브랜드톡(친구톡)</strong>: 광고성 메시지 발송, 이미지/버튼 첨부 가능</li>
                    <li style="margin-bottom: 8px;">카카오톡 채널(비즈니스 인증) 및 발신 프로필 등록 필요</li>
                    <li style="margin-bottom: 8px;">알림톡 템플릿은 카카오 사전 승인 필수</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">📋 템플릿 관리</h4>
                <ul style="padding-left: 20px; margin-bottom: 24px;">
                    <li style="margin-bottom: 8px;">문자 템플릿 등록 및 관리</li>
                    <li style="margin-bottom: 8px;">알림톡/브랜드톡 템플릿 등록 및 승인 관리</li>
                    <li style="margin-bottom: 8px;">자주 사용하는 메시지 템플릿화로 발송 효율화</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">📊 발송 관리</h4>
                <ul style="padding-left: 20px; margin-bottom: 24px;">
                    <li style="margin-bottom: 8px;">실시간 발송 결과 조회</li>
                    <li style="margin-bottom: 8px;">예약 발송 기능</li>
                    <li style="margin-bottom: 8px;">대량 발송 지원 (엑셀 업로드)</li>
                    <li style="margin-bottom: 8px;">발송 통계 및 분석 리포트</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">📇 주소록 관리</h4>
                <ul style="padding-left: 20px; margin-bottom: 24px;">
                    <li style="margin-bottom: 8px;">고객 정보 체계적 관리</li>
                    <li style="margin-bottom: 8px;">그룹별 분류 및 태그 관리</li>
                    <li style="margin-bottom: 8px;">엑셀 업로드/다운로드 지원</li>
                    <li style="margin-bottom: 8px;">수신거부 번호 자동 관리</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">🗳️ 선거문자 서비스</h4>
                <ul style="padding-left: 20px; margin-bottom: 24px;">
                    <li style="margin-bottom: 8px;">공직선거법에 따른 선거 회원 전용 서비스</li>
                    <li style="margin-bottom: 8px;">선거관리위원회 신고 발신번호 등록</li>
                    <li style="margin-bottom: 8px;">발송량 제한 없음 (자동 동보통신 총 8회 제한)</li>
                    <li style="margin-bottom: 8px;">선거 기간 종료 후 개인 회원 자동 전환</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px;">💰 요금 및 결제</h4>
                <ul style="padding-left: 20px; margin-bottom: 16px;">
                    <li style="margin-bottom: 8px;"><strong>선불 충전 방식</strong>: 포인트 충전 후 사용</li>
                    <li style="margin-bottom: 8px;"><strong>최소 충전 금액</strong>: 10,000원 (100원 = 100포인트)</li>
                    <li style="margin-bottom: 8px;"><strong>포인트 유효기간</strong>: 최종 충전일로부터 5년</li>
                    <li style="margin-bottom: 8px;"><strong>마일리지</strong>: 프로모션/보너스로 지급되는 무상 포인트</li>
                </ul>
            </div>
        `,
        'terms': `
            <div style="line-height: 1.8; color: var(--text-primary);">
            <h4 style="margin-top: 0; margin-bottom: 12px; color: var(--primary-color);">제1장 총칙</h4>
            <p style="margin-bottom: 12px;"><strong>제1조(목적)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">이 약관은 주식회사 아이뱅크(이하 ‘회사’라 합니다)가 운영하는 톡벨(TalkBell) 서비스의 이용과 관련하여 회사와 이용자의 권리∙의무 및 책임사항, 기타 필요한 사항을 규정함을 목적으로 합니다.</p>
            <p style="margin-bottom: 12px;"><strong>제2조(정의)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 이 약관에서 사용하는 용어의 정의는 다음과 같습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">“이메일(아이디/ID)”이라 함은 회원의 식별과 서비스 이용을 위하여 회원이 입력하고 회사가 승인한 이메일 주소를 말합니다.</li>
            <li style="margin-bottom: 6px;">“비밀번호”라 함은 회원이 이용하는 이메일과 일치되는 회원임을 확인하고 비밀보호를 위해 회원 자신이 정한 문자 또는 숫자의 조합을 말합니다.</li>
            <li style="margin-bottom: 6px;">“서비스”라 함은 이용자가 전송하고자 하는 내용ㆍ정보 등을 문자메시지(SMS), 장문메시지(LMS), 멀티미디어메시지(MMS)의 형태로 변환하여 전송하거나 카카오톡을 통한 알림톡 또는 브랜드 메시지의 형태로 변환하여 전송하고 알림톡 또는 브랜드 메시지 전송 실패 시 대체발송 옵션 설정에 따라 문자메시지, 멀티미디어메시지 등의 형태로 변환하여 전송하는 서비스 및 회사가 추가 개발하거나 다른 회사와의 제휴계약 등을 통해 이용자에게 제공할 일체의 서비스를 의미합니다.</li>
            <li style="margin-bottom: 6px;">“이용자(회원)”라 함은 회사와 서비스 이용계약을 체결한 자를 말하며, 다음 각 목으로 구분됩니다.</li>
            <li style="margin-bottom: 6px;">가)	개인 회원: 개인 자격으로 서비스를 이용하고자 하는 만 19세 이상의 대한민국 국적 거주민으로, 본인 명의 휴대폰 인증을 완료한 자</li>
            <li style="margin-bottom: 6px;">나)	사업자 회원: 유효한 사업자등록증을 보유하고 기업 명의로 서비스를 이용하는 자</li>
            <li style="margin-bottom: 6px;">다)	선거 회원: 선거 문자 서비스를 이용하기 위해 개인 회원에서 전환된 자로서, 공직선거법에 따른 예비 후보자, 후보자 및 선거사무소 당직자 등</li>
            <li style="margin-bottom: 6px;">“이용계약”이라 함은 서비스를 제공받기 위하여 회사와 회원 간에 체결하는 계약을 말합니다.</li>
            <li style="margin-bottom: 6px;">“이용제한”이라 함은 회사가 정한 일정한 요건에 따라 회원의 서비스 이용을 제한하는 것을 말합니다.</li>
            <li style="margin-bottom: 6px;">“휴면계정”이라 함은 12개월 이상 계속해서 로그인을 포함한 서비스 이용이 없는 아이디(ID)를 말합니다.</li>
            <li style="margin-bottom: 6px;">“카카오톡”이라 함은 주식회사 카카오(이하 ”카카오”)가 운영하는 모바일 메신저 기반의 실시간 커뮤니케이션 서비스 알림톡, 친구톡 또는 해당 서비스를 제공하는 어플리케이션을 말합니다.</li>
            <li style="margin-bottom: 6px;">“알림톡”이라 함은 주문, 예약, 결제, 배송 정보 등 정보통신망 이용촉진 및 정보보호 등에 관한 법률(이하 “정보통신망법”) 및 한국인터넷진흥원 지침 상 광고성 정보의 예외로 분류되는 정보 중 일부를 카카오톡 채널 추가 여부와 상관 없이 발송 가능한 메시지를 말합니다.</li>
            <li style="margin-bottom: 6px;">“브랜드 메시지”라 함은 광고성 정보 수신에 사전 동의하거나 ‘발신자’의 카카오톡 채널과 채널 친구 추가된 카카오톡 이용자에게만 발송 가능한 메시지를 말합니다.</li>
            <li style="margin-bottom: 6px;">“발신프로필”이라 함은 카카오톡 비즈메시지, 브랜드 메시지를 발송하고 “수신자”가 카카오톡 비즈메시지, 브랜드 메시지 발신처를 확인하기 위하여 사용하는 “발신자” 식별정보를 말합니다.</li>
            <li style="margin-bottom: 6px;">“스팸”이라 함은 정보통신망법을 위반하여 수신자가 원하지 않는데도 불구하고 일방적으로 전송 또는 게시되는 영리목적의 광고성 정보를 의미합니다.</li>
            <li style="margin-bottom: 6px;">“스미싱”이라 함은 메시지 내용 중 인터넷 주소를 클릭하면 악성코드가 설치되어 수신자가 모르는 사이에 금전적 피해 또는 개인·금융정보 탈취 피해를 야기하는 메시지를 말합니다.</li>
            <li style="margin-bottom: 6px;">“포인트”라 함은 이용자가 회사의 서비스를 이용하는데 있어 사용할 수 있는 회사가 인정한 선불 충전 결제 수단을 말합니다.</li>
            <li style="margin-bottom: 6px;">“마일리지”라 함은 회사가 프로모션 등을 통해 무상으로 지급한 적립금을 말합니다.</li>
            <li style="margin-bottom: 6px;">“블랙리스트(불법 전화번호 목록)”라 함은 발신번호 거짓표시, 보이스피싱, 불법스팸 등에 이용되어 전기통신역무 제공이 중지된 전화번호 목록을 말합니다.</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 이 약관에서 사용하는 용어 중 제1항에서 정하지 않은 것은 관계 법령 또는 상관례에 따릅니다.</p>
            <p style="margin-bottom: 12px;"><strong>제3조(약관의 게시와 개정)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 본 약관의 내용을 이용자가 쉽게 알 수 있도록 서비스 초기 화면에 게시합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 “약관의 규제에 관한 법률”, ”정보통신망법”, “전기통신사업법”, “전자상거래 등에서의 소비자보호에 관한 법률” 등 관련법을 위배하지 않는 범위에서 본 약관을 개정할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사가 약관을 개정할 경우에는 시행일자 및 개정사유를 명시하여 기존 약관과 함께 그 시행일자 7일 전(중대한 변경은 30일 전)부터 시행일자 전일까지 공지합니다. 이용자에게 불리한 약관의 개정의 경우에는 이용자가 등록한 이메일로 전송하는 방법 등으로 이용자에게 통지합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 회사가 전항에 따라 이용자에게 개정약관을 공지 또는 통지하면서 이용자에게 약관시행일까지 의사표시를 하지 않으면 승인한 것으로 본다는 뜻을 명확하게 공지 또는 통지하였음에도 이용자가 명시적으로 거부의 의사표시를 하지 아니한 경우 이용자가 개정약관에 동의한 것으로 봅니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 이용자는 개정된 약관에 대해 동의하지 않을 권리가 있습니다. 이용자가 개정약관의 적용에 동의하지 않는 경우 이용계약을 해지할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑥ 이용자는 약관의 변경에 대하여 주의의무를 다하여야 하며 변경된 약관으로 인한 회원의 피해는 회사가 책임지지 않습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제4조 (약관 이외의 준칙)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">이 약관에서 정하지 아니한 사항과 이 약관의 해석에 관하여는 국내 관계법령 또는 상관례에 따릅니다.</p>
            
            <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제2장 이용자의 이용계약 및 관리</h4>
            <p style="margin-bottom: 12px;"><strong>제5조(이용계약의 성립)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 이용계약은 회원이 되고자 하는 자(이하 “가입신청자”)가 이용신청 및 약관에 대한 동의와 회사의 이용승낙으로 성립하며, 회사는 가입신청자의 이용 신청을 승낙을 한 때부터 서비스를 개시합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 가입신청자는 서비스 이용을 위해 회사에 이메일 주소를 제공하여야 하며, 회사는 해당 이메일 주소를 아이디(ID)로 사용합니다. 가입신청자는 본인 소유의 실제 수신 가능한 이메일 주소를 사용하여야 하며, 이를 위반하여 발생하는 불이익에 대한 책임은 가입신청자에게 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사는 다음 각 호에 해당하는 신청에 대하여는 승낙을 하지 않거나 사후에 해지할 수 있습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">가입신청자가 이 약관에 의하여 이전에 이용자 자격을 상실한 적이 있는 경우, 단 회사의 이용자 재가입 승낙을 얻을 경우에는 예외로 함</li>
            <li style="margin-bottom: 6px;">실명이 아니거나 타인의 명의를 이용한 경우</li>
            <li style="margin-bottom: 6px;">허위의 정보를 기재하거나, 회사가 제시하는 내용을 기재하지 않은 경우</li>
            <li style="margin-bottom: 6px;">필수 제출 서류(3개월 이내 발급한 사업자등록증, 재직증명서 등)를 누락하거나 허위로 기재한 경우</li>
            <li style="margin-bottom: 6px;">만 19세 미만의 가입자인 경우 또는 외국인/법인 명의 휴대폰을 사용하는 개인 회원인 경우</li>
            <li style="margin-bottom: 6px;">이용자가 서비스의 정상적인 제공을 저해하거나 다른 이용자의 서비스 이용에 지장을 줄 것으로 예상되는 경우</li>
            <li style="margin-bottom: 6px;">기타 회사가 관련법령 등을 기준으로 하여 명백하게 사회질서 및 미풍양속에 반할 우려가 있음을 인정하는 경우</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 제1항에 따른 신청에 있어 회사는 이용자의 종류에 따라 전문기관을 통한 실명확인 및 본인인증을 요청할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 회사는 서비스 관련 설비의 여유가 없거나 기술상 또는 업무상 문제가 있는 경우에는 승낙을 유보할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑥ 회원은 이용계약 체결 시 실명, 실제 정보를 입력하여야 하며, 이를 위반한 회원은 법적인 보호를 받을 수 없고, 서비스 이용에 제한을 받을 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑦ 이용계약의 성립 시기는 회사가 가입완료를 신청절차 상에서 표기한 시점으로 합니다.</p>
            <p style="margin-bottom: 12px;"><strong>제6조(개인정보수집)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 적법하고 공정한 수단에 의하여 이용계약의 성립 및 이행에 필요한 최소한의 개인정보를 수집합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 개인정보의 수집 시 관련법규에 따라 개인정보 처리방침에 그 수집범위 및 목적을 사전고지 합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사는 개인정보처리방침에서 규정하고 있는 수집항목 및 이용목적 외에 불법스팸 발송 등으로 서비스 계약을 해지한 고객의 서비스 이용신청에 대한 승낙을 유보하기 위하여 성명, 업체명, 사업자등록번호, 전화번호, 해지사유 등의 정보를 수집 및 보관할 수 있습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제7조(개인정보의 보호 및 관리)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 관련 법령이 정하는 바에 따라 이용자의 개인정보를 보호하기 위해 노력합니다. 이용자의 개인정보의 보호 및 사용에 대해서는 관련 법령 및 회사가 별도로 고지하는 개인정보 처리방침이 적용됩니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 회원이 안전하게 서비스를 이용할 수 있도록 보안시스템을 갖추어야 하며 개인정보 처리방침을 공시하고 준수합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사는 이용자의 귀책사유로 인하여 노출된 이용자의 계정정보를 포함한 타인의 모든 개인정보, 비밀정보에 대해서 일체의 책임을 지지 않습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제8조 (이용자 정보의 변경 및 관리 의무)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 이용자는 개인정보설정 화면을 통하여 본인의 정보를 열람 및 수정할 수 있습니다. 다만, 법인 이용자는 홈페이지 기재된 회사의 전화 및 이메일로 법인정보의 수정을 요청하여야 합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 이용자는 서비스 이용신청 시 기재한 사항이나 중요 정보(기업명, 대표자명 등)가 변경되었을 경우 즉시 수정하거나 증빙서류를 제출하여야 하며, 변경하지 않음으로써 발생한 불이익에 대하여 회사는 책임을 지지 않습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 아이디와 비밀번호에 대한 관리 책임은 회원에게 있으며, 이를 제3자가 이용하도록 하여서는 안 됩니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 회원은 이메일 주소(아이디)를 원칙적으로 변경할 수 없습니다. 부득이한 사유로 변경하고자 하는 경우에는 이용계약을 해지하고 재가입하여야 합니다. 단, 회사가 인정하는 특별한 사유가 있는 경우 고객센터를 통해 예외적으로 변경을 신청할 수 있습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제9조 (이용자에 대한 통지)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사가 이용자에 대한 통지를 하는 경우 이 약관에 별도 규정이 없는 한 이용자가 제공한 이메일, (휴대)전화번호, 알림톡 등으로 통지할 수 있습니다. 단, 회원이 이메일 또는 휴대전화번호의 부재, 변경, 오류 등 또는 정보를 허위로 제출하거나 변경된 정보를 회사에 알리지 않은 경우 회사는 회원이 제출한 정보로 통지를 발송한 때에 회원에게 도달된 것으로 봅니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 전체 또는 불특정 다수 이용자에 대한 통지의 경우 7일 이상 서비스 공지사항에 게시함으로써 제1항의 통지에 갈음할 수 있습니다.</p>
            
            <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제3장 계약당사자의 권리 및 의무</h4>
            <p style="margin-bottom: 12px;"><strong>제10조(회사의 의무)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 관련법과 본 약관이 금지하거나 미풍양속에 반하는 행위를 하지 않으며, 계속적이고 안정적으로 서비스를 제공하기 위하여 노력합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 서비스 제공을 위한 시스템에 장애가 발생하거나 고장 발생 시에는 이를 최대한 신속히 수리 또는 복구합니다. 다만, 천재지변 등 불가항력의 경우에는 서비스를 일시 중단할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사는 이용자의 서비스 제공 목적에 맞는 서비스 이용여부를 확인하기 위하여 상시적으로 모니터링을 실시합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 회사는 스팸메시지 또는 스미싱(이하 “불법스팸”)으로부터 이용자를 보호하기 위하여 스팸차단(필터링) 부가 서비스를 통해 해당 문자메시지가 수신되지 않도록 차단할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 회사는 불법스팸 전송자 적발, 차단 등을 위해 차단된 문자의 내용, 불법스팸 발송 사업자 정보 등을 한국인터넷진흥원에 제공할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑥ 회사는 전기통신사업법 제84조의2 및 “고시”에 따라 발신번호 사전등록서비스를 제공 및 운영합니다. 이용자가 발신번호를 변작하거나 블랙리스트에 포함된 번호를 사용하는 경우 해당 메시지의 전송을 차단합니다.</p>
            <p style="margin-bottom: 12px;"><strong>제11조(이용자의 의무)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 이용자는 회사가 제공하는 서비스를 이용함에 있어 다음 각 호에 해당하는 행위를 하여서는 안됩니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">이용신청이나 변경 시 타인의 정보 또는 허위내용을 등록하는 행위</li>
            <li style="margin-bottom: 6px;">다른 이용자의 이메일 및 비밀번호를 도용하는 행위</li>
            <li style="margin-bottom: 6px;">회사의 승인 없이 영리 목적으로 서비스를 재판매하거나 임대하는 행위</li>
            <li style="margin-bottom: 6px;">회사 및 타인의 명예를 손상시키거나 업무를 방해하는 행위</li>
            <li style="margin-bottom: 6px;">불법스팸을 전송하거나 이로 인하여 타인의 재산상에 손해를 발생시키는 행위</li>
            <li style="margin-bottom: 6px;">서비스를 사용하여 사기 또는 국가기관 사칭을 목적으로 한 내용의 메시지를 발송하는 행위</li>
            <li style="margin-bottom: 6px;">타인의 발신번호를 도용하여 부정하게 사용하는 행위</li>
            <li style="margin-bottom: 6px;">광고성 정보를 전송하면서 정보성 메시지로 유형을 속여 발송하거나, 시스템상 강제로 적용되는 의무 표기 사항((광고), 080 수신거부 등)을 기술적 조치나 편법을 통해 임의로 삭제·변경·우회하는 행위</li>
            <li style="margin-bottom: 6px;">서비스의 안정적인 운영에 지장을 주거나 줄 우려가 있는 일체의 행위</li>
            <li style="margin-bottom: 6px;">제3자에게 임의로 서비스를 임대하는 행위</li>
            <li style="margin-bottom: 6px;">정보통신망법 제44조의 7(불법정보의 유통금지 등) 규정에 따라 불법스팸, 사기, 협박, 음란성, 범죄를 목적으로 하거나 교사 또는 방조하는 내용의 정보, 발신번호조작 등으로 인지되는 메시지를 발송하는 행위</li>
            <li style="margin-bottom: 6px;">기타 불법적이거나 부당한 행위</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 이용자는 이용자의 정보통신설비가 서비스 이메일 도용, 해킹, 바이러스 침입 등으로 불법스팸 발송에 오남용 되지 않도록 보안조치를 취하여야 합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 이용자는 정보통신망법에 따라 메시지 전송을 위하여 수신자의 사전 수신동의를 직접 얻어야 하며, 수신거부 요청에 대해서는 즉각적으로 처리해야 합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 이용자는 전기통신사업법 등 관련 법령에 따라 발신번호 사전등록을 완료하고 등록된 번호로만 메시지를 발송해야 합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 이용자가 회사에 제공한 수신자 정보(휴대전화번호 등)는 적법한 절차에 따라 수집된 것이어야 하며, 이와 관련하여 발생하는 개인정보보호법 위반 등의 법적 책임은 전적으로 이용자에게 있습니다.</p>
            
            <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제4장 이용자의 권리에 관한 조치</h4>
            <p style="margin-bottom: 8px; padding-left: 16px;">제12 조 (동의의 철회)</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">회사는 이용자가 서비스 화면에서 자신의 개인정보에 대한 수집, 이용 또는 제공에 대한 동의를 철회할 수 있도록 필요한 조치를 취해야 합니다.</p>
            <p style="margin-bottom: 12px;"><strong>제13조(이용자의 불만사항 접수 및 처리절차)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 불만사항은 일반전화, 이메일, 1:1 문의 등을 통해 접수합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 접수된 사항을 신속하게 처리하며, 처리가 곤란한 경우 그 사유와 일정을 통보합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 고객센터의 운영 시간 및 상담 채널(전화, 1:1 문의 등)은 홈페이지 내 공지사항 또는 고객센터</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">안내 페이지에 따릅니다. 운영 시간 외 접수된 문의는 익영업일에 순차적으로 처리됩니다.</p>
            
            
            <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제5장 서비스의 이용</h4>
            <p style="margin-bottom: 12px;"><strong>제14조 (서비스의 제공 및 변경)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 회원에게 문자(SMS, LMS, MMS), 카카오 알림톡, 카카오 브랜드 메시지 등 메시지 발송 및 부가 서비스를 제공합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 서비스는 연중무휴, 1일 24시간 제공을 원칙으로 합니다.</p>
            <p style="margin-bottom: 12px;"><strong>제15조 (서비스의 변경 및 중단)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 서비스 품질 향상 및 운영 상 필요에 따라 서비스의 전부 또는 일부를 변경, 추가, 중단할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 정기 점검, 긴급 점검, 시스템 교체 등 부득이한 사유가 있는 경우 서비스의 전부 또는 일부를 중단할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사는 무료로 제공되는 서비스의 일부 또는 전부를 회사의 정책 및 운영의 필요상 수정, 중단, 변경할 수 있으며 이에 대하여 관련법에 특별한 규정이 없는 한 이용자에게 별도의 보상을 하지 않습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제16조 (서비스 이용의 제한 및 정지)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 이용자가 다음 중 하나에 해당하는 경우 서비스의 이용을 제한하거나 정지할 수 있습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">방송통신위원회ㆍ한국인터넷진흥원 등 관계기관이 불법스팸 전송 사실을 확인하여 이용정지를 요청하는 경우</li>
            <li style="margin-bottom: 6px;">수신자의 스팸 신고가 급증하거나 스팸 발송이 확인된 경우</li>
            <li style="margin-bottom: 6px;">이용자가 발송하는 메시지로 인하여 회사의 서비스 제공에 장애를 야기하거나 야기할 우려가 있는 경우</li>
            <li style="margin-bottom: 6px;">이용자에게 제공하는 서비스가 스팸메시지ㆍ불법스팸메시지 발송에 이용되고 있는 경우</li>
            <li style="margin-bottom: 6px;">과학기술정보통신부장관 또는 한국인터넷진흥원 등 관련 기관이 발신번호 변작 등을 확인하여 이용정지를 요청하는 경우</li>
            <li style="margin-bottom: 6px;">회사 서비스의 안정적 운영을 방해할 목적으로 다량의 정보를 발송하거나 정보통신설비의 오동작 또는 시스템 보유 정보 파괴를 유발시키거나 유포하는 경우</li>
            <li style="margin-bottom: 6px;">이용자가 발신번호를 변작하는 등 거짓으로 표시한 경우</li>
            <li style="margin-bottom: 6px;">기타 관련 법령 또는 이 약관에서 금지하는 행위를 하거나 회사가 정한 이용조건에 위배되는 행위를 한 경우</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 이용제한 및 정지를 하고자 하는 경우에는 그 사유, 일시 및 기간을 정하여 회원에게 통지합니다. 단, 긴급한 경우 사전 통지 없이 제한할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 스팸 발송, 명의 도용 등으로 영구 정지된 경우, 보유한 포인트 및 마일리지는 소멸되며 환불되지 않습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제16조의2 (휴면 회원의 관리)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 이용자의 정보가 부당한 목적으로 사용되는 것을 방지하고 보다 원활한 서비스 제공을 위하여 12개월 이상 계속해서 로그인을 포함한 서비스 이용이 없는 계정을 휴면 회원으로 분류하고 서비스 이용을 정지할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">②회사는 휴면 전환 예정일 30일 전 및 7일 전에 회원에게 통지하며, 휴면 회원의 계정 정보는 전환일로부터 최대 5년 동안 별도 분리하여 보관합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 휴면 회원이 보유한 포인트 및 마일리지의 소멸 예정일 30일 전, 7일 전, 1일 전에 만료 안내를 통지합니다. (마케팅 수신 동의 여부와 무관하게 발송)</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 휴면 회원은 로그인을 통해 휴면 상태를 해제할 수 있습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제17조 (계약해지)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 이용자는 언제든지 탈퇴를 요청할 수 있습니다. 단, 다음의 경우 탈퇴 처리가 지연될 수 있습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">예약 발송이 남아있는 경우</li>
            <li style="margin-bottom: 6px;">환불 가능한 잔액에 대한 환불 신청을 하지 않은 경우</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사는 이용자가 타인의 명의 도용, 스팸 전송, 발신번호 변작 등 중대한 약관 위반 행위를 한 경우 이용자의 동의 없이 이용계약을 해지할 수 있습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">회사는 주민등록법을 위반한 명의도용 및 결제도용, 저작권법을 위반한 불법프로그램의 제공 및 운영방해, 정보통신망법을 위반한 스팸메시지 및 불법통신, 해킹, 악성프로그램의 배포, 접속권한 초과행위, 한국인터넷진흥원이 규정한 변작 등과 같이 관련법을 위반한 경우에는 즉시 사전 통보 없이 영구 이용정지를 할 수 있습니다.</li>
            <li style="margin-bottom: 6px;">서비스의 영구 이용정지 시에는 서비스 내의 포인트, 예치금, 혜택 및 권리 등도 모두 즉시 소멸되며 회사는 이에 대해 별도로 보상하지 않습니다.</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 해지 즉시 이용자의 모든 데이터는 소멸됩니다(단, 관련 법령에 따라 보관해야 하는 정보 제외).</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 제1항 제2호에도 불구하고, 회원이 소액 잔액에 대한 권리를 포기하고 즉시 탈퇴를 희망하는 경우 잔액 소멸에 동의한 후 탈퇴할 수 있습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제18조 (문자 발송량 제한)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 스팸 방지 및 시스템 안정을 위해 다음과 같이 발송량을 제한합니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">개인 회원: 1일 500건 (단, 회사가 인정하는 적법한 증빙서류 제출 시 예외 허용)</li>
            <li style="margin-bottom: 6px;">사업자 회원: 1회 최대 1,000,000건</li>
            <li style="margin-bottom: 6px;">선거 회원: 발송량 제한 없음 (단, 자동 동보통신 횟수 8회 제한 등 공직선거법 준수)</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 전항의 기준에도 불구하고 불법스팸 전송이 의심되거나 시스템 부하가 우려되는 경우 발송을 제한할 수 있습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제19조 (각종 자료의 저장기간)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 서비스 제공 중 발생한 데이터에 대해 다음 기간 동안 보관 후 파기합니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">통신비밀보호법에 따른 로그인 기록: 3개월</li>
            <li style="margin-bottom: 6px;">전자상거래법에 따른 대금 결제 및 공급 기록: 5년</li>
            <li style="margin-bottom: 6px;">스팸 발송 등으로 차단된 메시지 전송 로그: 1년</li>
            <li style="margin-bottom: 6px;">탈퇴 회원의 개인식별정보(재가입 방지용): 탈퇴일로부터 12개월</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회원은 자료의 보관 기간이 경과하기 전에 발송 내역 등을 직접 백업해야 하며, 보관 기간 경과 후 데이터 삭제에 대해 회사는 책임지지 않습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제20조 (게시물의 저작권)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 서비스에 대한 저작권 및 지적재산권은 회사에 귀속됩니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회원이 서비스 페이지에 게시하거나 등록한 자료의 지적재산권은 회원에게 귀속됩니다. 단, 회사는 서비스 홈페이지의 게재권을 가지며 회사의 서비스 내에 한하여 회원의 게시물을 활용할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회원은 서비스를 이용하여 얻은 정보를 가공, 판매하는 행위 등 게재된 자료를 상업적으로 이용할 수 없으며 이를 위반하여 발생하는 제반 문제에 대한 책임은 회원에게 있습니다.</p>
            
            <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제6장 요금 및 환불</h4>
            <p style="margin-bottom: 12px;"><strong>제21조 (요금 계산 및 결제)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사가 제공하는 유료서비스 이용과 관련하여 회원이 납부하여야 할 요금은 이용료 안내에 게재한 바에 따릅니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 서비스 이용 요금은 선불 충전(포인트) 차감 방식을 원칙으로 합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 메시지 발송 실패 시 차감된 포인트는 자동으로 복구(재적립)되는 것을 원칙으로 합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">단, 다음 각 호의 경우에는 발송이 실패 처리되더라도 포인트가 복구되지 않습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">스팸성 문구 포함, KISA(한국인터넷진흥원)의 요청 등으로 인해 통신사가 강제로 발송을 차단한 경우</li>
            <li style="margin-bottom: 6px;">발송 결과가 ‘성공(Success)’인 경우 (수신자가 단말기 자체 기능으로 수신을 차단하여 확인하지 못한 경우 포함)</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 이용자는 이용자의 관리 소홀 및 부주의로 인해 이용요금이 발생될 경우, 이에 대한 이용요금을 자신의 비용으로 모두 부담해야 합니다.</p>
            <p style="margin-bottom: 12px;"><strong>제22조 (포인트의 유효기간)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 유료 충전한 포인트의 유효기간은 마지막 충전일로부터 1년입니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 무상으로 지급된 마일리지의 유효기간은 지급일로부터 1년입니다. 단, 마케팅 이벤트 등을 통해 지급된 한시적 마일리지의 경우 별도로 공지된 유효기간을 따릅니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 유효기간이 경과한 포인트와 마일리지는 자동으로 소멸되며, 복구되지 않습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 회사는 포인트 및 마일리지의 소멸 예정일 30일 전, 7일 전, 1일 전에 회원에게 등록된 연락처(휴대전화 또는 이메일)로 소멸 내역을 통지합니다. 이는 마케팅 수신 동의 여부와 관계없이 발송될 수 있습니다. 다만, 제9조 [회원에 대한 통지]에 따라 회원이 이메일 또는 휴대전화번호의 부재, 변경, 오류 등 또는 정보를 허위로 제출하거나 변경된 정보를 회사에 알리지 않은 경우 회사는 회원이 제출한 정보로 통지를 발송한 때에 회원에게 도달된 것으로 봅니다.</p>
            <p style="margin-bottom: 12px;"><strong>제23조 (요금 등의 환불)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회원은 잔여 포인트가 10,000포인트 이상이고 예약된 발송 건이 없는 경우에 한해 환불을 신청할 수 있습니다. 1만 포인트 미만 소액 잔여분의 환불 요청은 반려될 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">환불 규정은 다음과 같습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">최소 환불 가능 금액: 잔여 포인트가 10,000포인트 이상 시 신청 가능합니다.</li>
            <li style="margin-bottom: 6px;">환불 수수료:</li>
            <li style="margin-bottom: 6px;">전액 결제 취소: 충전 후 7일 이내이며, 포인트 및 마일리지를 전혀 사용하지 않은 경우</li>
            <li style="margin-bottom: 6px;">환불: 충전 후 7일이 경과하였거나, 포인트를 일부라도 사용한 경우 잔여금액의 10%를 환불수수료로 공제 후 환불</li>
            <li style="margin-bottom: 6px;">마일리지 사용 시 : 충전 후 7일 이내라 하더라도, 충전 시 지급된 무료 마일리지를 사용한 경우에는 해당 결제 건을 서비스를 이용한 것으로 간주하여 잔여 포인트의 10%를 환불수수료로 공제 후 환불</li>
            <li style="margin-bottom: 6px;">선거 회원 특례: 선거 기간 종료 후 남은 잔액은 수수료 없이 100% 전액 환불합니다.</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 무료 지급된 마일리지는 환불 대상이 아니며 소멸됩니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 환불은 신청일로부터 영업일 기준 7일 이내에 등록된 계좌로 지급합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 회원이 관계 법령이나 약관을 위반하여 부당하게 요금을 면탈한 경우, 회사는 면탈한 금액의 2배에 해당하는 금액을 청구할 수 있습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 환불은 이용자가 충전 시 사용한 결제 수단으로 지급(결제 취소 등)하는 것을 원칙으로 합니다. 단, 현금 환불이 필요한 경우 다음 각 호의 기준을 따릅니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">개인 회원: 가입된 회원 본인 명의의 계좌로만 환불 가능</li>
            <li style="margin-bottom: 6px;">사업자(법인) 회원: 가입된 사업자(법인) 명의의 계좌로만 환불 가능 (대표자 개인 명의 등 타 명의 불가)</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑥ 제5항에도 불구하고 휴업, 폐업, 명의 변경 등으로 인하여 원 결제 수단 또는 등록된 계좌로의 환불이 불가능한 경우, 회원은 고객센터를 통해 정보 변경을 요청해야 합니다. 이때 회사는 회원에게 폐업사실증명원, 인감증명서 등 증빙 서류 제출을 요구할 수 있으며, 서류 확인 후 환불을 진행합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑦ 환불은 신청일(서류 제출이 필요한 경우 서류 접수 완료일)로부터 영업일 기준 7일 이내에 지급합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑧ 다음과 같은 경우 포인트는 환불되지 않습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">포인트 유효기간이 만료된 경우</li>
            <li style="margin-bottom: 6px;">제16조 (서비스 이용의 제한 및 정지)에 의한 영구 이용정지의 경우</li>
            <li style="margin-bottom: 6px;">회원이 서비스 자진 탈퇴 시 잔여 포인트 환불을 포기한 경우</li>
            </ul>
            
            <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제7장 손해배상 등</h4>
            <p style="margin-bottom: 12px;"><strong>제24조 (손해배상)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사의 귀책사유로 인해 서비스를 이용하지 못한 경우, 회사는 회원이 입은 손해를 배상합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 손해배상은 회원이 서비스를 이용하지 못한 시간에 해당하는 이용 요금의 3배를 한도로 합니다.</p>
            <p style="margin-bottom: 12px;"><strong>제25조 (면책)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 회사는 다음 각 호의 경우로 서비스를 제공할 수 없는 경우, 이로 인하여 이용자에게 발생한 손해에 대해서는 책임을 부담하지 않습니다.</p>
            <ul style="padding-left: 32px; margin-bottom: 16px;">
            <li style="margin-bottom: 6px;">천재지변, 기간통신사업자(통신사, 카카오)의 장애 등 불가항력의 상태가 있는 경우</li>
            <li style="margin-bottom: 6px;">서비스의 효율적인 제공을 위한 시스템 개선, 장비 증설 등 계획된 서비스 중지 일정을 사전에 공지한 경우</li>
            <li style="margin-bottom: 6px;">회사의 고의 또는 과실이 없는 사유로 인한 경우</li>
            <li style="margin-bottom: 6px;">이용자의 귀책사유(수신번호 오입력, 단말기 문제 등)로 서비스 이용에 장애가 있는 경우</li>
            </ul>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 회사는 제16조에 따라 이용자의 서비스 이용을 정지하거나 제한 또는 거절하는 경우, 이로 인하여 발생할 수 있는 이용자의 손해 등에 대해서는 책임을 부담하지 않습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">③ 회사는 무료로 제공하는 서비스(마일리지 발송 등) 이용과 관련하여 발생한 손해에 대해서는 책임을 지지 않습니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">④ 회사는 이용자가 게시 또는 전송한 자료의 내용에 대해서는 책임을 면합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑤ 회사는 이용자 상호간 또는 이용자와 제3자 상호간에 서비스를 매개로 하여 물품거래 등을 한 경우에는 책임을 면합니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">⑥ 회사는 선거 회원의 선거 비용 보전을 위해 발송 결과 리포트, 세금계산서, 080 수신거부 내역, 입금 확인증 등 회사가 제공하는 표준 양식의 증빙 서류를 제공합니다. 이용자가 특정 양식을 별도로 요구하거나, 선거관리위원회 제출 과정에서 발생한 서류 누락, 기한 경과, 보전 거부 등에 대해서는 책임을 지지 않습니다.</p>
            <p style="margin-bottom: 12px;"><strong>제25조 (분쟁조정 및 관할법원)</strong></p>
            <p style="margin-bottom: 8px; padding-left: 16px;">① 본 약관은 대한민국법령에 의하여 규정되고 이행됩니다.</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">② 서비스 이용과 관련하여 발생한 분쟁에 대해 소송이 제기될 경우, 회사의 본사 소재지를 관할하는 법원을 전속 관할 법원으로 합니다.</p>
            
            
            
            
            <p style="margin-bottom: 8px; padding-left: 16px;">부칙</p>
            <p style="margin-bottom: 8px; padding-left: 16px;">본 약관은 2026년 XX월 XX일부터 시행합니다.</p>
            </div>
        `,
        'privacy': `
            <div style="line-height: 1.8; color: var(--text-primary);">
                <p style="margin-bottom: 24px;">
                    ㈜아이뱅크(이하 "회사")는 「개인정보보호법」 제30조에 따라 이용자(정보주체)의 개인정보를 보호하고 이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 하기 위하여 다음과 같이 개인정보처리방침을 수립•공개합니다. 본 개인정보처리방침은 톡벨(TalkBell) 서비스(이하 "서비스")를 이용하는 이용자에게 적용됩니다.
                </p>
                
                <p style="margin-bottom: 12px;"><strong>제1조 (개인정보의 처리목적)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">회사는 다음의 목적을 위하여 개인정보를 처리합니다.</p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;"><strong>서비스 제공 및 계약 이행</strong>: 회원가입, 본인확인, 메시지(SMS/LMS/MMS, 알림톡, 친구톡 등) 발송 및 결과 제공, 유료 서비스 이용에 따른 요금 정산 및 결제, 발신번호 등록 및 관리</li>
                    <li style="margin-bottom: 6px;"><strong>회원 관리</strong>: 서비스 이용에 따른 본인확인, 개인식별, 불량회원의 부정 이용 방지와 비인가 사용 방지, 가입의사 확인, 휴면 계정 관리, 분쟁 조정을 위한 기록보존, 민원처리, 고지사항 전달</li>
                    <li style="margin-bottom: 6px;"><strong>선거문자 서비스 제공</strong>: 공직선거법에 따른 선거 회원 자격 확인, 선거 운동 문자 발송 및 080 수신거부 관리, 선거관리위원회 제출용 증빙서류 발급</li>
                    <li style="margin-bottom: 6px;"><strong>마케팅 및 광고 활용</strong>: 신규 서비스 개발, 접속 빈도 파악, 회원의 서비스 이용에 대한 통계, 이벤트 정보 및 참여기회 제공, 광고성 정보 제공(동의 시)</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제2조 (개인정보의 처리 및 보유 기간)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>① 법령에 따른 개인정보 처리 및 보유기간</strong></p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">법적근거</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">보존항목</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">보존기간</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;" rowspan="4">전자상거래 등에서의 소비자보호에 관한 법률</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">계약 또는 청약철회 등에 관한 기록</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">5년</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">대금 결제 및 재화 등의 공급에 관한 기록</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">5년</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">소비자의 불만 또는 분쟁 처리에 관한 기록</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">3년</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">표시/광고에 관한 기록</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">6개월</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">국세기본법, 법인세법</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">세법상 거래 증빙에 관한 기록</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">5년</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">통신비밀보호법</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">서비스 접속(로그) 기록</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">3개월</td>
                    </tr>
                </table>
                
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>② 서비스 정책에 따른 처리 및 보유 기간</strong></p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">보존항목</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">보존근거</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">보존기간</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">계정 식별 정보 (아이디, 휴대전화번호, CI/DI)</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">재가입 방지, 부정 이용 방지, 수사 협조</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">탈퇴일로부터 12개월</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">휴면 회원 정보</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">개인정보 보호 (별도 분리 보관)</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">휴면 전환일로부터 5년</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">발신번호 및 증빙서류</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">전기통신사업법에 따른 거짓번호 방지</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">서비스 종료 시까지</td>
                    </tr>
                </table>
                
                <p style="margin-bottom: 12px;"><strong>제3조 (처리하는 개인정보 항목)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>가) 회원 유형별 수집 항목</strong></p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">구분</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">유형</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">수집하는 개인정보 항목</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;" rowspan="2">개인 회원</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">필수</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">이름, 비밀번호, 휴대폰번호, 이메일(ID), CI/DI</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">선택</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">마케팅/광고 정보 수신동의</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;" rowspan="2">사업자 회원</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">필수</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">[대표] 이름, 비밀번호, 휴대폰번호, 이메일(ID), 회사명, 사업자등록번호, 대표자명, 사업장주소, 업태/종목, 담당자 정보, 사업자등록증 사본<br>[담당자] 이름, 비밀번호, 휴대폰번호, 이메일(ID)</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">선택</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">마케팅/광고 정보 수신동의, 세금계산서 담당자 정보</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">선거 회원</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">필수</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">(예비)후보자 등록 증명서, 위임장, 선거사무소 전화번호, 담당자 재직증명서</td>
                    </tr>
                </table>
                
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>나) 서비스 이용 과정에서 자동 수집되는 정보</strong></p>
                <p style="margin-bottom: 16px; padding-left: 16px;">IP Address, 쿠키, 방문 일시, 서비스 이용 기록, 접속 로그, 불량 이용 기록, 브라우저 정보, 기기 정보</p>
                
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>다) 서비스 이용 및 결제 과정에서 추가 수집되는 정보</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;"><strong>결제 및 환불</strong>: 신용카드 정보, 은행 계좌 정보, 입금자명</li>
                    <li style="margin-bottom: 6px;"><strong>발신번호 등록</strong>: 통신서비스이용증명원, 재직증명서, 위임장</li>
                    <li style="margin-bottom: 6px;"><strong>고객상담</strong>: 상담 신청 내용, 1:1 문의 내용 및 첨부파일</li>
                    <li style="margin-bottom: 6px;"><strong>세금계산서</strong>: 법인통장 사본</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제4조 (개인정보의 제3자 제공)</strong></p>
                <p style="margin-bottom: 24px; padding-left: 16px;">
                    회사는 원칙적으로 이용자의 개인정보를 제3자에게 제공하지 않습니다. 다만, 이용자의 별도 동의가 있거나 법령의 규정에 의한 경우(수사기관의 요구 등)는 예외로 합니다.
                </p>
                
                <p style="margin-bottom: 12px;"><strong>제5조 (개인정보 처리업무의 위탁에 관한 사항)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">회사는 원활한 서비스 제공을 위해 다음과 같이 개인정보 처리업무를 위탁하고 있습니다.</p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">수탁업체명</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">위탁업무 내용</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">결제대행사 (토스페이먼츠 등)</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">신용카드, 계좌이체, 가상계좌 결제 대행</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">Infobip (인포빕)</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">글로벌 메시지 발송 시스템 연동 및 정산</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">(주)카카오</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">알림톡, 친구톡(브랜드메시지) 발송 및 템플릿 검수</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">NICE평가정보 / KCB</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">휴대폰 본인인증 및 실명확인</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">Google LLC</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">웹 로그 분석 (Google Analytics)</td>
                    </tr>
                </table>
                
                <p style="margin-bottom: 12px;"><strong>제6조 (개인정보 파기 절차 및 방법에 관한 사항)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;"><strong>파기절차</strong>: 이용자가 입력한 정보는 목적 달성 후 별도의 DB에 옮겨져 내부 방침 및 기타 관련 법령에 따라 일정 기간 저장된 후 파기됩니다. 휴면 회원의 정보는 별도 분리하여 보관하며 5년 경과 시 파기합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>파기방법</strong>: 전자적 파일 형태는 복구 및 재생할 수 없는 기술적 방법을 사용하여 삭제, 종이 문서는 분쇄기로 분쇄하거나 소각합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제7조 (정보 주체와 법정대리인의 권리•의무 및 행사 방법)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">정보주체는 언제든지 개인정보 열람•정정•삭제•처리 정지 요구 등의 권리를 행사할 수 있습니다.</li>
                    <li style="margin-bottom: 6px;">권리 행사는 서면, 전자우편, 모사전송(FAX) 등을 통하여 하실 수 있으며 회사는 이에 대해 지체 없이 조치하겠습니다.</li>
                    <li style="margin-bottom: 6px;">만 14세 미만 아동의 개인정보는 수집하지 않음을 원칙으로 합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제8조 (개인정보의 안전성 확보 조치에 관한 사항)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>① 기술적 대책</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 12px;">
                    <li style="margin-bottom: 6px;">개인정보의 암호화: 비밀번호는 일방향 암호화, 주요 정보는 안전한 알고리즘으로 암호화 저장</li>
                    <li style="margin-bottom: 6px;">통신 구간 암호화: SSL/TLS 프로토콜을 통한 전송 구간 암호화 적용</li>
                    <li style="margin-bottom: 6px;">해킹 방지: 방화벽, 침입 탐지 시스템 운영 및 외부 접근 통제</li>
                </ul>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>② 관리적 대책</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 12px;">
                    <li style="margin-bottom: 6px;">접근 권한 관리: 개인정보 처리 인원을 최소한으로 제한 및 권한 관리</li>
                    <li style="margin-bottom: 6px;">정기 교육: 개인정보 취급자 대상 정기적인 보호 교육 실시</li>
                </ul>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>③ 물리적 대책</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">전산실 및 자료 보관실 접근 통제</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제9조 (개인정보의 자동수집 장치의 설치, 운영 및 그 거부에 관한 사항)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">회사는 이용자에게 맞춤화된 서비스를 제공하기 위해 쿠키(Cookie) 및 Google Analytics와 같은 분석 도구를 사용합니다.</li>
                    <li style="margin-bottom: 6px;">이용자는 웹 브라우저 설정을 통해 쿠키 저장을 거부할 수 있습니다. 단, 쿠키 저장을 거부할 경우 로그인이 필요한 일부 서비스 이용에 어려움이 있을 수 있습니다.</li>
                    <li style="margin-bottom: 6px;">Google Analytics의 경우, 개인을 식별할 수 없는 형태로 정보를 수집하며 이용자는 Google의 차단 기능을 통해 수집을 거부할 수 있습니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제10조 (개인정보 보호책임자에 관한 사항)</strong></p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">구분</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">개인정보보호책임자(CPO)</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">개인정보보호담당자</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">성명</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">[책임자 성명]</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">[담당자 성명]</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">전화</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;" colspan="2">1588-5412</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">이메일</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;" colspan="2">privacy@talkbell.co.kr / support@talkbell.co.kr</td>
                    </tr>
                </table>
                
                <p style="margin-bottom: 12px;"><strong>제11조 (정보주체의 권익 침해에 대한 구제 방법)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">정보주체는 개인정보침해로 인한 구제를 받기 위하여 아래의 기관에 문의할 수 있습니다.</p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">개인정보 분쟁조정위원회 (kopico.go.kr / 1833-6972)</li>
                    <li style="margin-bottom: 6px;">개인정보 침해신고센터 (privacy.kisa.or.kr / 118)</li>
                    <li style="margin-bottom: 6px;">대검찰청 (www.spo.go.kr / 1301)</li>
                    <li style="margin-bottom: 6px;">경찰청 (ecrm.police.go.kr / 182)</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제12조 (개인정보 열람청구 접수·처리하는 부서)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">부서명: 톡벨 고객서비스팀</li>
                    <li style="margin-bottom: 6px;">연락처: 1588-5412, support@talkbell.co.kr</li>
                    <li style="margin-bottom: 6px;">운영시간: 평일 09:30 ~ 17:30 (점심시간 11:30~13:00 제외)</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제13조 (개인정보 처리방침의 변경에 관한 사항)</strong></p>
                <p style="margin-bottom: 16px; padding-left: 16px;">
                    본 개인정보처리방침의 내용 추가, 삭제 및 수정이 있을 시에는 최소 7일 전부터 홈페이지 공지사항을 통해 고지할 것입니다.
                </p>
                
                <p style="margin-top: 24px; padding: 16px; background-color: var(--bg-color, #f8fafc); border-radius: 8px;">
                    이 개인정보처리방침은 202X년 X월 X일부터 적용됩니다.
                </p>
            </div>
        `,
        'spam': `
            <div style="line-height: 1.8; color: var(--text-primary);">
                <p style="margin-bottom: 24px;">
                    주식회사 아이뱅크(이하 "회사")는 다수 이용자의 편리한 서비스 이용과 스팸, 불법스팸으로 인한 폐해를 방지하기 위해 스팸방지정책을 수립하여 운영하고 있습니다. 아래와 같이 불법스팸(문자, 팩스, 카카오 비즈메시지)을 발송한 이용자에 대해서는 이용정지 및 해지, 형사고발 등의 조치를 취하겠습니다.
                </p>
                
                <p style="margin-bottom: 12px;"><strong>1. 용어 정의</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;"><strong>스팸</strong>: 정보통신망을 통해 이용자가 원하지 않는데도 불구하고 일방적으로 전송 또는 게시되는 영리목적의 광고성 정보</li>
                    <li style="margin-bottom: 6px;"><strong>불법스팸</strong>: 정보통신망 이용촉진 및 정보보호 등에 관한 법률(이하 "정보통신망법") 및 회사 운영정책을 위반하여 전송 또는 게시되는 영리목적의 광고성 정보</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>2. 발송 시 유의사항</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">"정보통신망법" 제50조에 의한 문자, 카카오 비즈메시지 등 발송 시 유의사항에 대해 안내 드립니다.</p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">영리 목적의 광고성 문자, 알림톡, 친구톡 등을 발송 시 반드시 수신자의 <strong>사전 동의</strong>를 얻어야 합니다.</li>
                    <li style="margin-bottom: 6px;">수신자의 사전 동의를 얻었다 하더라도 메시지 내용에 <strong>무료 수신거부 방법(080 번호 등)</strong>을 반드시 표시하여야 합니다.</li>
                    <li style="margin-bottom: 6px;">수신자의 수신 거부 시 기술적으로 수신거부를 회피하거나 방해해서는 안 됩니다.</li>
                    <li style="margin-bottom: 6px;">야간 시간대(오후 9시 ~ 다음날 오전 8시)에 광고성 정보를 전송할 경우 수신자로부터 별도의 <strong>야간 수신 동의</strong>를 얻어야 합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>3. 스팸방지 관련 약관 공지</strong></p>
                <div style="background-color: var(--bg-color, #f8fafc); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <p style="margin-bottom: 12px;"><strong>제11조 [이용자의 의무]</strong></p>
                    <p style="margin-bottom: 16px; padding-left: 16px;">4. 이용자는 스팸 또는 불법스팸을 전송함으로써 발생하는 모든 민·형사상의 책임을 부담합니다.</p>
                    
                    <p style="margin-bottom: 12px;"><strong>제16조 [서비스 이용의 제한 및 정지]</strong></p>
                    <p style="margin-bottom: 8px; padding-left: 16px;">2. 회사는 명의도용, 불법스팸 전송, 해킹, 악성 프로그램 배포 등 관련 법령 및 운영정책을 위반한 경우 즉시 영구이용정지를 할 수 있습니다. 이 경우 서비스 내 잔액, 포인트, 마일리지 등은 소멸되며 회사는 이를 보상하지 않습니다.</p>
                    <p style="margin-bottom: 8px; padding-left: 16px;">3. 회사는 다음 각 호에 해당하는 경우 서비스 이용을 정지할 수 있습니다.</p>
                    <ul style="padding-left: 32px; margin-bottom: 12px;">
                        <li style="margin-bottom: 4px;">① 방송통신위원회 또는 한국인터넷진흥원(KISA)이 불법스팸 전송사실을 확인하여 이용정지를 요청하는 경우</li>
                        <li style="margin-bottom: 4px;">② 이용자가 전송하는 대량의 스팸으로 인하여 회사의 시스템 장애를 야기하거나 야기할 우려가 있는 경우</li>
                        <li style="margin-bottom: 4px;">③ 수신자가 스팸으로 신고하는 건수가 급증하는 경우</li>
                    </ul>
                    <p style="margin-bottom: 16px; padding-left: 16px;">5. 회사는 스팸 전송을 방지하기 위하여 일일 발송량을 제한할 수 있으며, 자체 모니터링 시스템을 통해 감시를 강화할 수 있습니다.</p>
                    
                    <p style="margin-bottom: 12px;"><strong>제17조 [계약해지]</strong></p>
                    <p style="margin-bottom: 8px; padding-left: 16px;">2. 회사는 이용자가 다음 각 호에 해당할 경우 동의 없이 이용계약을 해지할 수 있습니다.</p>
                    <ul style="padding-left: 32px; margin-bottom: 12px;">
                        <li style="margin-bottom: 4px;">① 이용자가 약관을 위반하고 일정 기간 내에 위반 내용을 해소하지 않는 경우</li>
                        <li style="margin-bottom: 4px;">② 방송통신위원회 또는 KISA가 불법스팸 전송사실을 확인하여 계약해지를 요청하는 경우</li>
                        <li style="margin-bottom: 4px;">③ 이용정지 조치 이후 1년 이내에 동일한 사유가 재발한 경우</li>
                    </ul>
                    
                    <p style="margin-bottom: 12px;"><strong>제18조 [발송량 제한]</strong></p>
                    <p style="margin-bottom: 8px; padding-left: 16px;">회사는 스팸 방지를 위해 아래와 같이 발송량을 제한합니다.</p>
                    <ul style="padding-left: 32px;">
                        <li style="margin-bottom: 4px;">개인 회원: 1일 500건 (전기통신사업법 준수)</li>
                        <li style="margin-bottom: 4px;">사업자 회원: 1회 최대 1,000,000건 (운영 상황에 따라 조정 가능)</li>
                        <li style="margin-bottom: 4px;">단, 적법한 업무용 광고 발송 등 소명을 통해 사전 승인을 얻은 경우 제한을 완화할 수 있습니다.</li>
                    </ul>
                </div>
                
                <p style="margin-bottom: 12px;"><strong>4. 사전 수신동의</strong></p>
                <div style="background-color: #fff3cd; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <p style="margin-bottom: 8px;"><strong>제50조 (영리목적의 광고성 정보전송의 제한)</strong></p>
                    <p style="margin-bottom: 8px; padding-left: 16px;">1. 누구든지 수신자의 명시적인 수신거부의사에 반하는 영리목적의 광고성 정보를 전송하여서는 아니 된다.</p>
                    <p style="padding-left: 16px;">2. 수신자의 전화·모사전송기기에 영리목적의 광고성 정보를 전송하고자 하는 자는 당해 수신자의 사전 동의를 받아야 한다.</p>
                </div>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">광고 전송자는 전송 이전에 내용 및 전송매체에 대해 정확히 고지하고 동의를 받아야 합니다.</li>
                    <li style="margin-bottom: 6px;">하나의 사업자가 여러 서비스를 제공할 경우, 포괄적 동의가 아닌 <strong>서비스 유형별 개별 동의</strong>를 받아야 합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>5. 기존 거래관계</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">기존 거래관계가 있었거나 현재 지속 중인 이용자에게는 동종의 재화 및 서비스에 대한 광고에 한해 별도 동의 없이 전송할 수 있습니다.</li>
                    <li style="margin-bottom: 6px;">단순 무료 서비스 가입이나 문의만으로는 거래관계가 성립되지 않으므로 주의해야 합니다.</li>
                    <li style="margin-bottom: 6px;">거래관계에 의한 예외는 해당 거래를 기초로 하므로, 거래가 종료된 후 <strong>6개월이 경과</strong>한 경우에는 다시 사전 동의를 받는 것을 권장합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>6. 수신동의 철회</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">톡벨 서비스는 모든 광고성 메시지에 <strong>080 무료 수신거부 번호</strong>를 자동으로 포함하여 제공합니다. 회원은 이를 임의로 삭제하거나 변경해서는 안 됩니다.</li>
                    <li style="margin-bottom: 6px;">수신거부 의사는 해당 전송자가 보내는 모든 광고에 적용되어야 합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>7. 광고전송 허용시간</strong></p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">구분</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">시간</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">일반 전송 가능 시간</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">오전 8시 ~ 오후 9시</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">야간 전송 제한 시간</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">오후 9시 ~ 다음날 오전 8시 (별도 동의 필요)</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">카카오 브랜드 메시지</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">오후 8시 50분부터 제한될 수 있음</td>
                    </tr>
                </table>
                
                <p style="margin-bottom: 12px;"><strong>8. 광고 전송 시 표시사항</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>[문자 메시지의 명시사항 및 방법]</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 16px;">
                    <li style="margin-bottom: 6px;"><strong>(광고) 문구</strong>: 본문 시작 부분에 반드시 표기해야 합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>전송자 명칭 및 연락처</strong>: 수신자가 식별할 수 있는 업체명 또는 서비스명을 본문에 표기해야 합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>무료 수신거부 번호</strong>: 본문 하단 또는 끝부분에 080 번호 등을 명시하여 비용 부담 없이 수신거부할 수 있음을 알려야 합니다.</li>
                </ul>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>[카카오톡 비즈메시지의 명시사항]</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;"><strong>알림톡</strong>: 정보성 메시지만 가능하며, 광고성 내용이 포함될 경우 발송이 반려됩니다.</li>
                    <li style="margin-bottom: 6px;"><strong>친구톡/브랜드 메시지</strong>: (광고) 표기 및 수신거부 방법(채널 차단 등)이 포함되어야 합니다.</li>
                </ul>
                <p style="margin-bottom: 16px; padding: 12px; background-color: #d1fae5; border-radius: 8px;">
                    💡 톡벨 시스템은 광고 메시지 발송 시 (광고) 문구와 080 번호를 자동으로 삽입합니다.
                </p>
                
                <p style="margin-bottom: 12px;"><strong>9. 스팸을 위한 기술적 조치 금지</strong></p>
                <div style="background-color: #fee2e2; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <p style="margin-bottom: 8px;"><strong>제50조 (영리목적의 광고성 정보전송의 제한)</strong></p>
                    <p style="margin-bottom: 8px;">6. 영리를 목적으로 광고를 전송하는 자는 다음 각 호의 기술적 조치를 하여서는 아니 된다.</p>
                    <ul style="padding-left: 24px;">
                        <li style="margin-bottom: 4px;">① 수신거부를 회피·방해하는 조치</li>
                        <li style="margin-bottom: 4px;">② 전화번호를 자동으로 생성(생성기 등)하여 전송하는 조치</li>
                        <li style="margin-bottom: 4px;">③ 발신번호를 변작(조작)하여 전송하는 조치</li>
                    </ul>
                </div>
                <p style="margin-bottom: 24px; padding-left: 16px;">
                    회사는 <strong>발신번호 사전등록제</strong>를 통해 등록된 번호로만 발송을 허용하며, 변작이 의심될 경우 즉시 차단합니다.
                </p>
                
                <p style="margin-bottom: 12px;"><strong>10. 수신자에게 수신거부비용 부담 금지</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 16px;">
                    <li style="margin-bottom: 6px;">광고 전송 시 제공하는 수신거부 방법(080 ARS 등)은 수신자가 <strong>무료</strong>로 이용할 수 있어야 합니다.</li>
                    <li style="margin-bottom: 6px;">톡벨은 회원에게 080 무료 수신거부 서비스를 기본 기능으로 제공하여 이를 지원합니다.</li>
                </ul>
            </div>
        `,
        'refund': `
            <div style="line-height: 1.8; color: var(--text-primary);">
                <p style="margin-bottom: 24px;">
                    본 환불정책은 톡벨(TalkBell) 서비스 이용약관에 근거하여 포인트 충전, 마일리지, 환불에 관한 세부 사항을 안내합니다.
                </p>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--primary-color);">1. 포인트 충전 및 유효기간</h4>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left; width: 30%;">항목</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">내용</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">결제 방식</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">선불 충전(포인트) 방식</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">최소 충전 금액</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;"><strong>10,000원</strong> (100원 = 100포인트)</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">포인트 유효기간</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">최종 충전일로부터 <strong>5년</strong></td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">유효기간 만료 안내</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">소멸 30일 전부터 회원에게 통지</td>
                    </tr>
                </table>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--primary-color);">2. 마일리지 정책</h4>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">마일리지는 회사가 프로모션, 충전 보너스 등의 목적으로 <strong>무상으로 지급</strong>하는 적립금입니다.</li>
                    <li style="margin-bottom: 6px;">마일리지는 <strong>환불 대상이 아니며</strong>, 유상 포인트보다 우선 차감됩니다.</li>
                    <li style="margin-bottom: 6px;">마일리지의 유효기간은 지급일로부터 <strong>5년</strong>이며, 기간 만료 시 자동 소멸됩니다.</li>
                    <li style="margin-bottom: 6px;">프로모션별로 별도의 유효기간이 있을 수 있습니다.</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--primary-color);">3. 환불 기준</h4>
                <div style="background-color: var(--bg-color, #f8fafc); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <p style="margin-bottom: 12px;"><strong>환불 가능 조건</strong></p>
                    <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                        <tr style="background-color: #fff;">
                            <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left; width: 35%;">구분</th>
                            <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">조건</th>
                            <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left; width: 25%;">수수료</th>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #e2e8f0;"><strong>전액 환불</strong></td>
                            <td style="padding: 10px; border: 1px solid #e2e8f0;">충전 후 7일 이내 + 사용 내역 없음</td>
                            <td style="padding: 10px; border: 1px solid #e2e8f0; color: #22c55e;"><strong>수수료 없음</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #e2e8f0;"><strong>부분 환불</strong></td>
                            <td style="padding: 10px; border: 1px solid #e2e8f0;">충전 후 7일 경과 또는 사용 내역 있음</td>
                            <td style="padding: 10px; border: 1px solid #e2e8f0; color: #f59e0b;"><strong>잔여 포인트의 10%</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #e2e8f0;"><strong>선거 회원</strong></td>
                            <td style="padding: 10px; border: 1px solid #e2e8f0;">선거 기간 종료 후</td>
                            <td style="padding: 10px; border: 1px solid #e2e8f0; color: #22c55e;"><strong>수수료 없이 100% 환불</strong></td>
                        </tr>
                    </table>
                </div>
                
                <div style="background-color: #fee2e2; padding: 16px; border-radius: 8px; margin-bottom: 24px;">
                    <p style="margin-bottom: 8px;"><strong>⚠️ 환불 가능 최소 잔액</strong></p>
                    <p style="margin: 0; padding-left: 16px;"><strong>10,000원 이상</strong>부터 환불 가능합니다. (1만 원 미만은 환불 불가)</p>
                </div>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--primary-color);">4. 환불 제한 사항</h4>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">메시지 발송이 <strong>예약되어 있거나 진행 중</strong>인 경우 환불 신청이 제한됩니다.</li>
                    <li style="margin-bottom: 6px;"><strong>이미 사용된 포인트</strong>는 환불 대상이 아닙니다.</li>
                    <li style="margin-bottom: 6px;"><strong>마일리지</strong>(프로모션/이벤트로 지급된 무상 포인트)는 환불되지 않습니다.</li>
                    <li style="margin-bottom: 6px;">회원 탈퇴 시 환불 가능한 잔액(1만 원 이상)이 남아있으나 환불 신청을 하지 않은 경우 탈퇴가 제한됩니다.</li>
                </ul>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--primary-color);">5. 환불 절차</h4>
                <ol style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 8px;"><strong>환불 신청</strong>: 마이페이지 > 환불 신청 또는 고객센터(1588-5412)로 신청</li>
                    <li style="margin-bottom: 8px;"><strong>환불 검토</strong>: 신청일로부터 영업일 기준 3일 이내</li>
                    <li style="margin-bottom: 8px;"><strong>환불 처리</strong>: 환불 신청일로부터 <strong>영업일 기준 7일 이내</strong> 지급</li>
                </ol>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--primary-color);">6. 환불 방법</h4>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px;">
                    <tr style="background-color: var(--bg-color, #f8fafc);">
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">결제 방법</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">환불 방법</th>
                        <th style="padding: 10px; border: 1px solid #e2e8f0; text-align: left;">소요 기간</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">신용카드</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">결제 취소 처리</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">영업일 기준 3~5일</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">무통장입금</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">입금 계좌로 환불</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">영업일 기준 3~5일</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">계좌이체</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">입금 계좌로 환불</td>
                        <td style="padding: 10px; border: 1px solid #e2e8f0;">영업일 기준 1~3일</td>
                    </tr>
                </table>
                
                <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--primary-color);">7. 환불 문의</h4>
                <div style="background-color: #d1fae5; padding: 16px; border-radius: 8px;">
                    <p style="margin-bottom: 8px;"><strong>📞 고객센터</strong></p>
                    <ul style="padding-left: 20px; margin: 0;">
                        <li style="margin-bottom: 4px;">전화: <strong>1588-5412</strong></li>
                        <li style="margin-bottom: 4px;">이메일: <strong>support@tokbell.com</strong></li>
                        <li style="margin-bottom: 0;">운영시간: 평일 09:00 ~ 18:00</li>
                    </ul>
                </div>
            </div>
        `
    };
    
    document.getElementById('policyModalTitle').textContent = titleMap[type] || '정책';
    document.getElementById('policyModalBody').innerHTML = contentMap[type] || '<p>내용이 없습니다.</p>';
    
    openModal('policyModal');
}

// 모달 스타일 추가
(function() {
    if (!document.getElementById('footer-modal-styles')) {
        const style = document.createElement('style');
        style.id = 'footer-modal-styles';
        style.textContent = `
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.5);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            .modal-overlay.active {
                display: flex;
            }
            .modal {
                background-color: var(--surface-color, #ffffff);
                border-radius: 12px;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                width: 90%;
                max-height: 90vh;
                overflow-y: auto;
            }
            .modal-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 20px 24px;
                border-bottom: 1px solid var(--border-color, #e2e8f0);
                position: sticky;
                top: 0;
                background-color: var(--surface-color, #ffffff);
                z-index: 10;
            }
            .modal-title {
                font-size: 18px;
                font-weight: 600;
                color: var(--text-primary, #1e293b);
                margin: 0;
            }
            .modal-close {
                background: none;
                border: none;
                font-size: 28px;
                color: var(--text-secondary, #64748b);
                cursor: pointer;
                padding: 0;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 4px;
                transition: all 0.2s;
            }
            .modal-close:hover {
                background-color: var(--bg-color, #f8fafc);
                color: var(--text-primary, #1e293b);
            }
            .modal-body {
                padding: 24px;
                color: var(--text-primary, #1e293b);
            }
            .modal-footer {
                display: flex;
                justify-content: flex-end;
                gap: 12px;
                padding: 20px 24px;
                border-top: 1px solid var(--border-color, #e2e8f0);
                position: sticky;
                bottom: 0;
                background-color: var(--surface-color, #ffffff);
                z-index: 10;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                text-decoration: none;
            }
            .btn-outline {
                background-color: transparent;
                border: 1px solid var(--border-color, #e2e8f0);
                color: var(--text-primary, #1e293b);
            }
            .btn-outline:hover {
                background-color: var(--bg-color, #f8fafc);
            }
        `;
        document.head.appendChild(style);
    }
    
    // ESC 키로 모달 닫기 (모든 레이어 팝업 닫기)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' || e.keyCode === 27) {
            const activeModal = document.querySelector('.modal-overlay.active');
            if (activeModal) {
                const modalId = activeModal.id;
                if (modalId && typeof closeModal === 'function') {
                    closeModal(modalId);
                } else {
                    // closeModal 함수가 없는 경우 직접 닫기
                    activeModal.classList.remove('active');
                    activeModal.style.display = 'none';
                    document.body.style.overflow = '';
                }
            }
        }
    });
})();

