# Example: Content extraction (`sfp_email`)

**Pattern:** `content_extract` (representative of `sfp_phone`, `sfp_hashes`, …)  
**Source:** `modules/sfp_email.py`

## Input

Watches page/content types (`TARGET_WEB_CONTENT`, `RAW_FILE_META_DATA`, etc.)

## Acquisition

No external API. Reads `event.data` (HTML/text) from upstream spider or fetch modules.

## Conversion

Uses `SpiderFeetHelpers.extractEmailsFromText()` (or regex over content) to find addresses, emits:

```python
SpiderFeetEvent("EMAILADDR", email, self.__name__, source_event)
evt.moduleDataSource = event.moduleDataSource  # attribute to page source
```

## Key pattern: data source attribution

Pure extractors set `moduleDataSource` from the **parent** event so the graph shows where the email was found, not “module sfp_email”.

## Generalisation

`ContentExtractorPlugin` base:

- `watchedEvents()` = content types
- `extract(text) -> Iterator[TypedObservation]`
- Shared dedup via `self.results`

New extractors (IBAN, crypto addresses) become thin wrappers over `helpers` functions.
