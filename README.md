# 📰 Runaris Ghost News Management

Repositório central para gestão do feed de notícias "The Author's Pulse".

## 🚀 Como usar

1.  Edite o arquivo `news.json` seguindo o modelo.
2.  Adicione imagens na pasta `images/`.
3.  Execute `python deploy.py` para publicar as alterações.

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
