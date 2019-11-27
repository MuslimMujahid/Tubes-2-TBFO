import re
import itertools

# indeks left dan right sebagai 0 dan 1 (side)
left, right = 0, 1

# load file grammar di bagi dengan variable, terminal, dan production
def loadModel(modelPath):
	file = open(modelPath).read()
	K = (file.split("Variables:\n")[0].replace("Terminals:\n","").replace("\n",""))
	V = (file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables:\n","").replace("\n",""))
	P = (file.split("Productions:\n")[1])

	return cleanAlphabet(K), cleanAlphabet(V), cleanProduction(P)

#membuat format yang di terima python untuk production
def cleanProduction(expression):
	result = []
	#hapus spasi dan hapus titik koma dengan split pada string tersebut
	rawRulse = expression.replace('\n','').split(';')
	
	for rule in rawRulse:
		# memisahkan left side yang pipeline dengan membuat statement grammar yang baru
		leftSide = rule.split(' -> ')[0].replace(' ','')
		rightTerms = rule.split(' -> ')[1].split(' | ')
		for term in rightTerms:
			result.append( (leftSide, term.split(' ')) )
	return result

# membuat alphabet clean
def cleanAlphabet(expression):
	return expression.replace('  ',' ').split(' ')

# menghapus yang lama dan membuat production yang baru
def seekAndDestroy(target, productions):
	trash, ereased = [],[]
	for production in productions:
		if target in production[right] and len(production[right]) == 1:
			trash.append(production[left])
		else:
			ereased.append(production)
			
	return trash, ereased
 
# membuat grammar dengan format dictionary
def setupDict(productions, variables, terms):
	result = {}
	for production in productions:
		#
		if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
			result[production[right][0]] = production[left]
	return result

# menulis ulang hasil produksi 
def rewrite(target, production):
	result = []
	# mendapat posisi atau indeks target di produksi sebelah kanan
	# dan mengubah posisi menjadi list
	positions = [i for i,x in enumerate(production[right]) if x == target]
	# membuat target di produksi
	for i in range(len(positions)+1):
 		for element in list(itertools.combinations(positions, i)):
 			tadan = [production[right][i] for i in range(len(production[right])) if i not in element]
 			if tadan != []:
 				result.append((production[left], tadan))
	return result

# membuat dictionary menjadi format set atau tuples 
def dict2Set(dictionary):
	result = []
	for key in dictionary:
		result.append( (dictionary[key], key) )
	return result

# print rules dengan format grammar
def pprintRules(rules):
	for rule in rules:
		tot = ""
		for term in rule[right]:
			tot = tot +" "+ term
		print(rule[left]+" -> "+tot)

# membuat grammar dengan format pipeline standar
def prettyForm(rules):
	dictionary = {}
	for rule in rules:
		if rule[left] in dictionary:
			dictionary[rule[left]] += ' | '+' '.join(rule[right])
		else:
			dictionary[rule[left]] = ' '.join(rule[right])
	result = ""
	for key in dictionary:
		result += key+" -> "+dictionary[key]+"\n"
	return result