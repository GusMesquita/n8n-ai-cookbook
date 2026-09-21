# Convenções deste repositório

Este documento é auto-contido: não depende de nenhum outro repositório.

## O que é um workflow válido aqui

- **Sobrevive ao round-trip.** O arquivo tem que importar no n8n e voltar do
  `n8n export:workflow` com `nodes`, `connections` e `settings` idênticos. É o teste real —
  escrever o JSON à mão é permitido, entregar um que o n8n normalizaria não é.
- **Estado de instância fica de fora.** O export traz `id`, `versionId`, `createdAt`,
  `active`, `shared` e afins; nada disso entra no arquivo versionado, porque é do banco
  daquela instância e não do fluxo.
- Todo nó tem `type` **e** `typeVersion`, e os parâmetros seguem o formato daquela
  `typeVersion`. Declarar `typeVersion: 2` com parâmetros no formato v1 quebra o fluxo
  silenciosamente: o n8n importa, mas o nó roda com os defaults.
- Toda conexão aponta para um nó que existe no arquivo.
- `scripts/validate.py` verifica o que dá pra verificar sem subir o n8n (JSON, campos
  obrigatórios, conexões órfãs, credencial inline, URL fixa, README) e roda no CI.

## Configuração

- **Nenhuma URL fixa e nenhum segredo dentro do JSON.** Endpoints e chaves vêm de
  variáveis de ambiente do próprio n8n (`$env`), e o README de cada workflow lista quais.
- `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` é obrigatório. O padrão do n8n é **bloquear** o
  acesso a variáveis de ambiente nas expressões; sem essa linha todo `{{ $env.X }}` falha
  com *access to env vars denied*.
- Portas usadas nos exemplos, sem colisão:

  | Serviço | Porta no host |
  | --- | --- |
  | n8n | 5678 |
  | `lead-router` | 8000 |
  | `brasilapi-mcp-server` | 8001 |
  | `rag-starter-kit` | 8002 (escuta em 8000 dentro do container) |

- Do container do n8n, o host é `host.docker.internal` — `localhost` aponta pro próprio
  container.

## Ambiente

- **Node 26.9.0**, declarado em `.mise.toml` e `.nvmrc`.
- O `compose.yaml` sobe uma instância do n8n (tag fixa, não `latest`) para testar os
  workflows localmente.

## Segurança do n8n local

- `N8N_ENCRYPTION_KEY` é obrigatório — sem ele o n8n gera uma chave nova a cada start e
  as credenciais salvas viram lixo.
- A porta é publicada apenas em `127.0.0.1`. Autenticação é a conta de owner criada no
  primeiro acesso (o n8n 2.x removeu o `N8N_BASIC_AUTH_ACTIVE`).

## Documentação

Cada workflow vive no seu próprio diretório, com `workflow.json`, `README.md` e um
`screenshot.png` do canvas. Este é um repositório visual: a captura do fluxo comunica
mais rápido que a descrição em texto.
