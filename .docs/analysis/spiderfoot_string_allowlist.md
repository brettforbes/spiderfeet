# SpiderFoot string allowlist (post #17)

Intentional `spiderfoot` / `SpiderFoot` literals retained after Stage 1 string rebrand.
Used as input for X-01-03 grep sign-off.

## Upstream URLs and assets

- `github.com/smicallef/spiderfoot` — upstream fork attribution in README badges and About modal
- `twitter.com/spiderfoot` — upstream social links
- `asciinema.org/~spiderfoot` — upstream CLI tutorials
- `spiderfoot-wide.png` — CDN image path on spiderfeet.net (until #21 logo work)

## Vendor / API contracts

- `greynoise-spiderfoot` / `greynoise-spiderfoot-community` — GreyNoise API user-agent strings

## Test fixtures

- `linkedin.com/in/spiderfoot` — sample social profile URL in unit tests

## Python code identifiers (not user-facing strings)

- `SpiderFoot`, `SpiderFootPlugin`, `SpiderFootEvent`, etc. — internal class/API names (rename deferred)

## Docker / ops (deferred)

- Docker service name `spiderfoot`, user `spiderfoot`, volume paths — operational rename deferred
