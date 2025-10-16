## 1. Criando  uma Virtual Environment
1.1. Crie uma Virtual environment:
```sh
python -m venv venv
```
-------------------------
## 2. Ativando a Virtual environment

2.1. Para ativação da Virtual environment, digite:
- Linux
```sh
source venv/bin/activate
```
- Windows
```sh
\venv\Script\activate
```
----------------------------

## 3. Subindo o container do Docker

3. Comandos para subir os containers no Docker
- Container postgres e minio
````sh
docker compose -f composes/docker-compose.yml up -d
````

----------------------------
## 4. Instalando as dependências 
4.1. Para instalação das dependências, digite:
```sh
pip install -r requirements.txt

```
------------------------

## 5. Restaurando o banco de dados a partir do arquivo dump 
5.1 Para verificar o id do container postgres:
```sh
docker ps

```
5.2. Copiar o backup para o container postgres:
````sh
docker cp backup_postgres.dump <ID-CONTAINER-POSTGRES>:/tmp/
````

5.3. Comando para reustaurar o banco de dados:
````sh
PGPASSWORD=sale123 docker exec -it <ID-CONTAINER-POSTGRES> pg_restore -U postgres -d sale -v /tmp/dlt.dump
````
-------------------------
## 5.4 (Alternativa para WSL)

1. Comando WSL
````sh
PGPASSWORD="sale123" cat dlt.dump | docker exec -i <ID-CONTAINER-POSTGRES> pg_restore -U postgres -d sale
````

------------------------

## 6. Configurando o Minio

1. Acesse o painel do MinIO: http://localhost:9001
2. Crie um bucket chamado landing, que será usado para armazenar os arquivos .csv.
3. Configure as Access Keys:
  - access keys `SALE`
  - Adicione uma regra com o prefixo `*`.
  - Defina o nível de acesso como `readonly`.
------------------------


## 7. Executar Pipeline de Dados
7.1. Execultar script principal na raiz do projeto:
```sh
python salesforce_pipeline.py
```