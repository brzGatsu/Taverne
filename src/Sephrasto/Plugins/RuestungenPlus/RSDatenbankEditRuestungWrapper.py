# -*- coding: utf-8 -*-
from DatenbankElementEditorBase import DatenbankElementEditorBase, BeschreibungEditor
from Core.Ruestung import RuestungDefinition
from RuestungenPlus import RSDatenbankEditRuestung
from Hilfsmethoden import Hilfsmethoden, WaffeneigenschaftException
from PySide6 import QtWidgets, QtCore
from Wolke import Wolke
from Datenbank import Datenbank
from QtUtils.HtmlToolbar import HtmlToolbar
from QtUtils.TextTagCompleter import TextTagCompleter

class RSDatenbankEditRuestungWrapper(DatenbankElementEditorBase):
    def __init__(self, datenbank, rüstung=None):
        super().__init__(datenbank, RSDatenbankEditRuestung.Ui_dialog(), RuestungDefinition, rüstung)
        self.validator["Rüstungseigenschaften"] = True

    def onSetupUi(self):
        super().onSetupUi()

        ui = self.ui
        self.registerInput(ui.leName, ui.labelName)
        self.registerInput(ui.comboKategorie, ui.labelKategorie)
        self.registerInput(ui.sbZRS, ui.labelZRS)
        self.registerInput(ui.teEigenschaften, ui.labelEigenschaften)

    def load(self, rüstung):
        super().load(rüstung)
        self.ui.comboKategorie.addItems(self.datenbank.einstellungen["Rüstungen: Kategorien"].wert.keyList)
        self.ui.comboKategorie.setCurrentIndex(rüstung.kategorie)
        self.ui.sbZRS.setValue(rüstung.getRSGesamtInt())

        self.eigenschaftenCompleter = TextTagCompleter(self.ui.teEigenschaften, self.datenbank.ruestungseigenschaften.keys())
        self.ui.teEigenschaften.setPlainText(rüstung.text)
        self.ui.teEigenschaften.textChanged.connect(self.eigenschaftenChanged)

    def update(self, rüstung):
        super().update(rüstung)
        rüstung.kategorie = self.ui.comboKategorie.currentIndex()
        for i in range(0, 6):
            rüstung.rs[i] = int(self.ui.sbZRS.value())
        rüstung.text = self.ui.teEigenschaften.toPlainText().strip()


    def verifyEigenschaft(self, eigenschaftStr):
        reName = eigenschaftStr
        index = reName.find("(")
        if index != -1:
            reName = str.strip(reName[:index])
        
        if not reName in self.datenbank.ruestungseigenschaften:
            return False, "Unbekannte Rüstungseigenschaft '" + reName + "'"

        if index != -1:
            endIndex = eigenschaftStr[index:].find(")")
            if endIndex == -1:
                return False, "Parameter der Rüstungseigenschaft '" + reName + "' müssen mit ')' abgeschlossen werden. Mehrere Parameter werden mit Semikolon getrennt."

        return True, ""

    def eigenschaftenChanged(self):
        eigenschaftStr = self.ui.teEigenschaften.toPlainText()
        if eigenschaftStr:
            eigenschaften = list(map(str.strip, eigenschaftStr.strip().rstrip(',').split(",")))
            for el in eigenschaften:
                success, message = self.verifyEigenschaft(el)
                if not success:
                    self.ui.teEigenschaften.setProperty("error", True)
                    self.ui.teEigenschaften.style().unpolish(self.ui.teEigenschaften)
                    self.ui.teEigenschaften.style().polish(self.ui.teEigenschaften)
                    self.ui.teEigenschaften.setToolTip(message)
                    self.validator["Waffeneigenschaften"] = False
                    self.updateSaveButtonState()
                    return

        self.ui.teEigenschaften.setProperty("error", False)
        self.ui.teEigenschaften.style().unpolish(self.ui.teEigenschaften)
        self.ui.teEigenschaften.style().polish(self.ui.teEigenschaften)
        self.ui.teEigenschaften.setToolTip("")
        self.validator["Waffeneigenschaften"] = True
        self.updateSaveButtonState()