#!/usr/bin/env python3
"""Schema check: metaschema, examples valid, spec-forbidden docs rejected (adversarial-review 1.2, H-06, C-02).

Run: python3 tools/check_schemas.py   (needs jsonschema, pyyaml). Exit 1 on any failure.
Own docs: python3 tools/check_schemas.py <schema> FILE...   e.g. capability-map my-map.yaml (YAML or JSON, multi-doc ok)
"""
import copy, json, pathlib, sys
import yaml
from jsonschema import Draft202012Validator, FormatChecker

R = pathlib.Path(__file__).resolve().parent.parent
V = {}
for p in sorted((R / "schemas").glob("*.json")):
    s = json.loads(p.read_text())
    Draft202012Validator.check_schema(s)
    V[p.name.split(".")[0]] = Draft202012Validator(s, format_checker=FormatChecker())
MAX_BYTES, MAX_MSG = 1 << 20, 300  # 설계 제안값: 외부 문서 1 MiB, 오류 한 줄 300자
safe = lambda s: repr(str(s))[1:-1][:MAX_MSG]  # 제어 문자·개행 이스케이프 (터미널·CI 주석 주입 방지)
assert safe("a\x1b[2K\r\n::error::") == "a\\x1b[2K\\r\\n::error::"

class NoAliasLoader(yaml.SafeLoader):  # ponytail: 별칭 전면 거부. 명세 문서는 앵커가 필요 없다 (alias bomb 방지)
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise yaml.YAMLError("YAML alias(*ref) is not allowed")
        return super().compose_node(parent, index)

if len(sys.argv) > 1:  # validate the caller's own documents, skip the self-test
    sc, files = sys.argv[1], sys.argv[2:]
    if sc not in V or not files:
        sys.exit(f"usage: check_schemas.py <{'|'.join(V)}> FILE...")
    bad = 0
    for f in files:
        try:
            raw = pathlib.Path(f).read_bytes()
            if len(raw) > MAX_BYTES:
                raise ValueError(f"file larger than {MAX_BYTES} bytes")
            docs = list(yaml.load_all(raw.decode("utf-8"), Loader=NoAliasLoader))
        except (OSError, ValueError, yaml.YAMLError) as e:
            print(f"FAIL {safe(f)}\n  {safe(e)}"); bad += 1; continue
        for i, d in enumerate(docs):
            try:
                errs = sorted(V[sc].iter_errors(d), key=lambda e: str(e.json_path))
                lines = [f"{safe(e.json_path)}: {safe(e.message)}" for e in errs[:5]]
            except Exception as e:  # 비문자열 키 등: 이 문서만 실패로 보고하고 다음 파일을 계속 본다
                errs, lines = [e], [f"validator error: {safe(type(e).__name__)}: {safe(e)}"]
            print(f"{'OK  ' if not errs else 'FAIL'} {safe(f)}[{i}]", *lines, sep="\n  ")
            bad += bool(errs)
    sys.exit(1 if bad else 0)
load = lambda n: list(yaml.safe_load_all((R / "examples" / n).read_text(encoding="utf-8")))
EX = {"capability-map": "capability-map.example.yaml", "change-record": "change.example.yaml",
      "extension-manifest": "extension-manifest.example.yaml", "lexicon-pack": "lexicon.ko.yaml",
      "policy": "policy.example.yaml"}
fail = 0
for sc, f in EX.items():
    for i, d in enumerate(load(f)):
        errs = [e.message for e in V[sc].iter_errors(d)]
        print(f"{'OK  ' if not errs else 'FAIL'} example {f}[{i}]", *errs[:3], sep="\n  " if errs else "")
        fail += bool(errs)

C, M, P = load(EX["change-record"]), load(EX["extension-manifest"])[0], load(EX["policy"])
def mk(src, fn):
    d = copy.deepcopy(src); fn(d); return d
def set_(path, v):
    def f(d):
        *h, k = path
        for x in h: d = d[x]
        d[k] = v
    return f
def pop(*paths):
    def f(d):
        for path in paths:
            t = d
            for x in path[:-1]: t = t[x]
            t.pop(path[-1])
    return f
def both(*fs):
    return lambda d: [f(d) for f in fs]

