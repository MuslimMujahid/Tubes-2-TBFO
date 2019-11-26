# CYK (Cocke-Younger-Kasami) Parser Algorithm Kelompok Cuankie

# Membuat Fungsi CYK
def CYK(Grammar, Start, Languages):
    kamus = {}
    for a in range(0, len(Languages)):
        for b in range(a, len(Languages)):
            kamus[a,b] = []

    # Inisialisasi Variabel
    i = 0
    for c in Languages:
        for d in Grammar:
            left, right = d
            if c in right and left not in kamus[i, i]:
                kamus[i, i].append(left)
        i += 1

    # Untuk Substring yang panjangnya >= 1
    i = 0
    for e in range(1, len(Languages)):
        for i in range(0, len(Languages) - e):
            j = i + e
            for k in range(i, j):
                for a in kamus[i, k]:
                    for b in kamus[k+1, j]:
                        for d in Grammar:
                            left, right = d
                            form = ""
                            for x in range(len(right)):
                                form += right[x]
                            if (a+b in form) and left not in kamus[i, j]:
                                kamus[i, j].append(left)

    if Start in kamus[0, len(Languages)-1]:
        return True

    else:
        return False
