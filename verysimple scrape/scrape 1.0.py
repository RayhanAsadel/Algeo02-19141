import urllib.request
from bs4 import BeautifulSoup


sharelinkgan = input("AP News Link???? ")

link = sharelinkgan
linkhtml = urllib.request.urlopen(link)
soup = BeautifulSoup(linkhtml,'html.parser')

get = soup.find_all('div',class_='Article')
txt = get[0].find_all('p')
eachp = []
final = []
for i in range(len(txt)-2):
    paragraph = txt[i].get_text()
    eachp.append(paragraph)
    final = "\n".join(eachp)
print(final)

with open("doc1.txt","w") as abc:
   print(final, file=abc)