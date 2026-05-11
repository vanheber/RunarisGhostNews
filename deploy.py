import os
import json
import ftplib
from pathlib import Path
from dotenv import load_dotenv

# Carregar configurações
load_dotenv()

FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')
FTP_DIR = os.getenv('FTP_DIR', '/public_html/ghost/news')

def validate_json(file_path):
    print(f"🔍 Validando {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'news' not in data:
                raise ValueError("JSON inválido: Chave 'news' não encontrada.")
            print("✅ JSON válido.")
            return True
    except Exception as e:
        print(f"❌ Erro de validação: {e}")
        return False

def deploy():
    news_file = Path('news.json')
    
    if not validate_json(news_file):
        return

    if not all([FTP_HOST, FTP_USER, FTP_PASS]):
        print("❌ Erro: Credenciais de FTP não configuradas no arquivo .env")
        return

    print(f"🚀 Conectando a {FTP_HOST}...")
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            
            # Navegar para o diretório
            try:
                ftp.cwd(FTP_DIR)
            except:
                print(f"📂 Criando diretório {FTP_DIR}...")
                # Tenta criar o caminho recursivamente (simplificado)
                parts = FTP_DIR.strip('/').split('/')
                current = ''
                for part in parts:
                    current += '/' + part
                    try:
                        ftp.mkd(current)
                    except:
                        pass
                ftp.cwd(FTP_DIR)

            # Upload do news.json
            print(f"📤 Subindo {news_file.name}...")
            with open(news_file, 'rb') as f:
                ftp.storbinary(f'STOR {news_file.name}', f)
            
            # TODO: Futuramente implementar upload recursivo da pasta images/
            
            print("✨ Deploy concluído com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro no deploy: {e}")

if __name__ == "__main__":
    deploy()
