import os
import json
import ftplib
from pathlib import Path
# Carregar configurações (.env manual para evitar dependências externas)
def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env()

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

            # Arquivos para subir
            files_to_upload = ['news.json', '.htaccess']
            for filename in files_to_upload:
                local_file = Path(filename)
                if local_file.exists():
                    print(f"📤 Subindo {filename}...")
                    with open(local_file, 'rb') as f:
                        ftp.storbinary(f'STOR {filename}', f)
                else:
                    print(f"⚠️ Aviso: Arquivo {filename} não encontrado localmente.")
            
            # Upload recursivo da pasta images/
            images_dir = Path('images')
            if images_dir.exists() and images_dir.is_dir():
                print(f"📤 Subindo pasta images/...")
                # Garantir que o diretório images/ existe no FTP
                try:
                    ftp.cwd('images')
                except:
                    ftp.mkd('images')
                    ftp.cwd('images')
                ftp.cwd(FTP_DIR)  # volta ao diretório base
                for img_file in images_dir.iterdir():
                    if img_file.is_file():
                        print(f"  📤 {img_file.name}...")
                        with open(img_file, 'rb') as f:
                            ftp.storbinary(f'STOR images/{img_file.name}', f)
            else:
                print(f"⚠️ Aviso: Pasta images/ não encontrada.")
            
            print("✨ Deploy concluído com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro no deploy: {e}")

if __name__ == "__main__":
    deploy()
