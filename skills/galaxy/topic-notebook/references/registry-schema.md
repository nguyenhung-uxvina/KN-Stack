# Topic-Notebook Registry Schema

Location: `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` — append/update only.

Entry format (one `##` section per notebook):

    ## <alias>
    - nlm_id: <uuid>
    - url: https://notebooklm.google.com/notebook/<uuid>
    - scope: <1-line what questions this notebook answers>
    - source_count: <n> (tiers: S:<n> A:<n> B:<n> C:<n> | unknown for registered legacy)
    - persona: reference-mode | mentor-mode (shared with mentor-<name>)
    - status: active | retired
    - created: YYYY-MM-DD · last_refresh: YYYY-MM-DD
    - pinned_projects: [<project-ids or —>]

Rules: alias = kebab-case, unique; date format absolute; retired entries keep their section.
