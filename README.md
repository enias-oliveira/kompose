# Kompose

### Adicione aqui os erros e correções aplicadas

### EXEMPLO

---

**Código com erro:**

```dockerfile
# imagem base
FROM python:2.7

RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

WORKDIR /code
COPY . /code/

```

**Erros:**

- Versão do Python sem suporte pelo pip.
- Instalação dos requirementes.txt acontece antes do arquivo ser copiado para o container
  **O que ele causa:** Pip reclama da versão sem suporte e dificulta instalação de alguns pacotes que usam apenas versões mais atualizadas do python e pip não consegue instalar os requirementes sem os arquivos
  **Como corrigir:** Mudar versão da imagem e mover a copia do ambiente para ser antes de fazer o pip install
  **Código corrigido:**

```dockerfile
# imagem base
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2
```

---
