// 공통 푸터 생성 함수
function createFooter() {
    return `
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <h4 class="footer-title"><a href="support-center.html" class="footer-title-link">고객센터</a></h4>
                    <div class="footer-info">
                        <p class="footer-text">전화: 1588-5412</p>
                        <p class="footer-text">이메일: support@tokbell.com</p>
                        <p class="footer-text">운영시간: 평일 09:00 ~ 18:00</p>
                    </div>
                </div>
                <div class="footer-section">
                    <h4 class="footer-title">회사정보</h4>
                    <div class="footer-info">
                        <p class="footer-text">상호 : (주)아이뱅크</p>
                        <p class="footer-text">대표자: 정용관</p>
                        <p class="footer-text">사업자등록번호: 116-81-68774</p>
                        <p class="footer-text">통신판매업신고번호: 제2025-서울강서-0365호</p>
                        <p class="footer-text">주소: 서울 강서구 마곡동 779번지 보타닉게이트 10층</p>
                    </div>
                </div>
                <div class="footer-section">
                    <div class="footer-links">
                        <a href="javascript:void(0)" class="footer-link" onclick="event.preventDefault(); openPolicyModal('company')">회사소개</a>
                        <a href="javascript:void(0)" class="footer-link" onclick="event.preventDefault(); openPolicyModal('service')">서비스 소개</a>
                        <a href="javascript:void(0)" class="footer-link" onclick="event.preventDefault(); openPolicyModal('terms')">이용약관</a>
                        <a href="javascript:void(0)" class="footer-link" onclick="event.preventDefault(); openPolicyModal('privacy')">개인정보처리방침</a>
                        <a href="javascript:void(0)" class="footer-link" onclick="event.preventDefault(); openPolicyModal('spam')">스팸방지정책</a>
                        <a href="javascript:void(0)" class="footer-link" onclick="event.preventDefault(); openPolicyModal('refund')">환불정책</a>
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
                padding: 48px 24px 24px;
                margin-top: 64px;
            }
            .footer-content {
                max-width: 1400px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 32px;
                margin-bottom: 32px;
            }
            .footer-section {
                display: flex;
                flex-direction: column;
            }
            .footer-title {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 16px;
                color: var(--surface-color);
            }
            .footer-title-link {
                color: inherit;
                text-decoration: none;
            }
            .footer-title-link:hover {
                text-decoration: underline;
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
            .footer-links {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .footer-link {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.8);
                text-decoration: none;
                transition: color 0.2s;
            }
            .footer-link:hover {
                color: var(--surface-color);
                text-decoration: underline;
            }
            .footer-bottom {
                max-width: 1400px;
                margin: 0 auto;
                padding-top: 24px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
            }
            .footer-copyright {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.6);
                margin: 0;
            }
            @media (max-width: 768px) {
                .footer {
                    padding: 32px 16px 16px;
                }
                .footer-content {
                    grid-template-columns: 1fr;
                    gap: 24px;
                }
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
                        <td style="padding: 12px 0; font-weight: 600;">주소</td>
                        <td style="padding: 12px 0;">서울 강서구 마곡동 779번지 보타닉게이트 10층</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">대표전화</td>
                        <td style="padding: 12px 0;">1588-5412</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; font-weight: 600;">이메일</td>
                        <td style="padding: 12px 0;">support@tokbell.com</td>
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
                
                <p style="margin-bottom: 12px;"><strong>제1조 (목적)</strong></p>
                <p style="margin-bottom: 24px; padding-left: 16px;">
                    본 약관은 톡벨(이하 "회사")이 제공하는 인터넷 문자 발송 및 카카오톡 비즈메시지 서비스(이하 "서비스")의 이용과 관련하여 회사와 회원의 권리, 의무 및 책임사항, 기타 필요한 사항을 규정함을 목적으로 합니다.
                </p>
                
                <p style="margin-bottom: 12px;"><strong>제2조 (용어의 정의)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">본 약관에서 사용하는 용어의 정의는 다음과 같습니다.</p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;"><strong>회원</strong>: 회사와 서비스 이용계약을 체결하고 아이디(ID)를 부여받은 자로서, 개인 회원, 사업자 회원, 선거 회원을 포함합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>개인 회원</strong>: 만 19세 이상의 대한민국 거주민으로 본인 인증을 완료한 개인입니다.</li>
                    <li style="margin-bottom: 6px;"><strong>사업자 회원</strong>: 사업자등록증을 소유하고 기업 인증을 완료한 회원으로, '대표 계정'과 그 하위의 '담당자 계정'으로 구분됩니다.</li>
                    <li style="margin-bottom: 6px;"><strong>선거 회원</strong>: 공직선거법에 따라 선거 운동을 목적으로 가입하여 서비스를 이용하는 후보자 및 예비후보자 등을 말합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>포인트</strong>: 서비스를 이용하기 위해 회원이 유상으로 결제하여 충전한 선불 전자 지급 수단을 말합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>마일리지</strong>: 회사가 프로모션, 충전 보너스 등의 목적으로 회원에게 무상으로 지급하는 적립금을 말합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>발신번호</strong>: 메시지를 발송할 때 수신인에게 표시되는 보내는 사람의 전화번호를 말합니다.</li>
                    <li style="margin-bottom: 6px;"><strong>스팸 메시지</strong>: 정보통신망법 등 관련 법령을 위반하여 수신자의 동의 없이 전송되는 영리 목적의 광고성 정보를 말합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제3조 (약관의 게시와 개정)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">회사는 본 약관의 내용을 회원이 쉽게 알 수 있도록 서비스 초기 화면에 게시합니다.</li>
                    <li style="margin-bottom: 6px;">회사는 운영정책 변경 및 법령 개정에 따라 약관을 개정할 수 있으며, 개정 시 적용일자 7일 전(중대한 변경은 30일 전)부터 공지사항 등을 통해 회원에게 고지합니다.</li>
                </ul>
                
                <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제2장 이용계약 체결</h4>
                
                <p style="margin-bottom: 12px;"><strong>제4조 (이용계약의 성립)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">이용계약은 회원이 되고자 하는 자(이하 "가입신청자")가 약관의 내용에 동의하고, 회사가 정한 가입 양식에 따라 회원가입을 신청하면 회사가 이를 승낙함으로써 체결됩니다.</li>
                    <li style="margin-bottom: 6px;">가입신청자는 반드시 본인(개인) 또는 본인(법인)의 실명으로 신청하여야 하며, 실명 인증 절차를 거쳐야 합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제5조 (가입신청의 승낙과 제한)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">회사는 다음 각 호에 해당하는 신청에 대하여는 승낙을 하지 않거나 사후에 이용계약을 해지할 수 있습니다.</p>
                <ul style="padding-left: 32px; margin-bottom: 16px;">
                    <li style="margin-bottom: 6px;">실명이 아니거나 타인의 명의를 이용한 경우</li>
                    <li style="margin-bottom: 6px;">가입 신청 시 허위 정보를 기재하거나, 회사가 제시하는 증빙 서류를 제출하지 않은 경우</li>
                    <li style="margin-bottom: 6px;">부정한 용도(스팸 발송, 보이스피싱, 범죄 악용 등)로 서비스를 이용하고자 하는 경우</li>
                    <li style="margin-bottom: 6px;">만 19세 미만인 경우</li>
                    <li style="margin-bottom: 6px;">외국인 또는 법인 명의의 휴대폰을 사용하는 개인 회원인 경우</li>
                </ul>
                <p style="margin-bottom: 24px; padding-left: 16px;">사업자 회원의 경우, 대표 계정 승인 후 하위 담당자 계정을 생성할 수 있으며, 모든 담당자 계정의 이용 행위에 대한 책임은 대표 계정에게 귀속됩니다.</p>
                
                <p style="margin-bottom: 12px;"><strong>제6조 (선거 회원의 특칙)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">선거 회원은 공직선거법에 따른 예비후보자 및 후보자 등록을 마친 자에 한해 가입(전환)이 가능합니다.</li>
                    <li style="margin-bottom: 6px;">선거 회원은 선거관리위원회에 신고된 발신번호 1개만 등록하여 사용할 수 있습니다.</li>
                    <li style="margin-bottom: 6px;">선거 회원은 선거 기간 종료 후 개인 회원으로 자동 전환되며, 선거 관련 데이터는 관련 법령 및 운영정책에 따라 처리됩니다.</li>
                </ul>
                
                <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제3장 서비스의 이용</h4>
                
                <p style="margin-bottom: 12px;"><strong>제7조 (발신번호의 등록 및 관리)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">회원은 전기통신사업법에 따라 본인(또는 소속 법인) 명의의 발신번호를 사전에 등록하여야 하며, 등록되지 않은 번호로는 메시지를 발송할 수 없습니다.</li>
                    <li style="margin-bottom: 6px;">발신번호 등록 시 최근 3개월 이내 발급된 증빙 서류(통신서비스이용증명원 등)를 제출하여야 합니다.</li>
                    <li style="margin-bottom: 6px;">타인의 명의를 도용한 발신번호 등록이 확인될 경우, 회사는 즉시 해당 번호의 등록을 취소하고 서비스 이용을 정지할 수 있습니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제8조 (메시지의 발송 및 제한)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">회원은 정보통신망법 및 공직선거법 등 관련 법령을 준수하여 메시지를 발송해야 합니다.</p>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>광고성 메시지 발송 시 의무 사항:</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 16px;">
                    <li style="margin-bottom: 6px;">메시지 시작 부분에 (광고) 문구 표기</li>
                    <li style="margin-bottom: 6px;">메시지 하단에 무료수신거부 번호(080) 표기</li>
                    <li style="margin-bottom: 6px;">야간(오후 9시 ~ 익일 오전 8시) 발송 제한 (단, 별도 동의를 받은 경우 제외)</li>
                </ul>
                <p style="margin-bottom: 8px; padding-left: 16px;"><strong>발송 한도:</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">개인 회원: 1일 500건 (전기통신사업법에 따름)</li>
                    <li style="margin-bottom: 6px;">사업자 회원: 1회 최대 1,000,000건</li>
                    <li style="margin-bottom: 6px;">선거 회원: 발송량 제한 없음 (단, 자동 동보통신은 총 8회로 제한)</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제9조 (카카오톡 비즈메시지)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">알림톡 및 브랜드 메시지 발송을 위해서는 카카오톡 채널(비즈니스 인증) 및 발신 프로필 등록이 선행되어야 합니다.</li>
                    <li style="margin-bottom: 6px;">알림톡 템플릿은 카카오의 사전 승인을 받아야 하며, 승인된 내용과 다르게 변조하여 발송할 수 없습니다.</li>
                    <li style="margin-bottom: 6px;">알림톡은 정보성 메시지에 한하며, 광고성 내용이 포함될 경우 발송이 반려되거나 브랜드 메시지로 발송해야 합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제10조 (스팸 메시지 및 수신거부 관리)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">회사는 방송통신위원회 및 한국인터넷진흥원(KISA)의 스팸방지 가이드라인을 준수합니다.</li>
                    <li style="margin-bottom: 6px;">회원이 스팸 메시지(불법 도박, 성인물, 대출 광고 등)를 발송한 사실이 확인되거나 신고가 접수될 경우, 회사는 즉시 이용 정지 및 계약 해지 조치를 취할 수 있습니다.</li>
                    <li style="margin-bottom: 6px;">회원은 수신자가 수신거부(080 등)를 요청한 경우 해당 번호로 메시지를 발송해서는 안 되며, 이를 위반하여 발생하는 모든 책임은 회원에게 있습니다.</li>
                </ul>
                
                <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제4장 요금 및 포인트 정책</h4>
                
                <p style="margin-bottom: 12px;"><strong>제11조 (포인트 충전 및 유효기간)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">서비스 이용 요금은 선불 충전(포인트) 방식을 원칙으로 합니다.</li>
                    <li style="margin-bottom: 6px;">포인트의 최소 충전 금액은 10,000원이며, 100원당 100포인트로 적립됩니다.</li>
                    <li style="margin-bottom: 6px;">유상으로 충전한 포인트의 유효기간은 최종 충전일로부터 5년이며, 기간 경과 시 소멸됩니다.</li>
                    <li style="margin-bottom: 6px;">회사는 소멸 30일 전부터 회원에게 통지합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제12조 (마일리지)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">마일리지는 회사가 무상으로 지급하는 포인트로, 환불 대상이 아니며 유상 포인트보다 우선 차감됩니다.</li>
                    <li style="margin-bottom: 6px;">마일리지의 유효기간은 지급일로부터 5년이며(단, 프로모션별 별도 유효기간이 있을 수 있음), 기간 만료 시 자동 소멸됩니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제13조 (환불 및 정산)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">회원은 충전된 잔액에 대해 환불을 요청할 수 있으며, 환불 기준은 다음과 같습니다.</p>
                <ul style="padding-left: 32px; margin-bottom: 16px;">
                    <li style="margin-bottom: 6px;">환불 가능 최소 잔액: 10,000원 이상 (1만 원 미만은 환불 불가)</li>
                    <li style="margin-bottom: 6px;">전액 환불: 충전 후 7일 이내 사용 내역이 없는 경우</li>
                    <li style="margin-bottom: 6px;">부분 환불: 충전 후 7일이 경과하였거나 사용 내역이 있는 경우, 잔여 포인트의 10%를 위약금(환불 수수료)으로 공제한 후 잔액을 환급</li>
                </ul>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">메시지 발송이 예약되어 있거나 진행 중인 경우 환불 신청이 제한될 수 있습니다.</li>
                    <li style="margin-bottom: 6px;">선거 회원의 경우, 선거 기간 종료 후 남은 잔액에 대해 수수료 없이 100% 환불합니다.</li>
                    <li style="margin-bottom: 6px;">환불 금액은 환불 신청일로부터 영업일 기준 7일 이내에 지급합니다.</li>
                </ul>
                
                <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제5장 계약 해지 및 이용 제한</h4>
                
                <p style="margin-bottom: 12px;"><strong>제14조 (회원 탈퇴 및 자격 상실)</strong></p>
                <p style="margin-bottom: 8px; padding-left: 16px;">회원은 언제든지 탈퇴를 요청할 수 있습니다. 단, 다음의 경우 탈퇴가 제한될 수 있습니다.</p>
                <ul style="padding-left: 32px; margin-bottom: 16px;">
                    <li style="margin-bottom: 6px;">발송 중이거나 예약된 메시지가 있는 경우</li>
                    <li style="margin-bottom: 6px;">환불 가능한 잔액(1만 원 이상)이 남아있으나 환불 신청을 하지 않은 경우</li>
                </ul>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">회원이 잔액에 대한 권리를 포기하고 즉시 탈퇴를 원하는 경우, 잔액 소멸 동의 후 탈퇴가 가능합니다.</li>
                    <li style="margin-bottom: 6px;">사업자 회원의 대표 계정이 탈퇴할 경우, 소속된 모든 담당자 계정은 자동 탈퇴 처리됩니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제15조 (휴면 계정)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">최종 로그인 일로부터 1년 이상 서비스를 이용하지 않은 회원은 휴면 회원으로 전환됩니다.</li>
                    <li style="margin-bottom: 6px;">휴면 회원의 개인정보는 별도로 분리 보관되며, 휴면 전환 시점으로부터 5년 경과 시 파기될 수 있습니다.</li>
                    <li style="margin-bottom: 6px;">회사는 휴면 전환 30일 전 회원에게 안내합니다.</li>
                </ul>
                
                <h4 style="margin-top: 28px; margin-bottom: 12px; color: var(--primary-color);">제6장 기타</h4>
                
                <p style="margin-bottom: 12px;"><strong>제16조 (개인정보보호 및 보안)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">회사는 회원의 개인정보를 보호하기 위해 노력하며, 개인정보처리방침을 수립하고 준수합니다.</li>
                    <li style="margin-bottom: 6px;">회사는 Google Analytics 등 분석 도구 사용 시 개인식별정보를 암호화하거나 비식별화하여 처리합니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제17조 (손해배상 및 면책)</strong></p>
                <ul style="padding-left: 32px; margin-bottom: 24px;">
                    <li style="margin-bottom: 6px;">회사는 천재지변, 기간통신사업자의 회선 장애 등 불가항력으로 인해 서비스를 제공할 수 없는 경우 이에 대한 책임을 지지 않습니다.</li>
                    <li style="margin-bottom: 6px;">메시지 전송의 실패, 지연, 내용 변질 등이 회원의 귀책사유(오입력, 수신거부 등)로 인한 경우 회사는 책임을 지지 않습니다.</li>
                </ul>
                
                <p style="margin-bottom: 12px;"><strong>제18조 (분쟁의 해결)</strong></p>
                <p style="margin-bottom: 24px; padding-left: 16px;">
                    본 약관과 관련하여 회사와 회원 간에 분쟁이 발생할 경우, 회사의 본사 소재지를 관할하는 법원을 전속 관할 법원으로 합니다.
                </p>
                
                <p style="margin-top: 24px; padding: 16px; background-color: var(--bg-color, #f8fafc); border-radius: 8px;">
                    <strong>부칙</strong><br>
                    본 약관은 202X년 X월 X일부터 시행합니다.
                </p>
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

