# n8n-ai-cookbook

Coleção de workflows n8n prontos pra importar, que conectam serviços de IA a automações do dia a dia. É a camada de orquestração deste portfólio — a "cola" entre `lead-router` e `rag-starter-kit`.

## Workflows

### `lead-enrichment-and-scoring.json`
Webhook recebe um lead → chama o `lead-router` (enriquecimento + score via Claude) → se qualificado, notifica o time de vendas no Slack; senão, só loga.

```
Webhook → HTTP Request (lead-router) → IF (score >= 60) → Slack
```

### `rag-faq-autoresponder.json`
Webhook recebe uma pergunta → chama o `rag-starter-kit` → devolve a resposta baseada nos documentos ingeridos.

```
Webhook → HTTP Request (rag-starter-kit) → Respond to Webhook
```

## Como usar

1. Suba o serviço correspondente (`lead-router` e/ou `rag-starter-kit`) localmente ou em algum host.
2. No n8n, **Import from File** e selecione o `.json` do workflow desejado.
3. Ajuste as URLs dos nós HTTP Request para onde seus serviços estão rodando.
4. Configure as variáveis de ambiente do n8n com as mesmas chaves definidas em `API_KEYS` nos backends (veja "Autenticação" abaixo).
5. Ative o workflow — o n8n expõe uma URL de webhook pra você plugar em qualquer formulário, CRM ou integração externa.

## Autenticação

Desde que `lead-router` e `rag-starter-kit` passaram a suportar autenticação por `X-API-Key` (ver `AGENT_BEHAVIOR.md`/`README.md` de cada repo), os nós HTTP Request destes workflows já enviam o header lendo variáveis de ambiente do próprio n8n:

| Workflow | Nó | Variável de ambiente esperada |
| --- | --- | --- |
| `lead-enrichment-and-scoring.json` | HTTP Request - lead-router | `LEAD_ROUTER_API_KEY` |
| `rag-faq-autoresponder.json` | HTTP Request - rag-starter-kit | `RAG_STARTER_KIT_API_KEY` |

Se o backend correspondente estiver rodando sem `API_KEYS` configurado (modo dev, auth desligada), o header é enviado mas simplesmente ignorado pelo backend — nenhuma configuração adicional é necessária nesse caso.

## Por que JSON exportado, e não só descrição

Workflows do n8n são reproduzíveis 1:1 a partir do JSON — qualquer pessoa importa e já tem o fluxo funcionando, sem recriar nó por nó manualmente. É o formato que o próprio n8n usa para templates.

## Roadmap

- [ ] Workflow de re-treino/atualização periódica da base do rag-starter-kit
- [ ] Workflow de retry com backoff para o HTTP Request em caso de falha do serviço downstream
