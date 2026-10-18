# Prompt Change Log

## Test setup
- Model: gemini-3.5-flash-lite
- Test cases: test_cases.json (20 cases)
- Runner: run_tests.py, 20 second gap between calls

## v1: prompts/v1_basic.txt
- Result: 7 of 20 passed (results_v1.json)
- Prompt: system instruction with one field list, no examples, no rules for role or null values.
- Schema at time of run: name and role were string only. Both were fixed after the run (see below).

### Failures and the v2 fix

**Role copied from the job description (cases 2, 11, 12, 13)**
- What happened: the model put phrases like "data internship", "data science", "product team", and "developer" into role.
- Why: the prompt never defined role, and these inputs have no job title.
- v2 fix: define role as the job title only, and use null when no title is given.

**Role kept "intern" (cases 6, 14, 15, 18, 20)**
- What happened: role came back as "Finance Intern", "UI/UX intern", "Backend Intern", and "Data Intern".
- Why: the prompt did not say to remove the word "intern".
- v2 fix: remove "intern", "internship", and "trainee" from role.

**Role not null when only "Intern" is given (case 16)**
- What happened: role came back as "Intern".
- Why: same as above. "Intern" is not a job title.
- v2 fix: a title-less role becomes null.

**Casing (case 10)**
- What happened: role came back as "marketing" while the expected value is "Marketing".
- Why: the prompt did not say how to format role.
- v2 fix: capitalise the first letter. 

**Schema too strict (cases 8 and 17, ValidationError)**
- What happened: the reply was valid, but the schema rejected null values, so the case was marked as an invalid output.
- Why: schema.json allowed only strings for name and role. This is a test-design bug, not a prompt failure.
- Fix: name was changed to ["string", "null"] during the v1 testing. role was changed to ["string", "null"] after the v1 run. v2 uses both fixes. The v1 score is therefore affected by the schema, and cases 8 and 17 should not count as model failures.

## v2 revision 1: prompts/v2_advanced.txt (start_date rule)

- Problem: case 1 returned start_date null for "starting 2 February 2027". Expected value is "2027-02-02".
- Why: the v2 rule said "YYYY-MM-DD only if a full, valid date is stated". The model read this as "only dates already written as YYYY-MM-DD count", so it dropped the date.
- Change: the start_date rule now says to convert any full date to YYYY-MM-DD, with an example. Dates with only a month or year, or invalid dates, still become null.
- Result: case 1 now returns "2027-02-02" when run on its own. The full v2 run passed 20 of 20 (see the end of the log).


## v2 revision 2: prompts/v2_advanced.txt (role rule)

- Problem: cases 11 and 13 put a skill or interest into role ("Analytics", "developer"). Expected value is null, since neither application names the role applied for.
- Why: the role rule only said "job title only", so the model inferred a title from skills and interests.
- Change: role must come from the role the applicant says they are applying for. Skills, interests, teams, and departments are excluded. Otherwise null.
- Result: run before this revision: 18 of 20 passed. Full run after revision 3: 20 of 20 passed.


## v2 revision 3: prompts/v2_advanced.txt (role casing)

- Problem: case 10 returned role "marketing" instead of "Marketing". The model passed on the previous run by chance.
- Change: role titles now start with a capital letter.
- Result: 20 of 20 passed (results_v2.json).