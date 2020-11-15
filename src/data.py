import io
import collections
import os
import operator
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

global fileslist
global stemmed_file
global text_dir 


text_dir = 'static/text/'



def stemstring(line):
    lowercase_line = line.lower()
    tanda_baca = '''`’”“—!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for line in lowercase_line:
        if line in tanda_baca:
            lowercase_line = lowercase_line.replace(line," ")
    words = word_tokenize(lowercase_line)
    stemmed_words = []    
    for r in words: 
        if not r in stop_words:
            stemmed_words.append(ps.stem(r))
    return stemmed_words

def stemfiles(file):
    stemmed_file = []
    for i in range (files_qty):
        file1 = open(text_dir + fileslist[i],encoding='utf-8')
        line = file1.read()
        lowercase_line = line.lower()
        tanda_baca = '''`’”“—!()-[]{};:'"\, <>./?@#$%^&*_~'''
        for line in lowercase_line:
            if line in tanda_baca:
                lowercase_line = lowercase_line.replace(line," ")
        words = word_tokenize(lowercase_line)
        stemmed_words = []    
        for r in words: 
            if not r in stop_words:
                stemmed_words.append(ps.stem(r))
        stemmed_file.append(stemmed_words)
    return stemmed_file

def get_unique(stemmed_files,stemmed_query):
    files_qty = len(stemmed_files)
    unique = set(stemmed_files[0])
    if files_qty > 1:
        for i in range(1,files_qty):
            unique = unique.union(set(stemmed_files[i]))
    unique = unique.union(set(stemmed_query))
    return unique 

def get_bow(stemmed_file,unique):
    bow = []
    N = len(stemmed_file)
    for i in range (N):
        bow.append(dict.fromkeys(unique,0))
        for word in stemmed_file[i]:
            bow[i][word] += 1
    return bow

def bow_query(stemmed_query,unique):
    bow = dict.fromkeys(unique,0)
    for word in stemmed_query:
        bow[word] += 1
    return bow

def sim(frekuensi1,frekuensi2):
    import math
    sum = 0
    norm1 = 0
    norm2 = 0
    for key in (frekuensi1):
        sum += (frekuensi1)[key]*(frekuensi2)[key]
        norm1 = norm1+(frekuensi1)[key]*(frekuensi1)[key]
        norm2 = norm2+(frekuensi2)[key]*(frekuensi2)[key]
    return sum/(math.sqrt(norm1)*math.sqrt(norm2))

def get_result(bowlist,bow_query):
    result_dict = dict.fromkeys(fileslist,0)
    N = len(bowlist)
    for i in range(N):
        result_dict[fileslist[i]] = sim(bowlist[i],bow_query)
    sorted_result = sorted(result_dict.items(), reverse=True, key=operator.itemgetter(1))
    return(sorted_result)

def show_result(sorted_result,query):
    printed = 0
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
    """
    html += "<left><h3> Result for <i>" + query + "</i> : </h3></left>"
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
            html += "<br>"
            printed += 1
        else:
            continue
    if printed == 0:
        html += "<p><left>Tidak ada dokumen yang sesuai dengan query.</left></p>"
    html += "</body></html>"
    with open(os.path.join(current_path,'templates','hasil.html'),"w",encoding='utf-8') as write:
        write.write(html)

def show_term(stemmed_query,bow_query,bowlist):    
    term = []

    list_bowquery = []
    list_bowquery.append(bow_query)

    new_bowlist = list_bowquery + bowlist
    new_fileslist = ['Query'] + fileslist

    M = len(stemmed_query)
    N = len(new_bowlist)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
    """
    for i in range (N):
        if i == 0:
            html += "<p><left>dQuery : " + new_fileslist[i] + "</left></p>"
        else:
            html += "<p><left>d" + str(i) + ' : ' + new_fileslist[i] + "</left></p>"
    html += "</body></html>"
    with open(os.path.join(current_path,'templates','list.html'),"w",encoding='utf-8') as write:
        write.write(html)

def get_term_table(stemmed_query,bow_query,bowlist): 
    term = []
    termtable = pd.DataFrame()

    list_bowquery = []
    list_bowquery.append(bow_query)

    new_bowlist = list_bowquery + bowlist
    new_fileslist = ['Query'] + fileslist

    M = len(stemmed_query)
    N = len(new_bowlist)

    key = [p for p in range(1,N)]

    for i in range (M):
        term.append(dict.fromkeys(['Query'] + key,0))
        for k in range(N):
            for word in new_bowlist[k]:
                if word == stemmed_query[i]:
                    if k==0:
                        term[i]['Query'] = new_bowlist[k][word]
                    else:
                        term[i][k] = new_bowlist[k][word]
    termx = pd.DataFrame(term,index=stemmed_query)
    termtable = termx
    return termtable

#fileslist
current_path = os.getcwd()
files_path = os.path.join(current_path,'static','text')
fileslist = os.listdir(files_path)

#files_qty
files_qty = len(fileslist)

#stemmed_file
stemmed_file = stemfiles(fileslist)