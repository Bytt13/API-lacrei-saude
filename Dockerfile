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

# Informar ao Docker que a nossa aplicação usa a porta 8000
EXPOSE 8000

# Usamos gunicorn em vez do servidor de desenvolvimento do Django, pois é mais robusto para produção.
# Primeiro, instale o gunicorn: poetry add gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi"]