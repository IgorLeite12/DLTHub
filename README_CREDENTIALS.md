# Configuração de Credenciais PostgreSQL

## Como funciona o sistema de credenciais

Este projeto usa a biblioteca **dlt** (data load tool) para gerenciar credenciais de forma segura.

### Estrutura do arquivo `.dlt/secrets.toml`

O arquivo `.dlt/secrets.toml` armazena as credenciais do PostgreSQL. Este arquivo está no `.gitignore` para não expor senhas no repositório.

**Exemplo de configuração:**

```toml
[sources.postgres.credentials]
database = "nome_do_banco"
username = "seu_usuario"
password = "sua_senha"
host = "localhost"
port = 5432
```

### Campos obrigatórios

- **database**: Nome do banco de dados PostgreSQL
- **username**: Usuário do banco
- **password**: Senha do usuário

### Campos opcionais (com valores padrão)

- **host**: Servidor do banco (padrão: `"localhost"`)
- **port**: Porta do PostgreSQL (padrão: `5432`)

## Como o dlt carrega as credenciais

1. O decorador `@configspec` define a classe `PostgresCredentials` em `client.py`
2. O decorador `@with_config` injeta automaticamente as credenciais na função
3. Em `sources.py`, o parâmetro `credentials: PostgresCredentials = dlt.secrets.value` busca automaticamente do arquivo `secrets.toml`
4. O dlt procura a configuração seguindo o padrão: `sources.<nome_do_source>.credentials`

## Exemplo de uso

```python
# O dlt carrega automaticamente as credenciais
from salesforce.sources import postgres_source

# As credenciais são injetadas automaticamente
source = postgres_source()
```

## Segurança

- ✅ O arquivo `secrets.toml` está no `.gitignore`
- ✅ A senha é do tipo `TSecretStrValue` (mascarada em logs)
- ✅ Nunca commite o arquivo `secrets.toml` no git
- ✅ Use variáveis de ambiente em produção se preferir

## Alternativa: Variáveis de ambiente

Você também pode usar variáveis de ambiente:

```bash
export SOURCES__POSTGRES__CREDENTIALS__DATABASE="nome_do_banco"
export SOURCES__POSTGRES__CREDENTIALS__USERNAME="seu_usuario"
export SOURCES__POSTGRES__CREDENTIALS__PASSWORD="sua_senha"
export SOURCES__POSTGRES__CREDENTIALS__HOST="localhost"
export SOURCES__POSTGRES__CREDENTIALS__PORT="5432"
```

O dlt automaticamente detecta e usa essas variáveis.
