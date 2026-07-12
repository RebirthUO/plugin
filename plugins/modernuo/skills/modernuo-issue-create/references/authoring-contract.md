# Issue Intake Contract

Use this contract only after the parent skill verifies the repository declared
by the consuming project's applicable `AGENTS.md`.

## Live template ownership

The verified repository's current YAML issue forms are authoritative. Do not
keep a static form list, title prefix, label list, option list, or required-field
map in this skill. Select one form from the primary player-visible object and
preserve its field labels and order exactly. Split independent deliverables
instead of blending forms.

When maintaining a form, prefer class-level forms and capture only fields that
the repository genuinely requires. Template maintenance is a separate mutation
from creating an issue and requires explicit authorization.

## Intake boundary

Phase 1 records what the user already knows:

- goal and player/operator problem;
- observed and desired outcomes;
- named era, ruleset, facet, or system when supplied;
- user-supplied source links and policy decisions;
- explicit non-goals;
- enough reproduction or context to identify the request.

Do not research formulas, dates, canonical mechanics, implementation anchors,
or side effects here. For each missing behavior-changing field, add:

```text
RESEARCH_REQUIRED[Rn]: <claim or decision>
Why it matters: <behavior, era, scope, persistence, economy, client, or test risk>
```

Never substitute a likely interpretation. Community sites, emulator code,
ModernUO code, and local repository behavior are not official UO evidence.

## IntakePacket

```yaml
repository:
  full_name: owner/repository
  html_url: https://github.com/owner/repository
  instruction_file: path/to/AGENTS.md
  verified_at: ISO-8601
template:
  path: .github/ISSUE_TEMPLATE/example.yml
  ref: verified default-branch revision
title: English title with live prefix
labels: []
body: complete English body
research_required:
  - id: R1
    field: exact live form field
    question: missing claim or decision
    risk: why guessing would be unsafe
duplicate_check:
  result: clear | blocked
  matches: []
mutation:
  authorized: false
  performed: []
issue:
  number: null
  url: null
  updated_at: null
  body_digest: null
```

## Publication checks

1. Search exact and near-neighbor terms across open and closed issues.
2. Confirm every configured/requested label exists.
3. Validate English title/body, exact live prefix and field order, links, and
   absence of local paths and secrets.
4. Create once with the exact repository argument.
5. Read back repository, number, URL, title, labels, body, and revision.
6. After an ambiguous result, search for the exact title/body before retrying.

Creating an issue does not authorize comments, edits, labels, relationships,
projects, milestones, implementation, commits, pushes, or pull requests.
