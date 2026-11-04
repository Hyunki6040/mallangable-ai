# 보안 감사 보고서 — 2026-11-05

도구: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) (`.claude/skills/security-audit/`, `UPSTREAM` 커밋 고정)

## 1. 실행 범위

- 프로파일: **quick**, 부분 감사입니다. 사냥 1회와 최종 커버리지 비평 1회만 했고, 비평이 찾은 단위 6개는 `deferred`(`quick_profile_final_critic`)로 남겼습니다. 전체 커버리지를 주장하지 않습니다.
- 대상: 저장소 전체, 소스 기준 `a69ddbf`. 처음 하는 감사라 이전 결과가 없습니다.
- 예산: 따로 정하지 않았습니다. 에이전트는 정찰 1, 사냥 5, 검증 4, 비평 1로 모두 11개입니다. 검증 하나(`v-propagate`)는 결과 형식이 틀려 버리고 새 검증자로 다시 했습니다.
- 실행 경계: 대상 코드는 Docker 안에서만 실행했습니다. 조건은 `--network none`, 대상 읽기 전용, uid 65534, `cap-drop ALL`, 256 MiB, 60초, `env -i`이고, 쓰기는 에이전트별 scratch만 허용했습니다. 산출물은 부모 쪽 no-follow 승격기로만 옮겼습니다. 배포 환경이나 외부 서비스는 건드리지 않았습니다.

## 2. 요약

명세 저장소라 실행 서버는 없습니다. 실제 경계는 두 곳입니다. (a) 외부 문서를 받는 검사 도구, (b) 구현자가 그대로 옮길 규범 의사 코드입니다. 확인된 결함 2건은 모두 low입니다. 결함 1건은 검증이 더 필요하다고 판정됐고, 그 의존 사항은 이번 개정에서 명세 문장으로 닫았습니다.

## 3. 확인된 결함

| 심각도 | 제목 | 경계 | 관측 결과 |
| --- | --- | --- | --- |
| low | `decide()`의 하한 행동 예외가 주체·방향을 보지 않음 | 에이전트·다른 레이어 주체 → PDP 활성 상태 전이 | 같은 상태 S1에 대해 `activate`는 거부(깊이), `revert(target=S1)`는 허용[기록] |
| low | `check_schemas.py`가 문서 키·파일 이름의 제어 문자를 그대로 출력 | 외부 문서 작성자 → 검사자 터미널·CI 로그 | 원시 ESC 바이트 2개, 독립된 `::error title=forged::` 줄 생성. 종료 코드는 1로 유지 |

### 3.1 하한 행동 예외 범위 (`docs/04-control-spectrum.md:153`)

- 하위 신뢰 주체: 위임받은 에이전트(프롬프트 주입 가능), 감시자, 다른 레이어 사용자.
- 재현: 4.8 의사 코드를 그대로 옮겼습니다. 정책은 깊이 상한 D3, 권한 `[tasks.read]`, `gated`이고, 기록된 상태 S1은 D4에 `net.slack.post`를 가집니다. 결과는 `activate(S1)`가 `('deny','depth')`, `revert(target=S1)`가 주체와 무관하게 `('allow',['log'])`입니다.
- 조건: 호스트가 4.8을 그대로 구현하고, `revert`가 임의 StateId를 받으며 되살리기로도 쓰일 때(5.5) 성립합니다. 런타임 브로커의 호출별 PDP 확인이 실제 권한 사용을 막는지는 구현에 따라 다르므로 주장하지 않습니다.
- 영향: 이 상태 전이가 테넌트 상한, G5, 보류 재검증을 건너뜁니다. I4와 5.4(E10)에 어긋납니다.
- 조치(이번 개정): `floor_scoped(req)`를 추가했습니다. 사람 소유자, 자기 레이어, 이전 상태, 권한·깊이 비증가를 모두 만족할 때만 하한으로 봅니다. 그 밖의 `revert`는 `as_activate`로 같은 판정을 거칩니다. `uses_destructive` 분기도 추가했고, 5.5와 7.11에 같은 규칙을 적었습니다.

### 3.2 검사 도구 출력 주입 (`tools/check_schemas.py:29`, `:26`)

