# Vision Inspection Agent — 슬래시 커맨드

이 커맨드는 외부 API 호출 없이, 현재 Codex 세션 안에서 직접
이미지 분석 + 웹 리서치를 수행하고 PPT 보고서를 생성합니다.

## 인자 (Arguments)

`$ARGUMENTS` 형식: `<이미지경로> [product=<제품종류>] [focus=<중점항목>]`

예시:
- `/inspect images/pcb_01.png`
- `/inspect images/leather.jpg product=가죽 focus="스크래치, 변색"`

기본값:
- `product` → `PCB`
- `focus` → `표면 결함, 오염, 스크래치, 균열`

이미지 경로가 비어있으면 사용자에게 물어보세요.

## 절차

### 0. 사전 확인
- 이미지 파일이 존재하는지 확인 (없으면 사용자에게 알리고 중단)
- 출력 폴더 생성: `reports/<YYYYMMDD-HHMMSS>/`
- 입력 이미지를 출력 폴더에 `input.<원본확장자>`로 복사

### 1. 이미지 분석 (Vision)

이미지를 읽어서, 다음 페르소나로 분석:

> 당신은 **{product_type}** 제조 품질 검사 전문가입니다.
> 중점 검사 항목: {inspection_focus}

분석 결과를 **반드시 아래 JSON 스키마**로 `reports/<ts>/analysis.json` 에 저장
(이 스키마는 `render_report.py`가 그대로 소비함 — 키 이름 바꾸지 말 것):

```json
{
  "has_defect": true,
  "overall_assessment": "검사 결과 한 줄 요약 (한국어)",
  "overall_severity": "HIGH | MEDIUM | LOW | NONE",
  "confidence": 0.85,
  "defects": [
    {
      "type": "결함 유형 한국어 (예: 스크래치, 오염, 균열, 변색, 핀홀, 박리)",
      "type_en": "Defect type in English",
      "location_desc": "결함 위치 설명 (예: 우상단, 중앙부)",
      "bbox_normalized": [0.12, 0.08, 0.34, 0.27],
      "size_estimate": "정성적 크기 (미세 / 중간 / 큰)",
      "description": "결함 상세 묘사 (1~2문장)",
      "severity": "HIGH | MEDIUM | LOW",
      "possible_causes": ["원인 추정 1", "원인 추정 2", "원인 추정 3"]
    }
  ],
  "inspection_notes": "검사관 톤의 종합 소견 (3~4문장, 임원 보고용)",
  "recommended_actions": [
    "권장 조치 1 (구체적, 실행 가능)",
    "권장 조치 2",
    "권장 조치 3"
  ]
}
```

**중요 규칙:**
- `bbox_normalized`는 0~1 정규화 좌표 `[좌상x, 좌상y, 우하x, 우하y]`
  (이미지 전체가 (0,0)~(1,1), Y는 위→아래)
- 결함 없으면 `has_defect: false`, `defects: []`, `overall_severity: "NONE"`
- 추측은 신중히, 불확실하면 `confidence` 낮게
- 모든 한국어 텍스트는 임원 보고 톤 (간결, 단호)

### 2. 웹 리서치 (근본 원인 + 산업 표준)

웹 검색 기능이 환경에 있으면 사용해 **2~6회** 검색하여 다음 정보를 수집:
1. 검출된 결함 유형의 공정상 일반적 근본 원인
2. 산업 표준 검사 방법 / ISO·IEC 표준
3. 유사 사례 (논문, 케이스 스터디)
4. 예방·개선 모범 사례

웹 검색이 불가하면 모델 지식 기반으로 채우되, `_sources`는 빈 배열로 두고
`_queries`에 "(web search unavailable)" 한 줄을 남깁니다.

결함이 검출되지 않은 경우(`has_defect: false`)에도, 해당 제품의 일반적인
검사 표준·예방 모범 사례를 가볍게 채울 것.

결과를 `reports/<ts>/research.json` 에 저장 (스키마 고정):

```json
{
  "root_cause_analysis": [
    {"category": "공정 요인", "details": "1~2문장 한국어"},
    {"category": "설비 요인", "details": "..."},
    {"category": "재료 요인", "details": "..."},
    {"category": "환경 요인", "details": "..."}
  ],
  "industry_standards": [
    "관련 표준/규격 (간단한 설명 포함, 1줄)"
  ],
  "similar_cases": [
    "유사 사례 또는 논문 요약 (1~2문장)"
  ],
  "best_practices": [
    "모범 사례 1",
    "모범 사례 2",
    "모범 사례 3"
  ],
  "improvement_recommendations": [
    "개선 권고 1 (구체적, 우선순위 높음)",
    "개선 권고 2",
    "개선 권고 3"
  ],
  "_queries": ["수행한 검색 쿼리들"],
  "_sources": ["수집한 출처 URL들 (중복 제거)"]
}
```

`_queries`와 `_sources`는 실제 검색에서 사용·수집한 값으로 채울 것
(PPT 마지막 슬라이드에서 출처 목록으로 표시됨).

### 3. 렌더링 (PPT + 주석 PNG)

venv의 Python으로 `render_report.py`를 실행 (Windows PowerShell):

```powershell
.\.venv\Scripts\python.exe render_report.py `
  "reports/<ts>/input.<ext>" `
  "reports/<ts>/analysis.json" `
  "reports/<ts>/research.json" `
  --product "<product>" `
  --out "reports/<ts>/검사보고서.pptx" `
  --annotated-out "reports/<ts>/annotated.png"
```

POSIX(macOS/Linux)일 경우:
```bash
./.venv/bin/python render_report.py \
  "reports/<ts>/input.<ext>" \
  "reports/<ts>/analysis.json" \
  "reports/<ts>/research.json" \
  --product "<product>" \
  --out "reports/<ts>/검사보고서.pptx" \
  --annotated-out "reports/<ts>/annotated.png"
```

스크립트가 두 줄 출력하면 성공:
```
Wrote reports/<ts>/검사보고서.pptx
Wrote reports/<ts>/annotated.png
```

### 4. 결과 보고

사용자에게 다음을 알려줄 것:
- 생성된 폴더 경로: `reports/<ts>/`
- 핵심 결과: 종합 심각도 / 검출 결함 수 / 신뢰도
- PPT 열기 명령 한 줄
  - Windows: `Start-Process "reports/<ts>/검사보고서.pptx"`
  - macOS: `open "reports/<ts>/검사보고서.pptx"`
  - Linux: `xdg-open "reports/<ts>/검사보고서.pptx"`

오류 발생 시:
- JSON 스키마 위반 → 누락 키 명시하고 다시 시도
- 웹 검색 실패 → research.json을 최소 형태로 채워 PPT는 만들기
- 이미지 분석 실패 → 다른 이미지 시도 권유

## 비용 / 시간 가이드
- 1회 실행: 약 30초 ~ 2분 (웹 검색 호출 수에 따라)
- 외부 API 키 비용: **없음** (현재 Codex 세션 내에서 처리)
