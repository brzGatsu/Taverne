# -*- coding: utf-8 -*-
from PySide6 import QtWidgets, QtCore, QtGui
import copy
import re
from RuestungenPlus import RSCharakterRuestung
from Wolke import Wolke
from EventBus import EventBus
import logging
from CharakterRuestungPickerWrapper import RuestungPicker
from Core.Ruestung import Ruestung, RuestungDefinition
from Hilfsmethoden import Hilfsmethoden
from QtUtils.TextTagCompleter import TextTagCompleter
from functools import partial

class RSCharakterRuestungWrapper(QtCore.QObject):
    modified = QtCore.Signal()
    reloadRSTabs = QtCore.Signal()

    def __init__(self, index):
        super().__init__()

        self.index = index
        self.charTeilrüstungen = Wolke.Char.teilrüstungen1
        if self.index == 1:
            self.charTeilrüstungen = Wolke.Char.teilrüstungen2
        elif self.index == 2:
            self.charTeilrüstungen = Wolke.Char.teilrüstungen3

        self.form = QtWidgets.QWidget()
        self.ui = RSCharakterRuestung.Ui_formAusruestung()
        self.ui.setupUi(self.form)

        self.currentlyLoading = False

        self.ruestungsKategorien = list(Wolke.DB.einstellungen["Rüstungen: Kategorien"].wert.keys())
        self.ruestungsEigenschaften = Wolke.DB.einstellungen["RüstungenPlus Plugin: Rüstungseigenschaften"].wert

        self.ui.editGesamtName.editingFinished.connect(self.updateGesamtRuestung)
        self.ui.spinGesamtBE.valueChanged.connect(self.updateGesamtRuestung)

        if self.ruestungsEigenschaften:
            self.ui.labelHinweis.setText(self.ui.labelHinweis.text() + "\nEs werden außerdem nur die Eigenschaften der gesamten Rüstung (Zeile 1) ausgewertet.")

            self.labelEigenschaften = QtWidgets.QLabel("Eigenschaften")
            self.labelEigenschaften.setProperty("class", "h4")
            self.ui.Ruestungen.addWidget(self.labelEigenschaften, 0, 5, 1, 1)

            self.editGesamtEigenschaften = QtWidgets.QLineEdit()
            self.editGesamtEigenschaften.editingFinished.connect(self.updateGesamtRuestung)
            self.editGesamtEigenschaften.editingFinished.connect(partial(self.updateEigenschaftenTooltip, edit=self.editGesamtEigenschaften))
            self.ui.Ruestungen.addWidget(self.editGesamtEigenschaften, 1, 5, 1, 1)
            self.ui.editGesamtName.setMaximumSize(QtCore.QSize(200, 16777215))

        self.labels = []
        self.editRName = []
        self.sbZRW = []
        self.buttons = []
        self.editEigenschaften = []
        self.eigenschaftenCompleter = []
        row = 3
        index = 0
        for kategorie in self.ruestungsKategorien:
            col = 0
            label = QtWidgets.QLabel(kategorie)
            self.labels.append(label)
            self.ui.Ruestungen.addWidget(label, row, col, 1, 1)
            col += 1

            editRName = QtWidgets.QLineEdit()
            editRName.editingFinished.connect(self.updateRuestungen)
            if self.ruestungsEigenschaften:
                editRName.setMaximumSize(QtCore.QSize(400, 16777215))
            self.editRName.append(editRName)
            self.ui.Ruestungen.addWidget(editRName, row, col, 1, 3)
            col += 3

            spinZRW = QtWidgets.QSpinBox()
            spinZRW.valueChanged.connect(self.updateRuestungen)
            self.sbZRW.append(spinZRW)
            spinZRW.setMinimum(0)
            spinZRW.setMaximum(99)
            spinZRW.setAlignment(QtCore.Qt.AlignCenter)
            spinZRW.setButtonSymbols(QtWidgets.QSpinBox.PlusMinus)
            self.ui.Ruestungen.addWidget(spinZRW, row, col, 1, 1)
            col += 1

            if self.ruestungsEigenschaften:
                leEigenschaft = QtWidgets.QLineEdit()
                leEigenschaft.editingFinished.connect(self.updateRuestungen)
                leEigenschaft.editingFinished.connect(partial(self.updateEigenschaftenTooltip, edit=leEigenschaft))
                self.editEigenschaften.append(leEigenschaft)
                self.ui.Ruestungen.addWidget(leEigenschaft, row, col, 1, 1)
                eigenschaftenCompleter = TextTagCompleter(leEigenschaft, Wolke.DB.ruestungseigenschaften.keys())
                self.eigenschaftenCompleter.append(eigenschaftenCompleter)
                col += 1

            addR = QtWidgets.QPushButton()
            addR.setText('\u002b')
            addR.setProperty("class", "iconSmall")
            font = addR.font()
            font.setHintingPreference(QtGui.QFont.PreferNoHinting)
            addR.setFont(font)
            addR.clicked.connect(partial(self.selectArmor, index = index))
            self.buttons.append(addR)
            self.ui.Ruestungen.addWidget(addR, row, col, 1, 1)

            row += 1
            index += 1

        # Add summarized armor value widgets at the end so we can reuse some functions
        self.editRName.append(self.ui.editGesamtName)
        self.sbZRW.append(self.ui.spinGesamtRS)
        if self.ruestungsEigenschaften:
            self.editEigenschaften.append(self.editGesamtEigenschaften)
            eigenschaftenCompleter = TextTagCompleter(self.editGesamtEigenschaften, Wolke.DB.ruestungseigenschaften.keys())
            self.eigenschaftenCompleter.append(eigenschaftenCompleter)
        self.gesamtIndex = len(self.ruestungsKategorien)

    def load(self):
        self.currentlyLoading = True

        if self.index < len(Wolke.Char.rüstung):
            R = Wolke.Char.rüstung[self.index]
            self.loadArmorIntoFields(R, self.gesamtIndex)

        for index in range(len(self.charTeilrüstungen)):
            R = self.charTeilrüstungen[index]
            if index < len(self.ruestungsKategorien):
                self.loadArmorIntoFields(R, index)
        self.currentlyLoading = False

        if  Wolke.Char.zonenSystemNutzen:
            Wolke.Char.zonenSystemNutzen = False
            self.updateRuestungen()

    def updateGesamtRuestung(self):
        if self.currentlyLoading:
            return
        R = self.createRuestung(self.gesamtIndex)
        self.refreshDerivedArmorValues(R, self.gesamtIndex)
        while self.index >= len(Wolke.Char.rüstung):
            Wolke.Char.rüstung.append(Ruestung(RuestungDefinition()))

        if Wolke.Char.rüstung[self.index] != R:
            Wolke.Char.rüstung[self.index] = R
            self.modified.emit()
            self.refreshDerivedArmorValues(R, self.gesamtIndex)

    def getSchwerParam(self, eigenschaft):
        if "schwer" not in eigenschaft.lower():
            return None

        match = re.search(r"\((.+?)\)", eigenschaft, re.UNICODE)
        if not match:
            return None
        parameters = list(map(str.strip, match.group(1).split(";")))
        if not len(parameters) >= 1:
            return None
        return int(parameters[0])

    def updateRuestungen(self):
        if self.currentlyLoading:
            return
        ruestungNeu = []
        zrwGesamt = 0

        for index in range(len(self.ruestungsKategorien)):
            R = self.createRuestung(index)
            ruestungNeu.append(R)

            zrwGesamt += R.getRSGesamtInt()

            if R.name == "":
                self.buttons[index].setText('\u002b')
            else:
                self.buttons[index].setText('\uf2ed')

        if Hilfsmethoden.ArrayEqual(ruestungNeu, self.charTeilrüstungen):
            return

        self.charTeilrüstungen.clear()
        self.charTeilrüstungen += ruestungNeu

        definition = RuestungDefinition()
        definition.name = self.ui.editGesamtName.text()
        R = Ruestung(definition)

        rsGesamt = int(zrwGesamt / 6)

        #zrwGesamt = 0
        #for kategorie in range(len(self.ruestungsKategorien)):
        #    zrwGesamt += self.sbZRW[kategorie].value()

        for i in range(6):
            R.rs[i] = rsGesamt

        schwerCount = 0
        R.eigenschaften = []
        if self.ruestungsEigenschaften:
            for teilRüstung in self.charTeilrüstungen:
                for eigenschaft in teilRüstung.eigenschaften:
                    schwer = self.getSchwerParam(eigenschaft)
                    if schwer is not None:
                        schwerCount += schwer
                        continue

                    if eigenschaft not in R.eigenschaften:
                        R.eigenschaften.append(eigenschaft)

        if schwerCount > 0:
            R.eigenschaften.append(f"Schwer ({schwerCount})")

        beDelta = self.ui.spinGesamtBE.value() - self.ui.spinGesamtRS.value()
        R.be = R.getRSGesamtInt() + beDelta
        #if self.ruestungsEigenschaften:
        #    if self.editGesamtEigenschaften.text():
        #        R.eigenschaften = list(map(str.strip, self.editGesamtEigenschaften.text().split(",")))
        #    else:
        #        R.eigenschaften = []

        self.currentlyLoading = True
        self.loadArmorIntoFields(R, self.gesamtIndex)
        self.currentlyLoading = False
        self.updateGesamtRuestung()
        self.modified.emit()

    def refreshDerivedArmorValues(self, R, index):
        if index == self.gesamtIndex:
            punkte = 0
            for R in self.charTeilrüstungen:
                punkte += R.getRSGesamtInt()

            #punkte = sum(R.rs) + R.zrsMod
            self.ui.spinGesamtPunkte.setValue(punkte)
            if punkte % 6 != 0:
                missingPoints = 6 - punkte % 6
                if missingPoints == 1:
                    self.ui.spinGesamtPunkte.setToolTip("Der Rüstung fehlt " + str(missingPoints) + " Punkt ZRW für den nächsten Punkt RS.")
                else:
                    self.ui.spinGesamtPunkte.setToolTip("Der Rüstung fehlen " + str(missingPoints) + " Punkte ZRW für den nächsten Punkt RS.")
            else:
                self.ui.spinGesamtPunkte.setToolTip("")

    def createRuestung(self, index):
        name = self.editRName[index].text()
        if name in Wolke.DB.rüstungen:
            R = Ruestung(Wolke.DB.rüstungen[name])
        else:
            definition = RuestungDefinition()
            definition.name = name
            R = Ruestung(definition)
        R.rs = 6*[self.sbZRW[index].value()]

        if index == self.gesamtIndex:
            R.be = int(self.ui.spinGesamtBE.value())
        else:
            R.be = R.getRSGesamtInt()
            R.kategorie = index
        if self.ruestungsEigenschaften:
            if self.editEigenschaften[index].text():
                R.eigenschaften = list(map(str.strip, self.editEigenschaften[index].text().split(",")))
            else:
                R.eigenschaften = []
        return R

    def updateEigenschaftenTooltip(self, edit):
        eigenschaften = list(map(str.strip, edit.text().split(",")))
        tooltip = ""
        for eig in eigenschaften:
            name = re.sub(r"\((.*?)\)", "", eig, re.UNICODE).strip() # remove parameters
            if name in Wolke.DB.ruestungseigenschaften:
                ruestungseigenschaft = Wolke.DB.ruestungseigenschaften[name]
                if ruestungseigenschaft.text:
                    tooltip += "<b>" + eig + ":</b> " + ruestungseigenschaft.text + "\n"
            elif eig:
                tooltip += "<b>" + eig + ":</b> Unbekannte Eigenschaft\n"
        
        if tooltip:
            tooltip = tooltip[:-1].replace("\n", "<br>")
        edit.setToolTip(tooltip)

    def loadArmorIntoFields(self, R, index):
        self.editRName[index].setText(R.name)
        if index == self.gesamtIndex:
            self.ui.spinGesamtBE.setValue(EventBus.applyFilter("ruestung_be", R.be, { "name" : R.name }))

        self.sbZRW[index].setValue(R.getRSGesamtInt())

        if self.ruestungsEigenschaften:
            self.editEigenschaften[index].setText(", ".join(R.eigenschaften))
            self.updateEigenschaftenTooltip(self.editEigenschaften[index])

        self.refreshDerivedArmorValues(R, index)

        if index != self.gesamtIndex:
            if R.name == "":
                self.buttons[index].setText('\u002b')
            else:
                self.buttons[index].setText('\uf2ed')

    def selectArmor(self, index):
        if index >= len(self.charTeilrüstungen) or self.charTeilrüstungen[index].name == "":
            logging.debug("Starting RuestungPicker")

            pickerClass = EventBus.applyFilter("class_ruestungspicker_wrapper", RuestungPicker)
            picker = pickerClass(self.editRName[index].text(), 1, self.ruestungsKategorien[index])
            logging.debug("RuestungPicker created")
            if picker.ruestung is not None:
                self.currentlyLoading = True
                self.loadArmorIntoFields(Ruestung(picker.ruestung), index)
                self.currentlyLoading = False
                self.updateRuestungen()
        else:
            self.currentlyLoading = True
            self.loadArmorIntoFields(Ruestung(RuestungDefinition()), index)
            self.currentlyLoading = False
            self.updateRuestungen()

    def shouldShowCategory(kategorie, system):
        for rues in Wolke.DB.rüstungen:
            if Wolke.DB.rüstungen[rues].kategorie != kategorie:
                continue
            if Wolke.DB.rüstungen[rues].system != 0 and Wolke.DB.rüstungen[rues].system != system:
                continue
            return True
        return False