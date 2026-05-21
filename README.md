# Vision Inspection Agent — 실행 가이드

## 1. 환경 설정 (5분)

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 2. API 키 발급

1. https://console.anthropic.com 가입
2. Billing 메뉴에서 $10 정도 충전 (개인 카드, 데모 1회당 약 $0.5~2)
3. API Keys 메뉴에서 키 발급 (`sk-ant-...`)

## 3. 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열립니다 (http://localhost:8501)

## 4. 사용 흐름

1. 사이드바에 API 키 입력
2. 사이드바에서 제품 종류·검사 항목 설정
3. 이미지 업로드 (MVTec AD 등 공개 데이터셋)
4. "검사 시작" 클릭
5. 3단계 진행 상황 확인 (비전 분석 → 웹 리서치 → PPT 생성)
6. 결과 확인 후 PPT 다운로드

## 5. 데모 데이터 받기 (3분)

### MVTec AD (학술·연구용 무료)
- https://www.mvtec.com/company/research/datasets/mvtec-ad
- 15개 카테고리 (병, 케이블, 캡슐, 카펫, 그리드, 가죽 등)
- 각 카테고리별 정상/결함 이미지 수백 장

### Hugging Face에서 빠르게 받기
```python
# Python으로 일부만 다운로드
from datasets import load_dataset
ds = load_dataset("Voxel51/mvtec-ad", split="train[:50]")
```

또는 그냥 Hugging Face 페이지에서 샘플 이미지 다운로드:
- https://huggingface.co/datasets/Voxel51/mvtec-ad

### 그 외 추천 공개 데이터셋
- KolektorSDD: 전자 부품 결함
- DAGM 2007: 직물 결함
- NEU Surface Defect: 금속 표면 결함

## 6. 대표님 시연 시 추천 흐름

### 시연 직전 준비
- [ ] 결함이 명확한 MVTec 이미지 3~5장 미리 골라두기 (스크래치/오염/균열 각각)
- [ ] 미리 한 번 돌려서 결과 확인 (Claude가 응답 안 할 케이스 제거)
- [ ] 사이드바 product_type을 이미지에 맞게 미리 설정
- [ ] 한 번 PPT 생성 미리 해두고 백업

### 시연 멘트 예시
```
"이 도구는 외부 공개 데이터셋만 사용해 만든 검사 보조 에이전트입니다.
보안 이슈 없이 워크플로우만 검증했고, 같은 구조를 사내에 옮기면
저희 검사 업무에 즉시 활용 가능합니다.

지금 보시는 이미지는 산업 결함 공개 데이터셋(MVTec)의
○○ 결함입니다. 검사 시작 누르면..."

[검사 시작 클릭]

"보시는 것처럼 Claude가
1) 먼저 이미지를 정밀 분석해 결함 위치를 잡고
2) 그 결함에 대한 산업 표준·근본 원인을 웹에서 자동으로 조사하고
3) 마지막으로 임원 보고용 PPT를 자동 생성합니다.

이게 평소에 검사관 한 명이 30분~1시간 걸리는 작업입니다.
30초 만에 끝납니다."

[PPT 다운로드 → 슬라이드 보여주기]

"보안 이슈가 있는 사내 데이터는 폐쇄망 환경에 같은 워크플로우를
배포하면 됩니다. Claude는 SaaS 외에 AWS Bedrock, GCP Vertex,
온프레미스 등 다양한 배포 옵션을 지원합니다."
```

### 핵심 메시지 3가지
1. **"공개 데이터로 만들었지만 사내 워크플로우와 동일"**
2. **"30분 걸리던 보고서가 30초"**
3. **"주니어 1명이 ○일 만에 만든 결과물"**

## 7. 트러블슈팅

### "JSON 형식을 찾을 수 없습니다" 에러
- Claude가 가끔 JSON을 안 감싸고 출력. 같은 이미지로 한 번 더 시도.
- 또는 model을 Opus로 변경 (더 안정적)

### bbox가 부정확
- Vision 모델의 bbox는 추정치라 100% 정확하지 않음
- 정성적 위치 설명(location_desc)이 더 안정적
- 데모용으로는 큰 결함이 있는 이미지를 선택

### 검사 결과가 약함
- product_type을 더 구체적으로 (예: "PCB" → "산업용 PCB 솔더링 표면")
- inspection_focus를 명확히 (예: "솔더링 결함, 단선, 단락")

### API 비용 절약
- 데모 준비 시에는 sonnet으로 (3~5배 저렴)
- 실제 시연 때만 opus

## 8. 개선 아이디어 (시간 남으면)

- [ ] 여러 이미지 일괄 검사 모드
- [ ] 검사 통계 대시보드 (결함 유형별 분포)
- [ ] PPT 디자인을 회사 템플릿으로 변경
- [ ] 음성 입력으로 검사 항목 설정
- [ ] 슬랙/이메일로 보고서 자동 발송
