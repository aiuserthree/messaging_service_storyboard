/**
 * 화면설계서 오버레이 스크립트
 * - 페이지 컴포넌트에 번호 마커 표시
 * - 클릭 시 툴팁으로 기능 설명 표시
 * 
 * 사용법:
 * 1. <script src="js/spec-overlay.js"></script> 추가
 * 2. initSpecOverlay(specData) 호출
 */

(function() {
    // 스타일 삽입
    const style = document.createElement('style');
    style.textContent = `
        /* Spec 오버레이 토글 버튼 */
        .spec-toggle-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 99999;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
            transition: all 0.3s ease;
        }

        .spec-toggle-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5);
        }

        .spec-toggle-btn.active {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
        }

        .spec-toggle-btn.active:hover {
            box-shadow: 0 6px 20px rgba(34, 197, 94, 0.5);
        }

        /* 번호 마커 */
        .spec-marker {
            position: absolute;
            width: 28px;
            height: 28px;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            z-index: 9999;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
            border: 2px solid white;
            opacity: 0;
            transform: scale(0);
            pointer-events: none;
        }

        .spec-overlay-active .spec-marker {
            opacity: 1;
            transform: scale(1);
            pointer-events: auto;
        }

        .spec-marker:hover {
            transform: scale(1.15);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.5);
        }

        .spec-marker.active {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.5);
        }

        /* 툴팁 */
        .spec-tooltip {
            position: fixed;
            z-index: 100000;
            max-width: 400px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            opacity: 0;
            visibility: hidden;
            transform: translateY(10px);
            transition: all 0.2s ease;
        }

        .spec-tooltip.show {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .spec-tooltip-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 20px;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border-radius: 12px 12px 0 0;
            color: white;
        }

        .spec-tooltip-number {
            width: 32px;
            height: 32px;
            background: white;
            color: #2563eb;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 700;
            flex-shrink: 0;
        }

        .spec-tooltip-title {
            font-size: 16px;
            font-weight: 600;
        }

        .spec-tooltip-close {
            position: absolute;
            top: 12px;
            right: 12px;
            width: 28px;
            height: 28px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 18px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }

        .spec-tooltip-close:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        .spec-tooltip-body {
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
        }

        .spec-tooltip-section {
            margin-bottom: 16px;
        }

        .spec-tooltip-section:last-child {
            margin-bottom: 0;
        }

        .spec-tooltip-label {
            font-size: 12px;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        .spec-tooltip-content {
            font-size: 14px;
            color: #1e293b;
            line-height: 1.6;
        }

        .spec-tooltip-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .spec-tooltip-list li {
            position: relative;
            padding-left: 16px;
            margin-bottom: 6px;
            font-size: 13px;
            color: #475569;
        }

        .spec-tooltip-list li::before {
            content: '•';
            position: absolute;
            left: 0;
            color: #2563eb;
        }

        .spec-tooltip-tag {
            display: inline-block;
            padding: 2px 8px;
            background: #dbeafe;
            color: #2563eb;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 4px;
        }

        .spec-tooltip-tag.required {
            background: #fee2e2;
            color: #dc2626;
        }

        .spec-tooltip-tag.api {
            background: #d1fae5;
            color: #059669;
        }

        /* 하이라이트 효과 */
        .spec-highlight {
            outline: 3px solid #ef4444 !important;
            outline-offset: 4px !important;
            background-color: rgba(239, 68, 68, 0.05) !important;
            transition: all 0.3s ease;
        }

        /* 마커가 잘리지 않도록 부모 요소 overflow 처리 */
        .spec-overlay-active .form-group,
        .spec-overlay-active .card,
        .spec-overlay-active .form-select,
        .spec-overlay-active .form-input,
        .spec-overlay-active [class*="container"],
        .spec-overlay-active [class*="wrapper"] {
            overflow: visible !important;
        }

        /* 모달 내부 마커는 z-index 높게 */
        .modal-overlay .spec-marker {
            z-index: 100001 !important;
        }

        /* 모달이 열렸을 때 바닥 페이지 마커 숨기기 (모달 외부) */
        body.spec-modal-open.spec-overlay-active .spec-marker {
            opacity: 0 !important;
            pointer-events: none !important;
            transform: scale(0) !important;
        }

        /* 모달이 열렸을 때 열린 모달 내부 마커만 표시 */
        body.spec-modal-open.spec-overlay-active .modal-overlay.spec-modal-visible .spec-marker {
            opacity: 1 !important;
            pointer-events: auto !important;
            transform: scale(1) !important;
        }

    `;
    document.head.appendChild(style);

    // 전역 변수
    let isOverlayActive = false;
    let currentTooltip = null;
    let specData = [];

    // 토글 버튼 생성
    function createToggleButton() {
        const btn = document.createElement('button');
        btn.className = 'spec-toggle-btn';
        btn.innerHTML = '📋 화면설계 보기';
        btn.onclick = toggleOverlay;
        document.body.appendChild(btn);
        return btn;
    }

    // 툴팁 생성
    function createTooltip() {
        const tooltip = document.createElement('div');
        tooltip.className = 'spec-tooltip';
        tooltip.innerHTML = `
            <div class="spec-tooltip-header">
                <span class="spec-tooltip-number"></span>
                <span class="spec-tooltip-title"></span>
                <button class="spec-tooltip-close" onclick="window.closeSpecTooltip()">×</button>
            </div>
            <div class="spec-tooltip-body"></div>
        `;
        document.body.appendChild(tooltip);
        return tooltip;
    }

    // 마커 생성
    function createMarker(item, index) {
        const marker = document.createElement('div');
        marker.className = 'spec-marker';
        marker.textContent = index + 1;
        marker.dataset.index = index;
        
        // 대상 요소 찾기
        const target = document.querySelector(item.selector);
        if (!target) {
            console.warn(`Spec: 선택자를 찾을 수 없음 - ${item.selector}`);
            return null;
        }

        // position relative 설정
        const computedStyle = window.getComputedStyle(target);
        if (computedStyle.position === 'static') {
            target.style.position = 'relative';
        }

        // 마커 위치 설정
        marker.style.position = 'absolute';
        marker.style.top = item.position?.top || '-10px';
        marker.style.left = item.position?.left || '-10px';
        if (item.position?.right) marker.style.right = item.position.right;
        if (item.position?.bottom) marker.style.bottom = item.position.bottom;

        target.appendChild(marker);

        // 호버 이벤트 (마우스 올리면 툴팁 표시)
        marker.onmouseenter = (e) => {
            e.stopPropagation();
            showTooltip(item, index, marker);
        };

        // 클릭 이벤트도 유지 (모바일 대응)
        marker.onclick = (e) => {
            e.stopPropagation();
            showTooltip(item, index, marker);
        };

        return { marker, target };
    }

    // 툴팁 표시
    function showTooltip(item, index, marker) {
        // 이전 활성 마커 비활성화
        document.querySelectorAll('.spec-marker.active').forEach(m => m.classList.remove('active'));
        document.querySelectorAll('.spec-highlight').forEach(el => el.classList.remove('spec-highlight'));

        // 현재 마커 활성화
        marker.classList.add('active');
        marker.parentElement?.classList.add('spec-highlight');

        // 툴팁 내용 설정
        const tooltip = currentTooltip;
        tooltip.querySelector('.spec-tooltip-number').textContent = index + 1;
        tooltip.querySelector('.spec-tooltip-title').textContent = item.title;
        
        let bodyHtml = '';
        
        if (item.description) {
            bodyHtml += `
                <div class="spec-tooltip-section">
                    <div class="spec-tooltip-label">설명</div>
                    <div class="spec-tooltip-content">${item.description}</div>
                </div>
            `;
        }

        if (item.function) {
            bodyHtml += `
                <div class="spec-tooltip-section">
                    <div class="spec-tooltip-label">기능</div>
                    <div class="spec-tooltip-content">${item.function}</div>
                </div>
            `;
        }

        if (item.behavior && item.behavior.length > 0) {
            bodyHtml += `
                <div class="spec-tooltip-section">
                    <div class="spec-tooltip-label">동작</div>
                    <ul class="spec-tooltip-list">
                        ${item.behavior.map(b => `<li>${b}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        if (item.design && item.design.length > 0) {
            bodyHtml += `
                <div class="spec-tooltip-section">
                    <div class="spec-tooltip-label">디자인</div>
                    <ul class="spec-tooltip-list">
                        ${item.design.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        if (item.api) {
            bodyHtml += `
                <div class="spec-tooltip-section">
                    <div class="spec-tooltip-label">API</div>
                    <div class="spec-tooltip-content">
                        <span class="spec-tooltip-tag api">API</span> ${item.api}
                    </div>
                </div>
            `;
        }

        if (item.tags && item.tags.length > 0) {
            bodyHtml += `
                <div class="spec-tooltip-section">
                    <div class="spec-tooltip-label">태그</div>
                    <div class="spec-tooltip-content">
                        ${item.tags.map(tag => `<span class="spec-tooltip-tag ${tag.type || ''}">${tag.text}</span>`).join('')}
                    </div>
                </div>
            `;
        }

        tooltip.querySelector('.spec-tooltip-body').innerHTML = bodyHtml;

        // 위치 계산
        const markerRect = marker.getBoundingClientRect();
        const tooltipWidth = 400;
        const tooltipHeight = tooltip.offsetHeight || 300;
        
        let left = markerRect.right + 10;
        let top = markerRect.top;

        // 화면 밖으로 나가는지 체크
        if (left + tooltipWidth > window.innerWidth) {
            left = markerRect.left - tooltipWidth - 10;
        }
        if (top + tooltipHeight > window.innerHeight) {
            top = window.innerHeight - tooltipHeight - 20;
        }
        if (top < 10) top = 10;
        if (left < 10) left = 10;

        tooltip.style.left = left + 'px';
        tooltip.style.top = top + 'px';
        tooltip.classList.add('show');
    }

    // 툴팁 닫기
    window.closeSpecTooltip = function() {
        if (currentTooltip) {
            currentTooltip.classList.remove('show');
        }
        document.querySelectorAll('.spec-marker.active').forEach(m => m.classList.remove('active'));
        document.querySelectorAll('.spec-highlight').forEach(el => el.classList.remove('spec-highlight'));
    };

    // 오버레이 토글
    function toggleOverlay() {
        isOverlayActive = !isOverlayActive;
        const btn = document.querySelector('.spec-toggle-btn');
        
        if (isOverlayActive) {
            // 마커 지연 생성 (최초 활성화 시에만)
            createAllMarkers();
            document.body.classList.add('spec-overlay-active');
            btn.classList.add('active');
            btn.innerHTML = '✓ 화면설계 ON';
        } else {
            document.body.classList.remove('spec-overlay-active');
            btn.classList.remove('active');
            btn.innerHTML = '📋 화면설계 보기';
            window.closeSpecTooltip();
        }
    }

    // 모달 상태 감지 및 마커 표시/숨김 처리
    function checkModalState() {
        const modals = document.querySelectorAll('.modal-overlay');
        let isModalOpen = false;

        modals.forEach(modal => {
            const style = window.getComputedStyle(modal);
            // display가 none이 아니고, visibility가 hidden이 아니면 열린 것으로 판단
            if (style.display !== 'none' && style.visibility !== 'hidden') {
                isModalOpen = true;
                // 열린 모달에 클래스 추가
                modal.classList.add('spec-modal-visible');
            } else {
                // 닫힌 모달에서 클래스 제거
                modal.classList.remove('spec-modal-visible');
            }
        });

        if (isModalOpen) {
            document.body.classList.add('spec-modal-open');
        } else {
            document.body.classList.remove('spec-modal-open');
        }
    }

    // MutationObserver로 모달 상태 변화 감지 (최적화)
    let modalObserver = null;
    function observeModalChanges() {
        if (modalObserver) return; // 이미 실행 중이면 스킵
        
        // 모달 요소만 직접 감시 (전체 body 감시 제거)
        const modals = document.querySelectorAll('.modal-overlay');
        if (modals.length === 0) return;
        
        modalObserver = new MutationObserver(() => {
            requestAnimationFrame(checkModalState);
        });

        modals.forEach(modal => {
            modalObserver.observe(modal, {
                attributes: true,
                attributeFilter: ['style', 'class']
            });
        });

        // 초기 상태 체크
        checkModalState();
    }

    // 마커 생성 여부
    let markersCreated = false;
    
    // 마커 지연 생성
    function createAllMarkers() {
        if (markersCreated) return;
        markersCreated = true;
        
        specData.forEach((item, index) => {
            createMarker(item, index);
        });
        
        // 모달 감시 시작
        observeModalChanges();
    }

    // 초기화 (버튼과 툴팁만 생성, 마커는 지연)
    window.initSpecOverlay = function(data) {
        specData = data;

        // UI 요소만 생성 (마커는 버튼 클릭 시 생성)
        createToggleButton();
        currentTooltip = createTooltip();

        // 문서 클릭 시 툴팁 닫기
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.spec-marker') && 
                !e.target.closest('.spec-tooltip')) {
                window.closeSpecTooltip();
            }
        });

        console.log('✅ Spec Overlay 준비 완료 - ' + specData.length + '개 컴포넌트 (지연 로딩)');
    };
})();
