from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import httpx
from database import SessionLocal
from models import CotacaoDB

router = APIRouter(prefix="/cotacao", tags=["Cotação"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{moeda}")
async def obter_cotacao(moeda: str, db: Session = Depends(get_db)):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"

    async with httpx.AsyncClient() as client:
        resposta = await client.get(url)

    dados = resposta.json()
    chave = f"{moeda}BRL"
    valor = float(dados[chave]["bid"])

    nova_cotacao = CotacaoDB(moeda=moeda, valor=valor)
    db.add(nova_cotacao)
    db.commit()
    db.refresh(nova_cotacao)

    return {"moeda": moeda, "valor": valor}

from sqlalchemy import func

@router.get("/{moeda}/estatisticas")
def estatisticas_moeda(moeda: str, db: Session = Depends(get_db)):
    resultado = db.query(
        func.avg(CotacaoDB.valor),
        func.min(CotacaoDB.valor),
        func.max(CotacaoDB.valor),
        func.count(CotacaoDB.id)
    ).filter(CotacaoDB.moeda == moeda).first()

    media, minimo, maximo, total = resultado

    if total == 0:
        return {"mensagem": f"Nenhuma cotação registrada para {moeda} ainda"}

    return {
        "moeda": moeda,
        "media": round(media, 4),
        "minimo": minimo,
        "maximo": maximo,
        "total_registros": total
    }