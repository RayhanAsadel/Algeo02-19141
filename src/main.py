import data

query = input("Masukkan query: ")
stemmed_query = data.stemstring(query)

unique = data.get_unique(data.stemmed_file,stemmed_query)
bowlist = data.get_bow(data.stemmed_file,unique)
bow_query = data.bow_query(stemmed_query,unique)

sorted_result = data.get_result(bowlist,bow_query)
data.show_result(sorted_result)