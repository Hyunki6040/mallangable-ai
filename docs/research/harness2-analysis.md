# 조사 노트 — Harness² (google-research/harness2)

> 이 노트의 결론: Harness²는 **하네스 자체를 과제마다 고쳐 쓰는 연구 프레임워크**다. Mallangable의 하네스(5.6)는 에이전트를 감싸 *강제*하는 외피이므로 방향이 다르다. 그대로 가져올 것은 세 가지다. 첫째, **채점 정보가 방법(method) 쪽 맥락에 절대 들어가지 않게 하는 격리 장치**. 둘째, **채점 실패를 0점이 아니라 미채점으로 다루는 보고 규칙**. 셋째, **후보 출처를 숨긴 판정**. 모두 Mallang-Bench(10.2)와 G4(5.8)를 보강한다. 반대로 에이전트가 정책 훅·가드레일까지 고치게 하는 자기 편집은 받아들이지 않는다.

- 확인일: 2026-10-30
- 조사 대상: https://github.com/google-research/harness2 (공개 저장소, 존재 확인)
- 고정 커밋: `1cfe254e8d25b15f37048c3730134686abe60335` (2026-10-13). 아래 모든 소스 링크는 이 커밋 기준입니다.
- 방법: `git clone --depth 1`로 빈 임시 디렉터리에 받아 **읽기만** 했습니다(코드 실행 없음). 논문은 arXiv 초록 페이지와 HTML 본문을 웹으로 가져와 읽었습니다.
- 표기: `B` = `https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335`

