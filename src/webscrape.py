import urllib.request
from bs4 import BeautifulSoup
import os

# Input link apnews [associated press]
sharelinkgan = input("Masukkan Link AP News:  ")

# Masukkan link bentuk html -> parse pakai beautifulsoup
link = sharelinkgan
linkhtml = urllib.request.urlopen(link)
soup = BeautifulSoup(linkhtml,'html.parser')

# Membentuk text
get = soup.find_all('div',class_='Article')
txt = get[0].find_all('p')
eachp = []
final = []
for i in range(len(txt)):
    paragraph = txt[i].get_text()
    eachp.append(paragraph)
    final = "\n".join(eachp)
print(final)

# Write file atau save ke file
path = os.getcwd()
filename = input("Masukkan nama file beserta format: ")
with open(os.path.join(path,'static','text',filename),"w",encoding='utf-8') as write:
   print(final, file=write)