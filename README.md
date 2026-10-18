# Structured Information Extractor

A prompt-driven app that reads an internship application as plain text and returns a JSON object with four fields: `name`, `university`, `role`, and `start_date`. The output is checked against a JSON Schema.

Test data is fictional.

## Files
- `extractor.py`: sends one application to the Gemini API and validates the reply.
- `run_tests.py`: runs all 20 test cases, saves the replies, and prints a pass or fail for each case.
- `check_connection.py`: sends one short message to confirm the API key and model work.
- `prompts/v1_basic.txt`: first prompt version.
- `prompts/v2_advanced.txt`: final prompt version.
- `schema.json`: the JSON Schema the output must match.
- `test_cases.json`: 20 test cases (normal, incomplete, ambiguous, malformed, adversarial).
- `results_v1.json`, `results_v2.json`: saved replies from each test run.
- `PROMPT_CHANGELOG.md`: what changed in each prompt version and why.
- `RESULTS_TABLE.md`: pass and fail table for v1 and v2.
- `FAILURE_ANALYSIS.md`: what failed in v1 and what v2 fixed.
- `RISKS_AND_LIMITATIONS.md`: known risks and limits.

## Setup
1. Install Python 3.10 or newer.
2. Install the packages:
```
   pip install -r requirements.txt
```
3. Get a Gemini API key from Google AI Studio.
4. Copy `.env.example` to a new file named `.env`, then put your key after the equals sign:
```
   GEMINI_API_KEY=your-key-here
```
   Never commit `.env`. It is listed in `.gitignore`.

## Running the app
Check the connection first:
```
python check_connection.py
```
It prints a short reply if the key and model work.

Run the test suite:
```
python run_tests.py
```
This sends each of the 20 cases to the model, waiting 20 seconds between calls to stay within the free-tier limit. It takes about 7 minutes. Each case prints one line with its status. At the end it prints the number passed and saves the full results to `results_v2.json` (or the file named in `RESULTS_FILE`).

Do not press Ctrl+C during the run, because the results are only saved at the end.

## Model
Both prompt versions use `gemini-3.5-flash-lite`. The model is set on the first line of `extractor.py` (`MODEL`). Keep it the same when comparing prompt versions.

## Results
| Version | Passed | Notes |
|---|---|---|
| v1 (`v1_basic.txt`) | 7 of 20 | Partial schema: role and name did not accept null during the run. See `FAILURE_ANALYSIS.md`. |
| v2 (`v2_advanced.txt`) | 20 of 20 | Final run after three revisions. See `PROMPT_CHANGELOG.md`. |

The results come from one run per version. Replies can vary between runs, and v2 was tuned on the same 20 cases.
