# API de Cotação de Moedas
API REST em Python que consulta cotações de moedas em tempo real, salva cada consulta em um banco de dados e calcula estatísticas (média, mínimo e máximo) a partir do histórico coletado.
**API no ar:** `[<URL-DA-SUA-API>](https://api-cotacao-moeda.onrender.com/)` (documentação interativa em `/docs`)
> Observação: a API está hospedada em um plano gratuito, então a primeira requisição depois de um período sem uso pode demorar alguns segundos para responder.

## Tecnologias
- **FastAPI**: framework da API e documentação automática (Swagger)
- **SQLAlchemy**: acesso ao banco de dados
- **PostgreSQL (Neon)** em produção e **SQLite** no desenvolvimento local
- **httpx**: chamadas assíncronas à API externa
- **Jinja2**: página inicial
- **AwesomeAPI**: fonte das cotações
- **Render**: hospedagem

## Rotas
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Página inicial explicando a API |
| GET | `/cotacao/{moeda}` | Busca a cotação atual da moeda em reais, salva no histórico e devolve o valor |
| GET | `/cotacao/{moeda}/estatisticas` | Calcula média, mínimo, máximo e total de registros do histórico da moeda |
| GET | `/docs` | Documentação interativa (Swagger UI) |

Use o código da moeda em letras maiúsculas, por exemplo `USD`, `EUR` ou `GBP`.
### Exemplo de uso
```python
import requests

url = "<URL-DA-SUA-API>/cotacao/USD"
resposta = requests.get(url)

print(resposta.json())
```

Resposta de `GET /cotacao/GBP`:
```json
{
  "moeda": "GBP",
  "valor": 6.89481
}
```

Resposta de `GET /cotacao/USD/estatisticas`:
```json
{
  "moeda": "USD",
  "media": 5.2107,
  "minimo": 5.1846,
  "maximo": 5.2291,
  "total_registros": 8
}
```

Se a AwesomeAPI não estiver disponível ou não devolver a cotação pedida, a API responde com status `502` e uma mensagem explicando o motivo.

## Estrutura do projeto
```
.
├── main.py              # cria a aplicação e conecta os routers
├── database.py          # configuração da conexão com o banco
├── models.py            # tabela de cotações (SQLAlchemy)
├── routers/
│   ├── __init__.py
│   └── cotacoes.py      # rotas de cotação e estatísticas
├── templates/
│   └── index.html       # página inicial
└── requirements.txt
```

## Como rodar localmente
1. Clone o repositório e entre na pasta:
   ```bash
   git clone <URL-DO-REPOSITORIO>
   cd <PASTA-DO-PROJETO>
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. (Opcional) Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo.

5. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```

6. Acesse `http://127.0.0.1:8000` (página inicial) ou `http://127.0.0.1:8000/docs` (documentação).

## Variáveis de ambiente
| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DATABASE_URL` | Não | URL de conexão do PostgreSQL. Sem ela, o projeto usa SQLite local (`cotacoes.db`) |
| `AWESOMEAPI_KEY` | Recomendada | Chave gratuita da AwesomeAPI. Sem ela, as requisições ficam sujeitas a limites de uso mais restritos |

O arquivo `.env` não é versionado (está no `.gitignore`), pois pode conter credenciais.

## Aprendizados do projeto
- Consumo de uma API externa de forma assíncrona e tratamento de respostas inesperadas
- Persistência de dados com ORM e funções de agregação feitas pelo próprio banco
- Organização do código em routers
- Configuração por variáveis de ambiente, sem credenciais no código
- Deploy em nuvem com banco de dados externo
