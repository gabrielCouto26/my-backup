#!/bin/bash

# Sair imediatamente se um comando falhar
set -e

# --- Configuração ---
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
BACKUP_SCRIPT="backup.py"
ENV_FILE=".env" # Assumindo que .env está na raiz do projeto

# --- Configurar Ambiente Virtual ---
if [ ! -d "$VENV_DIR" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv "$VENV_DIR"
fi

echo "Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

# --- Instalar/Atualizar Dependências ---
echo "Instalando/Atualizando dependências..."
pip install -q --upgrade pip
pip install -q -r "$REQUIREMENTS_FILE"

# --- Carregar Variáveis de Ambiente ---
if [ -f "$ENV_FILE" ]; then
    echo "Carregando variáveis de ambiente de $ENV_FILE..."
    # Usar 'set -a' para exportar todas as variáveis, depois 'set +a' para reverter
    set -a
    source "$ENV_FILE"
    set +a
else
    echo "Aviso: arquivo .env não encontrado. Certifique-se de que GOOGLE_DRIVE_BACKUP_FOLDER_ID esteja definido em seu ambiente."
fi

# --- Validar variáveis de ambiente essenciais ---
if [ -z "$GOOGLE_DRIVE_BACKUP_FOLDER_ID" ]; then
    echo "Erro: GOOGLE_DRIVE_BACKUP_FOLDER_ID não está definido."
    echo "Por favor, defina-o em seu arquivo .env ou no ambiente."
    deactivate # Sair do venv de forma limpa
    exit 1
fi

# --- Definir OUTPUT_FOLDER local padrão se não estiver especificado ---
if [ -z "$OUTPUT_FOLDER" ]; then
    echo "OUTPUT_FOLDER não definido. Usando '/home/gabriel/Backup' como padrão."
    export OUTPUT_FOLDER="/home/gabriel/Backup"
fi

# --- Executar o Script de Backup ---
echo "Executando o script de backup..."
python "$BACKUP_SCRIPT"

# --- Desativar Ambiente Virtual ---
echo "Processo de backup concluído. Desativando ambiente virtual."
deactivate
