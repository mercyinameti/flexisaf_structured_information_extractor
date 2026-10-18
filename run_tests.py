import json
import time
from pathlib import Path

from jsonschema import ValidationError

from extractor import extract, parse_and_validate

SCHEMA = json.loads(Path("schema.json").read_text(encoding="utf-8"))
CASES = json.loads(Path("test_cases.json").read_text(encoding="utf-8"))
PROMPT = "prompts/v2_advanced.txt"
RESULTS_FILE = "results_v2.json"
MAX_TRIES = 3
PAUSE = 20  # seconds between cases, to stay under the per-minute limit


def run_case(case):
    """Run one test case, retrying if the API call itself fails."""
    last_error = ""
    for attempt in range(1, MAX_TRIES + 1):
        try:
            raw = extract(case["input"], PROMPT)
            break
        except Exception as error:
            last_error = str(error)
            if attempt < MAX_TRIES:
                time.sleep(PAUSE)
    else:
        return {"status": "error", "reply": last_error, "reason": "API call failed"}

    try:
        data = parse_and_validate(raw, SCHEMA)
    except (json.JSONDecodeError, ValidationError) as error:
        return {"status": "fail", "reply": raw, "reason": f"invalid output ({error.__class__.__name__})"}

    if data == case["expected"]:
        return {"status": "pass", "reply": raw, "reason": ""}
    return {"status": "fail", "reply": raw, "reason": "does not match expected"}


def save(results):
    """Write everything so far, so a stopped run keeps its results."""
    Path(RESULTS_FILE).write_text(json.dumps(results, indent=2), encoding="utf-8")


def main():
    results = []
    for case in CASES:
        result = run_case(case)
        result["id"] = case["id"]
        result["category"] = case["category"]
        result["expected"] = case["expected"]
        results.append(result)
        save(results)
        print(f"{case['id']:>2}  {case['category']:<12} {result['status']:<6} {result['reason']}", flush=True)
        time.sleep(PAUSE)

    passed = sum(r["status"] == "pass" for r in results)
    print(f"\n{passed} of {len(results)} passed")
    print(f"Full replies and expected answers saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()