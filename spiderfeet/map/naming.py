"""Kebab-case naming for TypeDB entity and relation labels."""


def kebab_case(identifier: str) -> str:
    """Convert SCREAMING_SNAKE or snake_case to kebab-case."""
    return identifier.lower().replace("_", "-")


def entity_type_for_nugget_id(nugget_id: str) -> str:
    """TypeDB entity label, e.g. INTERNET_NAME -> internet-name."""
    return kebab_case(nugget_id)


def relation_type_for_module_id(module_id: str) -> str:
    """TypeDB osint-service subtype, e.g. sfp_dnsresolve -> sfp-dnsresolve."""
    return kebab_case(module_id)
