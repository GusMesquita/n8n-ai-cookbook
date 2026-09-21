# n8n-ai-cookbook

Workflows n8n prontos pra importar, que conectam serviços de IA a automações do dia a dia.
É a camada de orquestração deste portfólio — a "cola" entre `lead-router` e `rag-starter-kit`.

Cada workflow tem diretório próprio, com o JSON, um README e a captura do canvas.

| Workflow | O que faz |
| --- | --- |
| [`lead-enrichment-and-scoring`](workflows/lead-enrichment-and-scoring/) | Webhook → `lead-router` (enriquece por CNPJ + pontua com o Claude) → Slack, ramificando por score |
| [`rag-faq-autoresponder`](workflows/rag-faq-autoresponder/) | Webhook → `rag-starter-kit` → responde a pergunta na mesma requisição, com as fontes |

## Subindo o n8n

```bash
cp .env.example .env
# N8N_ENCRYPTION_KEY=$(openssl rand -hex 32) — fixa, senão as credenciais salvas viram lixo
docker compose up -d
```

`http://127.0.0.1:5678` → crie a conta de owner → **Import from File** → escolha o
`workflow.json` do workflow desejado.

O `compose.yaml` já sobe o n8n com `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`. Sem isso as
expressões `{{ $env.X }}` destes workflows falham com *access to env vars denied* — é o
padrão do n8n bloquear.

## Configuração

Nenhuma URL e nenhuma chave vivem dentro do JSON: tudo vem de variáveis de ambiente do n8n,
definidas no `.env`.

| Variável | Usada por |
| --- | --- |
| `LEAD_ROUTER_URL` / `LEAD_ROUTER_API_KEY` | `lead-enrichment-and-scoring` |
| `RAG_STARTER_KIT_URL` / `RAG_STARTER_KIT_API_KEY` | `rag-faq-autoresponder` |

As chaves precisam bater com `API_KEYS` do backend correspondente. Backend em modo dev
(sem `API_KEYS`) ignora o header, e nada além disso precisa ser configurado.

Portas, sem colisão: n8n **5678** · `lead-router` **8000** · `brasilapi-mcp-server` **8001** ·
`rag-starter-kit` **8002**. Do container do n8n, o host é `host.docker.internal`.

## Validação

```bash
python3 scripts/validate.py
```

Stdlib pura, roda no CI. Pega JSON quebrado, nó sem `typeVersion`, conexão apontando pra nó
inexistente, credencial embutida no arquivo, URL fixa e workflow sem README.

## Por que JSON exportado, e não só descrição

Workflows do n8n são reproduzíveis 1:1 a partir do JSON — qualquer pessoa importa e já tem o
fluxo funcionando, sem recriar nó por nó. É o formato que o próprio n8n usa para templates.
As convenções que cada arquivo segue estão em [`docs/conventions.md`](docs/conventions.md).

## Roadmap

- [ ] Workflow de re-treino/atualização periódica da base do rag-starter-kit
- [ ] Workflow de retry com backoff para o HTTP Request em caso de falha do serviço downstream
