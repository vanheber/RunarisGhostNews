# 📰 Runaris Ghost News Management

Repositório central para gestão do feed de notícias "The Author's Pulse".

## 🚀 Como usar

1.  Edite o arquivo `news.json` seguindo o modelo.
2.  Adicione imagens na pasta `images/`.
3.  Execute `python3 deploy.py` para publicar as alterações. O script enviará o `news.json` e o `.htaccess` (CORS) para o servidor.

## ⚙️ Requisitos Técnicos

*   **CORS**: O repositório inclui um arquivo `.htaccess` pré-configurado para permitir que o Dashboard do Ghost acesse o JSON de qualquer origem.
*   **Deploy**: Utiliza FTP nativo do Python, sem dependências externas (não requer `python-dotenv`).

## 📐 Estrutura do JSON

Cada item no array `news` deve seguir este formato:

```json
{
    "id": "unique-id",
    "type": "novidade | video | release",
    "title": "Título Curto e Impactante",
    "content": "Descrição breve do conteúdo.",
    "url": "https://link-de-destino.com",
    "size": "large | medium | small",
    "image": "https://runaris.com.br/ghost/news/images/nome-da-imagem.jpg"
}
```

> **Nota**: O arquivo final é servido em `https://runaris.com.br/ghost/news/news.json`.

### Tamanhos (Size):
- **large**: Ocupa a largura total da sidebar. Ideal para anúncios principais.
- **medium**: Ocupa uma coluna. Bom para vídeos ou posts de blog.
- **small**: Ocupa uma coluna. Ideal para atualizações rápidas.
