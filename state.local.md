# Estado do Projeto - AutoBackup Drive

Este documento descreve as funcionalidades implementadas no projeto AutoBackup Drive, servindo como fonte de contexto para o desenvolvimento contínuo.

## Visão Geral
O projeto é uma ferramenta de automação de backup que coleta arquivos e diretórios locais, os compacta em um arquivo ZIP e realiza o upload para o Google Drive.

## Funcionalidades e Estágio de Desenvolvimento

### 1. Seleção de Arquivos (Backup Seletivo)
- **Descrição:** Lê uma lista de caminhos (arquivos ou pastas) a partir de um arquivo de configuração.
- **Implementação:** Arquivo `backup_files.txt` processado em `backup.py`.
- **Status:** ✅ Concluído.
- **Detalhes:** Suporta caminhos absolutos e relativos, lidando com arquivos individuais e diretórios recursivamente.

### 2. Compactação (Zipping)
- **Descrição:** Reúne todos os arquivos selecionados em um único arquivo `.zip` com timestamp.
- **Implementação:** Utiliza a biblioteca `zipfile` no `backup.py`.
- **Status:** ✅ Concluído.
- **Detalhes:** Cria uma estrutura temporária para organizar os arquivos antes de zippar, garantindo que o arquivo final seja consistente.

### 3. Integração com Google Drive
- **Descrição:** Upload automático do arquivo compactado para uma pasta específica no Google Drive.
- **Implementação:** Arquivo `upload.py` utilizando `google-api-python-client`.
- **Status:** ✅ Concluído.
- **Detalhes:** Realiza o upload via API v3, com suporte a `resumable media upload`.

### 4. Autenticação OAuth 2.0
- **Descrição:** Gerenciamento de credenciais para acesso seguro à API do Google.
- **Implementação:** `upload.py` utiliza `google-auth-oauthlib`.
- **Status:** ✅ Concluído.
- **Detalhes:** Utiliza `credentials.json` para o fluxo inicial, que deve ser executado localmente para gerar o `token.json`. As execuções subsequentes (locais ou em container) utilizam o `token.json` para autenticação não interativa.

### 5. Containerização (Docker)
- **Descrição:** Ambiente isolado e reproduzível para execução do backup.
- **Implementação:** `Dockerfile` e `docker-compose.yml`.
- **Status:** ✅ Concluído.
- **Detalhes:** Configurado para rodar via Python 3.11. Requer o arquivo `token.json` (gerado na primeira execução local) para operar de forma autônoma.

### 6. Logging de Execução
- **Descrição:** Sistema de logs para monitorar o processo de backup, desde a cópia dos arquivos até o upload.
- **Implementação:** Uso da biblioteca `logging` em `backup.py` e `upload.py`.
- **Status:** ✅ Concluído.
- **Detalhes:** Os logs registram cada etapa, sucesso, erros e o tempo total da operação, facilitando a depuração.

## Estrutura de Arquivos Chave
- `backup.py`: Orquestrador do processo (Leitura -> Cópia -> Zip -> Upload).
- `upload.py`: Lógica específica de comunicação com o Google Drive.
- `backup_files.txt`: Lista de alvos do backup.
- `requirements.txt`: Dependências do projeto.
- `state.local.md`: Documento de estado e funcionalidades do projeto.

## Próximos Passos Sugeridos
- [ ] Implementar rotação de backups (deletar backups antigos no Drive).
- [ ] Adicionar notificações (e-mail ou webhook) em caso de falha.
- [ ] Melhorar o tratamento de erros para caminhos inexistentes no `backup_files.txt`.
