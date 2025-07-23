# API Lacrei Saúde

## 1. Visão Geral

A API Lacrei Saúde é uma plataforma para gerenciamento de profissionais de saúde e suas respectivas consultas. Ela foi desenvolvida para ser robusta, escalável e de fácil manutenção, utilizando tecnologias modernas de desenvolvimento web.

## 2. Tecnologias Utilizadas

- **Backend:** Python, Django, Django REST Framework
- **Gerenciador de Pacotes:** Poetry
- **Banco de Dados:** PostgreSQL (produção), SQLite (desenvolvimento)
- **Containerização:** Docker, Docker Compose
- **Servidor WSGI:** Gunicorn
- **CI/CD:** GitHub Actions
- **Hospedagem:** AWS Elastic Beanstalk
- **Documentação da API:** `drf-spectacular` (Swagger/OpenAPI)

## 3. Setup

### 3.1. Setup Local (Recomendado)

**Pré-requisitos:**
* Python 3.12+
* Poetry

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd API-lacrei-saude
    ```

2.  **Instale as dependências com Poetry:**
    ```bash
    poetry install
    ```

3.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione a seguinte variável:
    ```
    SECRET_KEY='sua-chave-secreta-super-segura'
    ```
    *O banco de dados padrão é o `SQLite` para facilitar a configuração local.*

4.  **Execute as migrações e inicie o servidor:**
    ```bash
    poetry run python manage.py migrate
    poetry run python manage.py runserver
    ```

5.  **Acesse a API:**
    * **API:** `http://127.0.0.1:8000/api/`
    * **Documentação (Swagger):** `http://127.0.0.1:8000/api/docs/`

### 3.2. Setup com Docker

**Pré-requisitos:**
* Docker
* Docker Compose

**Passos:**

1.  Na raiz do projeto, execute:
    ```bash
    docker-compose up --build
    ```
    A aplicação estará disponível em `http://localhost:8000`.

## 4. Execução dos Testes

O projeto utiliza `pytest` e os testes cobrem os principais fluxos dos endpoints. Para executar a suíte de testes:

```bash
poetry run python manage.py test
```
Este comando é o mesmo utilizado no pipeline de CI para garantir a qualidade do código.

## 5. Fluxo de Deploy (CI/CD)

O pipeline de Integração e Entrega Contínua (CI/CD) é gerenciado pelo **GitHub Actions** (`.github/workflows/ci.yml`) e é acionado a cada `push` na branch `main`.

1.  **Job `build-and-test` (CI):**
    * Verifica o código com `flake8` (linting).
    * Executa a suíte de testes completa para garantir que novas alterações não quebrem a funcionalidade existente.

2.  **Job `deploy` (CD):**
    * É executado apenas se o job anterior for bem-sucedido.
    * Empacota a aplicação em um `deploy.zip`.
    * Realiza o deploy da nova versão no ambiente da **AWS Elastic Beanstalk** de forma automatizada.

## 6. Justificativas Técnicas

* **Django/DRF:** Escolhidos pela robustez, segurança "out-of-the-box" e ecossistema maduro, acelerando o desenvolvimento de APIs RESTful.
* **Poetry:** Para um gerenciamento de dependências determinístico, garantindo que os ambientes de desenvolvimento e produção sejam idênticos.
* **Docker:** Para criar ambientes padronizados e isolados, eliminando o "funciona na minha máquina" e simplificando o deploy.
* **AWS Elastic Beanstalk:** Abstrai a complexidade da infraestrutura na nuvem (EC2, Load Balancer, etc.), permitindo focar no código enquanto a AWS gerencia a escalabilidade e o deploy.
* **GitHub Actions:** Para automatizar todo o processo de teste e deploy, garantindo entregas rápidas e seguras.
* **`drf-spectacular`:** Para gerar documentação OpenAPI (Swagger) automaticamente a partir do código, mantendo a documentação sempre atualizada com a API.

## 7. Proposta de Rollback Funcional

A estratégia de deploy pode ser melhorada para permitir rollbacks mais seguros e rápidos.

### Estratégia Sugerida: Blue/Green Deployment

O AWS Elastic Beanstalk suporta nativamente o deploy Blue/Green.

**Como funciona:**

* **Ambiente Blue:** O ambiente de produção atual, recebendo todo o tráfego.
* **Deploy no Ambiente Green:** O pipeline de CD, em vez de atualizar o ambiente Blue, provisiona um novo ambiente idêntico (Green) com a nova versão da aplicação.
* **Validação:** Testes podem ser executados no ambiente Green para garantir que tudo está funcionando como esperado antes de liberar para os usuários.
* **Swap de URL:** Com um clique (ou comando de API), o Elastic Beanstalk troca as URLs. O tráfego é instantaneamente redirecionado para o ambiente Green, que se torna o novo Blue.
* **Rollback Imediato:** Se um problema for detectado, o rollback é feito simplesmente trocando a URL de volta para o ambiente Blue original, que foi mantido intacto. É uma operação quase instantânea e sem risco.

## 8. (Bônus) Proposta de Integração com a Assas

Para integrar um sistema de pagamentos como o Assas, a arquitetura seria:

* **App `pagamentos` no Django:** Um novo app dedicado para isolar a lógica de pagamentos.
* **Model `Pagamento`:** Associado a uma `Consulta`, armazenaria o `id` da cobrança no Assas, status, valor, etc.
* **`AssasService`:** Uma classe de serviço para encapsular a comunicação com a API do Assas (criar cobrança, consultar status). Isso centraliza a lógica e facilita a troca de provedor no futuro.
* **Endpoint de Pagamento:** Um endpoint como `/api/consultas/{id}/pagar/` que, ao ser chamado:
    * Usa o `AssasService` para gerar a cobrança.
    * Retorna a URL de pagamento para o cliente (frontend).
* **Webhook:** Um endpoint para receber notificações do Assas (ex: pagamento confirmado). Este endpoint atualizaria o status do pagamento no nosso banco de dados.

## 9. Documentação da API (Swagger)

A documentação da API é gerada automaticamente e está disponível de forma interativa. Após iniciar o servidor, acesse:

* **[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)**

Nesta página, você pode visualizar todos os endpoints, modelos de dados e testar as requisições diretamente do seu navegador.