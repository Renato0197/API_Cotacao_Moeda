from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from database import engine, Base
from routers import cotacoes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Cotação de Moedas")

templates = Jinja2Templates(directory="templates")

app.include_router(cotacoes.router)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")