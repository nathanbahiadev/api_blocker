# API Blocker

### Documentação
Para acessar a documentação, acesse:
- ```/redoc```
- ```/api/v1/documentation```


### Projeto
Para iniciar o projeto em sua máquina, primeiro faça o clone do repositórios, depois crie um ambiente virtual, como em ```python -m venv venv``` e instale as dependências necessárias com ```pip install -r requirements```


### Para iniciar o banco de dados
```
from conf.db_session import create_tables
create_tables()
```

### Variáveis de ambiente (exemplo .env)
```
DATABASE_URL="sqlite:///db.sqlite3"
```
