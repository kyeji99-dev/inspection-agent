# Vision Inspection Agent — 실행 가이드

Codex(또는 호환 AI 에이전트) 세션 안에서 **직접** 동작하는 AI 비전 검사 도구.
별도 API 키·서버 없이 슬래시 커맨드 한 줄로 결함 분석 → 웹 리서치 → PPT 보고서 생성.

## 1. 환경 설정 (3분)

Windows PowerShell:
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

설치되는 패키지: `python-pptx`, `Pillow` (그 외 의존성 없음, **API 키 불필요**).

## 2. 실행 — `/inspect` 슬래시 커맨드

### 2-1. Codex에 슬래시 커맨드 등록

이 프로젝트는 `.codex/prompts/inspect.md` 에 슬래시 커맨드를 정의해두었습니다.

**프로젝트 단위 prompt를 자동 인식하는 Codex 버전이라면** 별도 작업 없이 바로 사용 가능합니다.
인식이 안 되면 사용자 홈 폴더로 복사:

```powershell
# Windows
mkdir $HOME\.codex\prompts -Force
Copy-Item .codex\prompts\inspect.md $HOME\.codex\prompts\inspect.md
```

```bash
# macOS / Linux
mkdir -p ~/.codex/prompts
cp .codex/prompts/inspect.md ~/.codex/prompts/inspect.md
```

### 2-2. 사용

1. 프로젝트 폴더(`C:\inspection-agent`)에서 Codex 열기 (또는 `cd` 해서 세션 시작)
2. 분석할 이미지를 폴더 안에 두기 (예: `images/pcb_01.png`)
3. 슬래시 커맨드 입력:

```
/inspect images/pcb_01.png
```

옵션 인자:
```
/inspect images/pcb_01.png product=PCB focus="스크래치, 균열"
/inspect images/leather.jpg product=가죽 focus="변색, 오염"
```

기본값: `product=PCB`, `focus=표면 결함, 오염, 스크래치, 균열`

## 3. 동작 흐름

`/inspect` 한 줄을 입력하면 Codex 에이전트가:

1. **이미지 분석** — 결함 검출, 위치(bbox), 심각도, 추정 원인 → `analysis.json`
2. **웹 리서치** — 결함 유형 기반 산업 표준·근본 원인 자동 검색 → `research.json`
3. **PPT 렌더링** — `render_report.py` 호출 → 6슬라이드 임원 보고서 생성

소요 시간: 약 30초 ~ 2분 (검색 호출 수에 따라)

## 4. 결과물

`reports/<YYYYMMDD-HHMMSS>/` 폴더에 모두 모입니다:

| 파일 | 설명 |
|---|---|
| `input.<ext>` | 원본 이미지 (복사본) |
| `annotated.png` | AI 검출 결함 영역 표시 이미지 |
| `analysis.json` | 비전 분석 원시 데이터 |
| `research.json` | 웹 리서치 원시 데이터 |
| `검사보고서.pptx` | 6슬라이드 보고서 (표지 / 요약 / 결함 상세 / 근본 원인 / 권고 / 출처) |

PPT 빠르게 열기:
```powershell
Start-Process reports\<폴더이름>\검사보고서.pptx
```

## 5. 데모 데이터 받기 (3분)

### MVTec AD (학술·연구 용도 무료)
- https://www.mvtec.com/company/research/datasets/mvtec-ad
- 15개 카테고리: 병, 케이블, 캡슐, 카펫, 그리드, 가죽, 너트, 알약, 스크류, 타일, 칫솔, 트랜지스터, 우드, 지퍼, 메탈 너트
- 각 카테고리별 정상/결함 이미지 수백 장

### Hugging Face에서 빠르게 받기
```python
from datasets import load_dataset
ds = load_dataset("Voxel51/mvtec-ad", split="train[:50]")
```
또는 페이지에서 직접 다운로드: https://huggingface.co/datasets/Voxel51/mvtec-ad

### 그 외 추천 공개 데이터셋
- KolektorSDD: 전자 부품 결함
- DAGM 2007: 직물 결함
- NEU Surface Defect: 금속 표면 결함

