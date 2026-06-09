"""scan_ui target resolution for catalogue payload nuggets."""

from spiderfeet.api.services.scan_targets import resolve_scan_ui_seed, resolve_scan_ui_target


def test_payload_nugget_uses_anchor_and_seed():
    html = "<html><body>test@example.com</body></html>"
    anchor, typ, seed = resolve_scan_ui_seed("TARGET_WEB_CONTENT", html)
    assert typ == "INTERNET_NAME"
    assert anchor == "example.com"
    assert seed == ("TARGET_WEB_CONTENT", html)
    assert resolve_scan_ui_target("TARGET_WEB_CONTENT", html) == (anchor, typ)


def test_payload_nugget_webserver_headers():
    headers = "Server: nginx\r\nSet-Cookie: a=b"
    anchor, typ, seed = resolve_scan_ui_seed("WEBSERVER_HTTPHEADERS", headers)
    assert typ == "INTERNET_NAME"
    assert seed == ("WEBSERVER_HTTPHEADERS", headers)


def test_linked_url_internal_payload_seed():
    url = "https://example.com/path"
    anchor, typ, seed = resolve_scan_ui_seed("LINKED_URL_INTERNAL", url)
    assert typ == "INTERNET_NAME"
    assert anchor == "example.com"
    assert seed == ("LINKED_URL_INTERNAL", url)
