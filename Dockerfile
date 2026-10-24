# Utiliza a imagem oficial Python 3.11 slim como base otimizada
FROM python:3.11-slim

# Variáveis de ambiente para otimização e logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Atualiza pacotes básicos de sistema de forma enxuta
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia toda a estrutura modular exigida pela arquitetura
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY specs/ /app/specs/
COPY CONTEXT_RULES.md README.md /app/

# Criação de usuário não-root (Boas práticas de segurança em contêineres)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando de entrada estrito conforme documentação arquitetural
CMD ["pytest", "tests/test_harness.py", "-v"]