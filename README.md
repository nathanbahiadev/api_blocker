# API Blocker

### Para iniciar o banco de dados
```
from conf.db_session import create_tables
create_tables()
```


### Rotas
- [POST] /ip/verify/
```
{
    "ipaddress": "177.52.34.89",
    "system": "CarX",
    "limit_requests": 10,
    "limit_seconds": 60,
    "to_limit": true,
    "to_block": false,
    "show_time_left": true,
    "to_limit_response": {
        "message": "Acesso bloqueado temporariamente"
    },
    "to_block_response": {
        "message": "Acesso bloqueado indefinidamente. Entre em contato com o suporte para continuar acessando o sistema"
    },
}
 ```
- [POST] /ip/remove/
```
{
    "ipaddress": "177.52.34.89"
}
```
- [GET] /ip/blocked/?system=Autovist