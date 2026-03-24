# index.html 비교용 스냅샷

| 파일 | 설명 |
|------|------|
| **`index.html`** | 지금 작업 중인 랜딩 (로컬 워킹트리) |
| **`index.last-commit.html`** | **마지막으로 커밋된** `index.html` 내용을 복사한 파일. 브라우저로 열어 레이아웃·문구를 비교할 수 있습니다. |

### (선택) `index.before-today.html` 오프라인 스냅샷

과거 커밋을 파일로 남기려면 `save-before-today.ps1`으로 `index.before-today.html`을 만들 수 있습니다.

## 보는 방법

1. `index.html` — 주소 예: `file:///.../spec/index.html`
2. `index.last-commit.html` — 같은 폴더의 복사본으로 열기

## 스냅샷 다시 만들기 (커밋 후 HEAD가 바뀌었을 때)

저장소 루트에서:

```bash
git show HEAD:index.html > index.last-commit.html
```

PowerShell (UTF-8):

```powershell
git show HEAD:index.html | Out-File -FilePath index.last-commit.html -Encoding utf8
```

**참고:** “커밋하기 전”에 **직전 커밋**과 비교하려면, 위 명령은 **항상 마지막 커밋 버전**을 뽑습니다. 커밋한 뒤에 스냅샷을 갱신하면, 그다음부터는 새 커밋이 기준이 됩니다.
