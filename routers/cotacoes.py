from fastapi import APIRouter, Depends, HTTPException
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
    moeda = moeda.upper()
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"

    # 1. Tenta chamar a AwesomeAPI
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resposta = await client.get(url)
    except httpx.RequestError as erro:
        raise HTTPException(
            status_code=502,
            detail=f"Não foi possível acessar a AwesomeAPI: {erro}",
        )

    # 2. Tenta ler a resposta como JSON
    try:
        dados = resposta.json()
    except ValueError:
        dados = {}

    # 3. Confere se a resposta tem a cotação que esperamos
    chave = f"{moeda}BRL"
    if resposta.status_code != 200 or chave not in dados:
        print("Resposta inesperada da AwesomeAPI:", resposta.status_code, resposta.text[:300])
        raise HTTPException(
            status_code=502,
            detail=f"A AwesomeAPI não retornou a cotação de {moeda} (status {resposta.status_code})",
        )

    valor = float(dados[chave]["bid"])

    # 4. Salva no banco e responde (igual ao que já existia)
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