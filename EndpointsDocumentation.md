# Endpoints - Usuários

## POST /Register
Registra um novo usuário e retorna uma mensagem sobre o status de sucesso do cadastro.

### Body:
```json
{
  "username": "ashketchum",
  "email": "ash.ketchum@pallet.com",
  "password": "pikachu123"
}
```
### Response:
```json
{
  "msg": "Usuário criado com sucesso."
}
```

## POST /Login
Realiza o login do usuário e retorna um token de autentificação.

### Body:
```json
{
  "username": "ash.ketchum@pallet.com",
  "password": "pikachu123"
}
```

### Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer",
  "user_id": "64e438f7df86c",
  "username": "ashketchum",
  "email": "ash.ketchum@pallet.com"
}
```

# Endpoints - Times

## POST /team
Cria um time vazio para o usuário com 6 espaços disponíveis para serem preenchidos com pokemons.

### Body:
```json
{
  "user_id": "64e438f7df86c"
}
```

### Response:
```json
{
  "id": "64e438f7df86c",
  "user_id": "64e438f7df86c",
  "team": [null, null, null, null, null, null]
}
```

## GET /all_teams
Lista todos os times (preenchidos ou não) do usuário.

### Response:
```json
[
  {
    "id": "64e438f7df86c",
    "user_id": "64e438f7df86c",
    "team": [...]
  }
]
```

## GET /team/{team_id}
Disponibiliza um time específico, cada time criado possui um ID, cujo parâmetro é "team_id".

### Response:
```json
{
  "id": "64e438f7df86c",
  "user_id": "64e438f7df86c",
  "team": [...]
}
```

## POST /team/{team_id}/slot/{slot_index}
Adiciona um pokemon em uma das 6 posições do time, tem como parâmetros "team_id" e "slot_index"(cujas posições são numeradas de 0 a 5).

### Body:
```json
{
  "name": "Pikachu",
  "type": "Electric",
  "level": 25
}

```

### Response:
```json
{
  "id": "64e438f7df86c",
  "user_id": "64e438f7df86c",
  "team": [...]
}
```

## DELETE /team/{team_id}/slot/{slot_index}
Remove um pokemon de uma das 6 posições do time, tem como parâmetros "team_id" e "slot_index"(cujas posições são numeradas de 0 a 5).

### Response:
```json
{
  "id": "64e438f7df86c",
  "user_id": "64e438f7df86c",
  "team": [...]
}
```

## DELETE /team/{team_id}
Deleta um time, cujo parâmetros é "team_id".

### Response:
```json
{
  "id": "64e438f7df86c",
  "user_id": "64e438f7df86c",
  "team": [...]
}
```