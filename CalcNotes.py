# -*-coding:utf8-*-

from PyQt5.QtWidgets import QApplication, QCheckBox, QWidget, QMainWindow, \
    QLabel, QGridLayout, QLineEdit, QVBoxLayout, \
    QHBoxLayout, QPushButton, QScrollArea
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QCoreApplication
import numpy as np

import re

#### CONFIGURATION DES FONTES
appfont = QFont("Avenir Next", 18)
boldappfont = QFont("Avenir Next", 14)
boldappfont.setBold(True)


class Label(QLabel):
    def __init__(self, text):
        super(Label, self).__init__()
        self.setFont(appfont)
        self.setStyleSheet("font-size:14px")
        self.setText(text)


class Titre(QLabel):
    def __init__(self, text):
        super(Titre, self).__init__()
        self.setFont(boldappfont)
        self.setStyleSheet("font-size:24px")
        self.setText(text)
        self.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setMaximumHeight(25)


class Resultat(QLabel):
    def __init__(self, text):
        super(Resultat, self).__init__()
        self.setFont(appfont)
        self.setStyleSheet("font-size:20px;color:#FF0000")
        self.setText(text)
        self.setAlignment(Qt.AlignHCenter)
        self.setMaximumHeight(55)
        self.setWordWrap(True)


class Champ(QLineEdit):
    def __init__(self):
        super(Champ, self).__init__()
        self.setMaximumWidth(50)
        self.setFont(appfont)
        self.setText("")
        self.setStyleSheet("background-color:yellow;color:black")
        self.textChanged.connect(self.couleur_etat)

    def couleur_etat(self):

        if self.text() == "":
            self.setStyleSheet("background-color:yellow;color:black")

        elif self.text().isalnum():
            # print("alpha! ",self.text())
            try:
                # print(self.text(), "--->",type(self.text()))
                txt = re.sub(",", ".", str(self.text()))
                val = float(txt)
                # print("val  = {} // type val : {}".format(val,type(val)))
                if val > 0:
                    self.setStyleSheet("background-color:white;color:green")
                else:
                    self.setStyleSheet("background-color:white;color:red")

            except ValueError or TypeError:
                self.setStyleSheet("background-color:white;color:red")


class Check(QCheckBox):
    def __init__(self):
        super(Check, self).__init__()


