import sys, helper

# indeks left dan right sebagai 0 dan 1
left, right = 0, 1

# List kosong untuk membuat format baru terminal variable dan production
K, V, Productions = [],[],[]

# Variable baru untuk memanipulasi variable yang ter-input pada grammar
variablesJar = ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3', 'K3', 'L3', 'M3', 'N3', 'O3', 'P3', 'Q3', 'R3', 'S3', 'T3', 'U3', 'V3', 'W3', 'X3', 'Y3', 'Z3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4', 'K4', 'L4', 'M4', 'N4', 'O4', 'P4', 'Q4', 'R4', 'S4', 'T4', 'U4', 'V4', 'W4', 'X4', 'Y4', 'Z4']
variablesJar += ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5', 'K5', 'L5', 'M5', 'N5', 'O5', 'P5', 'Q5', 'R5', 'S5', 'T5', 'U5', 'V5', 'W5', 'X5', 'Y5', 'Z5']
variablesJar += ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6', 'J6', 'K6', 'L6', 'M6', 'N6', 'O6', 'P6', 'Q6', 'R6', 'S6', 'T6', 'U6', 'V6', 'W6', 'X6', 'Y6', 'Z6']
variablesJar += ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7', 'J7', 'K7', 'L7', 'M7', 'N7', 'O7', 'P7', 'Q7', 'R7', 'S7', 'T7', 'U7', 'V7', 'W7', 'X7', 'Y7', 'Z7']
variablesJar += ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8', 'J8', 'K8', 'L8', 'M8', 'N8', 'O8', 'P8', 'Q8', 'R8', 'S8', 'T8', 'U8', 'V8', 'W8', 'X8', 'Y8', 'Z8']
variablesJar += ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9', 'J9', 'K9', 'L9', 'M9', 'N9', 'O9', 'P9', 'Q9', 'R9', 'S9', 'T9', 'U9', 'V9', 'W9', 'X9', 'Y9', 'Z9']
variablesJar += ['A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10', 'J10', 'K10', 'L10', 'M10', 'N10', 'O10', 'P10', 'Q10', 'R10', 'S10', 'T10', 'U10', 'V10', 'W10', 'X10', 'Y10', 'Z10']
variablesJar += ['A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11', 'I11', 'J11', 'K11', 'L11', 'M11', 'N11', 'O11', 'P11', 'Q11', 'R11', 'S11', 'T11', 'U11', 'V11', 'W11', 'X11', 'Y11', 'Z11']
variablesJar += ['A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12', 'I12', 'J12', 'K12', 'L12', 'M12', 'N12', 'O12', 'P12', 'Q12', 'R12', 'S12', 'T12', 'U12', 'V12', 'W12', 'X12', 'Y12', 'Z12']

def isUnitary(rule, variables):
	# Sebelah kanan memiliki satu variabel
	if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
		return True
	return False

def isSimple(rule):
	# Variable menghasilkan satu terminal
	if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
		return True
	return False

# Mengubah nonterminal menjadi variable yang ada yang sudah di definisikan (handle variable)
for nonTerminal in V:
	if nonTerminal in variablesJar:
		variablesJar.remove(nonTerminal)

# Ngubah rule start menjadi start baru (langkah menuju remove unnit production) S0 -> S
def START(productions, variables):
	variables.append('S0')
	return [('S0', [variables[0]])] + productions

# menghapus rules yang memiliki term dan variable, mengubah A-Bc menjadi A->BZ dann Z->c
def removeTERM(productions, variables):
	newProductions = []
	# Membuat dictionary atau object untuk semua produksi, ex: A->a menjadi format dictionary python ["a"]="A"
	dictionary = helper.setupDict(productions, variables, terms=K)
	for production in productions:
		# term harus di cek apakah rules production simple
		if isSimple(production):
			# Produksi baru tidak akan di rubah bila CFG simple
			newProductions.append(production)
		else:
			for term in K:
				for index, value in enumerate(production[right]):
					if term == value and not term in dictionary:
						# produksi baru dengan bentuk variable->term dan menambahkannya (append)
						dictionary[term] = variablesJar.pop()
						# Set variable akan di update dengan menambah variable baru
						V.append(dictionary[term])
						newProductions.append( (dictionary[term], [term]) )
				
						production[right][index] = dictionary[term]
					elif term == value:
						production[right][index] = dictionary[term]
			newProductions.append( (production[left], production[right]) )
			
	# mengubah set yang lama dan menjadikannya rules
	return newProductions

# Kode untuk eliminasi rules yang bukan non unitary
def nonunitaryremoval(productions, variables):
	result = []
	for production in productions:
		k = len(production[right])
		# temporary variable adalah production left-side
		if k <= 2:
			result.append( production )
		else:
			newVar = variablesJar.pop(0)
			variables.append(newVar+'1')
			result.append( (production[left], [production[right][0]]+[newVar+'1']) )
			i = 1
#TODO
			for i in range(1, k-2 ):
				var, var2 = newVar+str(i), newVar+str(i+1)
				variables.append(var2)
				result.append( (var, [production[right][i], var2]) )
			result.append( (newVar+str(k-2), production[right][k-2:k]) ) 
	return result
	

# menghapus non-terminal rules seperti epsilon, membuat rules baru
def DELmakeNewRules(productions):
	newSet = []
	# menghapus leftside production sehingga hanya tersisa rightside untuk di manipulasi
	outlaws, productions = helper.seekAndDestroy(target='e', productions=productions)
	# membuat rules baru
	for outlaw in outlaws:
		for production in productions + [e for e in newSet if e not in productions]:
			if outlaw in production[right]:
				newSet = newSet + [e for e in  helper.rewrite(outlaw, production) if e not in newSet]

	# menambahkan rules yang tidak di ubah sebelumnya 
	return newSet + ([productions[i] for i in range(len(productions)) 
							if productions[i] not in newSet])

# remove unit terminal
def unit_production(rules, variables):
	unitaries, result = [], []
	for aRule in rules:
		if isUnitary(aRule, variables):
			unitaries.append( (aRule[left], aRule[right][0]) )
		else:
			result.append(aRule)
	for uni in unitaries:
		for rule in rules:
			if uni[right]==rule[left] and uni[left]!=rule[left]:
				result.append( (uni[left],rule[right]) )
	
	return result

# remove unit production, bila satu variable menghasilkan satu variable
def UNITremoval(productions, variables):
	i = 0
	result = unit_production(productions, variables)
	tmp = unit_production(result, variables)
	while result != tmp and i < 1000:
		result = unit_production(tmp, variables)
		tmp = unit_production(result, variables)
		i+=1
	return result

# Hasil akhir production setelah CFG di ubah menjadi CNF
def CFG2CNF(modelPath):
	K, V, Productions = helper.loadModel(modelPath)
	Productions = START(Productions, V)
	Productions = removeTERM(Productions, V)
	Productions = nonunitaryremoval(Productions, V)
	Productions = DELmakeNewRules(Productions)
	Productions = UNITremoval(Productions, V)
	return K, Productions

