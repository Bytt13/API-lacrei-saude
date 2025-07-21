#Imagem do python como base
FROM python:3.12-slim

#Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYHTONUNBUFFERED 1

#Definir diretorio de trabalho
WORKDIR /code

#Instalar poetry
RUN pip install poetry

#Copiar arquivos de dependência
COPY poetry.lock pyproject.toml /code/

#Instalar dependências do projeto
RUN poetry config virtualenvs.create false && poetry install --without dev --no-interaction --no-ansi --no-root

#Copiar resto do codigo do projeto
COPY . /code/
