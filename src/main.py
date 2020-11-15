import data
import pandas as pd
import os.path



query = input("Masukkan query: ")
stemmed_query = data.stemstring(query)

unique = data.get_unique(data.stemmed_file,stemmed_query)
bowlist = data.get_bow(data.stemmed_file,unique)
bow_query = data.bow_query(stemmed_query,unique)

sorted_result = data.get_result(bowlist,bow_query)
data.show_result(sorted_result)
data.show_term(stemmed_query,bow_query,bowlist)

#Dapatkan dataframe untuk termtable
termtable = pd.DataFrame()
termtable = data.get_term_table(stemmed_query,bow_query,bowlist)

#render dataframe as html
html = termtable.to_html()

#Mengwrite termtable ke html pada folder templates
path = os.getcwd()
with open(os.path.join(path,'templates','termtable.html'), "w") as file1:
    file1.write(html)
    file1.close()
