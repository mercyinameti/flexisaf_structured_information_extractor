# Failure Analysis

## Summary
- v1 passed 7 of 20. v2 passed 20 of 20 on the final run.
- The v1 failures came from three problems: the prompt never defined `role`, the schema rejected valid nulls, and the output format was not fixed.
- v2 fixed the prompt issues with explicit rules for `role` and `start_date`. Two of the v1 failures came from the schema, not the model.

## What v1 got wrong
1. **Role taken from the job description (cases 2, 11, 12, 13).** The prompt never said what `role` means, so the model copied phrases such as "data science" or "developer" from the text.
2. **Role kept the word "intern" (cases 6, 14, 15, 18, 20).** The prompt did not say to remove it.
3. **Role not null for a title-less input (case 16).** "Intern" was returned as the role.
4. **Casing (case 10).** "marketing" instead of "Marketing".
5. **Schema rejected nulls (cases 8 and 17).** The schema allowed only strings for `name` and `role`. These are test-design failures, not model failures.

## What changed in v2
- `role` is defined as the job title the applicant says they are applying for. Words like "intern" are removed, and skills, teams, and interests are excluded (revisions 2 and 3).
- `start_date` converts any full date to YYYY-MM-DD (revision 1).
- Each rule has a matching example or case in the test set.

## Remaining weaknesses
- **Single runs.** The model's wording varies between runs. Case 10 passed on one run and failed on another before the casing rule was added. A 20 of 20 result is one sample.
- **Tuned on the same cases.** The v2 rules were written after looking at these 20 failures, so the 20 of 20 result does not show the prompt works on new applications.
- **Changed two things at once.** v2 changed the prompt and the schema, so the gain cannot be credited to the prompt alone.
- **Fictional data.** All 20 cases are invented, so real applications may have formats the test set does not cover.
