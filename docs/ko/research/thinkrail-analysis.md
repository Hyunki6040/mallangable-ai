<!-- LANG-BAR -->
[English](../../en/research/thinkrail-analysis.md) · **한국어** · [简体中文](../../zh-CN/research/thinkrail-analysis.md) · [日本語](../../ja/research/thinkrail-analysis.md) · [Español](../../es/research/thinkrail-analysis.md)
<!-- /LANG-BAR -->

# 조사 노트 — ThinkRail (JetBrains/thinkrail)

> 이 노트의 결론: ThinkRail은 `pi` 코딩 에이전트를 감싸는 **에이전트 IDE 호스트**다. 사용자 앱을 고치는 Mallangable과 대상은 다르지만, "에이전트가 만든 변경을 사람이 안전하게 받아들이게 하는 호스트"라는 문제는 같다. 그대로 가져올 것은 다섯 가지다. ① **본 것을 근거로 한 되돌리기**(CAS). ② **판정 출력은 믿지 않는다**(형식이 틀리면 실패, 호스트 필드는 호스트가 채움). ③ **승인은 대상 지문에 묶이고, 범위가 정해져 있다.** ④ **받아들인 신뢰는 그 시점의 내용에만 해당한다**(나중에 생긴 항목은 다시 확인). ⑤ **저장 데이터에는 번역문을 넣지 않고, 용어팩은 데이터일 뿐 공유물이 바꿀 수 없다.** 반대로 "호스트는 프롬프트를 조립하지 않는다"는 원칙은 받아들이지 않는다. Mallangable의 하네스는 강제하는 쪽이기 때문이다.

- 확인일: 2026-11-03
- 조사 대상: https://github.com/JetBrains/thinkrail (공개, Apache-2.0, JetBrains 인큐베이터). 검색 결과에 나오는 같은 이름의 저장소 여럿은 이 저장소의 포크입니다.
- 고정 커밋: `c10f8808cee693e4abffeeb1844a132ed0a91cc5` (2026-11-03). 아래 모든 링크는 이 커밋 기준입니다.
- 방법: `git clone --depth 1`로 빈 임시 디렉터리에 받아 명세 문서(`SPEC.md`·`architecture.md`·`goal-and-requirements.md`)만 **읽었습니다.** 코드는 실행하지 않았습니다.

## 0. 확인한 것과 못 한 것

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| 저장소 존재·공개 여부 | 확인 | `gh repo view JetBrains/thinkrail`, 클론 성공 |
| 라이선스 | 확인 | [`LICENSE`](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/LICENSE) Apache 2.0. 이 저장소의 스키마·도구 방침(Apache-2.0)과 충돌 없음 |
| 제품 목표·아키텍처 문서 | 직접 읽음 | `goal-and-requirements.md`, `architecture.md` |
| 서버 하위 모듈 명세 | 일부 읽음 | `changes`, `host/planReview`, `agent`, `agent/mcp`, `agent/packages`, `extensions`, `todos`, `spec-graph`. 나머지 `SPEC.md`는 읽지 않음 |
| 명세와 구현의 일치 | 확인 안 함 | 명세 문서만 읽었고 소스·테스트는 읽지 않음. 아래 인용은 "ThinkRail 명세가 이렇게 정한다"는 뜻입니다 |
| 실행·재현 | 하지 않음 | 조사 범위 밖 |

## 1. ThinkRail은 무엇인가

`pi` 에이전트를 프로세스 안에서 돌리고, 그 위에 편집기·diff·터미널·리뷰 UI를 얹은 호스트입니다([`goal-and-requirements.md` L10-16](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L10-L16)). 세 고리로 나뉩니다. 엔진 호스트, 버전이 붙은 통신 계약(wire), UI 클라이언트입니다([`architecture.md` L19-28](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L19-L28)). 작업 공간은 git worktree라서 여러 에이전트가 서로 부딪히지 않고 병렬로 일합니다([`architecture.md` L107-122](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L107-L122)).

원칙 가운데 Mallangable과 겹치는 것과 갈리는 것:

| ThinkRail 원칙 | Mallangable과의 관계 |
| --- | --- |
| **신뢰는 명시적이다**: 복제한 저장소가 에이전트에 넣을 수 있는 것(스킬·확장·MCP 서버)은 프로젝트 단위 신뢰 승인 뒤에만 불러옴. 저장소가 정의한 MCP 서버는 항목별 승인이 따로 필요하고, 항목이 바뀌면 승인이 사라짐 ([L62-65](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L62-L65)) | 같은 방향. 공유받은 기능(6.9)과 I4에 대응 |
| **주입이 아니라 공급으로만 영향**: 호스트는 프롬프트를 조립하지 않음 ([L57-58](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L57-L58)) | 갈림. Mallangable 하네스(5.6)는 정책을 강제하고 역할별 맥락을 고른다(5.10) |
| **다시 계산하지 말고 보여 준다**: 호스트는 엔진이 보고한 값을 그대로 보여 줌 ([L59](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L59)) | 같은 방향. 비용 표시(8.10)는 `ModelPort` 계량값을 쓴다 |

