#!/usr/bin/env python3
"""Mallangable-AI 설계 공간 계산기 (Design Space Calculator)

설계 축(axis) 11개의 모든 조합을 나열하고 제약 3종으로 걸러 냅니다.
  - L (logical)   : 논리·계약상 성립할 수 없는 조합, 또는 같은 의미의 중복 표현(정규화)
  - N (normative) : 성립은 하지만 Mallangable-AI 규범(안전 원칙)이 금지하는 조합
  - S (soft)      : 허용하되 권장하지 않는 조합(경고)

사용법:
  python3 tools/design_space.py            # 요약(JSON)
  python3 tools/design_space.py --markdown # 문서용 표
  python3 tools/design_space.py --check P1  # 레퍼런스 프로파일 검사
  python3 tools/design_space.py --profile '{"A1":"D3", ...}'  # 임의 조합 검사
  python3 tools/design_space.py --profile my-profile.json     # 파일로 검사(설계 리뷰·ADR에 커밋)

축이나 제약을 바꿔 자기 제품의 설계 공간을 다시 계산하는 용도로 쓰세요.
표준 라이브러리만 사용합니다.
"""
import argparse
import collections
import itertools
import json
import os
import sys

AXES = collections.OrderedDict([
    ("A1", ("최대 변경 깊이", ["D1", "D2", "D3", "D4", "D5"])),
    ("A2", ("산출물 표현", ["decl", "sandboxed", "native"])),
    ("A3", ("에이전트 위치", ["client", "server", "hybrid"])),
    ("A4", ("실행 격리", ["none", "lang", "frame", "proc"])),
    ("A5", ("코드 가시성", ["open", "own", "hidden"])),
    ("A6", ("버전 토폴로지", ["snapshot", "fork", "lineage", "crdt"])),
    ("A7", ("기준판 전파", ["none", "manual", "proposed", "auto"])),
    ("A8", ("공유 범위", ["none", "tenant", "public"])),
    ("A9", ("모델 조달", ["sub", "byok", "credits", "tenant_cloud", "on_device"])),
    ("A10", ("관리 가시성", ["none", "V0", "V1", "V2", "V3"])),
    ("A11", ("활성화 방식", ["live", "preview", "gated"])),
])
STRUCTURAL = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]
ECONOMIC = ["A9", "A10", "A11"]
DEPTH_RANK = {"D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5}


# 논리 제약. 순서가 '첫 위반' 집계를 정하므로 바꾸지 말 것(--independent는 순서와 무관).
LOGICAL_RULES = [
    ("L1", lambda c: c["A5"] == "hidden" and c["A3"] != "server"),  # 코드를 만지는 에이전트가 사용자 쪽에 있으면 코드를 숨길 수 없다
    ("L2", lambda c: c["A9"] in ("sub", "on_device") and c["A3"] == "server"),  # 개인 구독·기기 모델은 서버 작업에 쓸 수 없다(약관·물리적 위치)
    ("L3", lambda c: c["A1"] in ("D1", "D2", "D3") and c["A2"] != "decl"),  # 2.6: D1~D3은 선언형. 코드 산출물이면 D4 이상
    ("L4", lambda c: (c["A1"] == "D4" and c["A2"] != "sandboxed")  # 2.6: D4는 샌드박스 코드
                     or (c["A1"] == "D5" and c["A2"] != "native")),  # 코어 변경은 네이티브 코드 수정이다
    ("L5", lambda c: c["A2"] == "decl" and c["A4"] != "none"),  # 정규화: 실행 코드가 없으면 실행 격리 축은 의미가 없다
    ("L6", lambda c: c["A2"] == "sandboxed" and c["A4"] == "none"),  # 샌드박스 산출물은 샌드박스가 있어야 한다
    ("L7", lambda c: c["A2"] == "native" and c["A4"] in ("lang", "frame")),  # 네이티브 코드는 언어·프레임 격리 안에서 '호스트 권한'을 가질 수 없다
    ("L8", lambda c: c["A6"] == "snapshot" and c["A7"] != "none"),  # 기준판과의 관계를 추적하지 않으면 전파할 대상이 없다
    ("L9", lambda c: c["A6"] == "crdt" and c["A7"] == "manual"),  # CRDT는 자동 병합이므로 수동 병합 단계가 없다
    ("L10", lambda c: c["A5"] == "own" and c["A6"] not in ("fork", "lineage")),  # '내 것만 보기'는 레이어가 분리된 토폴로지에서만 성립
    ("L11", lambda c: c["A5"] == "hidden" and c["A6"] == "crdt"),  # CRDT 복제본은 클라이언트에 있으므로 코드를 숨길 수 없다
]


def logical_all(c):
    return [r for r, f in LOGICAL_RULES if f(c)]


def logical(c):
    """논리 제약. 위반한 첫 규칙 id를 돌려준다(없으면 None)."""
    return next((r for r, f in LOGICAL_RULES if f(c)), None)


def normative(c):
    """규범 제약(Mallangable-AI 안전 원칙)."""
    code = c["A2"] != "decl"
    if code and c["A8"] == "public" and c["A4"] not in ("frame", "proc"):
        return "N1"  # 공개 공유되는 실행 코드는 프레임·프로세스 격리 필수
    if c["A2"] == "native" and c["A8"] != "none" and c["A4"] != "proc":
        return "N2"  # 공유되는 네이티브 코드는 별도 프로세스 필수
    if c["A9"] == "credits" and c["A10"] == "none":
        return "N3"  # 재판매 과금은 계량(최소 V0)이 필요
    if c["A8"] == "public" and c["A10"] == "none":
        return "N4"  # 공개 마켓은 감사 추적이 필요
    if DEPTH_RANK[c["A1"]] >= 4 and c["A11"] == "live":
        return "N5"  # 동작·코어 변경은 미리보기·승인 없이 즉시 활성화 금지
    if c["A1"] == "D5" and (c["A8"] != "none" or c["A6"] == "snapshot"):
        return "N6"  # D5는 사용자 레이어가 아닌 코어 포크(I1, 2.6): 공유 금지, 기준판 추적 필수
    return None


def soft(c):
    """권장하지 않는 조합(경고 목록)."""
    w = []
    code = c["A2"] != "decl"
    if code and c["A8"] == "public" and c["A11"] == "live":
        w.append("S1")  # 공개 공유 코드의 즉시 설치
    if c["A2"] == "native" and c["A4"] == "none":
        w.append("S2")  # 격리 없는 네이티브 코드(개인용 한정 권장)
    if c["A6"] == "lineage" and c["A7"] in ("none", "manual"):
        w.append("S3")  # 계보는 있는데 전파 보조가 없음 → 드리프트 누적
    if c["A1"] == "D5" and c["A6"] in ("fork", "lineage"):
        w.append("S4")  # 사용자별 코어 포크 → 병합 비용 폭증
    if c["A3"] == "hybrid" and c["A9"] == "sub":
        w.append("S5")  # 서버 단계에서 LLM 불가 → 의미 충돌은 클라이언트로 환송
    if c["A9"] == "on_device" and DEPTH_RANK[c["A1"]] >= 4:
        w.append("S6")  # 기기 모델로 동작 코드 생성 → 실패율 상승
    if c["A6"] == "crdt" and DEPTH_RANK[c["A1"]] >= 4:
        w.append("S7")  # 실시간 동기 문서에서 실행 코드 동시 편집
    return w


PROFILES = {
    "P1": ("개인 공방형", {"A1": "D4", "A2": "sandboxed", "A3": "client", "A4": "frame", "A5": "open",
                         "A6": "fork", "A7": "proposed", "A8": "none", "A9": "sub", "A10": "none", "A11": "preview"}),
    "P2": ("팀 큐레이션형", {"A1": "D3", "A2": "decl", "A3": "hybrid", "A4": "none", "A5": "own",
                          "A6": "lineage", "A7": "proposed", "A8": "tenant", "A9": "byok", "A10": "V2", "A11": "preview"}),
    "P3": ("기업 기밀형", {"A1": "D4", "A2": "sandboxed", "A3": "server", "A4": "proc", "A5": "hidden",
                         "A6": "lineage", "A7": "proposed", "A8": "tenant", "A9": "tenant_cloud", "A10": "V2", "A11": "gated"}),
    "P4": ("대중 소비자형", {"A1": "D2", "A2": "decl", "A3": "server", "A4": "none", "A5": "open",
                          "A6": "snapshot", "A7": "none", "A8": "public", "A9": "credits", "A10": "V1", "A11": "live"}),
    "P5": ("로컬 퍼스트 협업형", {"A1": "D3", "A2": "decl", "A3": "client", "A4": "none", "A5": "open",
                              "A6": "crdt", "A7": "auto", "A8": "tenant", "A9": "byok", "A10": "none", "A11": "preview"}),
    "P6": ("마켓 플랫폼형", {"A1": "D4", "A2": "sandboxed", "A3": "hybrid", "A4": "frame", "A5": "own",
                          "A6": "lineage", "A7": "proposed", "A8": "public", "A9": "credits", "A10": "V1", "A11": "gated"}),
    "P7": ("폐쇄망 공공형", {"A1": "D3", "A2": "decl", "A3": "server", "A4": "none", "A5": "hidden",
                          "A6": "lineage", "A7": "proposed", "A8": "tenant", "A9": "tenant_cloud", "A10": "V3", "A11": "gated"}),
}


# 비즈니스 모델(BM) 결합 판정.  ●=그대로 가능, ◐=조건부(운영 방식·외부 계약 필요), ○=구조상 불가
F, C, X = "●", "◐", "○"
GOV_RICH = ("V1", "V2", "V3")
PROPAGATES = ("proposed", "auto")
BMS = collections.OrderedDict([
    ("B1", ("라이선스 판매", lambda c: F)),
    ("B2", ("좌석 구독", lambda c: F)),
    ("B3", ("추론 크레딧 마진", lambda c: F if c["A9"] == "credits" else X)),
    ("B4", ("BYOK 플랫폼 요금", lambda c: (F if c["A3"] != "client" else C) if c["A9"] in ("byok", "tenant_cloud") else X)),
    ("B5", ("공유 마켓 수수료", lambda c: F if c["A8"] == "public" else (C if c["A8"] == "tenant" else X))),
    ("B6", ("거버넌스 애드온", lambda c: F if c["A10"] in GOV_RICH else (C if c["A10"] == "V0" else X))),
    ("B7", ("기밀 실행 프리미엄", lambda c: F if (c["A3"] == "server" and c["A5"] == "hidden") else (C if c["A3"] == "server" else X))),
    ("B8", ("기준판 지원 계약", lambda c: (F if c["A6"] == "lineage" else (C if c["A6"] == "fork" else X)) if c["A7"] in PROPAGATES else X)),
    ("B9", ("업그레이드 생존 보증", lambda c: F if (c["A6"] in ("fork", "lineage") and c["A7"] in PROPAGATES) else X)),
    ("B10", ("승격 분배", lambda c: (F if (c["A8"] != "none" and c["A10"] in GOV_RICH) else C) if c["A6"] == "lineage" else X)),
    ("B11", ("동네 개발자 연결", lambda c: F if (c["A5"] != "hidden" and c["A8"] != "none") else C)),
    ("B12", ("수요 신호 리포트", lambda c: F if c["A10"] != "none" else X)),
    ("B13", ("용어·도메인 팩", lambda c: F)),
    ("B14", ("모델 공급사 제휴", lambda c: X if c["A9"] == "on_device" else C)),
    ("B15", ("품질 등급 차등", lambda c: F if c["A9"] == "credits" else (C if (c["A9"] in ("byok", "tenant_cloud") and c["A3"] != "client") else X))),
    ("B16", ("성과 단위 과금", lambda c: X if c["A10"] == "none" else (F if c["A9"] == "credits" else (C if c["A9"] in ("byok", "tenant_cloud") else X)))),
    ("B17", ("런타임 OEM 라이선스", lambda c: F)),
    ("B18", ("해결 레시피 구독", lambda c: F if (c["A6"] in ("fork", "lineage") and c["A7"] in PROPAGATES) else X)),
    ("B19", ("기능의 제품화 분배", lambda c: F if c["A8"] == "public" else (C if c["A8"] == "tenant" else X))),
    ("B20", ("후원 기본값 슬롯", lambda c: C if c["A8"] == "public" else X)),
])


def bm_row(c):
    return {b: fn(c) for b, (_, fn) in BMS.items()}


def bm_markdown():
    lines = ["| BM | 이름 | " + " | ".join(PROFILES) + " |",
             "| --- | --- | " + " | ".join(":-:" for _ in PROFILES) + " |"]
    rows = {p: bm_row(PROFILES[p][1]) for p in PROFILES}
    for b, (name, _) in BMS.items():
        lines.append(f"| {b} | {name} | " + " | ".join(rows[p][b] for p in PROFILES) + " |")
    return "\n".join(lines)


def bm_stats():
    """권장 조합 전체에서 각 BM이 가능한(●) / 조건부(◐) 비율."""
    keys = list(AXES)
    tot = 0
    cnt = {b: collections.Counter() for b in BMS}
    for combo in itertools.product(*[AXES[k][1] for k in keys]):
        c = dict(zip(keys, combo))
        if classify(c)[0] != "clean":
            continue
        tot += 1
        for b, v in bm_row(c).items():
            cnt[b][v] += 1
    lines = ["| BM | 이름 | ● 가능 | ◐ 조건부 | ○ 불가 |", "| --- | --- | ---: | ---: | ---: |"]
    for b, (name, _) in BMS.items():
        f = cnt[b]
        lines.append(f"| {b} | {name} | {f[F] / tot * 100:.1f}% | {f[C] / tot * 100:.1f}% | {f[X] / tot * 100:.1f}% |")
    return "\n".join(lines)


def classify(c):
    l = logical(c)
    if l:
        return "logical", l, []
    n = normative(c)
    if n:
        return "normative", n, []
    w = soft(c)
    return ("warned" if w else "clean"), None, w


def enumerate_space():
    keys = list(AXES)
    stats = {
        "raw": 0, "logical_ok": 0, "normative_ok": 0, "clean": 0,
        "logical_reason": collections.Counter(), "normative_reason": collections.Counter(),
        "logical_independent": collections.Counter(), "logical_unique": collections.Counter(),
        "soft_hits": collections.Counter(),
        "clean_marginals": {k: collections.Counter() for k in keys},
    }
    families = collections.defaultdict(int)  # 구조 조합 -> 깨끗한 경제·정책 완성 수
    for combo in itertools.product(*[AXES[k][1] for k in keys]):
        stats["raw"] += 1
        c = dict(zip(keys, combo))
        hits = logical_all(c)
        stats["logical_independent"].update(hits)
        if len(hits) == 1:
            stats["logical_unique"][hits[0]] += 1
        kind, rule, warns = classify(c)
        if kind == "logical":
            stats["logical_reason"][rule] += 1
            continue
        stats["logical_ok"] += 1
        if kind == "normative":
            stats["normative_reason"][rule] += 1
            continue
        stats["normative_ok"] += 1
        for w in warns:
            stats["soft_hits"][w] += 1
        if kind == "clean":
            stats["clean"] += 1
            for k in keys:
                stats["clean_marginals"][k][c[k]] += 1
            families[tuple(c[k] for k in STRUCTURAL)] += 1
    full = 1
    for k in ECONOMIC:
        full *= len(AXES[k][1])
    dist = collections.Counter(families.values())
    stats["structural_families"] = len(families)
    stats["economic_full"] = full
    stats["completion_distribution"] = dict(sorted(dist.items(), reverse=True))
    stats["mean_completion"] = round(sum(families.values()) / max(1, len(families)), 2)
    return stats


def as_jsonable(stats):
    out = {}
    for k, v in stats.items():
        if isinstance(v, collections.Counter):
            out[k] = dict(sorted(v.items()))
        elif isinstance(v, dict) and v and isinstance(next(iter(v.values())), collections.Counter):
            out[k] = {kk: dict(vv) for kk, vv in v.items()}
        else:
            out[k] = v
    return out


def markdown(stats):
    raw = stats["raw"]
    pct = lambda x: f"{x / raw * 100:.2f}%"
    lines = []
    lines.append("| 단계 | 조합 수 | 전체 대비 |")
    lines.append("| --- | ---: | ---: |")
    lines.append(f"| 원시 조합 Ω | {raw:,} | 100% |")
    lines.append(f"| 논리 정합 (L 통과) | {stats['logical_ok']:,} | {pct(stats['logical_ok'])} |")
    lines.append(f"| 규범 정합 (L+N 통과) | {stats['normative_ok']:,} | {pct(stats['normative_ok'])} |")
    lines.append(f"| 권장 (경고 없음) | {stats['clean']:,} | {pct(stats['clean'])} |")
    lines.append("")
    lines.append(f"- 권장 조합의 구조 패밀리(A1~A8) 수: {stats['structural_families']:,}")
    lines.append(f"- 패밀리당 경제·정책 완성(A9~A11) 평균: {stats['mean_completion']} / {stats['economic_full']}")
    lines.append(f"- 완성 수 분포(완성 수: 패밀리 수): {stats['completion_distribution']}")
    lines.append("")
    lines.append("| 논리 위반 규칙 | 첫 위반 | 독립 위반 | 유일 위반 |")
    lines.append("| --- | ---: | ---: | ---: |")
    for r, n in sorted(stats["logical_independent"].items(), key=lambda x: -x[1]):
        lines.append(f"| {r} | {stats['logical_reason'][r]:,} | {n:,} | {stats['logical_unique'][r]:,} |")
    lines.append("")
    lines.append("| 규범 위반 규칙 | 걸러진 조합 |")
    lines.append("| --- | ---: |")
    for r, n in sorted(stats["normative_reason"].items(), key=lambda x: -x[1]):
        lines.append(f"| {r} | {n:,} |")
    lines.append("")
    lines.append("| 경고 규칙 | 해당 조합(규범 정합 중) |")
    lines.append("| --- | ---: |")
    for r, n in sorted(stats["soft_hits"].items(), key=lambda x: -x[1]):
        lines.append(f"| {r} | {n:,} |")
    lines.append("")
    lines.append("| 축 | 권장 조합에서 각 옵션의 등장 횟수 |")
    lines.append("| --- | --- |")
    for k, (name, opts) in AXES.items():
        m = stats["clean_marginals"][k]
        lines.append(f"| {k} {name} | " + ", ".join(f"{o} {m.get(o, 0):,}" for o in opts) + " |")
    return "\n".join(lines)


def check(c):
    unknown = [k for k in c if k not in AXES]
    if unknown:
        return {"error": f"알 수 없는 축: {unknown}"}
    missing = [k for k in AXES if k not in c]
    if missing:
        return {"error": f"누락된 축: {missing}"}
    bad = [k for k in AXES if c[k] not in AXES[k][1]]
    if bad:
        return {"error": f"허용되지 않은 옵션: {[(k, c[k]) for k in bad]}"}
    kind, rule, warns = classify(c)
    return {"result": kind, "violated": rule, "warnings": warns}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--check", help="레퍼런스 프로파일 id (P1~P7) 또는 all")
    ap.add_argument("--profile", help="JSON 문자열 또는 JSON 파일 경로로 임의 조합 검사")
    ap.add_argument("--bm", action="store_true", help="레퍼런스 프로파일 × BM 결합 행렬")
    ap.add_argument("--bm-stats", action="store_true", help="권장 조합 전체에서 BM별 가능 비율")
    a = ap.parse_args()
    if a.bm:
        print(bm_markdown())
        return
    if a.bm_stats:
        print(bm_stats())
        return
    if a.check:
        ids = list(PROFILES) if a.check == "all" else [a.check]
        if not set(ids) <= set(PROFILES):
            sys.exit(f"알 수 없는 프로파일: {a.check} (P1~P7 또는 all)")
        print(json.dumps({i: {"name": PROFILES[i][0], **check(PROFILES[i][1])} for i in ids},
                         ensure_ascii=False, indent=1))
        return
    if a.profile:
        try:
            if os.path.isfile(a.profile):
                with open(a.profile, encoding="utf-8") as fh:
                    prof = json.load(fh)
            else:
                prof = json.loads(a.profile)
        except json.JSONDecodeError as e:
            sys.exit(f"--profile JSON 오류: {e}")
        out = check(prof)
        if "error" not in out and out["result"] in ("clean", "warned"):
            out["business_models"] = {f"{b} {BMS[b][0]}": v for b, v in bm_row(prof).items()}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    stats = enumerate_space()
    print(markdown(stats) if a.markdown else json.dumps(as_jsonable(stats), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
