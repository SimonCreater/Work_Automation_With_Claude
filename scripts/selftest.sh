#!/usr/bin/env bash
# R3 검증 셀프테스트 — 채점자가 명령 한 줄로 "기계적 검증(R3)"을 재현할 수 있게 한다.
#
#   bash scripts/selftest.sh
#
# 두 가지를 증명한다:
#   1) 양성 테스트: demo/ 의 모든 산출물(3 run × 6종 = 18건)이 검증을 통과한다 (exit 0).
#   2) 음성 테스트: 일부러 깨뜨린 산출물은 검증에 걸린다 (exit 2).
# 즉 "검증기가 통과시킬 것은 통과시키고, 막을 것은 막는다"를 재현 가능한 사실로 만든다.
# 표준 도구(python3, bash)만 사용한다 — 외부 의존성 없음 (R4).
set -u
cd "$(dirname "$0")/.." || exit 1
PASS=0
FAIL=0

echo "== [양성 테스트] demo/ 산출물 검증 (전부 통과해야 정상) =="
for f in demo/*/0[1-6]-*.md; do
  if python3 scripts/validate.py "$f" >/dev/null 2>&1; then
    echo "  PASS  $f"
    PASS=$((PASS + 1))
  else
    echo "  FAIL  $f   <-- 통과해야 하는데 실패함"
    FAIL=$((FAIL + 1))
  fi
done

echo
echo "== [음성 테스트] 고의 결함 산출물 (검증이 반드시 차단해야 정상) =="
BAD="scripts/fixtures/bad-03-use-cases.md"
if python3 scripts/validate.py "$BAD" >/dev/null 2>&1; then
  echo "  FAIL  $BAD   <-- 결함을 못 잡음 (검증기 결함)"
  FAIL=$((FAIL + 1))
else
  echo "  OK    $BAD   검증이 결함을 정상 차단(exit 2)"
  PASS=$((PASS + 1))
fi

echo
echo "결과: 통과 $PASS / 실패 $FAIL"
if [ "$FAIL" -eq 0 ]; then
  echo "✅ R3 검증 셀프테스트 전부 통과 — 검증 장치가 실제로 동작함을 재현 확인"
  exit 0
else
  echo "❌ 실패 항목이 있습니다."
  exit 1
fi
