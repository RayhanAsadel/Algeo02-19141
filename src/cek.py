import io
import collections
import os
import operator
import pandas as pd
from nltk.tokenize import word_tokenize

#fileslist
current_path = os.getcwd()
files_path = os.path.join(current_path,'static','text')
fileslist = os.listdir(files_path)

#files_qty
files_qty = len(fileslist)

text_dir = 'static/text/'

printed = 0
import data
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <p><center> <h1> Hasil Pencarian </center> </h1> </p>
"""
query = input("Masukkan query: ")
stemmed_query = data.stemstring(query)
unique = data.get_unique(data.stemmed_file,stemmed_query)
bowlist = data.get_bow(data.stemmed_file,unique)
bow_query = data.bow_query(stemmed_query,unique)
sorted_result = data.get_result(bowlist,bow_query)
for i in range (files_qty):
    if sorted_result[i][1] != 0:
        html += "<p><left><a href=/static/text/" + sorted_result[i][0] + "> " + sorted_result[i][0] + " </a></left></p>"
        file1 = open(text_dir+sorted_result[i][0],encoding='utf-8')
        firstline = file1.readline()
        line = file1.read()
        words = word_tokenize(line)
        html += "\n"
        html += "<p><left>Jumlah kata: {}".format(len(words)) + "</left></p>"
        html += "\n<p><left>Tingkat Kemiripan: {:.2f} %".format(sorted_result[i][1]*100) + "</left></p>"
        html += "\n<p><left>" + firstline + "</left></p>"
        printed += 1
    else:
        continue
if printed == 0:
    html += "<p><left>Tidak ada dokumen yang sesuai dengan query.</left></p>"

html += "</body></html>"

with open(os.path.join(current_path,'templates','tes.html'),"w",encoding='utf-8') as write:
   write.write(html)

"""
for i in range (files_qty):
    if sorted_result[i][1] != 0:
        print (sorted_result[i][0])
        file1 = open(text_dir+sorted_result[i][0])
        firstline = file1.readline()
        line = file1.read()
        words = word_tokenize(line)
        print("Jumlah kata: {}".format(len(words)))
        print("Tingkat Kemiripan: {:.2f} %".format(sorted_result[i][1]*100))
        print(firstline)
        printed += 1
    else:
        continue
if printed == 0:
    print("Tidak ada dokumen yang sesuai dengan query.")
    print()
"""
