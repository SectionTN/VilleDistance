from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QInputDialog
from numpy import array
from pickle import dump


def verif_chemin(ch):
    if ch[0] == ch[-1] :
        return False
    i = 0
    while i < len(ch) - 1 and ord(ch[i]) in range(ord("A"), ord("J") + 1):
        i += 1
    return ord(ch[i]) in range(ord("A"), ord("Z") + 1)


def taille_fichier_texte():
    f_text = open("distance.txt", "r")
    i = 0
    ch = f_text.readline()
    while ch != "":
        i += 1
        ch = f_text.readline()
    return i


def chercher_chemin(T, N, chem):
    for i in range(N):
        if T[i]["chem"] == chem or T[i]["chem_inv"] == chem:
            return True
    return False


def recuperer_distance(T, N, chem):
    for i in range(N):
        if T[i]["chem"] == chem or T[i]["chem_inv"] == chem:
            return int(T[i]["distance"])
    return 0


def calculer_distance(T, N, chemin):
    S = 0
    for i in range(len(chemin) - 1):
        if chercher_chemin(T, N, chemin[i] + chemin[i + 1]):
            S += recuperer_distance(T, N, chemin[i] + chemin[i + 1])
        else:
            S += 0
    return S


def manipuler(chemin):
    f_text = open("distance.txt", "r")
    G = taille_fichier_texte()
    T = array([dict] * G)
    for i in range(G):
        e = dict(chem=str, distance=int, chem_inv=str)
        ch = f_text.readline()
        pos_vergule = ch.find(",")
        pos_egale = ch.find("=")
        e["chem"] = ch[pos_vergule - 1] + ch[pos_vergule + 1]
        e["distance"] = ch[pos_egale + 1: -1]
        e["chem_inv"] = ch[pos_vergule + 1] + ch[pos_vergule - 1]
        T[i] = e
    f_text.close()
    return calculer_distance(T, G, chemin)


def remplir():
    global N, TG
    N = window.n.text()
    if not N.isdigit():
        QMessageBox.critical(window, "Erreur de saisie", "N doit étre numerique", QMessageBox.Ok)
    elif not 3 <= int(N) <= 7:
        QMessageBox.critical(window, "Erreur de saisie", "N doit étre compris dans [3, 7]", QMessageBox.Ok)
    else:
        N = int(N)
        TG = array([dict] * N)
        file_chemin = open("chemin.dat", 'wb')
        e = dict(chem=str, dist=int)
        for i in range(N):
            chemin = QInputDialog.getText(window, "Chemin", "Donnez le chemin" + " " + str(i + 1) + ":")
            chemin = chemin[0]
            while chemin == "" or verif_chemin(chemin) is False:
                chemin = QInputDialog.getText(window, "Chemin", "Re-Donnez le chemin" + " " + str(i + 1) + ":")
                chemin = chemin[0]
            e["chem"] = chemin
            e["dist"] = manipuler(chemin)
            TG[i] = e
            dump(e, file_chemin)
            window.t_chemdist.insertRow(i)
            window.t_chemdist.setItem(i, 0, QTableWidgetItem(str(e["chem"])))
            window.t_chemdist.setItem(i, 1, QTableWidgetItem(str(e["dist"])))
        file_chemin.close()


def trier(TG, N):
    for i in range(N):
        for j in range(N - i - 1):
            if TG[j]["dist"] > TG[j + 1]["dist"]:
                aux = TG[i]
                TG[i] = TG[i + 1]
                TG[i + 1] = aux


def afficher():
    trier(TG, N)
    window.t_mchem.clear()
    window.t_mchem.addItem("Le meilleur chemin est:" + " " + TG[0]["chem"])


application = QApplication([])
window = loadUi("interface_chemin.ui")
window.show()
window.b_remplir.clicked.connect(remplir)
window.b_afficher.clicked.connect(afficher)
application.exec_()
