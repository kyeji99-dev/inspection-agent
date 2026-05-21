# AGENTS.md

이 파일은 AI 코딩 에이전트(Codex, Claude Code 등)가 이 프로젝트에서
일관되게 동작하도록 컨텍스트를 제공합니다.

## 프로젝트 개요

**Vision Inspection Agent** — AI 비전 기반 산업 결함 검사 보조 도구.
이미지 1장 → (분석 + 웹 리서치) → 6슬라이드 임원 보고용 PPT.

핵심 특징:
- **외부 API 키 불필요** — 현재 에이전트 세션 안에서 분석·리서치를 직접 수행
- PPT 렌더링은 로컬 Python (`python-pptx`)만 사용 → 네트워크·라이선스 의존성 없음
- 데모 데이터는 공개 데이터셋(MVTec AD) 기반

## 주 워크플로우: `/inspect`

자세한 절차는 [`.codex/prompts/inspect.md`](.codex/prompts/inspect.md)에 정의되어 있음.

요약:
1. 이미지 읽기 → `analysis.json` (결함 검출, bbox, 심각도) 생성
2. (선택) 웹 검색 → `research.json` (근본 원인, 산업 표준) 생성
3. `render_report.py` 호출 → `검사보고서.pptx` + `annotated.png` 생성

모든 산출물은 `reports/<YYYYMMDD-HHMMSS>/` 폴더에 저장.

## 파일 구조

| 경로 | 역할 |
|---|---|
| `.codex/prompts/inspect.md` | Codex 슬래시 커맨드 정의 (절차 + JSON 스키마) |
| `render_report.py` | PPT/오버레이 생성 — 외부 API 없음, JSON 입력만 |
| `batch_inspect.py` | 다수 이미지 일괄 처리 (검증·시연용) |
| `download_demo.py` | Hugging Face에서 MVTec AD 샘플 다운로드 |
| `requirements.txt` | `python-pptx`, `Pillow` 두 줄 |
| `.venv/` | Python 가상환경 (Python 3.13+) |
| `images/`, `images_diverse/` | 데모 입력 이미지 |
| `reports/` | 검사 결과 산출물 |

## Python 환경

Windows PowerShell:
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

POSIX:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`render_report.py`는 항상 venv의 Python으로 호출:
- Windows: `.\.venv\Scripts\python.exe`
- POSIX: `./.venv/bin/python`

## JSON 데이터 계약 (변경 금지)

`render_report.py`는 다음 두 JSON의 키를 그대로 소비합니다.
키 이름·구조를 임의로 바꾸면 PPT 생성이 실패합니다.

### `analysis.json` 필수 키
`has_defect`, `overall_assessment`, `overall_severity` (HIGH/MEDIUM/LOW/NONE),
`confidence`, `defects` (배열, 각 항목에 `type`/`type_en`/`location_desc`/
`bbox_normalized`/`size_estimate`/`description`/`severity`/`possible_causes`),
`inspection_notes`, `recommended_actions`.

### `research.json` 필수 키
`root_cause_analysis` (4개 카테고리: 공정/설비/재료/환경),
`industry_standards`, `similar_cases`, `best_practices`,
`improvement_recommendations`, `_queries`, `_sources`.

자세한 예시는 [`.codex/prompts/inspect.md`](.codex/prompts/inspect.md) 참조.

## 디자인 / 톤 규칙

- 모든 사용자 표시 텍스트는 **한국어**, **임원 보고 톤** (간결·단호·데이터 중심)
- 결함 유형은 한국어와 영문 병기 (`type` / `type_en`)
- bbox 추정은 신중하게, 불확실하면 `confidence`를 낮춰서 표현
- PPT 디자인 토큰(NAVY/ICE/심각도 색상)은 `render_report.py` 상단에 정의

## 검증 자료

`reports/batch-50/` 에 14개 카테고리 × 41장 검증 결과 보관.
디자인·내용 흐름 참고용:
- [`reports/batch-50/_summary.md`](reports/batch-50/_summary.md) — 전체 인덱스
- HIGH 심각도 5장 (transistor 01 / pill 07 / carpet 21 / toothbrush 32 / hazelnut 14)

## 작업 시 주의사항

- **외부 API 호출 코드 추가 금지** — `anthropic`·`openai` 같은 SDK는 의존성에서 의도적으로 제외됨
- **`render_report.py` JSON 스키마 변경 금지** — 변경 시 기존 41장 검증 결과 호환 깨짐
- **출력 폴더는 항상 `reports/<timestamp>/`** — 다른 위치에 쓰지 말 것
- 한글 파일명(`검사보고서.pptx`)은 PowerShell 콘솔에서 깨져 보일 수 있으나 실제 파일은 정상
