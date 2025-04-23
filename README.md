# 🛒 E-commerce API - Projeto Acadêmico

Este é um projeto desenvolvido para a disciplina **Big Data e Cloud Computing**, com o objetivo de aplicar conceitos de desenvolvimento de APIs RESTful, integração com bancos de dados em nuvem e deploy em serviços cloud.

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework principal da API.
- **MySQL (Azure Database for MySQL)**: Armazena dados de usuários e cartões.
- **MongoDB (Azure Cosmos DB - API for MongoDB)**: Armazena dados de produtos e pedidos.
- **SQLAlchemy**: ORM para integração com o MySQL.
- **Pydantic**: Validação e tipagem dos dados.
- **Docker**: Empacotamento da aplicação.
- **GitHub Actions**: CI/CD automatizado para deploy.
- **Azure App Service**: Hospedagem da API na nuvem.

## 📁 Estrutura do Projeto

```bash
app/
├── main.py                 # Inicializa a aplicação FastAPI
├── routers/                # Rotas separadas por recurso (user, card, product, order)
├── models/                 # Modelos ORM e Pydantic
├── database/               # Configuração de conexão com MySQL e MongoDB
├── ...
```

## 🧪 Endpoints Principais

- `GET /` - Verifica se a API está rodando
- `POST /users/` - Cria um novo usuário
- `GET /users/` - Lista usuários
- `POST /users/{user_id}/cards/` - Cadastra cartão para o usuário
- `POST /products/` - Cria um novo produto
- `POST /orders/` - Cria uma nova ordem

> A documentação interativa pode ser acessada via `/docs` (Swagger UI) quando a API estiver no ar.

## 🌐 Deploy

O projeto está hospedado em um ambiente gratuito do **Azure App Service**. Por ser um projeto acadêmico, o ambiente pode ser desativado após a conclusão da matéria.


Bernardo Moreira
Lucas Goulart
Marcelo Saggio
Tadeu Tovar
