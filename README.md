# Spec-Driven 분석·설계 하네스

[![validate-artifacts](https://github.com/SimonCreater/Work_Automation_With_Claude/actions/workflows/validate.yml/badge.svg)](https://github.com/SimonCreater/Work_Automation_With_Claude/actions/workflows/validate.yml)

**아이디어 한 문단**만 가진 사용자와 에이전트가 협의(인터뷰)하여, 시스템 분석·설계
산출물을 **단계별 승인 게이트**를 거쳐 생성하고, **기계적으로 검증**하는 재사용 가능한 하네스입니다.
특정 도메인에 하드코딩되어 있지 않아, 어떤 아이디어에도 수정 없이 동작합니다.

> GitHub Spec Kit / AWS Kiro 같은 Spec-Driven Development 도구의 아이디어를,
> 표준 분석·설계 산출물(유스케이스·DFD·ERD)에 맞춰 구현했습니다.

---

## 평가자 안내 (채점 매핑)

> 각 평가 항목의 증적이 **어느 파일에 있는지** 바로 찾을 수 있도록 정리했습니다.
> R3(기계적 검증)은 아래 한 줄로 **직접 재현**할 수 있습니다:
> ```bash
> bash scripts/selftest.sh      # demo 산출물 18종 통과 + 고의 결함 1건 차단(exit 2) 재현
> ```

| 평가 항목 | 증적 위치 |
|---|---|
| **R1** 에이전트가 먼저 묻는다 | [`demo/run1-equity-research/00-session-log.md`](demo/run1-equity-research/00-session-log.md) — 매 단계 에이전트 선질문 축어 기록 |
| **R2** 단계별 생성 + 승인 게이트 | 같은 로그의 S1~S6 각 끝 `[승인 게이트]` → 사용자 `승인` 교환 (6회) |
| **R3** 기계적 검증 (실패→자가수정 포함) | 같은 로그 **S3** — 훅 stderr 원문(예외흐름 누락 차단) → 수정 → 통과. 재현: `scripts/selftest.sh`, CI: [`.github/workflows/validate.yml`](.github/workflows/validate.yml) |
| **R4** 재사용성 | 하네스 무수정으로 3개 도메인 재적용(run1 주식 / run2 헬스장 / run3 여신) + [`demo/run2-gym-pt/99-retrospective.md`](demo/run2-gym-pt/99-retrospective.md) 회고 |
| **산출물 5종** | `demo/run1-equity-research/01~06` (요청서·요구사항·유스케이스·DFD·ADR + **보너스 ERD**) |
| **ADR("하지 않기로 한 결정")** | [`demo/run1-equity-research/06-adr.md`](demo/run1-equity-research/06-adr.md) — 목표주가 자동산정 제외 |

### 이론 ↔ 구현 매핑 (이론 + 실습)

산출물과 **검증 규칙**을 수업 이론에 1:1로 앵커링했습니다. 검증기는 형식뿐 아니라
각 이론의 핵심 규칙(예: 유스케이스는 예외 흐름 필수)을 기계적으로 강제합니다.

| 산출물 / 검증 규칙 | 이론 개념 | 교재 |
|---|---|---|
| 유스케이스 — **예외/대안 흐름 필수**, 액터·트리거·사전/사후조건 | 유스케이스·시나리오 모델링 | ch04 |
| DFD — 컨텍스트+Level 0, 프로세스(동사구)·외부엔티티·데이터 스토어 | 프로세스 모델링(DFD) | ch05 |
| ERD — 엔티티·PK·카디널리티, **DFD 데이터 스토어와 대응** | 데이터 모델링(ERD) | ch06 |
| 시스템 요청서·요구사항(검증 가능 서술)·ADR | 분석 단계 산출물 / 설계 의사결정 기록 | 강의 전반 |

---

## 30분 안에 내 아이디어로 첫 협의 시작하기

### 0. 사전 준비 (약 2분)
- [Claude Code](https://claude.com/claude-code)가 설치되어 있어야 합니다.
- Python 3 이 있어야 합니다(검증 훅 실행용). 외부 패키지는 필요 없습니다.

### 1. 이 리포에서 Claude Code 실행 (약 1분)
```bash
git clone <this-repo>
cd <this-repo>
claude
```
프로젝트 루트의 `.claude/CLAUDE.md`(운영지침)와 `.claude/settings.json`(검증 훅)이 자동으로 로드됩니다.

### 2. 아이디어 한 문단 던지기 (약 1분)
양식을 채울 필요 없이, 그냥 말하면 됩니다:
```
"종목명만 넣으면 공시·실적·뉴스를 요약해 리서치 메모 초안을 만들어주는 도구를 만들고 싶어"
```
에이전트가 `spec-pipeline` 스킬로 **먼저 질문을 시작**합니다. (R1)

### 3. 단계별로 답하며 진행 (약 20분)
산출물은 정해진 순서로 생성됩니다. 각 단계에서 에이전트가 2~4개 질문을 하고,
답을 모아 산출물을 만든 뒤 **검증을 통과시키고**, 당신에게 **승인을 요청**합니다. (R2, R3)

| 순서 | 산출물 |
|---|---|
| S1 | 시스템 요청서 |
| S2 | 요구사항 정의 (기능 + 비기능) |
| S3 | 유스케이스 2건 (정상 + 예외 흐름) |
| S4 | 구조 다이어그램 / DFD |
| S5 | ERD |
| S6 | ADR 2건+ ("하지 않기로 한 결정" 포함) |

승인하기 전에는 다음 단계로 넘어가지 않습니다. 진행/단계 확인은 `/next-stage` 커맨드로도 가능합니다.

### 4. 결과 확인 (약 1분)
산출물 6종이 `demo/<run>/` 아래에 마크다운으로 모입니다. 다이어그램은 Mermaid라
GitHub에서 바로 렌더링됩니다.

---

## 작동 방식 (제약 R1~R4 대응)

| 제약 | 구현 |
|---|---|
| **R1** 에이전트가 먼저 묻는다 | `spec-pipeline` 스킬이 빈 양식 대신 단계별 질문을 먼저 던짐 |
| **R2** 단계별 생성 + 승인 게이트 | S1→…→S6 순서, 각 단계 끝에서 명시적 사용자 승인 요구 |
| **R3** 기계적 검증 | `PostToolUse(Write)` 훅 → `scripts/validate.py`가 스키마 준수를 자동 검사 |
| **R4** 재사용성 | 템플릿·스키마·질문에 도메인 하드코딩 없음. 모든 값은 인터뷰에서 주입 |

### 자동화 2종
- **자동화① 파이프라인**: `.claude/skills/spec-pipeline/` (협의→산출물 구동)
- **자동화② 검증**: `.claude/settings.json` 훅 + `scripts/validate.py` (R3)

### 자동화 vs 비자동화 경계
- 자동화: 단계 진행, 템플릿 채우기, 형식·구조 규칙 검증
- 비자동화(사람): 아이디어 입력, 각 산출물 **내용 승인**, 도메인 사실 확인

---

## 리포 구조

```
.claude/
  CLAUDE.md                 # 운영지침 (역할·협의 규칙·단계·자동/비자동 경계)
  settings.json             # 검증 훅 등록 (PostToolUse: Write/Edit)
  skills/spec-pipeline/     # 자동화① 파이프라인 스킬
  commands/next-stage.md    # 단계 진행/승인 게이트 커맨드
templates/                  # 산출물 6종 템플릿 (도메인 비종속)
schemas/                    # 산출물별 검증 스키마 (JSON)
scripts/validate.py         # 자동화② 검증기 (표준 라이브러리만 사용)
scripts/selftest.sh         # R3 재현 셀프테스트 (양성 18 + 음성 1)
scripts/fixtures/           # 음성 테스트용 고의 결함 산출물
.github/workflows/          # CI: push마다 검증 셀프테스트 자동 실행
demo/
  run1-equity-research/     # 아이디어①(주식 리서치): 세션 로그 + 산출물 6종
  run2-gym-pt/              # 아이디어②(헬스장 PT): 무수정 재적용 + 회고
  run3-credit-memo/         # 아이디어③(기업 여신): 무수정 재적용
```

## 데모로 보는 실제 동작 (run3 — 기업 여신, 금융 도메인)

하네스를 **한 글자도 수정하지 않고** 세 번째 도메인에 적용해 전체 흐름을 검증한 사례입니다.
(run1=주식 리서치, run2=헬스장 PT와 도메인이 완전히 다름 → R4 입증)

- **입력 아이디어 한 문단**: "중소 제조업 여신 심사역을 위해, 3개년 재무제표와 산업 동향을 입력받아
  신용등급 의견·리스크 요인·근거 출처가 포함된 신용메모 초안을 생성하고, 심사역이 단계별로 승인하는 도구."
- **진행**: 에이전트가 먼저 질문(R1) → S1~S6를 순서대로 생성, 각 단계에서 검증 통과 후 승인 게이트(R2)
- **결과**: 산출물 6종 모두 `scripts/validate.py` 검증 **통과(6/6)**. 예시 산출물:
  - 요구사항: 기능(FR-1~4) + 비기능(성능 90초 이내 / 망분리 보안 / 판단경로 100% 추적)
  - 유스케이스: 초안 생성 · 단계별 승인 2건 (각각 정상 + 예외 흐름)
  - DFD: 프로세스 3개(재무지표 산출·초안 생성·승인 처리), 데이터 스토어 D1~D3
  - ERD: REVIEW_CASE / FINANCIAL_METRIC / MEMO_VERSION / APPROVAL_LOG (DFD 데이터 스토어와 정합)
  - ADR: "근거 출처 의무 부착" / **"최종 등급 확정·여신 승인은 자동화하지 않는다"(하지 않기로 한 결정)**

전체 세션 흐름은 [`demo/run3-credit-memo/00-session-log.md`](demo/run3-credit-memo/00-session-log.md)에서 볼 수 있습니다.

## 검증기 단독 실행 / R3 재현

훅 없이도 산출물을 직접 검사할 수 있습니다:
```bash
python3 scripts/validate.py demo/run1-equity-research/03-use-cases.md
```
위반이 있으면 항목을 출력하고 종료 코드 2로 끝납니다.

R3(기계적 검증)이 실제로 동작함을 **한 번에 재현**하려면:
```bash
bash scripts/selftest.sh
```
- **양성 테스트**: `demo/` 산출물 18종이 전부 검증을 통과(exit 0)
- **음성 테스트**: 고의로 예외 흐름을 뺀 산출물(`scripts/fixtures/bad-03-use-cases.md`)이 검증에 차단(exit 2)

이 셀프테스트는 push마다 GitHub Actions로도 자동 실행됩니다(상단 배지).
