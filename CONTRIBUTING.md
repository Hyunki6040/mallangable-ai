# 기여 안내

이 저장소는 구현체가 아니라 **명세**입니다. 기여는 크게 세 종류입니다: 본문 수정, 스키마·예시 수정, 계산기 규칙 수정.

## 시작 전에

```bash
pip install -r requirements.txt               # check_schemas.py 용
python3 tools/design_space.py --check all     # P1~P7 모두 clean이어야 함
python3 tools/check_schemas.py                # 마지막 줄이 ALL OK여야 함
```

두 명령이 통과하는 상태로 PR을 보내 주세요. 전체 열거(`python3 tools/design_space.py`)는 몇 분 걸립니다.

## 지켜야 할 것

- **식별자는 파일 사이의 계약입니다.** 축 `A1~A11`, 제약 `L`/`N`/`S`, 불변식 `I1~I10`, 하한 `F1~F7`, 게이트 `G0~G5`, 해결 단계 `R0~R5`, 프로파일 `P1~P7`, 사업 모델 `B1~B20`은 문서·스키마·`design_space.py`·`check_schemas.py`에 함께 나옵니다. 번호를 바꾸거나 지우지 말고, 새 항목은 뒤에 붙이세요. 폐기할 때는 번호를 비워 두고 "폐기"라고 적습니다.
- **문서의 수치는 계산 결과입니다.** `AXES`·`LOGICAL_RULES`·`normative()`·`soft()`·`BMS`를 바꾸면 도구를 다시 돌리고 `README.md`, `docs/01`, `docs/03`, `docs/09`, `CHANGELOG.md`의 수치를 모두 고칩니다.
- **`LOGICAL_RULES` 순서를 바꾸지 마세요.** "첫 위반" 집계가 순서에 의존합니다.
- **프로파일은 세 곳에 있습니다**: `design_space.py`의 `PROFILES`, `examples/profiles.yaml`, README 표.
- **예시 구조를 바꾸면** `check_schemas.py`의 `CASES` 변형 경로가 조용히 어긋날 수 있습니다. 금지 문서 검사가 모두 `OK`인지 확인하세요.
- 본문은 한국어, 쉬운 말로 씁니다. 요구 수준은 반드시(MUST)·해야 함(SHOULD)·할 수 있음(MAY). 출처 없는 수치는 **설계 제안값**으로 표시합니다. 출처는 1차 출처를 우선합니다([docs/references.md](docs/references.md)).

## 이슈·PR

- 제목이나 본문에 해당 장과 규칙 id를 적어 주세요(예: `3.3 L7`, `I10`, `6.5 R2`).
- 규칙에 반대할 때는 그 규칙이 **잘못 거르는 조합 하나**를 `--profile`로 보여 주면 가장 빨리 논의됩니다.
- 큰 변경(새 축, 새 불변식, 스키마 계약 변경)은 먼저 이슈로 제안해 주세요. 반영되면 `CHANGELOG.md`에 기록합니다.

## 라이선스

기여한 내용은 저장소 라이선스를 따릅니다. 문서(`docs/`, `README.md` 등)는 CC BY 4.0([LICENSE-docs](LICENSE-docs)), 스키마·예시·도구(`schemas/`, `examples/`, `tools/`)는 Apache-2.0([LICENSE](LICENSE))입니다.
