# Archive.org

**Module ID:** `sfp_archiveorg`

## Summary

Identifies historic versions of interesting files/pages from the Wayback Machine.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://archive.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://archive.org/projects/, https://archive.org/services/docs/api/

## Routes

- **Route seed nugget:** `INTERESTING_FILE`
- **Consumed:**
- `INTERESTING_FILE`
- `URL_PASSWORD`
- `URL_FORM`
- `URL_FLASH`
- `URL_STATIC`
- `URL_JAVA_APPLET`
- `URL_UPLOAD`
- `URL_JAVASCRIPT`
- `URL_WEB_FRAMEWORK`
- **Produced:**
- `INTERESTING_FILE_HISTORIC`
- `URL_PASSWORD_HISTORIC`
- `URL_FORM_HISTORIC`
- `URL_FLASH_HISTORIC`
- `URL_STATIC_HISTORIC`
- `URL_JAVA_APPLET_HISTORIC`
- `URL_UPLOAD_HISTORIC`
- `URL_WEB_FRAMEWORK_HISTORIC`
- `URL_JAVASCRIPT_HISTORIC`

## Flags and categories

- **Flags:** slow
- **Categories:** Search Engines
- **Use cases:** Footprint, Passive

## Module options

- `farback` — Number of days back to look for older versions of files/pages in the Wayback Machine snapshots. Comma-separate the values, so for example 30,60,90 means to look for snapshots 30 days, 60 days and 90 days back.
- `flashpages` — Query the Wayback Machine for historic versions of URLs containing Flash.
- `formpages` — Query the Wayback Machine for historic versions of URLs with forms.
- `intfiles` — Query the Wayback Machine for historic versions of Interesting Files.
- `javapages` — Query the Wayback Machine for historic versions of URLs using Java Applets.
- `javascriptpages` — Query the Wayback Machine for historic versions of URLs using Javascript.
- `passwordpages` — Query the Wayback Machine for historic versions of URLs with passwords.
- `staticpages` — Query the Wayback Machine for historic versions of purely static URLs.
- `uploadpages` — Query the Wayback Machine for historic versions of URLs accepting uploads.
- `webframeworkpages` — Query the Wayback Machine for historic versions of URLs using Javascript frameworks.

## Test seeds

- `INTERESTING_FILE`: input=`https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf` validation=smoke status=FINISHED; verdict=hit; archive.org wayback produces URL_* historic nuggets

## Catalogue notes

Internet Archive is a non-profit library of millions of free books, movies, software, music, websites, and more.
The Internet Archive, a 501(c)(3) non-profit, is building a digital library of Internet sites and other cultural artifacts in digital form. Like a paper library, we provide free access to researchers, historians, scholars, the print disabled, and the general public. Our mission is to provide Universal Access to All Knowledge.
We began in 1996 by archiving the Internet itself, a medium that was just beginning to grow in use. Like newspapers, the content published on the web was ephemeral - but unlike newspapers, no one was saving it. Today we have 20+ years of web history accessible through the Wayback Machine and we work with 625+ library and other partners through our Archive-It program to identify important web pages.