## 6. 대표님 시연 시 추천 흐름

### 시연 직전 준비
- [ ] 결함이 명확한 MVTec 이미지 3~5장 미리 골라두기 (스크래치/오염/균열 각각)
- [ ] 미리 한 번 `/inspect`로 돌려서 결과 PPT 확인 (응답 품질이 약한 케이스 제거)
- [ ] 시연용 이미지 폴더 정리 (`images/demo/`)
- [ ] 백업 PPT 한 부 미리 생성해두기

### 시연 멘트 예시
```
"이 도구는 외부 공개 데이터셋만 사용해 만든 검사 보조 에이전트입니다.
보안 이슈 없이 워크플로우만 검증했고, 같은 구조를 사내에 옮기면
저희 검사 업무에 즉시 활용 가능합니다.

지금 보시는 이미지는 산업 결함 공개 데이터셋(MVTec)의
○○ 결함입니다. 슬래시 커맨드 한 줄만 입력하면..."

[/inspect images/demo/pcb_01.png 입력]

"보시는 것처럼 Claude가
1) 먼저 이미지를 정밀 분석해 결함 위치를 잡고
2) 그 결함에 대한 산업 표준·근본 원인을 웹에서 자동으로 조사하고
3) 마지막으로 임원 보고용 PPT를 자동 생성합니다.

이게 평소에 검사관 한 명이 30분~1시간 걸리는 작업입니다.
30초~1분 만에 끝납니다."

[reports 폴더에서 PPT 열기 → 슬라이드 보여주기]

"보안 이슈가 있는 사내 데이터는 폐쇄망 환경에 같은 워크플로우를
배포하면 됩니다. Claude는 SaaS 외에 AWS Bedrock, GCP Vertex,
온프레미스 등 다양한 배포 옵션을 지원합니다."
```

### 핵심 메시지 3가지
1. **"공개 데이터로 만들었지만 사내 워크플로우와 동일"**
2. **"30분 걸리던 보고서가 30초"**
3. **"주니어 1명이 ○일 만에 만든 결과물"**

## 7. 트러블슈팅

### `/inspect`가 인식 안 됨
- 프로젝트 루트(`C:\inspection-agent`)에서 Codex 세션을 열었는지 확인
- `.codex/prompts/inspect.md` 파일 존재 확인
- Codex가 프로젝트 단위 prompt를 자동 인식 못하면 `~/.codex/prompts/` 로 복사 (위 2-1 참조)
- Codex 세션 재시작하면 슬래시 커맨드가 재로딩됩니다

### bbox가 부정확
- Vision 분석의 bbox는 추정치 — 100% 정확하지 않음
- 정성적 위치 설명(`location_desc`)이 더 안정적
- 데모용으로는 결함이 크고 명확한 이미지를 선택

### 검사 결과가 약함 / 추상적임
- `product` 인자를 더 구체적으로 (예: `product=PCB` → `product="산업용 PCB 솔더링 표면"`)
- `focus` 인자를 명확히 (예: `focus="솔더링 결함, 단선, 단락"`)
- 같은 이미지로 한 번 더 돌리면 다른 각도의 분석이 나올 수도 있음

### `render_report.py` 실행 시 에러
- venv 활성화 상태인지 확인 (`(.venv)` 프롬프트)
- `pip install -r requirements.txt` 다시 실행
- `analysis.json` / `research.json`이 유효한 JSON인지 확인

### 웹 검색 결과가 빈약함
- 결함 유형이 너무 일반적이면(예: 그냥 "결함") 검색어가 약해짐
- `focus` 인자에 구체 키워드를 넣으면 검색 품질이 올라감

## 8. 개선 아이디어 (시간 남으면)

- [ ] 여러 이미지 일괄 검사 모드 (`/inspect-batch images/*.png`)
- [ ] 검사 통계 대시보드 (결함 유형별 분포)
- [ ] PPT 디자인을 회사 템플릿으로 변경
- [ ] 이전 검사 결과와의 시계열 비교
- [ ] 슬랙/이메일로 보고서 자동 발송
