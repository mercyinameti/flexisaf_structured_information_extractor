# Pass and Fail Results

## v1: prompts/v1_basic.txt (7 of 20 passed)

| # | Category | Status | Reason |
|---|----------|--------|--------|
| 1 | normal | pass | |
| 2 | ambiguous | fail | role copied from text ("data internship") |
| 3 | normal | pass | |
| 4 | normal | pass | |
| 5 | normal | pass | |
| 6 | normal | fail | role kept "Intern" ("Finance Intern") |
| 7 | incomplete | pass | |
| 8 | incomplete | fail | schema rejected null name (ValidationError) |
| 9 | incomplete | pass | |
| 10 | incomplete | fail | role casing ("marketing" vs "Marketing") |
| 11 | ambiguous | fail | role copied from text ("data science") |
| 12 | ambiguous | fail | role copied from text ("product team") |
| 13 | ambiguous | fail | role copied from text ("developer") |
| 14 | malformed | fail | role kept "intern" ("UI/UX intern") |
| 15 | malformed | fail | role kept "Intern" ("Backend Intern") |
| 16 | malformed | fail | role should be null ("Intern") |
| 17 | adversarial | fail | schema rejected null fields (ValidationError) |
| 18 | adversarial | fail | role kept "Intern" ("Data Intern") |
| 19 | adversarial | pass | |
| 20 | adversarial | fail | role kept "Intern" ("Data Intern") |

## v2: prompts/v2_rules_and_examples.txt

| # | Category | Status | Reason |
|---|----------|--------|--------|
| 1 | normal | pass | |
| 2 | ambiguous | pass | |
| 3 | normal | pass | |
| 4 | normal | pass | |
| 5 | normal | pass | |
| 6 | normal | pass | |
| 7 | incomplete | pass | |
| 8 | incomplete | pass | |
| 9 | incomplete | pass | |
| 10 | incomplete | pass | |
| 11 | ambiguous | pass | |
| 12 | ambiguous | pass | |
| 13 | ambiguous | pass | |
| 14 | malformed | pass | |
| 15 | malformed | pass | |
| 16 | malformed | pass | |
| 17 | adversarial | pass | |
| 18 | adversarial | pass | |
| 19 | adversarial | pass | |
| 20 | adversarial | pass | |