import ast
f = open("test_related_feature_words.txt",'r')
summary = f.read()
f.close()
result = ast.literal_eval(summary)
print(result["food"].split(" "))
