import json
import sys
from pathlib import Path

from jsonschema import ValidationError

from extractor import parse_and_validate

SCHEMA = json.loads(Path("schema.json").read_text(encoding="utf-8"))


def check_reply(raw_text):
    """Return (True, data) if the reply matches the schema, otherwise (False, message)."""
    try:
        return True, parse_and_validate(raw_text, SCHEMA)
    except (json.JSONDecodeError, ValidationError) as error:
        return False, str(error).splitlines()[0]


def check_results_file(path):
    """Check every saved reply in a results file and print the ones that fail."""
    results = json.loads(Path(path).read_text(encoding="utf-8"))
    valid_count = 0
    for item in results:
        ok, detail = check_reply(item["reply"])
        if ok:
            valid_count += 1
        else:
            print(f"Case {item['id']}: invalid - {detail}")
    print(f"{valid_count} of {len(results)} replies match the schema")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_results_file(sys.argv[1])
    else:
        sample = '{"name": "Ada Obi", "university": "University of Uyo", "role": "Data Analyst", "start_date": "2027-02-02"}'
        ok, detail = check_reply(sample)
        print("Valid" if ok else f"Invalid: {detail}")