# Batch-50 검증 보고서

## 개요

- **다운로드**: Voxel51/mvtec-ad train split에서 stride 샘플링 50장
- **실제 사용 가능**: 41장 (나머지 9장은 ground-truth segmentation 마스크 → 스킵)
- **카테고리 수**: 14개 (MVTec AD 표준 13개 + 비표준 1개)
- **결과**: 41/41 PPT 렌더링 성공 ✅
- **결함 검출 분포**: HIGH 4건 · MEDIUM 7건 · LOW 2건 · NONE 28건

## 카테고리 분포 & 결함 통계

| 카테고리 | 표본 수 | 결함 검출 | 비고 |
|---|---:|---:|---|
| transistor | 2 | 1 (HIGH 1) | TO-220 리드 굽힘 |
| metal_nut | 2 | 1 (MEDIUM 1) | 표면 손상 |
| pill | 4 | 3 (HIGH 1, MEDIUM 2) | 인쇄 결함 + 반점 |
| zipper | 4 | 0 | 모두 정상 |
| tile | 2 | 1 (MEDIUM 1) | 어두운 패치 |
| hazelnut | 4 | 4 (MEDIUM 2, LOW 2) | 곰팡이/박리/변색 |
| wood | 2 | 0 | 모두 정상 |
| carpet | 3 | 1 (HIGH 1) | 검은 실/cut |
| leather | 3 | 0 | 모두 정상 |
| screw | 4 | 0 | 모두 정상 |
| toothbrush | 1 | 1 (HIGH 1) | 심한 오염 |
| bottle | 2 | 0 | 모두 정상 |
| grid | 3 | 0 | 모두 정상 |
| capsule | 3 | 0 | 모두 정상 |
| misc | 2 | 0 | 비MVTec 표본 |
| **합계** | **41** | **13 (32%)** | |

## 전체 결과 (각 행 = 1장의 PPT 보고서)

| # | 카테고리 | 심각도 | 결함 유형 | 보고서 |
|---:|---|:---:|---|---|
| 00 | transistor | NONE | — | [00_transistor](div_000_idx0000/검사보고서.pptx) |
| 01 | transistor | **HIGH** | 리드 굽힘 (중앙) | [01_transistor](div_001_idx0132/검사보고서.pptx) |
| 02 | metal_nut | NONE | — | [02_metal_nut](div_002_idx0264/검사보고서.pptx) |
| 03 | metal_nut | MEDIUM | 표면 손상/얼룩 | [03_metal_nut](div_003_idx0396/검사보고서.pptx) |
| 04 | pill | MEDIUM | 표면 반점 | [04_pill](div_004_idx0529/검사보고서.pptx) |
| 05 | pill | NONE | — | [05_pill](div_005_idx0661/검사보고서.pptx) |
| 06 | pill | MEDIUM | 표면 반점 | [06_pill](div_006_idx0793/검사보고서.pptx) |
| 07 | pill | **HIGH** | 인쇄 결함 (FF→FT) | [07_pill](div_007_idx0925/검사보고서.pptx) |
| 08 | zipper | NONE | — | [08_zipper](div_008_idx1058/검사보고서.pptx) |
| 09 | zipper | NONE | — | [09_zipper](div_009_idx1190/검사보고서.pptx) |
| 10 | zipper | NONE | — | [10_zipper](div_010_idx1322/검사보고서.pptx) |
| 11 | zipper | NONE | — | [11_zipper](div_011_idx1454/검사보고서.pptx) |
| 12 | tile | NONE | — | [12_tile](div_012_idx1587/검사보고서.pptx) |
| 13 | tile | MEDIUM | 어두운 패치 | [13_tile](div_013_idx1719/검사보고서.pptx) |
| 14 | hazelnut | MEDIUM | 외피 갈색 패치 | [14_hazelnut](div_014_idx1851/검사보고서.pptx) |
| 15 | hazelnut | LOW | 상단 외피 변색 | [15_hazelnut](div_015_idx1983/검사보고서.pptx) |
| 16 | hazelnut | MEDIUM | 외피 chip/박리 | [16_hazelnut](div_016_idx2116/검사보고서.pptx) |
| 17 | hazelnut | LOW | 외피 결정성 얼룩 | [17_hazelnut](div_017_idx2248/검사보고서.pptx) |
| 18 | wood | NONE | — | [18_wood](div_018_idx2380/검사보고서.pptx) |
| 19 | carpet | NONE | — | [19_carpet](div_019_idx2512/검사보고서.pptx) |
| 20 | carpet | NONE | — | [20_carpet](div_020_idx2645/검사보고서.pptx) |
| 21 | carpet | **HIGH** | 검은 실/cut | [21_carpet](div_021_idx2777/검사보고서.pptx) |
| 22 | misc | NONE | — | [22_misc](div_022_idx2909/검사보고서.pptx) |
| 23 | misc | NONE | — | [23_misc](div_023_idx3041/검사보고서.pptx) |
| 24 | leather | NONE | — | [24_leather](div_024_idx3174/검사보고서.pptx) |
| 25 | leather | NONE | — | [25_leather](div_025_idx3306/검사보고서.pptx) |
| 26 | wood | NONE | — | [26_wood](div_026_idx3438/검사보고서.pptx) |
| 27 | leather | NONE | — | [27_leather](div_027_idx3571/검사보고서.pptx) |
| 28 | screw | NONE | — | [28_screw](div_028_idx3703/검사보고서.pptx) |
| 29 | screw | NONE | — | [29_screw](div_029_idx3835/검사보고서.pptx) |
| 30 | screw | NONE | — | [30_screw](div_030_idx3967/검사보고서.pptx) |
| 31 | screw | NONE | — | [31_screw](div_031_idx4100/검사보고서.pptx) |
| 32 | toothbrush | **HIGH** | 심한 오염/사용흔 | [32_toothbrush](div_032_idx4232/검사보고서.pptx) |
| 33 | bottle | NONE | — | [33_bottle](div_033_idx4364/검사보고서.pptx) |
| 34 | bottle | NONE | — | [34_bottle](div_034_idx4496/검사보고서.pptx) |
| 35 | grid | NONE | — | [35_grid](div_035_idx4629/검사보고서.pptx) |
| 36 | grid | NONE | — | [36_grid](div_036_idx4761/검사보고서.pptx) |
| 37 | grid | NONE | — | [37_grid](div_037_idx4893/검사보고서.pptx) |
| 38 | capsule | NONE | — | [38_capsule](div_038_idx5025/검사보고서.pptx) |
| 39 | capsule | NONE | — | [39_capsule](div_039_idx5158/검사보고서.pptx) |
| 40 | capsule | NONE | — | [40_capsule](div_040_idx5290/검사보고서.pptx) |

