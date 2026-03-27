from pydantic import BaseModel


class ComponentUpdate(BaseModel):
    created_at: str | None = None
    new_status: str | None = None
    old_status: str | None = None
    id: str | None = None


class Component(BaseModel):
    created_at: str | None = None
    id: str | None = None
    name: str | None = None
    status: str | None = None


class IncidentUpdate(BaseModel):
    body: str | None = None
    created_at: str | None = None
    display_at: str | None = None
    id: str | None = None
    incident_id: str | None = None
    status: str | None = None
    updated_at: str | None = None


class Incident(BaseModel):
    backfilled: bool | None = None
    created_at: str | None = None
    id: str | None = None
    impact: str | None = None
    incident_updates: list[IncidentUpdate] = []
    name: str | None = None
    shortlink: str | None = None
    status: str | None = None
    updated_at: str | None = None


class Page(BaseModel):
    id: str | None = None
    status_description: str | None = None
    status_indicator: str | None = None


class StatusPageWebhook(BaseModel):
    meta: dict | None = None
    page: Page | None = None
    component: Component | None = None
    component_update: ComponentUpdate | None = None
    incident: Incident | None = None