class ExitButton(QPushButton):
    def __init__(self, text):
        super(ExitButton, self).__init__()
        self.setStyleSheet("background-color:#FFD0D0;color:black;font-weight:bold")
        self.setText(text)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setWindowTitle("Calcul de la note sur 20")
        # self.setWindowFlag(Qt.FramelessWindowHint)

        self.setMaximumWidth(300)
        self.setMaximumHeight(400)
        self.e = 0
        self._p1 = 0
        self._p2 = 0
        self._p3 = 0
        self.val_per_col = 10

        main_lay = QVBoxLayout()
        grille = QGridLayout()

        ####
        start_txt = "En attente de donneés"
        titre = Titre("Calcul de la note sur 20")
        titre.setFont(boldappfont)

        #### OPTIONS ###
        self._chck_arrondi = Check()
        self._chck_arrondi.setText("Arrondi 0.5+")
        self._chck_arrondi.setToolTip("Cochez la case si vous voulez arrondir les notes à 0.5+")

        self._btn_exit = ExitButton("QUITTER")
        self._btn_exit.setToolTip("Cliquez pour quitter l'app")

        ### UI ###
        label1 = Label("Note de l'élève:")
        self.champ1 = Champ()
        label2 = Label("Note sur:")
        self.champ2 = Champ()
        label3 = Label("Note à ramener sur :")
        self.champ3 = Champ()
        self.label4 = Resultat(start_txt)
        self.label4.repaint()
        self.label4.setStyleSheet("font-size:20px;color:#FF0000")

        label_row = Label("nombre de valeurs par colonne:")
        self.nb_row = Champ()
        self.nb_row.setToolTip("Optionnel: \nSi le champ est vide, 10 valeurs par colonne")

        layout_options = QHBoxLayout()
        layout_options.addWidget(label_row)
        layout_options.addWidget(self.nb_row)

        self._btn_liste = QPushButton("VOIR LA LISTE DES NOTES POSSIBLES")

        grille.addWidget(self._chck_arrondi, 0, 0)
        grille.addWidget(label1, 1, 0)
        grille.addWidget(self.champ1, 1, 1)
        grille.addWidget(label2, 2, 0)
        grille.addWidget(self.champ2, 2, 1)
        grille.addWidget(label3, 3, 0)
        grille.addWidget(self.champ3, 3, 1)

        main_lay.addWidget(titre)
        main_lay.addLayout(grille)
        main_lay.addWidget(self.label4)

        main_lay.addSpacing(30)

        main_lay.addLayout(layout_options)
        main_lay.addWidget(self._btn_liste)
        main_lay.addSpacing(30)
        main_lay.addWidget(self._btn_exit)

        w = QWidget()
        # w.setMaximumHeight(600)
        w.setLayout(main_lay)

        self.setCentralWidget(w)

        self.champ1.textChanged.connect(self.note_eleve)
        self.champ2.textChanged.connect(self.total_sur)
        self.champ3.textChanged.connect(self.note_sur)
        self._btn_liste.clicked.connect(self.montrer_notes_possibles)
        self._chck_arrondi.stateChanged.connect(self.montrer_resultats)
        self._btn_exit.clicked.connect(QCoreApplication.quit)
        self.nb_row.textChanged.connect(self.nombre_de_valeurs_par_col_dans_tableau)

        # if self.champ1.textChanged or self.champ2.textChanged or self.champ3.textChanged:
        #    self.montrer_resultat()

    def nombre_de_valeurs_par_col_dans_tableau(self):
        if self.nb_row.text() == "":
            self.val_per_col = 10
        else:
            try:
                self.val_per_col = int(self.nb_row.text())
            except TypeError or ValueError:
                self.val_per_col = 10

    def note_eleve(self):
        self.e = 0
        if self.champ1.text() == "":
            print("le champ 1 est vide!")
            txt = "Champ 1 vide!"
            self.label4.setStyleSheet("color:red;font-size:20px")
            self.label4.setText(txt)
            self.e = 1
            # self.montrer_resultat()
        else:
            try:
                self._p1 = str(self.champ1.text())
                self._p1 = re.sub(",", ".", str(self.champ1.text()))
                self._p1 = float(self._p1)
                # print("nouvelle valeur P1 = ", self._p1, "TYPE : ", type(self._p1))


            except ValueError:
                self.label4.setStyleSheet("font-size:20px")
                self.txt = "Format de données du champ 1 incorrect"
                self.label4.setText(self.txt)
                self.e = 1
                # self.montrer_resultat()

        if type(self._p1) is float:
            self.montrer_resultats()

    def montrer_notes_possibles(self):
        """ affiche un pop-up"""
        t = int(round(float(self.champ2.text()), 0))  # total de l'évaluation
        c = int(round(float(self.champ3.text()), 0))  # note ramenée sur c
        self.popup = QWidget()

        ##### GETTING DATA #######
        liste_i, notes_possibles, nb_pos = show_results(t, c)

        ### Layouts utilisés ####
        popup_final_layout = QVBoxLayout()
        head_layout = QHBoxLayout()
        grille_notes = QGridLayout()

        #### PARAMETRES ####
        nb_val_per_col = self.val_per_col
        nb_col = int(round((nb_pos / nb_val_per_col), 0))  # Nombre de colonnes à afficher -> 10 valeurs par colonne
        print("NB COLONNES = ", nb_col)
        x_list = [x for x in range(nb_val_per_col)] * nb_col

        for num_col in range(0, nb_col):
            print("NUMERO COLONNE =", num_col)
            evaluation_sur = Label("/" + self.champ2.text())
            sep = Label("--->")
            note_ramenee_a = Label("/" + self.champ3.text())

            ### LARGEUR ###
            evaluation_sur.setFixedWidth(35)
            sep.setFixedWidth(35)
            note_ramenee_a.setFixedWidth(35)

            ### ALIGNEMENT ###
            evaluation_sur.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            note_ramenee_a.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            sep.setAlignment(Qt.AlignCenter)

            ### COULEUR ####
            evaluation_sur.setStyleSheet("color:red")
            note_ramenee_a.setStyleSheet("color:red")
            sep.setStyleSheet("color:red")

            ### AJOUT AU LAYOUT ###
            head_layout.addWidget(evaluation_sur)
            head_layout.addWidget(sep)
            head_layout.addWidget(note_ramenee_a)

        y_list = []
        for num_col in range(nb_col):
            # print("NUMERO COLONNE = ", num_col)
            y1 = 3 * num_col
            # print("Y1 = ", y1)
            for i in range(nb_val_per_col):
                y_list.append((y1, y1 + 1, y1 + 2))
        ziplist = list(zip(x_list, y_list))

        for note_sur, note, pos in zip(liste_i, notes_possibles, ziplist):
            ##### ARRONDI ########
            note_sur = round(note_sur, 1)
            note = round(note, 1)
            if self._chck_arrondi.isChecked():
                note = arrondi_sup(note)
                note_sur = arrondi_sup(note_sur)
            # print("NOTE A L'EVALUATION =>", note_sur," NOTE RAMENEE -> ",note)

            #### CREATION DES LABELS ######
            note_el = Label(str(note_sur))
            note_maj = Label(str(note))
            sep = QLabel("--->")

            #### SETUP DES LABELS ######
            width = 35
            note_el.setMinimumWidth(width)
            # print("LARGEUR LABEL NOTE EVAL => ",note_el.width())
            note_el.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            note_maj.setMinimumWidth(width)
            note_maj.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            #### POSITION DANS LA GRILLE #####
            x = pos[0]
            y1 = pos[1][0]
            y2 = pos[1][1]
            y3 = pos[1][2]

            #### AJOUT DES WIDGETS ######
            grille_notes.addWidget(note_el, x, y1)
            grille_notes.addWidget(sep, x, y2)
            grille_notes.addWidget(note_maj, x, y3)

        self.recap = QWidget()
        popup_final_layout.addLayout(head_layout)
        popup_final_layout.addLayout(grille_notes)
        popup_final_layout.setSpacing(10)

        self.recap.setLayout(popup_final_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.recap)

        intermediate_layout = QVBoxLayout()
        intermediate_layout.addWidget(scroll_area)

        # popup_final_layout.addWidget(scroll_area)

        # popup_final_layout.addWidget(recap)
        self.popup.setLayout(intermediate_layout)
        # self.recap.show()
        self.popup.show()

    def total_sur(self):
        """met en forme la case "évaluation sur ..." """
        self.e = 0

        try:
            self._p2 = re.sub(",", ".", str(self.champ2.text()))
            self._p2 = float(self._p2)

            self.montrer_resultats()

        except ValueError:
            self.e = 1

    def note_sur(self):
        """met en forme la case "note sur ..." """
        self.e = 0
        try:
            self._p3 = re.sub(",", ".", str(self.champ3.text()))
            self._p3 = float(self._p3)
            self.montrer_resultats()
        except ValueError:
            self.e = 1

    def montrer_resultats(self):
        """ Affiche la note"""
        # print("je calcule un résultat...")
        # print("e = ", self.e)

        try:
            self._p1 = float(self._p1)
            self._p2 = float(self._p2)
            self._p3 = float(self._p3)
            if self.e != 1:
                if self._p1 > 0 and self._p2 != 0 and self._p3 > 0:
                    # print("P1 = ", self._p1, " // P2 = ", self._p2, " // P3 = ", self._p3)
                    self.note_eleve = round((self._p1 * self._p3 / self._p2), 1)
                    if self._chck_arrondi.isChecked():
                        self.note_eleve = arrondi_sup(self.note_eleve)

                    # self.label4.setStyleSheet("font-size:40px")

                    if round(self.note_eleve, 1) > round(self._p3 / 2, 1):
                        print("note de l'élève : {}/{}".format(self.note_eleve, self._p3))
                        print("note au dessus de la moyenne!")
                        self.label4.setStyleSheet("color:green;font-size:40px")
                    else:
                        print("note de l'élève : {}/{}".format(self.note_eleve, self._p3))
                        print("note en dessous de la moyenne!")
                        self.label4.setStyleSheet("color:red;font-size:40px")
                    self.txt = str(self.note_eleve) + "/" + self.champ3.text()
                    self.label4.setText(self.txt)
                    self.e = 0

        except ValueError or TypeError:
            self.e = 0
            self.label4.setStyleSheet("font-size:20px")
            self.txt = "Pas de données valides"
            self.label4.setText(self.txt)

        ####


def show_results(t: float, c=20, step=0.5):
    """ t : total /n
    c : cible"""

    nb_pos = int(round(t / step, 0)) + 1

    notes = []
    i_list = []
    for j in np.arange(0, t + 1, step):
        i_list.append(j)
        n = j * c / t  # Calcul de l'équivalence
        notes.append(n)

    return i_list, notes, nb_pos


def arrondi_sup(val: float = 0.3):
    val = str(val)
    split = val.split(".")
    entier = int(split[0])
    decimales = int(split[1])

    if decimales == 0:
        pass
    elif 0 < decimales < 5:
        print("arrondi à 0.5")
        decimales = 5
    else:
        print("arrondi au point sup")
        decimales = 0
        entier += 1

    round_val = float(str(entier) + "." + str(decimales))
    print("valeur arrondie! {} ->{}".format(val, round_val))
    return round_val


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    w = UI()
    w.show()

    sys.exit(app.exec())
