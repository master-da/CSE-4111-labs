import requests
from bs4 import BeautifulSoup

start_word = "Colonialism"
end_word = "Yan Bingtao"

max_depth = 4

api_url = "https://en.wikipedia.org/wiki/"

def req(word, depth):
    
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Probing: ", word)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    if depth > max_depth:
        return None
    url = api_url + word
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        if link.get('href') and link.get('href').startswith('/wiki/') and link.get('href').find(':') == -1 and link.get('title'):
            if link.get('title') == end_word:
                return [word, end_word]
            else:
                print("link: ", link.get('title'), "from:", word, "depth:", depth)
                res = req('_'.join(link.get('title').split(" ")), depth + 1)
                if res:
                    return [word] + res
    return None

print(req(start_word, 1))
