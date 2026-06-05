from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import init_db
from app.routers import auth, companies, contacts, leads

app = FastAPI(title="OpenAffi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(contacts.router)
app.include_router(leads.router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    init_db()

@app.exception_handler(Exception)
async def error_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": "internal error"})
