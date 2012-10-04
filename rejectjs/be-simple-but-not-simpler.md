# Be simple, but not simpler
## by Pavel Filippov

Pull-request based workflow.

### Attitude

Be consistent.

Be fair.

Be lazy.

Boyscout rule.

### Design

Separate anonymous functions.

Stick to known patterns, favor readability over cleverness.

### Code

Wrap native methods and types for cross-browser code (underscore.js).

#### No

- `window.location`
- Raw AJAX calls
- Inline CSS and HTML
- i18n and l10n specific data

### Workflow

Keep history clean.

Embrace `git rebase -i`

Reject simple merge

Embrace `git pull --rebase`

Comments on diffs

#### What should be automated

Formatting conventions

Linters

Continuous Integration
