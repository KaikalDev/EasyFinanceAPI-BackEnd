# 💸 EasyFinanceAPI

**API RESTful com FastAPI para controle financeiro pessoal**, oferecendo gerenciamento completo de usuários, metas, cofrinhos e transações.  
Ideal para organizar sua grana e ter controle total sobre entradas, saídas e objetivos.

---

## 🚀 Endpoints

> ⚠️ Exceto as rotas de cadastro e login, todas exigem autenticação JWT.  
> Envie o token no header da requisição:  
> `Authorization: Bearer <seu_token_aqui>`

---

### 🔐 Autenticação & Usuário

| Método | Rota                  | Descrição                        |
|--------|-----------------------|----------------------------------|
| POST   | `/user/add`           | Cadastra um novo usuário         |
| POST   | `/user/login`         | Login e retorno do JWT           |
| GET    | `/user/get/{id}`      | Dados do usuário                 |
| GET    | `/user/me`            | ID do usuário logado             |
| PUT    | `/user/editNome/{id}` | Edita o nome                     |
| PUT    | `/user/editSenha/{id}`| Edita a senha                    |
| DELETE | `/user/delete/{id}`   | Remove o usuário                 |
| GET    | `/user/historico`     | Todas as transações do usuário   |

---

### 🎯 Metas (Goals)

| Método | Rota                | Descrição               |
|--------|---------------------|-------------------------|
| POST   | `/goal/add`         | Cria uma nova meta      |
| GET    | `/goal/get/{id}`    | Busca meta por ID       |
| PUT    | `/goal/edit/{id}`   | Atualiza uma meta       |
| DELETE | `/goal/delete/{id}` | Remove uma meta         |

---

### 🐖 Cofrinhos (Piggybanks)

| Método | Rota                        | Descrição                    |
|--------|-----------------------------|------------------------------|
| POST   | `/piggybank/add`            | Cria um cofrinho             |
| GET    | `/piggybank/get/{id}`       | Retorna cofrinho por ID      |
| PUT    | `/piggybank/edit/{id}`      | Edita nome do cofrinho       |
| DELETE | `/piggybank/delete/{id}`    | Deleta o cofrinho            |
| GET    | `/piggybank/{id}/historico` | Transações desse cofrinho    |

---

### 💳 Transações (Transactions)

| Método | Rota                       | Descrição               |
|--------|----------------------------|-------------------------|
| POST   | `/transaction/add`         | Adiciona nova transação |
| GET    | `/transaction/get/{id}`    | Busca por ID            |
| PUT    | `/transaction/edit/{id}`   | Atualiza transação      |
| DELETE | `/transaction/delete/{id}` | Remove transação        |

---

## 📁 Estrutura do Projeto
```
api/
├── data/
│   └── db.py                 # Configuração do banco (SQLAlchemy async)
│   └── models.py             # Configuração das entidades do banco
|
├── routers/                        # Endpoints organizados por domínio
│   ├── userRouters.py              # Rotas relacionadas a usuários
│   ├── goalRouters.py              # Rotas de metas financeiras
│   ├── piggybankRouters.py         # Rotas de cofrinhos virtuais
│   └── transactionRouters.py       # Rotas de transações
│
├── schemas/                  # Modelos Pydantic para validação e resposta
│   ├── User.py
│   ├── Goal.py
│   ├── Piggybank.py
│   └── Transaction.py
│
├── services/                 # Camada de lógica de negócio (Services)
│   ├── UserServices.py
│   ├── GoalService.py
│   ├── PiggybankService.py
│   └── TransactionService.py
│
├── utils/                    # Geração e verificação de tokens JWT
│   └── auth.py
|   └── config.py
|   └── dependencies.py
│
└── app.py

```



---

## ▶️ Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/KaikalDev/EasyFinanceAPI-BackEnd.git
cd easyfinance-api

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode o servidor
uvicorn main:app --reload


