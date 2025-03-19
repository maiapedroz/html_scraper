# html-webscraper
#### Script para ler o html, compilar o conteúdo e gerar um arquivo ePUB.
#### Feito com o objetivo de ler livros web serializados do Wildbow (Worm, Pact, Twig...)
#### Autor: Pedro Maia.
---
## > Como funciona?
Com a biblioteca BeautifulSoup4, é possível puxar todo o html da página e consequentemente separar o hmtl por elementos div. Dessa forma o script consegue buscar por títulos, conteúdo e numero de capitúlos separadamente.

## Erros conhecidos
Não baixa o arco 0 de Ward, debugando descobri que o problema está no final do capítulo 2, entre a ultima linha e o texto de proximo capitulo, porém como já li, ignorei o problema.