- 하위 신뢰 주체: `check_schemas.py <schema> FILE` 명령에 넘기는 외부 문서나 파일 이름의 작성자.
- 재현: lexicon-pack의 `concepts` 키를 `"x\e]0;PWNED\a\e[2K\rOK   forged.yaml[0]\n::error title=forged::…"`로 만들었습니다. 이 키가 `json_path`에 그대로 들어가 출력됐습니다.
- 영향: 출력과 로그만 위조됩니다(창 제목, 가짜 `OK` 줄, GitHub Actions 주석). 판정, 종료 코드, 파일, 자격 증명에는 영향이 없습니다.
- 조치(이번 개정): 출력하는 모든 문자열에 `safe()`(repr 이스케이프, 300자 자르기)를 씁니다. 회귀 검사로 assert를 하나 넣었습니다. 샌드박스에서 다시 돌린 결과 ESC 0개, `::` 줄 0개입니다.

## 4. 검증이 더 필요함

| 제목 | 위치 | 막힌 점 | 상태 |
| --- | --- | --- | --- |
| 기준판 전파 자동 적용이 권한 변화 없음만 확인함 | `docs/06-versioning-and-lineage.md:121-122` | `apply(merged)`가 `ChangeStore.activate`(E10)를 거치는지 명세에 정의되지 않았음 | 명세 소유자가 이번 개정에서 정의: 자동 적용도 `activate()`를 거치고, 승인 필요면 PROPOSED. `delta_permissions`는 다시 계산 |

첫 검증자는 이 건을 기각했습니다. 근거는 05:150, 05:205, 07:77에 따라 활성화가 늘 PDP를 거친다는 것이었습니다. 하지만 그 결과가 형식 오류라 규칙대로 버렸고, 새 검증자는 06:122가 `activate`와 묶여 있다는 문장이 없다는 점을 막힌 점으로 보고 `needs_validation`으로 판정했습니다. 두 해석 모두 6.5에 명시 문장이 필요하다는 데는 같은 결론이라, 그 문장을 추가했습니다.

## 5. 강화 메모 (결함 아님, 반영 여부)

- 반영: change-record 결정적 계약은 실행 가능한 형태가 하나 이상 있어야 합니다. 서술형만 있는 기록은 이제 거부됩니다.
- 반영: `permissions_delta` 재계산, `approved_by`는 사람 주체이며 `agent`와 달라야 함. 스키마 설명과 7.11에 넣었습니다.
- 반영: `network.allow`와 정책 `allowlist`가 IP 리터럴을 거부합니다. 공개 접미사 와일드카드, egress 권한 존재, `setKnob` default ⊆ ceiling은 준수 검사기 MUST로 적고 `False` 기대 회귀 사례를 추가했습니다.
- 반영: YAML 별칭과 1 MiB 초과 파일을 거부합니다. 555 B 별칭 폭탄이 75.5 MB를 출력하던 문제와 601 B 입력의 OOM이 없어졌습니다. 문서별 예외는 격리했습니다(비문자열 키).
- 반영: `design_space.py --profile`·`--check`는 실패 판정에서 종료 코드 1을 내고, 중복 키와 비객체 JSON을 거부합니다.
- 반영: CI `permissions: contents: read`. 4.7 발췌의 `net.allowlist`를 `net.slack.post`로 고쳤습니다(L-04).
- 미반영(제안): Actions를 커밋 SHA로 고정, `requirements.txt` 해시 고정, capability id `*` 의미 정의, 공유 시 `content_hash` 필수화, 승인 지문 필드.

긍정 패턴: `yaml.safe_load` 사용. 교차 문서 규칙을 `ACCEPTED (validator MUST check)`로 드러내는 회귀 구조. 깊이와 형태 대응을 세 곳에서 강제.

## 6. 커버리지

원장 17개 단위: covered 8 · candidate 3(모두 최종 판정 완료) · blocked 0 · deferred 6.

최종 비평이 찾아 미룬 단위:
1. 승인·동의를 재계산한 권한 변화, content_hash, `Contract-Migrated` 동의에 묶는 문제
2. capability id `*`와 호출별 PDP 대 마운트 시 부여
3. `check_schemas.py` OK 판정과 YAML→JSON 데이터 모델 차이(비문자열 키, 중복 키)
4. 릴리스 서명 고정, 폐기, 다운그레이드
5. R3 해결 캐시 오염(같은 테넌트 Sybil 노드)
6. 7.3 역할 분리와 7.5 라벨 행동 규칙(간접 주입)

다음 감사는 standard 프로파일로 이 6개부터 시작해야 합니다.