# (name, schema, doc, expected_rejected). False = not expressible in JSON Schema; validator MUST check.
CASES = [
    ("D4 + permissions_delta.add, no G5, no approved_by (I4)", "change-record",
     mk(C[1], pop(("validation", "gates", "G5"), ("provenance", "approved_by"))), True),
    ("judge_instance == generator_instance (I7)", "change-record",
     mk(C[0], set_(("provenance", "judge_instance"), C[0]["provenance"]["generator_instance"])), False),
    ("G4 pass but no judge_instance (I7)", "change-record", mk(C[0], pop(("provenance", "judge_instance"))), True),
    ("contract = single judge item, deterministic defaulted (2.5)", "change-record",
     mk(C[0], set_(("contract",), [{"id": "looks-ok", "check": "judge", "expect": "보기 좋다"}])), True),
    ("D5 record with only G0 (5.8)", "change-record",
     mk(C[0], both(set_(("depth",), "D5"), set_(("validation", "gates"), {"G0": "pass"}))), True),
    ("points with invalid id", "change-record", mk(C[0], set_(("points",), ["NOT A POINT!!"])), True),
    ("intent = 4 spaces (I9)", "change-record", mk(C[0], set_(("intent",), "    ")), True),
    ("provenance.at = 'yesterday'", "change-record", mk(C[0], set_(("provenance", "at"), "yesterday")), True),
    ("manifest D3 + form native (2.6)", "extension-manifest", mk(M, set_(("artifact", "form"), "native")), True),
    ("manifest D3 + form sandboxed (2.6, L3)", "extension-manifest",
     mk(M, both(set_(("artifact", "form"), "sandboxed"), set_(("state",), {"schema_version": 1}))), True),
    ("manifest D4 + native (2.6)", "extension-manifest",
     mk(M, both(set_(("depth",), "D4"), set_(("artifact", "form"), "native"))), True),
    ("network allow '*' with no egress capability", "extension-manifest",
     mk(M, both(set_(("network",), {"allow": ["*"]}), set_(("permissions",), []))), True),
    ("contract = prose-only deterministic item, no executable form (2.5)", "change-record",
     mk(C[0], set_(("contract",), [{"id": "prose", "check": "tree-query", "expect": "목록 2건"}])), True),
    ("network allow IP literal 169.254.169.254 (7.11)", "extension-manifest",
     mk(M, set_(("network",), {"allow": ["169.254.169.254"]})), True),
    ("network allow host but permissions lack egress capability (I4, cross-document)", "extension-manifest",
     mk(M, set_(("network",), {"allow": ["hooks.slack.com"]})), False),
    ("network allow public-suffix wildcard *.co.uk (cross-document, PSL)", "extension-manifest",
     mk(M, both(set_(("network",), {"allow": ["*.co.uk"]}), set_(("permissions",), ["net.slack.post"]))), False),
    ("D4 sandboxed with no state (5.9)", "extension-manifest",
     mk(M, both(set_(("depth",), "D4"), set_(("artifact", "form"), "sandboxed"), pop(("state",)))), True),
    ("depth ceiling D9 / default banana", "policy",
     mk(P[1], set_(("policy", "knobs", "depth"), {"ceiling": "D9", "default": "banana"})), True),
    ("org depth ceiling D5 > tenant D3 (I5, cross-document)", "policy",
     mk(P[2], set_(("policy", "knobs", "depth"), {"ceiling": "D5"})), False),
    ("default outside ceiling", "policy",
     mk(P[1], set_(("policy", "knobs", "depth"), {"ceiling": "D2", "default": "D4"})), True),
    ("capabilities default outside ceiling (setKnob, validator MUST)", "policy",
     mk(P[1], set_(("policy", "knobs", "capabilities"), {"ceiling": ["tasks.read"], "default": ["net.slack.post"]})), False),
    ("floors missing 6 of 7", "policy", mk(P[1], set_(("policy", "floors"), ["rollback"] * 7)), True),
]
for name, sc, doc, want in CASES:
    got = any(True for _ in V[sc].iter_errors(doc))
    ok = got == want
    fail += not ok
    tag = "rejected" if got else ("ACCEPTED (validator MUST check)" if not want else "ACCEPTED")
    print(f"{'OK  ' if ok else 'FAIL'} forbidden {tag} :: {name}")
print("FAILED" if fail else "ALL OK", f"({fail} failure(s))")
sys.exit(1 if fail else 0)
