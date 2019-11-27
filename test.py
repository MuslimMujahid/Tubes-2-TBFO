tokens = [':', '.', '+', '-', '*', '/', '<', '>', '<=', '>=', '==', '(', ')', '[', ']', ',', "'"]
languages = open("syntax.txt").read() + '\nqwertyuiop'

for token in tokens:
    read = len(token)
    for i in range(len(languages)-read):
        CC = languages[i:i+read]
        if CC == token:
            if not (languages[i-1] == " "):
                print("Tidak ada spasi di awal")
                print("before")
                print (languages[:i])
                print("after")
                print(languages[i:])
                languages = languages[:i] + " " + languages[i:]
            elif not (languages[i+read+1] == " "):
                print("Tidak ada spasi setelah")
                print("before")
                print (languages[:i+read])
                print("after")
                print(languages[i+read:])
                languages = languages[:i+read] + " " + languages[i+read:]
languages = languages[:len(languages)-11]
languages = languages.split(' ')
for x in range(languages.count('')) :
    languages.remove('')
print(languages)
# print(languages.split(' '))