## 2. 대응표 — ThinkRail 개념 → Mallangable

판정: **채택**(거의 그대로), **변형**(취지만 가져옴), **확인**(이미 있음, 근거만 추가), **거부**, **보류**.

| # | ThinkRail 개념 | 출처 | Mallangable 위치 | 판정 | 이유 |
| --- | --- | --- | --- | --- | --- |
| T1 | 되돌리기 요청은 "사용자가 본 것"의 해시를 들고 오고, 지금 상태와 다르면 `STALE_VIEW`로 아무것도 쓰지 않음. 클라이언트는 내용을 보내지 않음 | [`changes/SPEC.md` L39-43, L116-118](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L39-L43) | 5.5, I3 | **채택** | 기준판 전파·다른 기기·감시자 자동 복구가 활성 상태를 옮길 수 있다. "아까 거 되돌려"가 엉뚱한 상태를 되돌리면 F1이 오히려 사고가 된다 |
| T2 | 되돌리기 영수증 id가 곧 되살리기 토큰. 되살리기도 같은 연산. 모르는 id는 조용히 넘기지 않고 `RECEIPT_UNKNOWN` | [`changes/SPEC.md` L81-112](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L81-L112) | 5.5, 8.7 | **변형** | Mallangable 되돌리기는 포인터 이동이라 바이트 링이 필요 없다. 가져올 것은 "되살리기 = 같은 연산"과 "못 하면 명시적으로 알림" |
| T3 | 원본 읽기 실패는 부재가 아니다. 부재로 읽으면 파일 전체 되돌리기가 사용자 파일을 휴지통에 보냄 | [`changes/SPEC.md` L119-122](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L119-L122) | 6.5, 2.3(`null` = 삭제) | **채택** | ⊕에서 `null`은 키 삭제다. 상위 레이어를 못 읽은 것을 "없음"으로 처리하면 전파가 사용자 기능을 지운다 |
| T4 | 리뷰어 출력은 믿지 않음: 판정 단어는 엄격 검사, 형식이 틀리면 승인이 아니라 실패. 결과 객체는 명시적으로 다시 만들어 모델이 지어낸 호스트 전용 필드를 버림. 지적 없는 "수정 요청"은 거부 | [`host/planReview.SPEC.md` L62-81](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L62-L81) | 5.8 G4, E12 | **채택** | E12에 "판정 결과 스키마 검사"만 있고, 검사 실패 시 결과가 정해져 있지 않다 |
| T5 | 승인은 판정이지 확정이 아님: 열린 지적이 남아 있으면 approve도 확정하지 않음 | [`host/planReview.SPEC.md` L102-106](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L102-L106) | 5.8 G4 | **채택** | 재판정 라운드가 이전 지적을 덮는 경로를 막는다 |
| T6 | 두 진입점(에이전트 도구·사람 버튼)이 같은 수정 횟수 상한을 공유. 공유하지 않으면 수정→판정→수정이 무한 반복 | [`host/planReview.SPEC.md` L117-119](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L117-L119) | 5.8 G1 재시도 상한 | **채택** | G1 상한이 하나의 경로에만 걸리면 비용 공격자(7.1)가 다른 경로로 돈다 |
| T7 | 판정자를 세션이 아니라 결과를 돌려주는 하위 작업으로 둠. 끝나면 결과, 실패하면 거부, 회복은 한 곳 | [`host/planReview.SPEC.md` L21-42](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L21-L42) | 5.7 판정자 | **확인** | 이미 판정자는 읽기 전용·쓰기는 판정 결과뿐이다. 근거로만 인용 |
| T8 | MCP 도구 호출 확인: `readOnlyHint`가 없는 호출만 묻는다. 선택지는 거부·이번만·이 대화에서·항상. "항상"은 프로젝트 범위이고 대상(`command`+`args` 또는 `url`)의 SHA-256이 같을 때만 유효. 긍정 답이 아닌 모든 것(닫기, 다른 메시지, 중단)은 거부 | [`agent/mcp/SPEC.md` L129-150](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/mcp/SPEC.md#L129-L150) | 4.8, G5, 8.5 | **변형** | 승인 피로(4.10)를 줄이면서 승인이 다른 대상으로 새지 않게 한다. Mallangable에는 승인 범위·수명 규칙이 없다 |
| T9 | 신뢰를 주면 **그때 있던 것만** 확인된 것으로 친다. 나중에 pull·브랜치로 생긴 스킬은 `pending-ack` | [`agent/SPEC.md` L993-1000](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L993-L1000) | 6.9 `subscribe` 공유 | **채택** | 구독형 공유는 보낸 사람이 고칠 때마다 내용이 바뀐다. 첫 수락이 이후 내용까지 덮으면 7.7 "설치 후 원격에서 내용을 바꿨다"와 같은 구멍이 생긴다 |
| T10 | 같은 이름이면 신뢰 높은 쪽이 이김: 내장 → 개인 → 프로젝트 순. 저장소는 내 스킬을 가릴 수 없음. 내장 확장은 켜져 있는 동안 같은 이름 도구 충돌에서 이김 | [`agent/SPEC.md` L991-992](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L991-L992), [`extensions/SPEC.md` L32-37](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/extensions/SPEC.md#L32-L37) | 6.9, O3 | **변형** | Mallangable 레이어 합성은 "사용자에 가까운 쪽이 이김"이다. 그 규칙은 그대로 두고, **받은 공유물**이 명령·단축키 같은 식별자를 가로채는 경우에만 적용 |
| T11 | 끄기 스위치는 확장이 기여한 모든 것(팩토리·도구·스킬)을 함께 끔. 렌더러는 남겨 과거 기록은 계속 보임 | [`architecture.md` L376-382](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L376-L382) | 5.9 감시자·세이프 모드 | **채택** | 한 기능이 여러 슬롯·명령·훅에 걸치면 슬롯 하나만 끄는 격리는 반쪽이다 |
| T12 | 목록 조회는 부작용이 없다: 카탈로그는 설치도, 확장 코드 실행도 하지 않음. 도구 이름은 실제 로드가 기록한 것에서 읽음. 목록 때마다 팩토리를 돌리던 방식은 거부됨 | [`agent/packages/SPEC.md` L23-25, L128-131](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/packages/SPEC.md#L23-L25) | 7.7, 7.11 | **채택** | 공유·마켓의 미리보기 화면에서 D4 코드를 돌리면 승인 전 실행이 된다(5.9 "승인 전 D4는 권한 0" 위반) |
| T13 | 계획 단계마다 작업 창(시작 시점 기준선)을 열고, 끝나면 **그 단계가 바꾼 경로만** 커밋. 다른 대화와 창이 겹치면 `shared`로 표시하고 귀속을 추측하지 않음 | [`todos/SPEC.md` L64-80](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/todos/SPEC.md#L64-L80) | 6.4, 기록자 | **변형** | 같은 사용자의 생성 작업 둘이 한 레이어에서 겹치면 어느 기능의 변경인지 흐려진다(I9) |
| T14 | `agent_end`는 시도 경계일 뿐(재시도·압축 뒤에 더 일할 수 있음). `agent_settled`만 완료. 입력 대기는 수준 신호라 보는 것만으로 지워지지 않음 | [`architecture.md` L141-156](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L141-L156) | 5.6 AG-UI 대응, 8.5 상태어 | **채택** | 재시도 중간에 "준비됐어요"가 뜨면 상태어 고정 규칙(8.5)이 깨진다 |
| T15 | 호환성 대장: 엔진 결함·빠진 API를 메우는 적응마다 "업그레이드 때 다시 볼 것"과 "지워도 되는 조건"을 적음. 명세는 버전 번호를 다시 적지 않고 무엇을 확인했는지 적음 | [`pi-compatibility.md` L11-16](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/pi-compatibility.md#L11-L16), [`architecture.md` L205-211](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L205-L211) | 5.6 대응표 | **채택** | 5.6 Claude Code 표의 `onFailure` 판 조건처럼, 대응표 항목은 런타임 판에 따라 낡는다 |
| T16 | UI 문자열은 키 카탈로그. 하드코딩 문자열은 린트로 실패. 저장·통신 데이터에는 번역문을 넣지 않고 렌더 때 문장화. 사용자 언어 파일은 전역 데이터 폴더에서만 읽음(복제한 저장소가 UI를 다시 쓸 수 없게). 대체 순서: 지역 정확 → 내장 정확 → 내장 기본 → 영어 | [`architecture.md` L430-454](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L430-L454) | 8.9 용어팩 | **채택** | 키 카탈로그·린트는 이미 있다. 빠진 것은 저장 규칙, 출처 제한, 대체 순서. 출처 제한이 없으면 공유물이 권한 경고 문구("환자 정보 접근")를 순한 말로 바꿀 수 있다 |
| T17 | 에이전트·도구 출력은 번역하지 않음 | [`architecture.md` L443-444](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L443-L444) | 8.9 적용 지점(E13 설명자) | **거부** | ThinkRail 사용자는 개발자다. Mallangable의 basic 사용자에게는 설명자가 일반 용어로 다시 써야 한다 |
| T18 | 하위 에이전트의 신뢰는 부모가 **불러온** 신뢰와 현재 기록 둘 다를 넘지 못함. 철회하면 자식도 따라감 | [`agent/SPEC.md` L1443-1452](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L1443-L1452) | 5.7 역할, I4 | **확인** | I4·역할 분리로 이미 보장. 근거로만 인용 |
| T19 | 리뷰 주석은 엔진 중립 선택자(`lineRange`·`textQuote`·`json-pointer`·`region` 등)로 걸고, 렌더러가 "놓임/못 놓임"을 보고 | [`architecture.md` L330-346](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L330-L346) | 8.2 화면 지목, 6.12 | **보류** | 기준판이 바뀐 뒤 지목 앵커가 다른 요소에 조용히 붙는 문제와 같다. 기능 지도 형식을 확정할 때(10.4 로드맵) 다시 봄 |
| T20 | 호스트가 프롬프트를 조립하지 않음 | [`goal-and-requirements.md` L57-58](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L57-L58) | 5.6, 5.10 | **거부** | 하네스는 "비결정적 에이전트를 감싸는 결정적 외피"다(5.6). 맥락 공급(5.10)은 I6을 지키는 수단이다 |

## 3. 반영한 편집

문구는 ThinkRail 문장을 옮긴 것이 아니라 개념을 다시 쓴 것이며, 각 자리에 출처를 남겼습니다.

| # | 대응 | 파일·위치 | 내용 |
| --- | --- | --- | --- |
| E-1 | T4·T5·T6 | `docs/05-reference-architecture.md` 5.8 「판정 출력 처리」 | 형식 오류 = 실패, 호스트 필드는 호스트가, 지적 없는 수정 요청 거부, 열린 지적 있으면 확정 안 함, 재시도 상한은 모든 진입점 공유 |
| E-2 | T1·T2 | 5.5 「되돌리기는 본 것을 근거로」 | `revert(expect=본 상태 id)`, 다르면 아무것도 안 하고 현재 상태 제시, 되살리기 = 같은 연산, 못 하면 명시적 알림 |
| E-3 | T11 | 5.9 「감시자와 세이프 모드」 | 격리·끄기 단위는 기능 전체. 영수증·기록은 계속 보임 |
| E-4 | T14 | 5.6 AG-UI 대응 아래 | 시도 경계 ≠ 완료, 승인대기는 수준 신호 |
| E-5 | T15 | 5.6 매핑 예 아래 | 대응표 항목마다 확인한 동작·재확인 조건·제거 조건 |
| E-6 | T8 | `docs/04-control-spectrum.md` 4.8 배치 원칙 | 승인 범위 세 가지, 승인 = 대상 지문에 묶임, 긍정 외 응답은 거부, 읽기 전용은 묻지 않음 |
| E-7 | T3 | `docs/06-versioning-and-lineage.md` 6.5 규칙 | 읽기 실패를 삭제(`null`)로 취급하지 않음 |
| E-8 | T13 | 6.4 | 동시 생성은 작업 사본을 따로, 기록은 자기 경로만, 겹치면 귀속 추측 금지 |
| E-9 | T9·T10 | 6.9 규칙 | 수락은 그 시점 내용에만, 받은 공유물은 식별자를 가로채지 못함 |
| E-10 | T12 | `docs/07-trust-and-security.md` 7.11 | 목록·미리보기·권한 표시는 코드 실행 없이 매니페스트에서 |
| E-11 | T16 | `docs/08-experience-design.md` 8.9 「저장과 출처」 | 개념 id + 인자로 저장, 용어팩 출처 제한, 대체 순서 |

## 4. 넣지 않은 것

- **스키마 변경**: E-6의 "승인 = 대상 지문"을 스키마 필드로 넣는 것은 미뤘습니다. 지금 규칙은 기존 `permissions_delta`·`approved_by`로 표현됩니다. 승인 기록을 변경 기록과 따로 저장하는 형식을 정할 때 넣습니다.
- **worktree 기반 작업 공간 그대로**: Mallangable의 격리 단위는 저장소, 작업 단위는 브랜치입니다(6.4). 작업 사본을 어떻게 만들지(worktree·임시 복제)는 구현 선택으로 둡니다.
- **정확한 버전 고정 규칙(architecture 결정 10)**: 저장소 운영 규칙이지 명세 내용이 아닙니다. "명세는 버전을 다시 적지 않고 무엇을 확인했는지 적는다"는 취지만 E-5에 반영했습니다.
- **영수증 링 상한(20개·64 MiB)**: Mallangable 되돌리기는 포인터 이동이라 해당 없습니다.
