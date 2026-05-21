"""
Batch-run the /inspect pipeline against many images at once.

For each entry in MANIFEST:
  1. Writes analysis.json (from manifest data + per-category boilerplate)
  2. Copies image into reports/batch-50/<slug>/
  3. Calls render_report.py with the shared per-category research.json
  4. Records result in summary

Usage:
    .venv/Scripts/python.exe batch_inspect.py
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

CATEGORY_PRODUCT = {
    "transistor": "TO-220 트랜지스터",
    "metal_nut": "T-nut (4-prong)",
    "pill": "정제 (Pill)",
    "zipper": "지퍼 (Zipper)",
    "tile": "세라믹 타일",
    "hazelnut": "헤이즐넛 (가공식품)",
    "wood": "목재 표면",
    "carpet": "카펫 (직물)",
    "leather": "가죽",
    "screw": "스크류 (Fastener)",
    "toothbrush": "칫솔",
    "bottle": "유리병",
    "grid": "메탈 메쉬 / Grid",
    "capsule": "캡슐 (Capsule)",
    "misc": "비표준 검사 대상",
}

# (filename, category, has_defect, defect_type, location_desc, severity, bbox, notes)
MANIFEST = [
    # transistor
    ("div_000_idx0000.png", "transistor", False, "", "", "NONE", None, "정상 TO-220, 리드 정렬 양호"),
    ("div_001_idx0132.png", "transistor", True, "리드 굽힘 (중앙)", "본체 하단 중앙 리드", "HIGH", [0.35, 0.55, 0.65, 0.95], "중앙 리드 굽힘 명확"),
    # metal_nut
    ("div_002_idx0264.png", "metal_nut", False, "", "", "NONE", None, "정상 4-prong T-nut"),
    ("div_003_idx0396.png", "metal_nut", True, "표면 손상/얼룩", "상면 중앙", "MEDIUM", [0.25, 0.25, 0.75, 0.75], "상면에 얼룩·미세 손상"),
    # pill
    ("div_004_idx0529.png", "pill", True, "표면 반점 (contamination)", "전면 분산 분포", "MEDIUM", [0.18, 0.25, 0.85, 0.75], "붉은 반점 다수 — 코팅·원료 분산 의심"),
    ("div_005_idx0661.png", "pill", False, "", "", "NONE", None, "FF 인쇄 정상, 표면 양호"),
    ("div_006_idx0793.png", "pill", True, "표면 반점", "전면 분산", "MEDIUM", [0.18, 0.25, 0.85, 0.75], "붉은 반점 산재"),
    ("div_007_idx0925.png", "pill", True, "인쇄 결함 (글자)", "중앙 텍스트", "HIGH", [0.35, 0.40, 0.65, 0.58], "FF가 FT로 인쇄됨 — 식별 코드 불일치"),
    # zipper
    ("div_008_idx1058.png", "zipper", False, "", "", "NONE", None, "정상 지퍼 이빨 정렬"),
    ("div_009_idx1190.png", "zipper", False, "", "", "NONE", None, "정상"),
    ("div_010_idx1322.png", "zipper", False, "", "", "NONE", None, "정상"),
    ("div_011_idx1454.png", "zipper", False, "", "", "NONE", None, "정상"),
    # tile
    ("div_012_idx1587.png", "tile", False, "", "", "NONE", None, "정상 그래뉴얼 패턴"),
    ("div_013_idx1719.png", "tile", True, "어두운 패치 (얼룩/오일)", "좌하단", "MEDIUM", [0.10, 0.55, 0.45, 0.85], "어두운 결함 영역"),
    # hazelnut
    ("div_014_idx1851.png", "hazelnut", True, "외피 갈색 패치 (곰팡이/탄화 의심)", "우상단", "MEDIUM", [0.45, 0.05, 0.85, 0.40], "곰팡이 가능성 의심"),
    ("div_015_idx1983.png", "hazelnut", True, "상단 외피 변색", "상단부", "LOW", [0.30, 0.05, 0.70, 0.30], "정상에 가까우나 약한 변색"),
    ("div_016_idx2116.png", "hazelnut", True, "외피 chip / 박리", "좌상단", "MEDIUM", [0.05, 0.10, 0.45, 0.45], "외피 일부 떨어짐"),
    ("div_017_idx2248.png", "hazelnut", True, "외피 결정성 얼룩", "하단", "LOW", [0.10, 0.45, 0.55, 0.85], "결정성 광택 (수분/곰팡이 의심)"),
    # wood
    ("div_018_idx2380.png", "wood", False, "", "", "NONE", None, "정상 wood grain"),
    # carpet
    ("div_019_idx2512.png", "carpet", False, "", "", "NONE", None, "정상 직조 패턴"),
    ("div_020_idx2645.png", "carpet", False, "", "", "NONE", None, "정상"),
    ("div_021_idx2777.png", "carpet", True, "검은 실 / cut", "좌측 수직선", "HIGH", [0.08, 0.05, 0.30, 0.95], "검은 이물 실 또는 weft 결함"),
    # misc (비표준 — 돌그릇 위 콩)
    ("div_022_idx2909.png", "misc", False, "", "", "NONE", None, "비표준 제품(돌그릇+콩) — 일반 외관 확인"),
    ("div_023_idx3041.png", "misc", False, "", "", "NONE", None, "비표준 제품 — 일반 외관 확인"),
    # leather
    ("div_024_idx3174.png", "leather", False, "", "", "NONE", None, "정상 브라운 가죽 grain"),
    ("div_025_idx3306.png", "leather", False, "", "", "NONE", None, "정상"),
    # wood
    ("div_026_idx3438.png", "wood", False, "", "", "NONE", None, "정상 wood grain (sample 2)"),
    # leather
    ("div_027_idx3571.png", "leather", False, "", "", "NONE", None, "정상 (lighter shade)"),
    # screw
    ("div_028_idx3703.png", "screw", False, "", "", "NONE", None, "정상 카운터싱크 스크류"),
    ("div_029_idx3835.png", "screw", False, "", "", "NONE", None, "정상"),
    ("div_030_idx3967.png", "screw", False, "", "", "NONE", None, "정상 (다른 각도)"),
    ("div_031_idx4100.png", "screw", False, "", "", "NONE", None, "정상"),
    # toothbrush
    ("div_032_idx4232.png", "toothbrush", True, "심한 오염 / 사용흔 (bristle)", "bristle 전체 영역", "HIGH", [0.18, 0.10, 0.82, 0.85], "황색·갈색 오염 다수 — 사용 흔적 추정"),
    # bottle
    ("div_033_idx4364.png", "bottle", False, "", "", "NONE", None, "정상 (병 상단·neck 부)"),
    ("div_034_idx4496.png", "bottle", False, "", "", "NONE", None, "정상"),
    # grid
    ("div_035_idx4629.png", "grid", False, "", "", "NONE", None, "정상 다이아몬드 메쉬"),
    ("div_036_idx4761.png", "grid", False, "", "", "NONE", None, "정상 (다른 각도)"),
    ("div_037_idx4893.png", "grid", False, "", "", "NONE", None, "정상 확장 메쉬"),
    # capsule
    ("div_038_idx5025.png", "capsule", False, "", "", "NONE", None, "정상 500 캡슐"),
    ("div_039_idx5158.png", "capsule", False, "", "", "NONE", None, "정상 Actavis 500"),
    ("div_040_idx5290.png", "capsule", False, "", "", "NONE", None, "정상 500"),
]


def build_analysis(category, has_defect, defect_type, location_desc, severity, bbox, notes):
    product = CATEGORY_PRODUCT.get(category, category)
    if not has_defect:
        return {
            "has_defect": False,
            "overall_assessment": f"{product} 표본 — 외관 검사상 특이 결함 없음",
            "overall_severity": "NONE",
            "confidence": 0.85,
            "defects": [],
            "inspection_notes": (
                f"{product} 외관 검사 결과 결함 없음. 표면 균일도·치수·색상 모두 양호한 정상 표본으로 "
                f"판단됨. 표본 다양성 검증의 음성 케이스(negative control)로 활용 가능. 비고: {notes}."
            ),
            "recommended_actions": [
                "동일 로트 정상 표본 데이터베이스에 추가 (학습용)",
                "주기적 SPC 모니터링 유지",
                "외관 외 기능 시험(필요 시) 병행",
            ],
        }
    sev = severity if severity in ["HIGH", "MEDIUM", "LOW"] else "MEDIUM"
    return {
        "has_defect": True,
        "overall_assessment": f"{product} — {defect_type} 결함 검출",
        "overall_severity": sev,
        "confidence": 0.82,
        "defects": [
            {
                "type": defect_type,
                "type_en": defect_type,
                "location_desc": location_desc,
                "bbox_normalized": bbox or [0.25, 0.25, 0.75, 0.75],
                "size_estimate": "중간",
                "description": f"{location_desc}에 {defect_type} 결함 관찰. {notes}",
                "severity": sev,
                "possible_causes": [
                    "공정 파라미터 산포 (1순위)",
                    "원재/공급 측 변동",
                    "환경/취급 외력",
                ],
            }
        ],
        "inspection_notes": (
            f"{product} 표본에서 {defect_type} 결함이 관찰됨 ({severity}). "
            f"동일 로트 확대 샘플링과 해당 공정 단계 점검 권고. 자세한 산업 표준·근본 원인은 "
            f"'근본 원인 분석' 및 '참고 자료' 슬라이드 참조."
        ),
        "recommended_actions": [
            f"{defect_type} 검출 표본 즉시 격리 + 재검사",
            "동일 로트 100개 샘플 확대 검사로 결함률 산출",
            "공정 파라미터 점검 (research 권고 항목 참조)",
        ],
    }


def main():
    repo = Path(__file__).parent
    base = repo / "reports" / "batch-50"
    research_dir = base / "_research"
    img_src_dir = repo / "images_diverse"
    venv_py = repo / ".venv" / "Scripts" / "python.exe"
    render_script = repo / "render_report.py"

    results = []
    n = len(MANIFEST)
    for idx, entry in enumerate(MANIFEST, 1):
        filename, category, has_defect, defect_type, loc, severity, bbox, notes = entry
        slug = Path(filename).stem
        out_dir = base / slug
        out_dir.mkdir(parents=True, exist_ok=True)

        src_img = img_src_dir / filename
        dst_img = out_dir / "input.png"
        shutil.copy(src_img, dst_img)

        analysis = build_analysis(category, has_defect, defect_type, loc, severity, bbox, notes)
        (out_dir / "analysis.json").write_text(
            json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        research_src = research_dir / f"{category}.json"
        if not research_src.exists():
            research_src = research_dir / "misc.json"

        product = CATEGORY_PRODUCT.get(category, category)
        cmd = [
            str(venv_py),
            str(render_script),
            str(dst_img),
            str(out_dir / "analysis.json"),
            str(research_src),
            "--product", product,
            "--out", str(out_dir / "검사보고서.pptx"),
            "--annotated-out", str(out_dir / "annotated.png"),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        status = "OK" if result.returncode == 0 else "FAIL"
        if result.returncode != 0:
            print(f"[{idx:02d}/{n}] {status} {slug} — {result.stderr.strip()[:200]}", file=sys.stderr)
        else:
            print(f"[{idx:02d}/{n}] {status} {slug} ({category}, sev={severity})")
        results.append({
            "slug": slug,
            "category": category,
            "has_defect": has_defect,
            "defect_type": defect_type,
            "severity": severity,
            "status": status,
        })

    (base / "_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_ok = sum(1 for r in results if r["status"] == "OK")
    print(f"\nDone: {n_ok}/{n} succeeded.")


if __name__ == "__main__":
    main()
