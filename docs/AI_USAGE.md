# AI usage — factual draft for the group to review

## Tools actually used

OpenAI Codex in the Codex desktop app assisted with official-source research, local course-material reading, API retrieval, Python acquisition/integration/analysis code, SQL, source auditing, results interpretation, notebook, slide creation and speaking materials. No claim is made that the code was written without assistance. The notebook and presentation explicitly disclose this.

## Advantages observed

- Faster setup of a reproducible multi-source workflow and municipality harmonization.
- Help identifying unit/definition mismatches: station records versus physical masts, coverage versus observed speed, missing versus zero.
- Consistent generation of figures, audit tables and point-evidence mapping.
- Help adding proper held-out evaluation and sensitivity analyses.

## What did not work and corrections made

1. Initial Python commands failed because required libraries were missing. An isolated project environment was created; versions are recorded.
2. Initial system-Python HTTPS requests failed certificate verification. Retrieval used a correctly configured requests environment/curl; verification was not disabled.
3. A direct form-based BFS export returned an error page. The documented BFS REST API was used instead; CSV response format was detected correctly.
4. A naive join to current municipality codes left population missing and lost merger components. Official BFS correspondences fixed seven changed codes, and conservation of the population total is now asserted.
5. An initial no-station indicator was constant in the main sample and produced a singular predictor. It is now included only when variable in explanatory regressions.
6. A 100-test sensitivity sample had only two Intermediate and one Rural municipality. Those group-model estimates were removed; the coverage diagnostic is retained honestly.
7. Infrastructure-based predictions were weak on held-out cantons. No model was portrayed as successful merely because it fitted training data.

8. A repeated PostgreSQL notebook run initially failed because existing foreign keys prevented table replacement. The loader now recreates only the project tables in dependency order, and a full notebook rerun passed.
9. Initial slide images were not embedded correctly; the media-loading method was corrected and the PPTX was checked for embedded assets. PDF export used a checked office conversion after the initial exporter failed.

## Disadvantages and review responsibilities

AI can generate plausible methods or interpretation that do not match the available data. In particular, station density must not be equated with coverage, the 5G record share with 5G tests, nor association with causation. AI cannot know your personal experience or prove all members understand the work. Each member must review their parts, run the notebook, rehearse and add their actual experience. Do not invent a personal reflection or claim human verification that has not happened.

The initial planning message from Arthik is human-supplied context. Any earlier AI tools used by group members are unknown and should be added by the group. The public repository, formal approval, live presentation, MP4 recording and Moodle upload are not claimed as completed unless independently verified.
