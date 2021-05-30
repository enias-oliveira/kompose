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

**O que ele causa:**

- Pip reclama da versão sem suporte e dificulta instalação de alguns pacotes que usam apenas versões mais atualizadas do python
- Pip não consegue instalar os requirementes sem os arquivos

**Como corrigir:**

- Mudar versão da imagem
- Mover a copia do ambiente para ser antes de fazer o pip install

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

**Código com erro:**

```yaml
version: '3.3'
services:
  db:
    image: postgres:latest
    env_file: envs/dev.env
    ports:
      - 5432:5432

  migration:
    build: .
    env_file: envs/dev.env
    command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py migrate'

    stdin_open: true
    tty: true

    depends_on:
      - db

  web:
    env_file: envs/dev.env
    command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py runserver 0.0.0.0:8000'

    stdin_open: true
    tty: true
    ports:
      - 8000:8001

    depends_on:
      - db
      - migration
```

**Erros:**

- Serviço web não tinha imagem e nem local aonde o arquivo dockerfile está localizado.
- A ponte das portas do serviço web está diferente da porta que o django usa
- Não existe volume como ponte para código externo e do container
- Não existe volume externo

**O que ele causa:**

- Serviço web não consegue ser montado
- Servidor Django não recebe as requisições
- As edições no código fonte não farão efeito no servidor dentro do container
- Dados não serão persistentes

**Como corrigir:**

- Adicionar "build" e local do arquivo com o DockerFile "."
- Mudar a porta do container de 8000 para 8001
- Adicionar ponte dos arquivos de desenvolvimento e container
- Adicionar volume externo

**Código corrigido:**

```yaml
version: '3.3'
services:
  db:
    image: postgres:latest
    env_file: envs/dev.env
    ports:
      - 5432:5432
    volumes:
      - kompose:/var/lib/postgresql/data

  migration:
    build: .
    env_file: envs/dev.env
    command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py migrate'

    stdin_open: true
    tty: true

    depends_on:
      - db

  web:
    build: .
    env_file: envs/dev.env
    command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py runserver 0.0.0.0:8000'

    stdin_open: true
    tty: true
    ports:
      - 8000:8000

    volumes:
      - .:/code

    depends_on:
      - db
      - migration

volumes:
  kompose:
    external: true
```

---