## 검증 관점에서의 평가

### ✅ 통과한 항목
- **다중 카테고리 대응**: 14개 카테고리에 대해 동일 파이프라인이 일관되게 동작
- **결함/정상 양쪽 처리**: 결함 있을 때(13건)는 bbox+annotation 표시, 없을 때(28건)는 "결함 없음" 메시지로 자연스럽게 처리
- **심각도 차등**: HIGH/MEDIUM/LOW 색상 코드와 PPT 표지 메시지가 자동으로 차등 표시됨
- **PPT 일관성**: 모든 41개 보고서가 동일한 6슬라이드 구조(표지/요약/결함/원인/권고/출처)로 출력
- **카테고리별 research 공유**: 14개 research.json만으로 41개 보고서의 "근본 원인 분석"·"권고" 슬라이드를 채움 → 효율적

### ⚠️ 한계 / 개선 여지
- **이미지 분석은 Claude Code 세션 내 수동 진행** (자동화하려면 Anthropic API 필요 → 원래 `/inspect` 슬래시 커맨드는 대화형 1회 실행이 정상 사용 시나리오)
- **카테고리별 공유 research라 한 PPT의 권고가 그 표본에 100% 맞춤이 아님** — 실제 시연에서는 1장씩 `/inspect` 호출해서 표본 특화 research를 받는 게 더 정확
- **데이터셋이 train split에 GT 마스크를 섞어둠** — 다운로드 시 마지막 ~9장(인덱스 5500+)은 마스크 (이번 검증에서 자동 식별·스킵)
- **bbox는 시각 추정** — 정확도가 픽셀 단위는 아니지만 데모용으로는 충분
- **시연용으로 가장 좋은 표본 추천**:
  - `01_transistor` (TO-220 리드 굽힘, HIGH)
  - `07_pill` (인쇄 결함 FT, HIGH)
  - `21_carpet` (검은 실, HIGH)
  - `32_toothbrush` (심한 오염, HIGH)
  - `14_hazelnut` (곰팡이 의심, MEDIUM)

## 파일 구조

```
reports/batch-50/
├── _summary.md           ← 이 파일
├── _results.json         ← 41개 결과 raw 데이터 (machine-readable)
├── _research/            ← 14개 카테고리별 공유 research.json
│   ├── transistor.json
│   ├── metal_nut.json
│   ├── pill.json
│   ├── ... (13 more)
│   └── misc.json
└── div_XXX_idxYYYY/      ← 41개 표본별 폴더
    ├── input.png         ← 원본
    ├── annotated.png     ← AI 결함 영역 표시 (결함 있을 때)
    ├── analysis.json     ← 표본별 분석 결과
    └── 검사보고서.pptx   ← 최종 PPT (6슬라이드)
```

## 다음 단계 제안

- HIGH 심각도 5건의 PPT를 먼저 열어보고 디자인/내용 흐름 확인
- 시연 시 사용할 3~5장 골라서 별도 `images/demo/` 폴더로 복사
- 실제 사내 데이터로 전환 시: `/inspect <사내이미지>` 1장씩 실행 → 표본 특화 분석 가능
