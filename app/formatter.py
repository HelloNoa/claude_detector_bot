from app.schemas import StatusPageWebhook

STATUS_EMOJI = {
    "operational": "\u2705",
    "degraded_performance": "\u26a0\ufe0f",
    "partial_outage": "\U0001f7e1",
    "major_outage": "\U0001f534",
    "under_maintenance": "\U0001f527",
    "investigating": "\U0001f50d",
    "identified": "\U0001f4cc",
    "monitoring": "\U0001f4c8",
    "resolved": "\u2705",
    "update": "\U0001f4dd",
}


def _emoji(status: str | None) -> str:
    return STATUS_EMOJI.get(status or "", "\u2139\ufe0f")


def format_message(payload: StatusPageWebhook) -> str:
    lines: list[str] = []

    if payload.incident:
        inc = payload.incident
        emoji = _emoji(inc.status)
        lines.append(f"{emoji} <b>[Incident] {inc.name}</b>")
        lines.append(f"Status: <b>{inc.status}</b> | Impact: {inc.impact}")

        if inc.incident_updates:
            latest = inc.incident_updates[0]
            lines.append(f"\n{latest.body}")

        if inc.shortlink:
            lines.append(f"\n<a href=\"{inc.shortlink}\">Details</a>")

    elif payload.component:
        comp = payload.component
        cu = payload.component_update
        old = cu.old_status if cu else "unknown"
        new = cu.new_status if cu else comp.status
        emoji = _emoji(new)
        lines.append(f"{emoji} <b>[Component] {comp.name}</b>")
        lines.append(f"{old} → <b>{new}</b>")

    else:
        lines.append("\u2139\ufe0f Status page updated")
        if payload.page:
            lines.append(f"{payload.page.status_description}")

    return "\n".join(lines)