#!/usr/bin/env python3
"""
산출물 기계적 검증기 (R3).

두 가지 방식으로 호출된다:
  1) 단독 실행:   python3 scripts/validate.py demo/run1/01-system-request.md
  2) Claude Code PostToolUse(Write) Hook: stdin 으로 JSON({"tool_input":{"file_path":...}})

파일명으로 schemas/*.schema.json 중 하나를 매칭하고, 그 스키마의 규칙을 검사한다.
산출물이 아니면(매칭 스키마 없음) 조용히 통과한다.

위반이 있으면 stderr 로 위반 항목을 출력하고 exit code 2 로 종료한다.
(Claude Code 에서 exit 2 는 호출을 차단하고 stderr 를 에이전트에게 피드백한다.)
표준 라이브러리만 사용하므로 어떤 환경에서도 의존성 없이 동작한다 (R4).
"""
import json
import os
import re
import sys

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas")


def get_target_path():
    """인자가 있으면 그것을, 없으면 stdin 의 hook payload 에서 file_path 를 얻는다."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    try:
        data = json.load(sys.stdin)
    except Exception:
        return None
    return (data.get("tool_input") or {}).get("file_path")


def load_schema_for(path):
    """파일명에 'match' 문자열이 포함되는 스키마를 찾아 반환. 없으면 None."""
    if not os.path.isdir(SCHEMA_DIR):
        return None
    base = os.path.basename(path)
    for fname in sorted(os.listdir(SCHEMA_DIR)):
        if not fname.endswith(".schema.json"):
            continue
        with open(os.path.join(SCHEMA_DIR, fname), encoding="utf-8") as f:
            schema = json.load(f)
        if schema.get("match") and schema["match"] in base:
            return schema
    return None


def check(schema, content):
    """스키마를 적용해 위반 메시지 리스트를 반환한다."""
    violations = []

    for section in schema.get("required_sections", []):
        if section not in content:
            violations.append(f"필수 섹션 누락: '{section}'")

    for rule in schema.get("rules", []):
        rtype = rule.get("type")
        if rtype == "no_placeholders":
            if "{{" in content or "}}" in content:
                violations.append(
                    "채워지지 않은 템플릿 placeholder('{{ }}')가 남아 있습니다. 모두 실제 내용으로 대체하세요."
                )
        elif rtype == "must_contain":
            if not re.search(rule["pattern"], content):
                violations.append(rule.get("message", f"필수 패턴 누락: {rule['pattern']}"))
        elif rtype == "min_pattern_count":
            found = len(re.findall(rule["pattern"], content))
            if found < rule.get("min", 1):
                violations.append(
                    f"{rule.get('message', rule['pattern'])} (현재 {found}건)"
                )
    return violations


def main():
    path = get_target_path()
    if not path or not path.endswith(".md") or not os.path.isfile(path):
        sys.exit(0)  # 산출물 파일이 아니면 통과

    schema = load_schema_for(path)
    if schema is None:
        sys.exit(0)  # 매칭되는 스키마 없음 → 검증 대상 아님

    with open(path, encoding="utf-8") as f:
        content = f.read()

    violations = check(schema, content)

    if violations:
        artifact = schema.get("artifact", "artifact")
        sys.stderr.write(
            f"[검증 실패] {os.path.basename(path)} ({artifact}) — {len(violations)}건 위반:\n"
        )
        for v in violations:
            sys.stderr.write(f"  - {v}\n")
        sys.stderr.write("위 항목을 수정한 뒤 다시 저장하세요. 통과 전에는 다음 단계로 진행하지 않습니다.\n")
        sys.exit(2)

    print(f"[검증 통과] {os.path.basename(path)} ({schema.get('artifact')})")
    sys.exit(0)


if __name__ == "__main__":
    main()
