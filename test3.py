fichier_classe = open("Culure_BDD_V3.csv", "w")
sortie = csv.writer(fichier_classe)

with open('class1.csv', newline='') as mon_fichier:
    liste2 = list(csv.reader((mon_fichier), dialect='excel', delimiter=';', lineterminator=';;;'))
    liste_splitee = []
    for ligne in liste2:
        ligne_splitee = ligne[0].split(',')
        liste_splitee.append(ligne_splitee)

import operator

liste_triee = sorted(liste_splitee, key=operator.itemgetter(28), reverse=True)

for ligne in liste_triee:
    sortie.writerow(ligne)

fichier_classe.close()