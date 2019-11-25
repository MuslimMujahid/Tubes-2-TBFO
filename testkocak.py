def getRulesFromExternal(namafile):
	k = open(namafile,"r").read().split("\n")
	b = []
	for i in range(0,len(k)):
		if (not (k[i] == '') and ("->" in k[i])):
			b.append(k[i])
			
	return b



d = getRulesFromExternal("grammartest.txt")
print(d)


# Grammar = ["S->AB", "S->BC", "A->AB", "A->a", "B->CC", "B->b", "C->AB", "C->a"]



# c = getRulesFromExternal("grammartest.txt")
# print(c)


