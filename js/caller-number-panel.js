        let currentStep = 1;
        let selectedMemberType = ''; // 'personal' or 'business'
        let selectedOwnershipType = '';
        let numberType = null; // 'MOBILE' or 'LANDLINE'
        let requiresAuth = false;
        let authCompleted = false;
        let authInfo = null;

        // 현재 회원 유형 확인 함수 (실제로는 API 호출)
        function getCurrentMemberType() {
            // 실제로는 API 호출 또는 localStorage에서 가져옴
            // 예시: localStorage.getItem('memberType') 또는 API 호출
            // 개인사업자, 법인사업자, 선거회원으로 전환한 경우 'business' 반환
            // 그 외의 경우 'personal' 반환
            
            // 시뮬레이션: localStorage에서 회원 유형 확인
            const memberType = localStorage.getItem('memberType');
            if (memberType === 'business' || memberType === 'corporate' || memberType === 'election') {
                return 'business';
            }
            return 'personal'; // 기본값: 개인회원
        }

        // 테스트용 회원 유형 설정 함수
        function setTestMemberType(type) {
            localStorage.setItem('memberType', type);
            updateMemberTypeDisplay();
            showToast(`회원 유형이 ${type === 'personal' ? '개인회원' : '기업회원'}으로 설정되었습니다.`, 'success');
        }

        // 현재 회원 유형 표시 업데이트
        function updateMemberTypeDisplay() {
            const memberType = getCurrentMemberType();
            const typeText = memberType === 'personal' ? '개인회원' : '기업회원';
            const display = document.getElementById('currentMemberTypeDisplay');
            const dashboardEl = document.getElementById('dashboardMemberType');
            const callerPanelDisplay = document.getElementById('callerPanelMemberTypeDisplay');
            if (display) display.textContent = typeText;
            if (dashboardEl) dashboardEl.textContent = typeText;
            if (callerPanelDisplay) callerPanelDisplay.textContent = typeText;
        }

        function filterStatus(status) {
            // 모든 필터 버튼에서 active 클래스 제거
            document.querySelectorAll('.status-filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // 클릭한 버튼에 active 클래스 추가
            event.currentTarget.classList.add('active');
            
            // 테이블 행 필터링
            const tbody = document.getElementById('callerNumberTableBody');
            if (!tbody) return;
            
            const rows = tbody.querySelectorAll('tr[data-status]');
            
            rows.forEach(row => {
                const rowStatus = row.getAttribute('data-status');
                
                if (status === 'all') {
                    // 전체: 모든 행 표시
                    row.style.display = '';
                } else {
                    // 선택한 상태와 일치하는 행만 표시
                    if (rowStatus === status) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        }

        // selectMemberType 함수 제거 (더 이상 필요 없음)

        // 발신번호 유형 자동 인식
        function detectNumberType() {
            const input = document.getElementById('callerNumberInput');
            const number = input.value.replace(/[^0-9]/g, '');
            const badgeDiv = document.getElementById('numberTypeBadge');
            const badgeText = document.getElementById('numberTypeText');
            const authText = document.getElementById('authRequirementText');
            
            if (number.startsWith('010')) {
                numberType = 'MOBILE';
                requiresAuth = true;
                if (badgeDiv) badgeDiv.style.display = 'block';
                if (badgeText) { badgeText.className = 'number-type-badge number-type-mobile'; badgeText.textContent = '휴대폰 번호'; }
                if (authText) authText.textContent = '본인인증이 필요합니다';
            } else if (/^(02|0[3-6][1-5])/.test(number)) {
                numberType = 'LANDLINE';
                requiresAuth = false;
                if (badgeDiv) badgeDiv.style.display = 'block';
                if (badgeText) { badgeText.className = 'number-type-badge number-type-landline'; badgeText.textContent = '유선번호'; }
                if (authText) authText.textContent = '본인인증이 필요하지 않습니다';
            } else if (number.length > 0) {
                numberType = null;
                if (badgeDiv) badgeDiv.style.display = 'none';
            } else {
                numberType = null;
                if (badgeDiv) badgeDiv.style.display = 'none';
            }
            
            // 개인 회원 - 본인 명의 또는 기업 회원 - 본인(자사) 명의인 경우 서류 섹션 업데이트
            if (selectedOwnershipType === 'self') {
                updateDocumentSection();
            }
            
            // 본인인증 섹션 업데이트
            const authSection = document.getElementById('authSection');
            if (authSection) {
                // 본인(자사) 명의이고 휴대폰 번호일 때만 본인인증 필요
                if (requiresAuth && numberType === 'MOBILE' && selectedOwnershipType === 'self') {
                    authSection.style.display = 'block';
                    const authHelpText = document.getElementById('authHelpText');
                    if (authHelpText) {
                        authHelpText.textContent = selectedMemberType === 'personal' 
                            ? '발신번호 명의자 본인인증이 필요합니다' 
                            : '서류 제출자 본인인증이 필요합니다';
                    }
                    
                    // 본인인증 버튼 표시 및 상태 초기화
                    if (!authCompleted) {
                        authCompleted = false;
                        const authStatus = document.getElementById('authStatus');
                        if (authStatus) {
                            authStatus.innerHTML = '<button type="button" class="btn btn-primary" id="authButton" onclick="openPhoneAuth()">휴대폰 본인인증</button>';
                        }
                    }
                } else {
                    authSection.style.display = 'none';
                    authCompleted = false;
                }
            }
        }

        function checkDuplicateNumber() {
            const number = document.getElementById('callerNumberInput').value;
            if (!number) {
                showToast('발신번호를 입력해주세요.', 'warning');
                return;
            }
            // 중복 확인 로직
            showToast('사용 가능한 발신번호입니다.', 'success');
        }

        // STEP 3에서 명의 구분 선택 및 서류 섹션 업데이트
        function updateOwnershipSection() {
            const ownershipSection = document.getElementById('ownershipTypeSection');
            const authSection = document.getElementById('authSection');
            const docSection = document.getElementById('documentSection');
            
            if (selectedMemberType === 'personal') {
                // 개인 회원 명의 구분
                ownershipSection.innerHTML = `
                    <div class="flex gap-2" style="flex-direction: column;">
                        <label style="display: flex; align-items: center; gap: 8px; padding: 12px; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">
                            <input type="radio" name="ownershipType" value="self" onchange="selectOwnershipType('self')">
                            <div>
                                <strong>본인 명의</strong>
                                <p style="font-size: 12px; color: var(--text-secondary); margin: 4px 0 0 0;">본인 명의 발신번호를 등록합니다</p>
                            </div>
                        </label>
                        <label style="display: flex; align-items: center; gap: 8px; padding: 12px; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">
                            <input type="radio" name="ownershipType" value="others" onchange="selectOwnershipType('others')">
                            <div>
                                <strong>타인 명의</strong>
                                <p style="font-size: 12px; color: var(--text-secondary); margin: 4px 0 0 0;">타인 명의 발신번호를 등록합니다. 위임장 및 추가 서류가 필요합니다</p>
                            </div>
                        </label>
                    </div>
                `;
            } else {
                // 기업 회원 명의 구분
                ownershipSection.innerHTML = `
                    <div class="flex gap-2" style="flex-direction: column;">
                        <label style="display: flex; align-items: center; gap: 8px; padding: 12px; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">
                            <input type="radio" name="ownershipType" value="self" onchange="selectOwnershipType('self')">
                            <div>
                                <strong>본인(자사) 명의</strong>
                                <p style="font-size: 12px; color: var(--text-secondary); margin: 4px 0 0 0;">본인(자사) 명의 발신번호를 등록합니다</p>
                            </div>
                        </label>
                        <label style="display: flex; align-items: center; gap: 8px; padding: 12px; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">
                            <input type="radio" name="ownershipType" value="others" onchange="selectOwnershipType('others')">
                            <div>
                                <strong>타인 명의</strong>
                                <p style="font-size: 12px; color: var(--text-secondary); margin: 4px 0 0 0;">타인 명의 발신번호를 등록합니다. 위임장 및 추가 서류가 필요합니다</p>
                            </div>
                        </label>
                        <label style="display: flex; align-items: center; gap: 8px; padding: 12px; border: 1px solid var(--border-color); border-radius: var(--radius-md); cursor: pointer;">
                            <input type="radio" name="ownershipType" value="other_company" onchange="selectOwnershipType('other_company')">
                            <div>
                                <strong>타사 명의</strong>
                                <p style="font-size: 12px; color: var(--text-secondary); margin: 4px 0 0 0;">타사(다른 기업) 명의 발신번호를 등록합니다. 위임장, 위임하는 업체의 사업자등록증 및 수임하는 업체의 사업자등록증이 필요합니다</p>
                            </div>
                        </label>
                    </div>
                `;
            }
            
            // 본인인증 섹션 표시/숨김
            // 본인(자사) 명의이고 휴대폰 번호일 때만 본인인증 필요
            if (requiresAuth && numberType === 'MOBILE' && selectedOwnershipType === 'self') {
                authSection.style.display = 'block';
                document.getElementById('authHelpText').textContent = selectedMemberType === 'personal' 
                    ? '발신번호 명의자 본인인증이 필요합니다' 
                    : '서류 제출자 본인인증이 필요합니다';
                
                // 본인인증 버튼 표시 및 상태 초기화
                authCompleted = false;
                const authStatus = document.getElementById('authStatus');
                if (authStatus) {
                    authStatus.innerHTML = '<button type="button" class="btn btn-primary" id="authButton" onclick="openPhoneAuth()">휴대폰 본인인증</button>';
                }
            } else {
                authSection.style.display = 'none';
                // 본인인증 상태 초기화
                authCompleted = false;
            }
        }

        function selectOwnershipType(type) {
            selectedOwnershipType = type;
            updateDocumentSection();
            
            // 본인인증 섹션 업데이트
            const authSection = document.getElementById('authSection');
            if (authSection) {
                // 본인(자사) 명의이고 휴대폰 번호일 때만 본인인증 필요
                if (requiresAuth && numberType === 'MOBILE' && selectedOwnershipType === 'self') {
                    authSection.style.display = 'block';
                    document.getElementById('authHelpText').textContent = selectedMemberType === 'personal' 
                        ? '발신번호 명의자 본인인증이 필요합니다' 
                        : '서류 제출자 본인인증이 필요합니다';
                    
                    // 본인인증 버튼 표시 및 상태 초기화
                    authCompleted = false;
                    const authStatus = document.getElementById('authStatus');
                    if (authStatus) {
                        authStatus.innerHTML = '<button type="button" class="btn btn-primary" id="authButton" onclick="openPhoneAuth()">휴대폰 본인인증</button>';
                    }
                } else {
                    authSection.style.display = 'none';
                    // 본인인증 상태 초기화
                    authCompleted = false;
                    const authStatus = document.getElementById('authStatus');
                    if (authStatus) {
                        authStatus.innerHTML = '<span style="color: var(--text-secondary);">본인인증이 필요하지 않습니다</span>';
                    }
                    const authButton = document.getElementById('authButton');
                    if (authButton) {
                        authButton.style.display = 'none';
                    }
                }
            }
            // 휴대폰+본인 명의 선택 순간 스텝 바에서 3·4단계 숨김
            updateStepIndicatorVisibility();
            // 2단계 푸터: 휴대폰+본인 명의+인증완료 시 등록 버튼 표시
            updateStep2FooterButton();
        }

        // 2단계에서 휴대폰+본인 명의+인증 완료면 '등록' 버튼, 아니면 '다음' 버튼
        function updateStep2FooterButton() {
            const nextBtn = document.getElementById('nextBtn');
            const submitBtn = document.getElementById('submitBtn');
            if (!nextBtn || !submitBtn) return;
            if (currentStep === 2 && numberType === 'MOBILE' && selectedOwnershipType === 'self' && authCompleted) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = 'block';
                submitBtn.textContent = '등록';
            } else if (currentStep === 2) {
                nextBtn.style.display = 'block';
                submitBtn.style.display = 'none';
                submitBtn.textContent = '승인요청';
            }
        }

        // 휴대폰+본인 명의일 때 스텝 인디케이터에서 3·4단계 숨김
        function updateStepIndicatorVisibility() {
            const step3El = document.getElementById('step3');
            const step4El = document.getElementById('step4');
            if (!step3El || !step4El) return;
            if (numberType === 'MOBILE' && selectedOwnershipType === 'self') {
                step3El.style.display = 'none';
                step4El.style.display = 'none';
            } else {
                step3El.style.display = '';
                step4El.style.display = '';
            }
        }

        // 명의 구분별 서류 섹션 업데이트
        function updateDocumentSection() {
            const docSection = document.getElementById('documentSection');
            const fileAccept = '.jpg,.jpeg,.gif,.png,.pdf,.tif,.tiff,.zip';
            const maxSize = 10 * 1024 * 1024; // 10MB
            
            if (!selectedOwnershipType) {
                docSection.innerHTML = '<p style="color: var(--text-secondary);">명의 구분을 선택해주세요.</p>';
                return;
            }

            let html = '';
            
            if (selectedMemberType === 'personal') {
                if (selectedOwnershipType === 'self') {
                    // 개인 - 본인 명의
                    // 휴대폰 번호인 경우 본인인증만 필요 (통신서비스이용증명원 불필요)
                    // 유선번호인 경우 통신서비스이용증명원 필요
                    if (numberType === 'MOBILE') {
                        // 휴대폰 번호: 서류 불필요
                        html = `
                            <div style="margin-top: 20px;">
                                <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">휴대폰 번호는 본인인증만으로 등록 가능합니다.</p>
                            </div>
                        `;
                    } else if (numberType === 'LANDLINE') {
                        // 유선번호: 통신서비스이용증명원 필요
                        html = `
                            <div style="margin-top: 20px;">
                                <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">발신번호 소유 확인을 위한 서류 제출이 필요합니다</p>
                                <label class="form-label required">통신서비스 이용증명원 또는 통신사 가입증명서</label>
                                <div class="file-upload-area" onclick="document.getElementById('certFile').click()">
                                    <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                    <input type="file" id="certFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'certFile', ${maxSize})">
                                </div>
                                <div class="form-help">
                                    통신사(SKT, KT, LG U+ 등)에서 발급한 최근 3개월 이내 서류를 제출해 주세요<br>
                                    통신사 홈페이지, 고객센터, 대리점에서 발급 가능합니다<br>
                                    발신번호와 명의자 정보가 명확히 표시된 서류를 제출해 주세요<br>
                                    * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB<br>
                                    * 서류가 여러 장일 경우 zip 파일로 압축하여 첨부하세요
                                </div>
                                <div id="certFileDisplay"></div>
                            </div>
                        `;
                    } else {
                        // 번호 타입 미선택
                        html = `
                            <div style="margin-top: 20px;">
                                <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">발신번호를 입력해주세요.</p>
                            </div>
                        `;
                    }
                } else {
                    // 개인 - 타인 명의
                    html = `
                        <div style="margin-top: 20px;">
                            <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">타인 명의 발신번호 등록을 위한 서류 제출이 필요합니다</p>
                            <label class="form-label required">통신서비스 이용증명원 또는 통신사 가입증명서</label>
                            <div class="file-upload-area" onclick="document.getElementById('certFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="certFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'certFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                통신사(SKT, KT, LG U+ 등)에서 발급한 최근 3개월 이내 서류를 제출해 주세요<br>
                                통신사 홈페이지, 고객센터, 대리점에서 발급 가능합니다<br>
                                발신번호와 명의자 정보가 명확히 표시된 서류를 제출해 주세요<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="certFileDisplay"></div>
                            
                            <label class="form-label required" style="margin-top: 20px;">위임장</label>
                            <div class="file-upload-area" onclick="document.getElementById('powerOfAttorneyFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="powerOfAttorneyFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'powerOfAttorneyFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                발신번호 명의자의 위임장이 필요합니다<br>
                                위임자와 수임자 정보가 명확히 기재되어야 합니다<br>
                                위임자의 서명 또는 날인이 필요합니다<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="powerOfAttorneyFileDisplay"></div>
                            
                            <label class="form-label required" style="margin-top: 20px;">재직증명서 또는 신분증</label>
                            <div class="file-upload-area" onclick="document.getElementById('employeeCertOrIdFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="employeeCertOrIdFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'employeeCertOrIdFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                재직증명서: 최근 3개월 이내 발급된 서류<br>
                                신분증: 주민등록증, 운전면허증, 여권 등<br>
                                수임자(제출자)의 신원 확인을 위한 서류입니다<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="employeeCertOrIdFileDisplay"></div>
                        </div>
                    `;
                }
            } else {
                // 기업 회원
                if (selectedOwnershipType === 'self') {
                    // 기업 - 본인(자사) 명의
                    // 휴대폰 번호인 경우 본인인증 완료 여부와 관계없이 통신서비스이용증명원 불필요
                    // 유선번호인 경우 통신서비스이용증명원 필요
                    if (numberType === 'MOBILE') {
                        // 휴대폰 번호: 서류 불필요
                        html = `
                            <div style="margin-top: 20px;">
                                <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">휴대폰 번호는 추가 서류 제출이 필요하지 않습니다.</p>
                            </div>
                        `;
                    } else if (numberType === 'LANDLINE') {
                        // 유선번호: 통신서비스이용증명원 필요
                        html = `
                            <div style="margin-top: 20px;">
                                <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">발신번호와 발신번호 소유자(기업)간의 관계를 입증할 수 있는 서류 제출이 필요합니다</p>
                                <label class="form-label required">통신서비스 이용증명원 또는 통신사 가입증명서</label>
                                <div class="file-upload-area" onclick="document.getElementById('certFile2').click()">
                                    <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                    <input type="file" id="certFile2" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'certFile2', ${maxSize})">
                                </div>
                                <div class="form-help">
                                    통신사(SKT, KT, LG U+ 등)에서 발급한 최근 3개월 이내 서류를 제출해 주세요<br>
                                    법인 명의 발신번호의 경우 법인 가입증명서를 제출해 주세요<br>
                                    * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                                </div>
                                <div id="certFile2Display"></div>
                            </div>
                        `;
                    } else {
                        // 번호 타입 미선택
                        html = `
                            <div style="margin-top: 20px;">
                                <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">발신번호를 입력해주세요.</p>
                            </div>
                        `;
                    }
                } else if (selectedOwnershipType === 'others') {
                    // 기업 - 타인 명의
                    html = `
                        <div style="margin-top: 20px;">
                            <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">타인 명의 발신번호 등록을 위한 서류 제출이 필요합니다</p>
                            <label class="form-label required">통신서비스 이용증명원 또는 통신사 가입증명서</label>
                            <div class="file-upload-area" onclick="document.getElementById('certFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="certFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'certFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                통신사(SKT, KT, LG U+ 등)에서 발급한 최근 3개월 이내 서류를 제출해 주세요<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="certFileDisplay"></div>
                            
                            <label class="form-label required" style="margin-top: 20px;">위임장</label>
                            <div class="file-upload-area" onclick="document.getElementById('powerOfAttorneyFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="powerOfAttorneyFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'powerOfAttorneyFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                발신번호 명의자의 위임장이 필요합니다<br>
                                위임자와 수임자(제출자) 정보가 명확히 기재되어야 합니다<br>
                                위임자의 서명 또는 날인이 필요합니다<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="powerOfAttorneyFileDisplay"></div>
                            
                            <label class="form-label required" style="margin-top: 20px;">재직증명서 또는 신분증</label>
                            <div class="file-upload-area" onclick="document.getElementById('employeeCertOrIdFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="employeeCertOrIdFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'employeeCertOrIdFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                재직증명서: 최근 3개월 이내 발급된 서류<br>
                                신분증: 주민등록증, 운전면허증, 여권 등<br>
                                수임자(제출자)의 신원 확인을 위한 서류입니다<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="employeeCertOrIdFileDisplay"></div>
                        </div>
                    `;
                } else {
                    // 기업 - 타사 명의
                    html = `
                        <div style="margin-top: 20px;">
                            <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">타사 명의 발신번호 등록을 위한 서류 제출이 필요합니다</p>
                            <label class="form-label required">통신서비스 이용증명원 또는 통신사 가입증명서</label>
                            <div class="file-upload-area" onclick="document.getElementById('certFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="certFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'certFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                통신사(SKT, KT, LG U+ 등)에서 발급한 최근 3개월 이내 서류를 제출해 주세요<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="certFileDisplay"></div>
                            
                            <label class="form-label required" style="margin-top: 20px;">위임장</label>
                            <div class="file-upload-area" onclick="document.getElementById('powerOfAttorneyFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="powerOfAttorneyFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'powerOfAttorneyFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                발신번호를 위임하는 기업(타사)의 위임장이 필요합니다<br>
                                위임 기업과 수임 기업 정보가 명확히 기재되어야 합니다<br>
                                위임 기업의 법인 직인이 날인되어야 합니다<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="powerOfAttorneyFileDisplay"></div>
                            
                            <label class="form-label required" style="margin-top: 20px;">위임하는 업체의 사업자등록증</label>
                            <div class="file-upload-area" onclick="document.getElementById('delegatorBusinessFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="delegatorBusinessFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'delegatorBusinessFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                발신번호를 위임하는 기업(타사)의 사업자등록증을 제출해 주세요<br>
                                국세청 홈택스에서 발급 가능합니다<br>
                                법인명과 사업자등록번호가 명확히 표시되어야 합니다<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="delegatorBusinessFileDisplay"></div>
                            
                            <label class="form-label required" style="margin-top: 20px;">수임하는 업체의 사업자등록증</label>
                            <div class="file-upload-area" onclick="document.getElementById('delegateeBusinessFile').click()">
                                <p>파일을 선택하거나 드래그하여 놓으세요</p>
                                <input type="file" id="delegateeBusinessFile" style="display: none;" accept="${fileAccept}" onchange="handleFileUpload(this, 'delegateeBusinessFile', ${maxSize})">
                            </div>
                            <div class="form-help">
                                발신번호를 수임하는 기업(자사)의 사업자등록증을 제출해 주세요<br>
                                국세청 홈택스에서 발급 가능합니다<br>
                                법인명과 사업자등록번호가 명확히 표시되어야 합니다<br>
                                * jpg, jpeg, gif, png, pdf, tif, tiff, zip 첨부 가능 / 최대 10MB
                            </div>
                            <div id="delegateeBusinessFileDisplay"></div>
                        </div>
                    `;
                }
            }
            
            docSection.innerHTML = html;
        }

        function nextStep() {
            // 현재 단계 검증
            if (currentStep === 1) {
                const callerNumber = document.getElementById('callerNumberInput').value;
                if (!callerNumber) {
                    showToast('발신번호를 입력해주세요.', 'warning');
                    return;
                }
                if (!numberType) {
                    showToast('유효한 발신번호를 입력해주세요.', 'warning');
                    return;
                }
            }
            if (currentStep === 2) {
                if (!selectedOwnershipType) {
                    showToast('명의 구분을 선택해주세요.', 'warning');
                    return;
                }
                if (requiresAuth && !authCompleted) {
                    showToast('본인인증을 완료해주세요.', 'warning');
                    return;
                }
                // 휴대폰+본인 명의+인증 완료: 3·4단계 생략, 등록 버튼만 표시하고 여기서 종료
                if (numberType === 'MOBILE' && selectedOwnershipType === 'self' && authCompleted) {
                    updateStep2FooterButton();
                    return;
                }
            }
            if (currentStep === 3) {
                const contactPhone = document.getElementById('contactPhoneInput').value;
                if (!contactPhone) {
                    showToast('연락처를 입력해주세요.', 'warning');
                    return;
                }
            }
            
            if (currentStep < 4) {
                document.getElementById(`step${currentStep}Content`).style.display = 'none';
                document.getElementById(`step${currentStep}`).classList.remove('active');
                document.getElementById(`step${currentStep}`).classList.add('completed');
                
                currentStep++;
                document.getElementById(`step${currentStep}Content`).style.display = 'block';
                document.getElementById(`step${currentStep}`).classList.add('active');
                
                // STEP 2 진입 시 명의 구분 섹션 업데이트
                if (currentStep === 2) {
                    updateOwnershipSection();
                    updateStepIndicatorVisibility();
                }
                
                if (currentStep === 4) {
                    document.getElementById('nextBtn').style.display = 'none';
                    document.getElementById('submitBtn').style.display = 'block';
                    document.getElementById('submitBtn').textContent = '승인요청';
                    // 최종 확인 정보 업데이트
                    updateReviewInfo();
                } else {
                    document.getElementById('nextBtn').style.display = 'block';
                    document.getElementById('submitBtn').style.display = 'none';
                    document.getElementById('submitBtn').textContent = '승인요청';
                    // 휴대폰 번호 + 본인 명의: 2단계에서 인증 완료 시 등록 버튼 표시 (3·4단계 생략)
                    updateStep2FooterButton();
                }
            }
        }

        function updateReviewInfo() {
            document.getElementById('reviewMemberType').textContent = selectedMemberType === 'personal' ? '개인' : '기업';
            document.getElementById('reviewCallerNumber').textContent = document.getElementById('callerNumberInput').value || '-';
            document.getElementById('reviewNumberType').textContent = numberType === 'MOBILE' ? '휴대폰 번호' : '유선번호';
            
            let ownershipText = '';
            if (selectedMemberType === 'personal') {
                ownershipText = selectedOwnershipType === 'self' ? '본인 명의' : '타인 명의';
            } else {
                if (selectedOwnershipType === 'self') ownershipText = '본인(자사) 명의';
                else if (selectedOwnershipType === 'others') ownershipText = '타인 명의';
                else ownershipText = '타사 명의';
            }
            document.getElementById('reviewOwnershipType').textContent = ownershipText;
            document.getElementById('reviewPurpose').textContent = document.getElementById('purposeInput').value || '-';

            var businessAddrRow = document.getElementById('reviewBusinessAddressRow');
            var businessAddrCell = document.getElementById('reviewBusinessAddress');
            if (businessAddrRow && businessAddrCell) {
                if (selectedMemberType === 'business') {
                    businessAddrRow.style.display = '';
                    businessAddrCell.textContent = '서울특별시 강남구 테헤란로 123'; // 회원 정보(기업)의 사업장 주소
                } else {
                    businessAddrRow.style.display = 'none';
                    businessAddrCell.textContent = '-';
                }
            }
        }

        function handleFileUpload(input, id, maxSize) {
            const file = input.files[0];
            if (!file) return;
            
            // 파일 크기 검증
            if (file.size > maxSize) {
                showToast(`파일 크기는 최대 ${maxSize / 1024 / 1024}MB까지 가능합니다.`, 'error');
                input.value = '';
                return;
            }
            
            // 파일 형식 검증
            const allowedExtensions = ['.jpg', '.jpeg', '.gif', '.png', '.pdf', '.tif', '.tiff', '.zip'];
            const fileName = file.name.toLowerCase();
            const isValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
            
            if (!isValidExtension) {
                showToast('허용되지 않은 파일 형식입니다. (jpg, jpeg, gif, png, pdf, tif, tiff, zip만 가능)', 'error');
                input.value = '';
                return;
            }
            
            const display = document.getElementById(id + 'Display');
            const fileSizeMB = (file.size / 1024 / 1024).toFixed(2);
            display.innerHTML = `
                <div class="uploaded-file">
                    <span>${file.name} (${fileSizeMB}MB)</span>
                    <button type="button" class="btn btn-sm" onclick="removeFile('${id}')">삭제</button>
                </div>
            `;
        }

        function removeFile(id) {
            document.getElementById(id).value = '';
            const display = document.getElementById(id + 'Display');
            if (display) {
                display.innerHTML = '';
            }
        }

        function openPhoneAuth() {
            // 본인인증 팝업 호출 (실제로는 본인인증 서비스 연동)
            showToast('본인인증 팝업이 열립니다.', 'info');
            
            // 시뮬레이션: 인증 완료 처리
            setTimeout(() => {
                authCompleted = true;
                authInfo = {
                    name: '홍길동',
                    birthDate: '1990-01-01',
                    carrier: 'SKT'
                };
                
                const authStatus = document.getElementById('authStatus');
                authStatus.innerHTML = `
                    <div class="auth-completed">
                        <span>인증 완료</span>
                        <span style="font-size: 12px; color: var(--text-secondary);">(${authInfo.name})</span>
                    </div>
                `;
                document.getElementById('authButton').style.display = 'none';
                showToast('본인인증이 완료되었습니다.', 'success');
                
                // 본인인증 완료 후 서류 섹션 업데이트 (본인(자사) 명의인 경우)
                if (selectedOwnershipType === 'self') {
                    updateDocumentSection();
                }
                // 휴대폰 + 본인 명의: 2단계에서 즉시 다음 → 등록 버튼으로 전환
                function showRegisterButton() {
                    if (currentStep !== 2 || numberType !== 'MOBILE' || selectedOwnershipType !== 'self' || !authCompleted) return;
                    const nextBtn = document.getElementById('nextBtn');
                    const submitBtn = document.getElementById('submitBtn');
                    if (nextBtn) {
                        nextBtn.style.setProperty('display', 'none', 'important');
                        nextBtn.style.visibility = 'hidden';
                    }
                    if (submitBtn) {
                        submitBtn.style.setProperty('display', 'block', 'important');
                        submitBtn.style.visibility = 'visible';
                        submitBtn.textContent = '등록';
                    }
                }
                showRegisterButton();
                updateStep2FooterButton();
                setTimeout(showRegisterButton, 0);
                setTimeout(showRegisterButton, 100);
            }, 1000);
        }

        function submitRegister() {
            // 최종 검증
            if (!selectedMemberType || !selectedOwnershipType || !numberType) {
                showToast('필수 정보를 모두 입력해주세요.', 'warning');
                return;
            }
            
            // 본인(자사) 명의이고 휴대폰 번호일 때만 본인인증 필수
            if (selectedOwnershipType === 'self' && requiresAuth && !authCompleted) {
                showToast('본인인증을 완료해주세요.', 'warning');
                return;
            }
            
            showToast('발신번호 등록 신청이 완료되었습니다. 영업일 기준 1~3일 이내 승인 처리됩니다.', 'success');
            closeModal('registerModal');
            
            // 폼 초기화
            resetCallerRegisterForm();
        }

        function resetCallerRegisterForm() {
            currentStep = 1;
            // 현재 회원 유형에 따라 자동 설정
            selectedMemberType = getCurrentMemberType();
            selectedOwnershipType = '';
            numberType = null;
            requiresAuth = false;
            authCompleted = false;
            authInfo = null;
            
            // STEP 표시 초기화
            for (let i = 1; i <= 4; i++) {
                document.getElementById(`step${i}`).classList.remove('active', 'completed');
                const stepContent = document.getElementById(`step${i}Content`);
                if (stepContent) {
                    stepContent.style.display = 'none';
                }
            }
            document.getElementById('step1').classList.add('active');
            document.getElementById('step1Content').style.display = 'block';
            
            // 스텝 인디케이터 3·4단계 다시 표시
            const step3El = document.getElementById('step3');
            const step4El = document.getElementById('step4');
            if (step3El) step3El.style.display = '';
            if (step4El) step4El.style.display = '';
            
            // 버튼 초기화
            document.getElementById('nextBtn').style.display = 'block';
            document.getElementById('submitBtn').style.display = 'none';
            document.getElementById('submitBtn').textContent = '승인요청';
            
            // 입력값 초기화
            document.getElementById('registerForm').reset();
            const numberTypeBadge = document.getElementById('numberTypeBadge');
            if (numberTypeBadge) {
                numberTypeBadge.style.display = 'none';
            }
        }

        // 발신번호 등록 모달 열기
        function openRegisterModal() {
            resetCallerRegisterForm();
            openModal('registerModal');
        }

        function deleteCallerNumber(id) {
            if (confirm('정말 삭제하시겠습니까? 삭제 후에는 복구할 수 없습니다.')) {
                showToast('삭제되었습니다.', 'success');
            }
        }

        function viewDetail(id) {
            // 실제로는 API 호출하여 데이터를 가져옴
            // 예시 데이터
            const detailData = {
                2: {
                    callerNumber: '02-1234-5678',
                    carrier: 'KT',
                    purpose: '고객센터',
                    status: '승인대기',
                    registerDate: '2024-01-15',
                    approveDate: '-',
                    memberType: '기업',
                    ownershipType: '본인(자사) 명의',
                    numberType: '유선번호',
                    contactPhone: '010-1111-2222',
                    contactEmail: 'contact@example.com',
                    documents: [
                        { name: '사업자 등록증', fileName: 'business_registration.pdf', uploadDate: '2024-01-15' },
                        { name: '재직증명서', fileName: 'employment_certificate.pdf', uploadDate: '2024-01-15' },
                        { name: '통신서비스 이용증명원', fileName: 'telecom_certificate.pdf', uploadDate: '2024-01-15' }
                    ]
                }
            };

            const data = detailData[id];
            if (!data) {
                showToast('상세 정보를 불러올 수 없습니다.', 'error');
                return;
            }

            // 모달에 데이터 채우기
            document.getElementById('detailCallerNumber').textContent = data.callerNumber;
            document.getElementById('detailCarrier').textContent = data.carrier;
            document.getElementById('detailPurpose').textContent = data.purpose;
            
            // 상태 배지 생성
            let statusBadge = '';
            if (data.status === '승인완료') {
                statusBadge = '<span class="badge badge-success">승인완료</span>';
            } else if (data.status === '승인대기') {
                statusBadge = '<span class="badge badge-warning">승인대기</span>';
            } else if (data.status === '반려') {
                statusBadge = '<span class="badge badge-danger">반려</span>';
            }
            document.getElementById('detailStatus').innerHTML = statusBadge;
            
            document.getElementById('detailRegisterDate').textContent = data.registerDate;
            document.getElementById('detailApproveDate').textContent = data.approveDate;
            document.getElementById('detailMemberType').textContent = data.memberType;
            document.getElementById('detailOwnershipType').textContent = data.ownershipType;
            document.getElementById('detailNumberType').textContent = data.numberType;
            document.getElementById('detailContactPhone').textContent = data.contactPhone;
            document.getElementById('detailContactEmail').textContent = data.contactEmail || '-';

            // 서류 목록 표시 (상세 모달 전용 id 사용)
            const detailDocSection = document.getElementById('detailDocumentSection');
            const detailDocList = document.getElementById('detailDocumentList');
            if (data.documents && data.documents.length > 0 && detailDocList) {
                detailDocList.innerHTML = data.documents.map(doc => `
                    <div style="padding: 12px; border: 1px solid var(--border-color); border-radius: var(--radius-md); margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>${doc.name}</strong>
                                <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                    ${doc.fileName} · 업로드일: ${doc.uploadDate}
                                </div>
                            </div>
                            <button class="btn btn-sm btn-outline" onclick="downloadDocument('${doc.fileName}')">다운로드</button>
                        </div>
                    </div>
                `).join('');
                if (detailDocSection) detailDocSection.style.display = 'block';
            } else {
                if (detailDocSection) detailDocSection.style.display = 'none';
            }

            // 모달 열기
            const modalEl = document.getElementById('detailModal');
            if (modalEl) {
                modalEl.style.display = 'flex';
                modalEl.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }

        function downloadDocument(fileName) {
            // 실제로는 파일 다운로드 API 호출
            showToast(`${fileName} 다운로드를 시작합니다.`, 'info');
        }

        function viewRejectionReason(id) {
            alert('반려 사유: 서류가 불명확합니다. 명확한 서류를 다시 제출해주세요.');
        }

        var editingCallerId = null;

        function openEditPurposeModal(id, callerNumber, currentPurpose) {
            editingCallerId = id;
            document.getElementById('editPurposeModalNumber').textContent = callerNumber;
            document.getElementById('editPurposeInput').value = currentPurpose || '';
            openModal('editPurposeModal');
            setTimeout(function() { document.getElementById('editPurposeInput').focus(); }, 100);
        }

        function saveCallerPurpose() {
            var purpose = (document.getElementById('editPurposeInput').value || '').trim();
            if (!purpose) {
                showToast('용도를 입력해주세요.', 'error');
                return;
            }
            if (editingCallerId == null) return;
            var row = document.querySelector('#callerNumberTableBody tr[data-id="' + editingCallerId + '"]');
            if (row) {
                var numberTd = row.querySelector('.caller-number-cell');
                if (numberTd) {
                    var num = numberTd.textContent.replace(/\s*\([^)]*\)\s*$/, '').trim();
                    numberTd.innerHTML = num + ' <span style="color: var(--text-secondary);">(' + purpose + ')</span>';
                    numberTd.onclick = function() { openEditPurposeModal(editingCallerId, num, purpose); };
                }
            }
            showToast('용도가 수정되었습니다.', 'success');
            closeModal('editPurposeModal');
            editingCallerId = null;
        }

// 발신번호 패널 전용 초기화 (mypage.html#caller에서 사용)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { updateMemberTypeDisplay(); });
} else {
    updateMemberTypeDisplay();
}
