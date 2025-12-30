# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:45:34 2017

@author: Aeolitus
"""
import UI.CharakterTalentPicker
from PySide6 import QtCore, QtWidgets, QtGui
from Wolke import Wolke
import copy
from Hilfsmethoden import Hilfsmethoden
from Core.Talent import Talent
from QtUtils.AutoResizingTextBrowser import TextEditAutoResizer
from EventBus import EventBus
from QtUtils.Toggle import Toggle
from PySide6.QtWidgets import QHeaderView

class TalentPicker(object):
    def __init__(self,fert,ueber):
        super().__init__()
        self.fert = fert
        self.form = QtWidgets.QDialog()
        self.ui = UI.CharakterTalentPicker.Ui_Dialog()
        self.ui.setupUi(self.form)

        if ueber:    
            self.refC = Wolke.Char.übernatürlicheFertigkeiten
            self.refD = Wolke.DB.übernatürlicheFertigkeiten
            windowSize = Wolke.Settings["WindowSize-TalentUeber"]
            self.form.resize(windowSize[0], windowSize[1])
        else:
            self.refC = Wolke.Char.fertigkeiten
            self.refD = Wolke.DB.fertigkeiten
            self.form.resize(self.form.size()*0.7)
        
            windowSize = Wolke.Settings["WindowSize-TalentProfan"]
            self.form.resize(windowSize[0], windowSize[1])

        if self.fert is None:
            self.gekaufteTalente = list(Wolke.Char.talente.keys())
        else:
            self.gekaufteTalente = self.refC[fert].gekaufteTalente.copy()

        self.form.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowMaximizeButtonHint |
                QtCore.Qt.WindowMinimizeButtonHint)
        
        self.autoResizeHelper = TextEditAutoResizer(self.ui.plainText)

        self.ui.splitter.adjustSize()
        width = self.ui.splitter.size().width()
        self.ui.splitter.setSizes([int(width*0.4), int(width*0.6)])

        self.onSetupUi()

        self.currentTalent = ""
        self.talentKosten = {}
        self.talentKommentare = {}
        self.talentSpezialisiert = {}

        talente = []
        for el in Wolke.DB.talente:
            talent = Wolke.DB.talente[el]
            if el in Wolke.Char.talente:
                talent = Wolke.Char.talente[el]

            if (ueber and not talent.spezialTalent) or (not ueber and talent.spezialTalent):
                continue

            fertMatch = False
            if self.fert is None:
                for f in talent.fertigkeiten:
                    if f in Wolke.Char.übernatürlicheFertigkeiten:
                        fertMatch = True
                        break
            else:
                fertMatch = self.fert in talent.fertigkeiten

            if fertMatch and Wolke.Char.voraussetzungenPrüfen(talent):
                talente.append(talent.name)
                if talent.name in Wolke.Char.talente:
                    self.talentKosten[talent.name] = Wolke.Char.talente[talent.name].kosten
                    self.talentKommentare[talent.name] = Wolke.Char.talente[talent.name].kommentar
                    self.talentSpezialisiert[talent.name] = Wolke.Char.talente[talent.name].spezialisiert
                else:
                    self.talentKosten[talent.name] = EventBus.applyFilter("talent_kosten", talent.kosten, { "charakter" : Wolke.Char, "talent" : talent.name })
                    self.talentKommentare[talent.name] = ""
                    self.talentSpezialisiert[talent.name] = talent.spezialisiertDefault
        self.talente = sorted(talente, key=Hilfsmethoden.unicodeCaseInsensitive)


        vheader = self.ui.listTalente.verticalHeader()
        vheader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        vheader.setDefaultSectionSize(Hilfsmethoden.emToPixels(3.4));
        vheader.setMaximumSectionSize(Hilfsmethoden.emToPixels(3.4));

        header = self.ui.listTalente.horizontalHeader()
        header.setMinimumSectionSize(0)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ui.listTalente.setHorizontalHeaderItem(0, item)

        if not ueber:
            self.kostenIndex = 1
            self.ui.listTalente.setColumnCount(2)
        else:
            self.kostenIndex = 2
            self.ui.listTalente.setColumnCount(3)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            item = QtWidgets.QTableWidgetItem()
            item.setText("Spezialisiert")
            item.setToolTip("Ohne Spezialisierung verfügst du nur über den PW, mit Spezialisierung über den PW(S).")
            item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.ui.listTalente.setHorizontalHeaderItem(1, item)

        header.setSectionResizeMode(self.kostenIndex, QHeaderView.ResizeToContents)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Kosten")
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ui.listTalente.setHorizontalHeaderItem(self.kostenIndex, item)
        
        self.spezialisierungParents = []
        self.spezialisierungToggles = []
        self.kostenLabels = []
        self.ui.listTalente.setRowCount(len(talente))

        self.rowCount = 0
        for el in talente:
            talent = Wolke.DB.talente[el]
            item = QtWidgets.QTableWidgetItem(talent.anzeigename)
            item.setData(QtCore.Qt.UserRole, el)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            if talent.name in self.gekaufteTalente:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.listTalente.setItem(self.rowCount, 0, item)

            if ueber:
                p = QtWidgets.QWidget()
                layout = QtWidgets.QHBoxLayout()
                layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                layout.setContentsMargins(0,0,0,0)
                p.setLayout(layout)
                spezialisiertToggle = Toggle()
                spezialisiertToggle.setFixedWidth(Hilfsmethoden.emToPixels(4))
                spezialisiertToggle.setCheckedInstant(self.talentSpezialisiert[talent.name])
                spezialisiertToggle.toggled.connect(self.spezialisiertChanged)
                if not talent.spezialisierbar:
                    spezialisiertToggle.setEnabled(False)

                layout.addWidget(spezialisiertToggle)
                self.spezialisierungParents.append(p)
                self.spezialisierungToggles.append(spezialisiertToggle)

                self.ui.listTalente.setCellWidget(self.rowCount,1,p)
                if talent.name not in self.gekaufteTalente:
                    spezialisiertToggle.hide()

            kosten = talent.kosten
            if talent.spezialisierbar and self.talentSpezialisiert[talent.name] and talent.spezialTalent:
                kosten = kosten * 2
            kostenLabel = QtWidgets.QLabel(str(kosten) + " EP")
            self.kostenLabels.append(kostenLabel)
            self.ui.listTalente.setCellWidget(self.rowCount,self.kostenIndex, kostenLabel)

            self.rowCount += 1

        if ueber:
            self.ui.listTalente.itemChanged.connect(self.on_item_changed)
        self.ui.listTalente.currentItemChanged.connect(self.updateFields)
        self.ui.listTalente.currentCellChanged.connect(self.updateFields)
        self.ui.listTalente.cellClicked.connect(self.updateFields) 

        if self.rowCount > 0:
            self.updateFields()
        self.ui.textKommentar.textChanged.connect(self.kommentarChanged)

        fwWarnung = Wolke.DB.einstellungen["Talente: FW Warnung"].wert
        if self.fert is None or ueber or self.refC[self.fert].wert >= fwWarnung:
            self.ui.labelTip.hide()
        else:
            self.ui.labelTip.setText("<span style='" + Wolke.FontAwesomeCSS + f"'>\uf071</span>&nbsp;&nbsp;Talente lohnen sich üblicherweise erst ab einem Fertigkeitswert von {fwWarnung}.")

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()
        self.ret = self.form.exec()

        if ueber:
            Wolke.Settings["WindowSize-TalentUeber"] = [self.form.size().width(), self.form.size().height()]
        else:
            Wolke.Settings["WindowSize-TalentProfan"] = [self.form.size().width(), self.form.size().height()]

        if self.ret == QtWidgets.QDialog.Accepted:
            self.gekaufteTalente = []
            for i in range(self.rowCount):
                item = self.ui.listTalente.item(i, 0)
                el = item.data(QtCore.Qt.UserRole)
                if item.checkState() == QtCore.Qt.Checked:  
                    self.gekaufteTalente.append(el)
                    talent = Wolke.Char.addTalent(el)
                    if talent.variableKosten:
                        talent.kosten = self.talentKosten[el]
                    if talent.kommentarErlauben:
                        talent.kommentar = self.talentKommentare[el]
                    if ueber:
                        talent.spezialisiert = self.spezialisierungToggles[i].isChecked()
                else:
                    Wolke.Char.removeTalent(el)
        else:
            self.gekaufteTalente = None
            
    def onSetupUi(self):
        pass # for usage in plugins

    def on_item_changed(self, item):
        # Only react if the changed item is checkable
        if item.flags() & QtCore.Qt.ItemIsUserCheckable:
            state = item.checkState()
            self.spezialisierungToggles[item.row()].setVisible(state == QtCore.Qt.Checked)

    def spezialisiertChanged(self, enabled):
        row = self.ui.listTalente.currentRow()
        if row < 0:
            return
        item = self.ui.listTalente.item(row, 0)
        talent = Wolke.DB.talente[item.data(QtCore.Qt.UserRole)]

        kosten = talent.kosten
        if enabled:
            kosten = kosten * 2
        self.kostenLabels[row].setText(str(kosten) + " EP")
        
    def kommentarChanged(self, text):
        if not self.currentTalent:
            return
        self.talentKommentare[self.currentTalent] = text

    def updateFields(self):
        row = self.ui.listTalente.currentRow()
        if row < 0:
            return
        item = self.ui.listTalente.item(row, 0)
        talent = Wolke.DB.talente[item.data(QtCore.Qt.UserRole)]

        self.currentTalent = talent.name
        self.ui.labelName.setText(talent.anzeigename + (" (verbilligt)" if talent.verbilligt else ""))
        self.ui.labelInfo.hide()

        if talent.spezialTalent:
            self.ui.labelInfo.show()
            self.ui.labelInfo.setText(talent.kategorieName(Wolke.DB))


        if talent.kommentarErlauben:
            self.ui.textKommentar.show()
            self.ui.labelKommentar.show()
            self.ui.textKommentar.setText(self.talentKommentare[tal])
        else:
            self.ui.textKommentar.hide()
            self.ui.labelKommentar.hide()

        text = talent.text
        if talent.info:
            text += f"\n<b>Taverne</b>: {talent.info}"
        self.ui.plainText.setText(Hilfsmethoden.fixHtml(text))