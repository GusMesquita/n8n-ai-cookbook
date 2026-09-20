# Convenções deste repositório

Este documento é auto-contido: não depende de nenhum outro repositório.

## O que é um workflow válido aqui

- O JSON é **exportado do n8n**, nunca escrito à mão. Export manual perde campos
  (`meta`, `versionId`, `settings`, `pinData`) e produz arquivos que falham na importação.
- Todo nó tem `type` **e** `typeVersion`, e os parâmetros seguem o formato daquela
  `typeVersion`. Declarar `typeVersion: 2` com parâmetros no formato v1 quebra o import.
- Toda conexão aponta para um nó que existe no arquivo.
- `scripts/validate.py` verifica os três itens acima no CI.

## Configuração

- **Nenhuma URL fixa e nenhum segredo dentro do JSON.** Endpoints e chaves vêm de
  variáveis de ambiente do próprio n8n (`$env`), e o README de cada workflow lista quais.
- Portas usadas nos exemplos são documentadas e não colidem entre si.

## Ambiente

- **Node 26.9.0**, declarado em `.mise.toml` e `.nvmrc`.
- O `compose.yaml` sobe uma instância do n8n para testar os workflows localmente.

## Segurança do n8n local

- `N8N_ENCRYPTION_KEY` é obrigatório — sem ele o n8n gera uma chave nova a cada start e
  as credenciais salvas viram lixo.
- Autenticação básica ligada, e a porta publicada apenas em `127.0.0.1`.

## Documentação

Cada workflow vive no seu próprio diretório, com `workflow.json`, `README.md` e um
`screenshot.png` do canvas. Este é um repositório visual: a captura do fluxo comunica
mais rápido que a descrição em texto.
