from app.routers import auth, workspaces, integrations, public, services, inventory, forms, staff, conversations, dashboard
from app.services import automation

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.on_event("startup")
async def startup_event():
    automation.start_automation()

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}", tags=["auth"])
app.include_router(workspaces.router, prefix=f"{settings.API_V1_STR}/workspaces", tags=["workspaces"])
app.include_router(integrations.router, prefix=f"{settings.API_V1_STR}/workspaces", tags=["integrations"])
app.include_router(services.router, prefix=f"{settings.API_V1_STR}/workspaces/services", tags=["services"])
app.include_router(inventory.router, prefix=f"{settings.API_V1_STR}/workspaces/inventory", tags=["inventory"])
app.include_router(forms.router, prefix=f"{settings.API_V1_STR}/workspaces/forms", tags=["forms"])
app.include_router(staff.router, prefix=f"{settings.API_V1_STR}/workspaces/staff", tags=["staff"])
app.include_router(conversations.router, prefix=f"{settings.API_V1_STR}/workspaces/conversations", tags=["conversations"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/workspaces/dashboard", tags=["dashboard"])
app.include_router(public.router, prefix=f"{settings.API_V1_STR}/public", tags=["public"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CareOps API"}
