# 4 - Дан список URL различных сайтов. Нужно составить список доменных имен сайтов.

def get_dom(url_str):
    if url_str.find('://') == -1:
        index = 0
    else:
        index = url_str.find('://') + 3
    if url_str[index:].find('/') == -1:
        url_str += "/"
        last_index = -1
    else:
        last_index = url_str[index:].find('/') + index
    return url_str[index:last_index]

url_lst =[
    "https://www.google.com/search?q=url&oq=url&aqs=chrome..69i57j69i60l2.482j0j4&sourceid=chrome&ie=UTF-8",
    "https://www.tinkoff.ru/blog/articles/platinum-features/"
    "?internal_source=help-visit_on:blog-slider_from:/tinkoff-platinum/faq/",
    "https://gb.ru/education",
    "https://github.com/Sokolqe?tab=repositories",
    "https://github.com/Sokolqe",
    "app.diagrams.net"
]

result = set([get_dom(i) for i in url_lst])
print(result)