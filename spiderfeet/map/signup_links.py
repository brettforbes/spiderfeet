"""API key signup URL and bucket classification from OSINT catalogue."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from spiderfeet.map.subscriptions import subscription_tier_for_service

URL_RE = re.compile(r"https?://[^\s)\]\"']+")

MANUAL_HINTS = (
    "wait for",
    "few days",
    "contact",
    "request an api",
    "approval",
    "sales",
    "commercial",
    "email you",
    "write to",
)
SELF_REG_HINTS = (
    "register",
    "signup",
    "sign up",
    "sign-up",
    "create a free",
    "create an account",
    "free account",
)
CC_HINTS = ("credit card", "payment required", "paid plan", "purchase", "billing")

SignupBucket = str  # self-serve | review | manual | paid-risk


def _first_url(*parts: str) -> str:
    for part in parts:
        match = URL_RE.search(part or "")
        if match:
            return match.group(0).rstrip(".,;")
    return ""


def _classify_instructions(model: str, instructions: List[str]) -> Tuple[SignupBucket, str]:
    text = " ".join(instructions).lower()
    model_u = (model or "").upper()
    if "COMMERCIAL_ONLY" in model_u or "paid" in model_u.lower():
        return "paid-risk", "Catalogue marks commercial/paid — confirm a free tier before signing up."
    if any(h in text for h in CC_HINTS):
        return "paid-risk", "Instructions mention payment/billing — verify no card before signing up."
    if any(h in text for h in MANUAL_HINTS):
        return "manual", "Likely approval or email turnaround — not instant self-serve."
    if any(h in text for h in SELF_REG_HINTS) or "FREE_AUTH" in model_u:
        return "self-serve", "Self-registration steps documented in catalogue."
    if instructions:
        return "review", "Has instructions — open link and confirm signup is free with no card."
    return "review", "No step-by-step instructions — check provider site."


def signup_metadata(service: Dict[str, Any]) -> Dict[str, Any]:
    """Derive signup_url, signup_bucket, and signup_note for a catalogue service."""
    tier = subscription_tier_for_service(service)
    data_source = service.get("data_source") or {}
    instructions_raw = data_source.get("api_key_instructions") or []
    if isinstance(instructions_raw, str):
        instructions = [instructions_raw]
    else:
        instructions = [str(x) for x in instructions_raw]
    model = str(data_source.get("model") or "")
    website = str(data_source.get("website") or "")
    signup_url = _first_url(" ".join(instructions), website)

    if tier == "paid_auth":
        bucket: SignupBucket = "paid-risk"
        note = "Paid tier module — skip unless you accept paid signup."
    else:
        bucket, note = _classify_instructions(model, instructions)

    return {
        "signup_url": signup_url or website or None,
        "signup_bucket": bucket,
        "signup_note": note,
    }