## 0. 확인한 것과 못 한 것

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| 저장소 존재·공개 여부 | 확인 | `gh repo view google-research/harness2`, 클론 성공 |
| 라이선스 | 확인 | [`LICENSE`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/LICENSE) Apache 2.0, [`pyproject.toml`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/pyproject.toml#L9) `license = "Apache-2.0"` |
| 핵심 소스(`harness2/core/*`, `substrate/*`) | 직접 읽음 | 본문 링크 |
| 논문 | 존재·초록 확인, 본문 일부 확인 | [arXiv:2610.14224](https://arxiv.org/abs/2610.14224), 2026-10-09 제출. 본문은 HTML을 요약 도구로 읽었으므로 **절 번호와 인용은 원문 PDF로 다시 대조해야 합니다** |
| 프로젝트 사이트 | 존재 확인 | https://harness2.github.io (README가 링크) |
| Google Research 블로그 글 | **찾지 못함** | 사이트·README·논문 어디에도 블로그 링크가 없음 |
| 실험 수치 재현 | 하지 않음 | 모델 호출 비용이 들고, 조사 범위 밖 |
| `prompts.py`(1,163줄) 전문 | 일부만 읽음 | 격리 지시문과 INV/DOM 구간만 확인 |
| 벤치마크 어댑터(`benchmarks/*.py`) | 읽지 않음 | 방법론과 무관한 연결 코드 |

## 1. Harness²는 무엇인가

### 1.1 목적

README는 하네스를 "모델이 에이전트로 행동하게 하는 주변 시스템(프롬프트, 도구, 메모리, 스킬, 오케스트레이션 등)"으로, *harnessing*을 그 시스템을 최적화하는 과정으로 정의합니다([README L19-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L19-L21)). Harness²는 **모델 가중치는 고정한 채** 두 단계의 재귀로 하네스를 고칩니다([README L23-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L23-L33)).

- **과제 수준 재귀**: 지금 과제의 실행 하네스를 대조형 **Propose–Probe–Compose** 단계로 다듬습니다. 정답 피드백 없이, 실행 사이의 행동 대조만 근거로 씁니다.
- **하네싱 수준 재귀**: 과제마다 채택된 하네스와 증거가 붙은 교훈을 지속형 *개선 하네스*(라이브러리)에 쌓아 다음 과제에 씁니다.

논문 초록은 동기로 두 가지를 듭니다. 열린 세계의 과제는 설계 시점에 보지 못한 것이라 **정답 검증기가 없고**, 기존 재귀적 자기 개선은 과제 특화적이라 일반화가 안 된다는 점입니다([arXiv 초록](https://arxiv.org/abs/2610.14224)).

### 1.2 구조와 핵심 추상화

| 추상화 | 정의 | 출처 |
| --- | --- | --- |
| 세 축 분리 | 방법(재귀·프롬프트·선택·라이브러리), 기반(substrate: 에이전트 프레임워크), 벤치마크(`BenchSpec` 값 + 어댑터)를 섞지 않음 | [`core/spec.py` L15-20](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L15-L20) |
| 편집 가능한 8개 구성요소 c1..c8 | 시스템 프롬프트, 가드레일, 메모리, 도구 안내, 하위 에이전트, 스킬, 스크립트, 플러그인 | [README L68-73](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L68-L73) |
| `SurfaceSpec` | 프레임워크별 편집 표면(경로, 상시 주입 파일, 길이 상한, 훅 파일, 허용 훅 이벤트) | [`core/tree.py` L40-60](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L40-L60) |
| 상시 주입(always-on) 상한 | OpenCode 24,000자, Codex 8,000자. Codex는 `AGENTS.md`를 매 턴 주입하고 32,768바이트에서 조용히 자른다는 이유를 적어 둠 | [`substrate/opencode.py` L42-51](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L42-L51), [`substrate/codex.py` L39-47](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L39-L47) |
| 편집 규약 | "생략은 상속": 제안은 바꾸는 파일만 냄 | [`core/tree.py` L15-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L15-L21) |
| 경로 탈출 거부 | 절대 경로, `..` 포함 경로를 거부 | [`core/tree.py` L82-89](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L82-L89) |
| `BenchmarkAdapter` | 벤치마크가 채워야 하는 전부: `tasks`, `task_prompt`(채점 기준 제거), `execute`, `trajectory`, `validate_tree`, `score` 등 | [`core/spec.py` L200-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L200-L250) |
| `Substrate` | `surface`, `materialise`, `execute`, `read_trajectory`, `preflight` | [`substrate/base.py` L47-80](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L47-L80) |
| 역할 | 실행자(executor), 하네스 편집자(INV·DOM 두 차원), 구성자(composer), 선택자(selector), 경험 반성자(experience reflector). 채점자(judge)는 방법 바깥 | [README L37](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L37) 그림 설명, [`core/recursion.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py), [`core/selection.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19) |

### 1.3 Propose–Probe–Compose

1. **Propose**: 편집자가 두 차원의 후보를 냅니다. INV는 "에이전트가 일하는 방식"(도구·절차), DOM은 "그 분야 실무자가 아는 것"입니다([`core/prompts.py` L347-373](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L347-L373)). 논문 §2.2.1은 이를 영역과 무관한 결함과 영역 특화 결함으로 설명합니다.
2. **Probe**: 각 후보를 **같은 과제에서** 실행해 기준 실행과 궤적·산출물을 비교합니다(논문 §2.2.1).
3. **Compose**: 증거가 받쳐 주는 변경을 합치고, 충돌하는 편집은 고치고, 한 후보를 채택하거나 현재 하네스를 유지합니다(논문 §2.2.1). 구성 지시문은 INV 편집과 DOM 편집을 합치는 것을 기대 결과로 둡니다([`core/prompts.py` L934](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L934)).

확장 방식은 둘입니다([`core/recursion.py` L343-566](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L343-L566)).

- **병렬(`agg`)**: INV k개 + DOM k개 후보를 같은 기준 증거에서 만들고 실행한 뒤, 서로 독립인 구성 k개를 만듭니다.
- **순차(`seq`)**: k번의 Propose–Probe–Compose를 이어 붙이며, 다듬은 하네스와 누적 증거를 다음 단계로 넘깁니다.

잘못된 제안은 **한 번 재시도**하고, 그래도 안 되면 현재 하네스를 그대로 물려받습니다([`core/recursion.py` L15-19, L36](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L36), [L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L242-L251)). 재시도 때는 검증 오류 문장을 그대로 되먹입니다. 어댑터 규약도 "오류 메시지는 재시도 피드백으로 그대로 들어가니 행동 가능한 문장으로 쓰라"고 요구합니다([`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)).

### 1.4 이벤트·궤적 모델

Harness²에는 Mallangable 5.6 같은 **생애주기 이벤트 모델이 없습니다.** 대신 두 가지가 있습니다.

- **공통 궤적 문법**: 기반마다 다른 기록 형식을 `[ACTION]` / `[OBSERVATION]` / `[ERROR]` 줄로 렌더링합니다([`core/spec.py` L230-231](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L230-L231), [`substrate/codex.py` L386-389](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L386-L389), [`substrate/opencode.py` L384-388](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L384-L388)). 궤적 전체를 파일로 주고, 개별 관측만 길이 상한(기본 50,000자, 10,000자 미만 금지)으로 자릅니다([`core/spec.py` L163-167](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L163-L167), [`core/context.py` L15-27](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L15-L27)).
- **증거는 파일로, 프롬프트는 포인터로**: 편집자는 `context/` 아래 과제·궤적·산출물·하네스·라이브러리·후보를 디스크에서 읽고, 모든 편집의 근거가 된 궤적 지점을 인용해야 합니다([`core/context.py` L521-544](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L521-L544)).
- **훅은 편집 대상**: Codex 기반에서는 `.codex/hooks.json`이 편집 표면에 들어갑니다. 허용 이벤트는 `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PreCompact`, `PostCompact`, `SessionStart`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `Stop`입니다([`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72)). 검사기는 `command` 형식만 받습니다. 형식이 틀린 훅은 오류 없이 **아예 실행되지 않으므로**, 제안자가 보는 시점에 형식을 강제한다고 적혀 있습니다([`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)).

### 1.5 평가 방법론

| 장치 | 내용 | 출처 |
| --- | --- | --- |
| 점수 없는 실행 보기 | 방법이 아는 실행 정보 `RunView`는 "절대 점수를 싣지 않는다" | [`core/spec.py` L176-187](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L187) |
| 채점은 선택 이후에만 | `score()`는 `core.judge`만, 선택이 확정된 뒤에만 부름. 방법 쪽 어떤 모듈도 `judge`를 import하지 않음 | [`core/spec.py` L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L247-L250), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19), [BENCHMARKS L34](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L34) |
| 채점 실패 ≠ 0점 | 실패는 `None`, 분모에서 제외, 0점으로 캐시하지 않음. 미채점은 따로 보고 | [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18), [EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118), [BENCHMARKS L67-68](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L67-L68) |
| 정답 경로 차단 | 벤치마크가 선언한 `leak_globs`가 맥락에 들어가면 예외 | [`core/context.py` L399-416](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L416) |
| 채점 흔적 트립와이어 | 채점기 출력 표지 문자열이 맥락 파일 이름·본문, 또는 에이전트가 쓴 하네스에 있으면 거부. "트립와이어이지 방어 자체가 아니다. 걸리면 표지 목록을 넓히지 말고 새는 읽기 경로를 찾아라" | [`core/context.py` L419-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L419-L518) |
| 측정 단어 금지 | 에이전트에게 보이는 벤치마크 문구에 benchmark, evaluation, grader, rubric, score가 있으면 거부: "일을 묘사하라, 측정을 묘사하지 말라" | [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126) |
| 명시적 무채점 지시 | 편집자·선택자 프롬프트에 "맥락에 채점 기준·정답·점수는 없다. 채점자가 원하는 것을 추측하지 말라" | [`core/prompts.py` L41-53](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L41-L53), 논문 부록 H |
| 익명 선택 | 후보에 A, B, …를 붙이고 `task_id\|k\|mode` 시드로 섞음(재실행해도 같음). 선택 풀은 최종 후보 k개뿐이고 기준 실행은 넣지 않음 | [`core/selection.py` L71-76](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L76), [L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L93-L111) |
| 선택자 실패 시 대체 | 선택자가 실패하면 중립 대체(전달된 기준 실행, 없으면 첫 최종 후보)를 고르고 `fallback`으로 기록 | [`core/selection.py` L237-252](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L237-L252) |
| 예산 항등식 | 과제당 실행 R = 4k(기준 k + 후보 2k + 최종 k), 개선 세션 P = 3k. 라벨이 겹치면 덮어쓰기로 보고 숫자 검사보다 먼저 실패시킴 | [`core/ledger.py` L15-33, L89-113](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L113) |
| 실행 동일성 | 완료 표지에 하네스 트리 지문을 넣어, 다른 구성에서 나온 실행을 재사용하지 않음 | [`core/runmark.py` L15-20, L41-61, L91-102](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L102) |
| 후보 다양성 | 후보 하네스 사이 줄 단위 Jaccard로 한 몸으로 수렴하는지 측정 | [`core/tree.py` L407-427](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L407-L427) |
| 웹 접근 경고 | 공개 벤치마크라 채점 기준이 온라인에 있음. 검증 실행에서 Codex 실행이 **지시 없이 자기 과제의 채점 기준을 내려받음**. 실행 호스트에서 네트워크 수준 차단을 권하고, 사용한 제한을 결과와 함께 보고하라고 함 | [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109), [README L166-171](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L166-L171) |
| 라이브러리 범위 | 실행·모드·영역 단위로 분리, 각 실행은 모든 영역을 빈 상태에서 시작. 같은 영역 안에서는 앞선 과제만 읽음 | [`core/library.py` L15-24](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L15-L24), [EXPERIMENTS L16-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L16-L19) |
| 경험 항목 | `cue`·`lesson`·`evidence`가 모두 있어야 저장(`confidence` 선택). 없으면 라이브러리에 넣지 않음 | [`core/library.py` L43-47, L106-123](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L43-L123), [`core/selection.py` L494-501](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L494-L501) |

벤치마크는 JobBench, LAB, WorkBuddy-Bench 세 가지입니다([README L129-133](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L129-L133)). README와 초록이 밝힌 결과는 GLM-5와 Gemini 3.5 Flash에서 단일 단계로 WorkBuddy-Bench 최대 11.5점, JobBench 4.5점, LAB 부분 통과율 11.8%p 향상입니다([README L41-45](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L41-L45)). 논문 부록 F의 한계는 두 가지입니다. 재귀 예산이 늘면 추론 비용이 늘고, 정답 감독이 없으니 판단이 실행 변동과 모델 공통 편향에 민감합니다. 이 수치는 직접 재현하지 않았습니다.

### 1.6 라이선스

- 본체: Apache 2.0([README L199-204](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L199-L204)). 이 저장소가 스키마·도구에 쓰려는 Apache-2.0(README 「라이선스」)과 충돌하지 않습니다.
- `third_party/`, 벤치마크, 데이터셋은 각 상류 라이선스를 따릅니다. WorkBuddy-Bench는 **지역 제한이 있는 Tencent 자체 라이선스**입니다([BENCHMARKS L80-83](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L80-L83)).
- 이 노트는 짧은 구절 인용과 링크만 쓰고 코드는 옮기지 않았습니다. 아래 제안 문구도 개념을 우리 말로 다시 쓴 것이며, 출처 표기만 남깁니다.

## 2. 대응표 — Harness² 개념 → Mallangable

판정: **채택**(거의 그대로), **변형**(취지만 가져옴), **거부**.

| # | Harness² 개념 | Mallangable 위치 | 판정 | 이유 |
| --- | --- | --- | --- | --- |
| M1 | 하네스 = 편집 가능한 c1..c8 트리 | 5.6 정의(결정적 외피) | **거부**(정의 차원) | 우리 하네스는 정책을 *강제*하는 쪽입니다. 에이전트가 가드레일·훅을 고치는 구조는 I8(권위 있는 집행은 제어면만)과 7.11 "정책 파일 불변"에 어긋납니다. 절차(스킬·프롬프트)만 오프라인으로 다듬는 것은 가능 |
| M2 | 훅 형식이 틀리면 조용히 실행 안 됨, 쓰기 시점에 형식 검사 | 5.6 「주의」, 7.2 기기 하네스 훅 | **채택** | 훅이 실패하면 열린 채로 남는(fail-open) 경로를 하나 더 드러냅니다. 기기 훅 설정은 쓰는 시점에 스키마를 검사하고, 서버 수신 검사가 최종 권위라는 기존 원칙을 보강 |
| M3 | Codex 훅 이벤트 목록 | 5.6 「매핑 예」 | **변형** | Claude Code 외 두 번째 대응표 후보입니다. 다만 출처가 Harness²의 검사기이지 Codex 공식 문서가 아니므로 "확인 필요"로 표시 |
| M4 | `RunView`에 점수 없음, 채점은 선택 이후, 채점 흔적 트립와이어, `leak_globs` | 10.2 숨은 검사, I7 | **채택** | Mallang-Bench의 SBR은 숨은 검사가 정말 숨어 있어야 의미가 있습니다. 숨은 검사가 생성·판정 맥락에 새면 SBR은 낙관적으로 왜곡됩니다 |
| M5 | 채점 실패는 `None`, 분모 제외, 따로 보고 | 10.2 「보고 형식」 | **채택** | 실패를 0으로 넣으면 CSR이 내려가고, 빼고 숨기면 올라갑니다. 둘 다 정직하지 않습니다 |
| M6 | 웹 접근으로 채점 기준 유출, 네트워크 제한 보고 | 10.2 구성·보고, 7.3 외부 통신 허용 목록 | **채택** | 공격 세트·추출 세트·숨은 검사가 공개되면 같은 문제가 생깁니다. 7.3의 허용 목록 규칙을 벤치마크 실행 조건으로도 요구 |
| M7 | 측정 단어 금지(일을 묘사하라) | 10.2 요청 세트 | **채택** | 요청 세트 문장에 "검사", "채점" 같은 단어가 있으면 에이전트가 측정 자체를 겨냥할 수 있습니다 |
| M8 | 익명·시드 셔플 선택, 기준 실행 제외 | 5.8 G4 판정, 5.7 판정자 | **변형** | 판정자가 후보가 어느 생성자·하네스·모델 경로에서 왔는지 모르게 합니다. I7(다른 인스턴스)에 "출처 맹검"을 더하는 것 |
| M9 | 예산 항등식 R=4k, P=3k, 라벨 중복 검사 | 10.2 CPC, 5.6 예산 | **변형** | 비용 비교가 공정하려면 "몇 번 실행·몇 번 판정했나"를 함께 보고해야 합니다. 정확한 항등식은 Harness² 방법에만 맞으므로 *보고 항목*만 가져옴 |
| M10 | 하네스 지문으로 실행 동일성 판별 | `change-record.schema.json` `provenance` | **채택** | 지금 `agent`는 "역할@하네스" 문자열뿐이라 하네스 *구성*이 바뀌어도 기록이 같습니다. 내용 해시를 두면 재현·감사·벤치 비교가 됩니다 |
| M11 | 잘못된 제안은 1회 재시도 후 현재 상태 유지 | 5.8 G1 「실패 시」, 5.6 예산 | **채택** | G1은 "이유를 에이전트에 돌려줌"만 있고 상한과 종료 상태가 없습니다. 비용 공격자(7.1)를 생각하면 상한과 "변경 없음" 종료가 필요 |
| M12 | 영역별 경험 라이브러리(cue·lesson·evidence) | 5.3 `ResolutionCache`, 6장 해결 캐시, 7.5 범위 분리 | **변형** | 범위 분리는 이미 7.5에 있습니다. 가져올 것은 "증거 필드가 없는 교훈은 저장하지 않는다"는 저장 조건과, 벤치에서 캐시를 빈 상태로 시작했는지 밝히는 보고 항목 |
| M13 | Propose–Probe–Compose(정답 없는 대조 개선) | 10.1 O1·O4, 5.7 병합자·승격자 | **변형(선택)** | 대화형 변경 하나에 실행 4k번은 시간 등급(8.4)과 비용에 맞지 않습니다. 서버 잡(병합·승격)이나 O4 판정자 신뢰도 연구의 출발점으로만 남김 |
| M14 | `[ACTION]/[OBSERVATION]/[ERROR]` 궤적 문법 | 5.11 텔레메트리, G4 증거 | **보류** | E4·E5 이벤트로 같은 정보를 만들 수 있습니다. 판정자 입력 형식을 정할 때 다시 봄 |
| M15 | 후보 다양성(Jaccard) | — | **거부** | 우리 명세에는 다수 후보를 만드는 단계가 없습니다(YAGNI) |
| M16 | 상시 주입 길이 상한과 그 이유 | 5.10 컨텍스트 공급 | **보류** | 역할별 컨텍스트 예산을 정할 때 참고할 수치입니다. 지금 명세에 넣을 근거는 약함 |

## 3. 제안 편집 목록 (우선순위순, 최대 10)

각 항목은 최소 편집입니다. 문구는 Harness² 문장을 옮긴 것이 아니라 개념을 다시 쓴 것입니다.

### E-1. 10.2 Mallang-Bench에 숨은 검사 격리 규칙 추가 (M4)

- 파일: `docs/10-open-problems.md`, 「### 구성」 표 바로 아래
- 근거: [`core/spec.py` L176-187, L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L250), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19), [`core/context.py` L399-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L518)
- 제안 문구:

```markdown
숨은 검사 격리 (반드시):
- 숨은 검사와 그 결과는 해석자·생성자·판정자의 맥락에 들어가지 않는다. 채점은 활성화가 끝난 뒤 별도 프로세스가 한다.
- 실행기는 생성·판정 맥락을 만들 때마다 숨은 검사 파일 경로와 검사 결과 표지 문자열을 찾아, 발견하면 실행을 멈춘다. 이 검사는 경보 장치일 뿐 방어가 아니다. 걸리면 표지 목록을 넓히지 말고 새는 읽기 경로를 고친다.
(출처: Harness²의 점수 없는 실행 보기와 채점 흔적 트립와이어, google-research/harness2 `core/spec.py`, `core/context.py`)
```

### E-2. 10.2 「보고 형식」에 미채점 규칙 추가 (M5)

- 파일: `docs/10-open-problems.md`, 「### 보고 형식」 문단 끝
- 근거: [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18), [EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118)
- 제안 문구:

```markdown
채점이 실패한 요청(숨은 검사 실행 오류, 판정 모델 오류)은 0점이 아니라 **미채점**이다. 지표의 분모에서 빼고, 미채점 건수를 지표와 나란히 보고한다. 예: "CSR 0.71 (n=192, 미채점 8)".
```

### E-3. 10.2 「보고 형식」에 실행 환경 보고 항목 추가 (M6, M9, M12)

- 파일: `docs/10-open-problems.md`, E-2 문단 다음
- 근거: [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109), [`core/ledger.py` L15-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L33), [`core/library.py` L21-23](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L21-L23)
- 제안 문구:

```markdown
함께 보고할 실행 조건:
- **네트워크 제한**: 생성 에이전트가 접근할 수 있었던 호스트 목록. 숨은 검사·공격 세트·추출 세트를 호스팅하는 주소는 실행 중 차단한다. 공개 벤치마크에서는 에이전트가 지시 없이 채점 기준을 내려받은 사례가 보고되었다(Harness² 실험 안내서).
- **호출 수**: 성공한 변경 1개당 생성 실행 수와 판정 세션 수(재시도 포함). CPC만으로는 다른 하네스끼리 공정하게 비교할 수 없다.
- **캐시 상태**: 해결 캐시·학습된 교훈을 빈 상태로 시작했는지, 앞 요청의 결과를 쓰게 했는지.
```

### E-4. 5.8 G4에 출처 맹검 추가 (M8)

- 파일: `docs/05-reference-architecture.md`, 5.8 게이트 표 `G4 판정` 행의 "내용" 칸
- 근거: [`core/selection.py` L71-76, L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L111), 논문 §2.2.2
- 현재: `판정자가 스크린샷·의도로 의미 충족 판정`
- 제안: `판정자가 스크린샷·의도로 의미 충족 판정. 판정자는 산출물이 어느 생성자·하네스·모델 경로에서 왔는지 모른다(출처 맹검). 후보가 여럿이면 재현 가능한 시드로 섞은 익명 id로 제시`

### E-5. 5.8 G1 실패 시 재시도 상한 명시 (M11)

- 파일: `docs/05-reference-architecture.md`, 5.8 게이트 표 `G1 정적 검사` 행의 "실패 시" 칸
- 근거: [`core/recursion.py` L15-19, L36, L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L251), [`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)
- 현재: `이유를 에이전트에 돌려줌`
- 제안: `이유를 고칠 수 있는 문장으로 에이전트에 돌려줌. 재시도 상한(제안값: 1회)을 넘으면 변경 없이 현재 상태를 유지하고 종료`

### E-6. 5.6 「주의」에 훅 실패 시 열림 경고 추가 (M2)

- 파일: `docs/05-reference-architecture.md`, 5.6 마지막 「주의:」 문단 뒤
- 근거: [`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)
- 제안 문구:

```markdown
형식이 틀린 훅 설정은 많은 런타임에서 오류 없이 **아예 실행되지 않는다.** 즉 실패하면 열린 채로 남는다. 하네스 플러그인은 훅 설정을 쓰는 시점에 런타임이 받는 이벤트 이름·처리기 형식으로 검사하고, 세션 시작(E1) 때 훅이 실제로 등록됐는지 확인한다. 에이전트는 정책 훅·가드레일 파일을 고칠 수 없다(도구 경계, E4).
(참고: Harness²는 Codex 훅 파일을 같은 이유로 쓰는 시점에 검사한다. google-research/harness2 `core/tree.py`)
```

### E-7. `change-record.schema.json`에 하네스 지문 필드 추가 (M10)

- 파일: `schemas/change-record.schema.json`, `properties.provenance.properties`에서 `prompt_hash` 다음
- 근거: [`core/runmark.py` L15-20, L41-61](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L61), [`substrate/base.py` L26-32](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L26-L32)
- 제안 필드(`required`는 바꾸지 않음, 선택 필드):

```json
"harness_digest": {
  "type": "string",
  "pattern": "^sha256:[0-9a-f]{64}$",
  "description": "변경을 만든 하네스 구성(스킬·훅·정책 사본·도구 목록)의 내용 해시. 같은 agent 문자열이라도 구성이 다르면 값이 다르다"
}
```

- 비고: Harness²는 SHA-1 앞 16자를 씁니다. 여기서는 기존 `prompt_hash` 형식과 맞춰 SHA-256 전체를 제안합니다. 반영하면 `examples/change.example.yaml` 검증을 다시 돌려야 합니다(선택 필드라 기존 예시는 그대로 통과해야 정상).

### E-8. 10.2 요청 세트에 측정 단어 금지 추가 (M7)

- 파일: `docs/10-open-problems.md`, 「### 구성」 표 `요청 세트` 행 "내용" 칸 끝
- 근거: [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126)
- 덧붙일 문구: `. 요청 문장은 할 일만 말하고 측정은 말하지 않는다("검사", "채점", "점수" 등 금지)`

### E-9. 5.6 대응표에 Codex 열 후보 추가 (M3)

- 파일: `docs/05-reference-architecture.md`, 「### 매핑 예: Claude Code 훅」 표 뒤에 짧은 문단
- 근거: [`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72) (Codex 공식 문서가 아닌 2차 출처)
- 제안 문구:

```markdown
Codex CLI도 같은 방식으로 대응됩니다(E1 `SessionStart`, E2 `UserPromptSubmit`, E4 `PreToolUse`, E5 `PostToolUse`, E6 `PermissionRequest`, E11 `Stop`, E12 `SubagentStop`, E15 `PreCompact`). 이 목록은 Harness²가 검사하는 이벤트 집합에서 가져온 것이므로, 반영 전 Codex 공식 문서와 대조해야 합니다.
```

### E-10. 참고 문헌에 Harness² 추가

- 파일: `docs/references.md`, 「## 에이전트 보안」 앞에 새 절
- 제안 문구:

```markdown
## 하네스 개선과 평가

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · 코드(Apache-2.0): https://github.com/google-research/harness2
  - 숨은 검사 격리, 미채점 보고, 출처 맹검 판정, 하네스 지문(5.6, 5.8, 10.2)의 근거. 조사 노트: [research/harness2-analysis.md](research/harness2-analysis.md)
```

## 4. 넣지 않은 것

- **자기 편집 하네스(M1)**: 사용자 앱을 고치는 에이전트가 자기 정책 훅까지 고치면, 5.6이 하네스를 정의한 이유("비결정적 에이전트를 감싸는 결정적 외피")가 사라집니다.
- **Propose–Probe–Compose를 기본 생성 흐름(5.4)에 넣는 것**: 변경 하나에 실행 4k번이 들고 T0~T2 시간 등급을 지킬 수 없습니다. 쓸 곳은 서버 잡의 실험적 선택지와 O4 연구입니다.
- **벤치마크 수치 인용**: 직접 재현하지 않았고, 우리 문제(앱 수정)와 과제 분포가 다릅니다.
