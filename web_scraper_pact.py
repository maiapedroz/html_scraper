import requests
import re
from bs4 import BeautifulSoup
from ebooklib import epub

# pegar o titulo do arco
def pegarTitulo(arco, url):
    r = requests.get(url)
    b = BeautifulSoup(r.text, "html.parser")

    div = b.find("div", {"class": "entry-content"})
    indice = 0
    for p in div.find_all("p"):
        indice += 1
        if indice == arco:
            strong = p.find("strong")
            if strong:  # Verifica se o elemento <strong> existe
                # Filtra apenas os textos que estão diretamente dentro do <strong>
                titulo = ''.join([str(content) for content in strong.contents if isinstance(content, str)])
                titulo = titulo.strip()  # Remove espaços no início e no final
                titulo = titulo.replace(" ", "").replace(":", "_")  # Remove espaços e substitui ":" por "_"
                return titulo

    return None  # Retorna None se o arco não for encontrado


# Gera um array com todos os links dos capitulos de um arco
def LinksDosCapitulos(arco, url):
    r = requests.get(url)
    b = BeautifulSoup(r.text, "html.parser")

    div = b.find("div", {"class": "entry-content"})
    indice = 0
    for p in div.find_all("p"):
        indice+=1
        if(indice == arco):
            links = p.find_all('a')

    saida = []
    indice = 1
    for link in links:
        
        href = link['href']
        # Adiciona 'https://' se a URL não começar com http:// ou https://
        if not (href.startswith('http://') or href.startswith('https://')):
            href = f'https://{href}'  # Adiciona o prefixo https://
            
        if arco == 6 and indice == 11:
            pass
        elif arco == 7 and indice == 3:
            saida.append("https://pactwebserial.wordpress.com/2014/06/03/void-7-3/")
            saida.append("https://pactwebserial.wordpress.com/2014/06/07/void-7-4/")
            saida.append(href)
        elif arco == 8 and indice == 5:
            saida.append("https://pactwebserial.wordpress.com/2014/07/19/signature-8-5/")
        elif arco == 10 and indice == 3:
            saida.append("https://pactwebserial.wordpress.com/2014/08/21/mala-fide-10-3/")
        elif arco == 10 and indice == 4:
            saida.append("https://pactwebserial.wordpress.com/2014/08/23/mala-fide-10-4/")
        elif arco == 15 and indice == 2:
            saida.append("https://pactwebserial.wordpress.com/2015/01/08/possession-15-2/")
        elif arco == 16 and indice == 3:
            saida.append("https://pactwebserial.wordpress.com/2015/01/31/judgment-16-3/")
            saida.append(href)
        else:
            saida.append(href)  # Adiciona a URL (agora sempre com https://)
        indice+=1

    return saida

# Lê o table of contents e retorna o total de arcos
def pegarTotaldeArcos(url):
    r = requests.get(url)
    b = BeautifulSoup(r.text, "html.parser")

    nArcos = 0

    div = b.find("div", {"class": "entry-content"})
    for p in div.find_all("p"):
        nArcos += 1
    
    return nArcos

# Extrai o conteudo de um capitulo
def LerConteudo(links, conteudoCapitulos):
    for url in links:
        #print(url) # debug checar URLs
        
        r = requests.get(url)
        b = BeautifulSoup(r.text, "html.parser")


        div = b.find("div", {"class": "entry-content"})
        chapter_text = ""
        for p in div.find_all("p"):
            chapter_text += p.text + "\n\n"
        conteudoCapitulos.append(chapter_text)


# Função para criar o arquivo epub
def create_epub(book_title, capitulos):
    book = epub.EpubBook()

    # Definir metadados do livro
    book.set_title(book_title)
    book.set_language('en')

    # Criar e adicionar capítulos ao epub
    chapter_items = []
    for i, chapter in enumerate(capitulos):
        chapter_title = f"Chapter {i+1}"
        epub_chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i+1}.xhtml', lang='en')
        epub_chapter.content = f"<h1>{chapter_title}</h1><p>{chapter.replace('\n', '<br>')}</p>"
        book.add_item(epub_chapter)
        chapter_items.append(epub_chapter)
    
    # Definir a estrutura de navegação
    book.toc = tuple(chapter_items)
    book.spine = ['nav'] + chapter_items

    # Adicionar o índice
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Definir o estilo CSS básico
    style = 'BODY { font-family: Arial, sans-serif; }'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Salvar o arquivo epub
    epub.write_epub(f'{book_title}.epub', book, {})


# Main:
url = 'https://pactwebserial.wordpress.com/table-of-contents/'
totaldeEPUBS = 0
nArcos = pegarTotaldeArcos(url)
print(nArcos, 'arcos encontrados, digite quais você quer baixar (Siga esse exemplo para baixar os arcos 11 ao 16: 11-16, ou deixe em branco para baixar todos) ')
ArcosEscolhidos = input()
if not ArcosEscolhidos:
    inicio = 1
    fim = nArcos
else:
    inicio, fim = map(int, ArcosEscolhidos.split('-'))

# Corrigido para incluir o fim
for arco in range(inicio, fim + 1):

    conteudoCapitulos = []
    
    LerConteudo(LinksDosCapitulos(arco, url), conteudoCapitulos)
    create_epub(pegarTitulo(arco, url), conteudoCapitulos)
    totaldeEPUBS+=1

print(f"{totaldeEPUBS} EPUBs foram criados")