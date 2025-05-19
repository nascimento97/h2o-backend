## h2o – Monitoramento de Consumo de Água

Este repositório contém a API **h2o**, desenvolvida em FastAPI, para registro e acompanhamento do consumo de água por usuários. Permite cadastro sem senha, autenticação via JWT, registro de peso e ingestão de água, e recuperação de histórico com filtros.

---

## 🗂️ Estrutura do Projeto

```
project-root/
├── .env                   # Variáveis de ambiente (SECRET_KEY, etc.)
├── alembic/               # Migrações de banco (Alembic)
├── app/
│   ├── core/
│   │   ├── config.py      # Configurações centrais (pydantic-settings)
│   │   └── security.py    # Criação e validação de JWT
│   ├── database.py        # Engine, Session e dependência get_db
│   ├── models/            # Models SQLAlchemy + mixins (soft delete, timestamps)
│   ├── schemas/           # Schemas Pydantic para validação de request/response
│   ├── services/          # Lógica de negócio (User, Weight, Intake)
│   ├── dependencies/      # Dependências de autenticação (get_current_user)
│   ├── routers/           # APIRouters para usuários, pesos e ingestão
│   └── main.py            # Instancia FastAPI, CORS e inclui routers
├── tests/                 # Testes unitários e de integração
├── requirements.txt       # Dependências do Python
└── README.md              # Documentação do projeto
```

---

## ⚙️ Funcionalidades

1. **Cadastro de usuário**

   * Somente nome (único) e peso inicial.
   * Cria automaticamente registro de peso com timestamp.

2. **Login/Logout**

   * Login apenas pelo nome, gera token JWT com expiração de 24 horas.
   * Logout revoga o token (via blacklist).

3. **Registro de peso**

   * Endpoint privado para criação de pesos adicionais.
   * Cada peso é imutável após registro e armazena data de criação.

4. **Registro de ingestão de água**

   * Quantidades fixas: 200 ml, 350 ml ou 500 ml.
   * Armazena usuário, quantidade e timestamp.

5. **Histórico de ingestão**

   * Filtros opcionais por quantidade e intervalo de datas.
   * Soft-deletes em todas as tabelas.

6. **Documentação automática**

   * Swagger UI: `/docs`
   * ReDoc:       `/redoc`

---

## 🚀 Instalação e Execução

1. **Clone o repositório**

   ```bash
   git clone https://github.com/nascimento97/h2o-backend.git
   cd h2o-backend
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate     # macOS/Linux
   .venv\Scripts\activate.bat    # Windows
   ```

3. **Instale dependências**

   ```bash
   pip install -r requirements.txt
   pip install pydantic-settings
   ```

4. **Configure variáveis de ambiente**
   Crie um arquivo `.env` na raiz com pelo menos:

   ```
   SECRET_KEY=sua_chave_secreta_bem_grande
   ```

5. **Execute as migrações (opcional)**
   Caso use Alembic:

   ```bash
   alembic upgrade head
   ```

6. **Inicie o servidor**

   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📋 Endpoints Principais

| Rota                 | Método | Autenticação | Descrição                                        |
| -------------------- | ------ | ------------ | ------------------------------------------------ |
| `POST /users/`       | POST   | ❌            | Cria novo usuário com peso inicial               |
| `POST /users/login`  | POST   | ❌            | Login por nome — retorna acesso JWT              |
| `POST /users/logout` | POST   | ✅            | Revoga o token JWT                               |
| `POST /weights/`     | POST   | ✅            | Cria novo registro de peso                       |
| `POST /intake/`      | POST   | ✅            | Registra ingestão de água                        |
| `GET  /intake/`      | GET    | ✅            | Recupera histórico (filtros por quantidade/data) |
| `GET  /health`       | GET    | ❌            | Health check (status “ok”)                       |

---

## 🧪 Testes

* Execute todos os testes com:

  ```bash
  pytest --cov=app
  ```

---
