#!/usr/bin/env python3
"""Script para verificar se o ambiente está configurado corretamente."""

import sys
from pathlib import Path


def check_python_version():
    """Verifica versão do Python."""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requer 3.8+)")
        return False


def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print("\n📦 Verificando dependências...")
    
    dependencies = {
        "dlt": "dlt",
        "psycopg2": "psycopg2",
    }
    
    all_ok = True
    for name, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} não instalado")
            all_ok = False
    
    return all_ok


def check_secrets_file():
    """Verifica se o arquivo secrets.toml existe."""
    print("\n🔐 Verificando credenciais...")
    
    secrets_path = Path(".dlt/secrets.toml")
    if secrets_path.exists():
        print(f"   ✅ Arquivo .dlt/secrets.toml encontrado")
        return True
    else:
        print(f"   ❌ Arquivo .dlt/secrets.toml NÃO encontrado")
        print(f"      Crie o arquivo com base em .dlt/secrets.toml.example")
        return False


def check_postgres_connection():
    """Tenta conectar ao PostgreSQL."""
    print("\n🗄️  Verificando conexão PostgreSQL...")
    
    try:
        import dlt
        from salesforce.client import PostgresCredentials, make_postgres_client
        
        # Tenta obter credenciais
        try:
            client = make_postgres_client()
            print("   ✅ Conexão com PostgreSQL estabelecida")
            
            # Testa uma query simples
            cursor = client.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"   ℹ️  PostgreSQL: {version.split(',')[0]}")
            cursor.close()
            client.close()
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao conectar: {e}")
            return False
            
    except ImportError as e:
        print(f"   ⚠️  Não foi possível importar módulos: {e}")
        return False


def check_table_exists():
    """Verifica se a tabela User existe."""
    print("\n📊 Verificando tabela 'User'...")
    
    try:
        from salesforce.client import make_postgres_client
        
        client = make_postgres_client()
        cursor = client.cursor()
        
        # Verifica se a tabela existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'User'
            );
        """)
        
        exists = cursor.fetchone()[0]
        
        if exists:
            # Conta registros
            cursor.execute("SELECT COUNT(*) FROM \"User\";")
            count = cursor.fetchone()[0]
            print(f"   ✅ Tabela 'User' encontrada ({count} registros)")
        else:
            print(f"   ⚠️  Tabela 'User' não encontrada")
            print(f"      Altere o nome da tabela em salesforce/sources.py")
        
        cursor.close()
        client.close()
        
        return exists
        
    except Exception as e:
        print(f"   ⚠️  Erro ao verificar tabela: {e}")
        return False


def main():
    """Executa todas as verificações."""
    print("=" * 60)
    print("🔍 VERIFICAÇÃO DO AMBIENTE - dlthub PostgreSQL ETL")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_secrets_file(),
        check_postgres_connection(),
        check_table_exists(),
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks[:4]):  # Primeiras 4 verificações são críticas
        print("✅ AMBIENTE CONFIGURADO CORRETAMENTE!")
        print("\n🚀 Execute: python salesforce_pipeline.py")
    else:
        print("❌ AMBIENTE COM PROBLEMAS")
        print("\n📖 Consulte COMO_RODAR.md para instruções")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
