from PySide6 import QtWidgets, QtCore, QtGui
import shutil
import os
from EventBus import EventBus
from Wolke import Wolke
from EinstellungenWrapper import EinstellungenWrapper
import copy
import re
from CheatsheetGenerator import CheatsheetGenerator
from Core.DatenbankEinstellung import DatenbankEinstellung
from Hilfsmethoden import Hilfsmethoden

class Plugin:
    def __init__(self):
        EventBus.addAction("datenbank_laden", self.datenbankLadenHandler)
        EventBus.addFilter("pdf_export", self.pdfExportKulturkundeHook)
      
    @staticmethod
    def getDescription():
        return "Ermöglicht es, über eine Datenbankeinstellung Fertigkeiten festzulegen, bei denen (Kultur) im namen angehängt wird."

    def changesCharacter(self):
        return False

    def datenbankLadenHandler(self, params):
        self.db = params["datenbank"]

        e = DatenbankEinstellung()
        e.name = "Kulturkunde Plugin: Fertigkeiten"
        e.beschreibung = "Fügt den Namen der aufgelisteten Fertigkeiten noch '(Kultur)' hinzu. Die Angabe erfolgt als kommaseparierte Liste."
        e.text = "Straßenkunde, Diplomatie, Mythenkunde, Darbietung"
        e.typ = "TextList"
        e.separator = ","
        self.db.loadElement(e)

    def pdfExportKulturkundeHook(self, fields, params):
        fertNameToKey = {}
        for k,v in fields.items():
            if k.startswith("Fertigkeit") and k.endswith("NA"):
                fertNameToKey[v] = k[:-2]

        for name in self.db.einstellungen["Kulturkunde Plugin: Fertigkeiten"].wert:
            if name in fertNameToKey:
                key = fertNameToKey[name] + "NA"
                fields[key] = fields[key] + " (Kultur)"
        return fields