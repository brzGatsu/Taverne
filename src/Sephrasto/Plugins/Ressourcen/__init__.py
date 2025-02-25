from EventBus import EventBus
from PySide6 import QtWidgets, QtGui
from Wolke import Wolke
from CharakterEditor import Tab
from Ressourcen import CharakterRessourcenWrapper
from Ressourcen.Ressource import Ressource
from Core.DatenbankEinstellung import DatenbankEinstellung
from Scripts import ScriptContext, Script, ScriptParameter

class Plugin:
    def __init__(self):
        EventBus.addAction("charaktereditor_geschlossen", self.charakterEditorGeschlossenHook)
        EventBus.addAction("charakter_epgesamt_geändert", self.charakterEpgesamtGeändertHook)
        EventBus.addAction("datenbank_laden", self.datenbankLadenHook)
        EventBus.addAction("charakter_instanziiert", self.charakterInstanziiertHook)
        EventBus.addAction("pre_charakter_aktualisieren", self.preCharakterAktualisierenHook)
        EventBus.addAction("charakter_serialisiert", self.charakterSerialisiertHook)
        EventBus.addAction("charakter_deserialisiert", self.charakterDeserialisiertHook)
        EventBus.addFilter("pdf_export", self.pdfExportFilter)
        EventBus.addFilter("scripts_available", self.scriptsAvailableHook)
        self.ressourcenTab = None

    def changesCharacter(self):
        return True

    def createCharakterTabs(self):
        self.ressourcenTab = CharakterRessourcenWrapper.CharakterRessourcenWrapper()
        tab = Tab(44, self.ressourcenTab, self.ressourcenTab.form, "Ressourcen")
        return [tab]

    def charakterEditorGeschlossenHook(self, params):
        self.ressourcenTab = None

    def charakterEpgesamtGeändertHook(self, params):
        if self.ressourcenTab is not None:
            self.ressourcenTab.updateInfoLabel()

    def datenbankLadenHook(self, params):
        self.db = params["datenbank"]

        e = DatenbankEinstellung()
        e.name = "Ressourcen Plugin: Standardressourcen"
        e.beschreibung = ""
        e.text = '''{\
    "Ansehen" : ["unbekannt", "wohlwollend betrachtet", "geschätzt", "respektiert", "bewundert", "verehrt"],
    "Einkommen" : ["elend, 1 D", "karg, 4 D", "annehmbar, 16 D", "reichlich, 64 D", "üppig, 128 D", "prachtvoll, 256 D"],
    "Entschlossenheit" : ["lethargisch, 3 EnP", "zögerlich, 4 EnP", "optimistisch, 5 EnP", "bestimmt, 6 EnP", "standhaft, 7 EnP", "unerschütterlich, 8 EnP"],
    "Gefolge" : ["kein Gefolge", "klein/unerfahren", "klein/erfahren oder mittel/unerfahren", "klein/meisterlich, mittel/erfahren oder groß/unerfahren", "mittel/meisterlich, groß/erfahren oder sehr groß/unerfahren", "groß/meisterlich oder sehr groß/erfahren"],
    "Stand" : ["Benachteiligte", "Unterschicht", "Mittelschicht", "Obere Mittelschicht", "Oberschicht", "Elite"],
    "Verbindungen" : ["kein Einfluss", "etwas Einfluss in bestimmten Bereichen", "etwas Einfluss in vielen Bereichen", "ansehnlicher Einfluss", "immenser Einfluss", "kennt jeden"],
    "Tierbegleiter" : ["kein Begleiter", "gewöhnlich, +2 EP", "überdurchschnittlich, +4 EP", "außergewöhnlich, +6 EP", "herausragend, +8 EP", "einzigartig, +10 EP"]
}'''
        e.typ = "JsonDict"
        e.separator = "\n"
        e.strip = False
        self.db.loadElement(e)

    def charakterInstanziiertHook(self, params):
        char = params["charakter"]
        char.ressourcen = []
        char.finanzenAnzeigen = False

        for ressource in self.db.einstellungen["Ressourcen Plugin: Standardressourcen"].wert.keys():
            setattr(char, ressource + "Mod", 0)
            char.charakterScriptAPI[f'get{ressource}Mod'] = lambda ressource=ressource: getattr(char, ressource + "Mod")
            char.charakterScriptAPI[f'set{ressource}Mod'] = lambda mod, ressource=ressource: setattr(char, ressource + "Mod", mod)
            char.charakterScriptAPI[f'modify{ressource}'] = lambda mod, ressource=ressource: setattr(char, ressource + "Mod", getattr(char, ressource + "Mod") + mod)

    def preCharakterAktualisierenHook(self, params):
        char = params["charakter"]
        for ressource in self.db.einstellungen["Ressourcen Plugin: Standardressourcen"].wert.keys():
            setattr(char, ressource + "Mod", 0)

    def charakterSerialisiertHook(self, params):
        ser = params["serializer"]
        char = params["charakter"]

        ser.beginList('Ressourcen')
        for ressource in char.ressourcen:
            ser.begin('Ressource')
            ressource.serialize(ser)
            ser.end() #ressource
        ser.end() #ressourcen

    def charakterDeserialisiertHook(self, params):
        ser = params["deserializer"]
        char = params["charakter"]

        if ser.find('Ressourcen'):
            for tag in ser.listTags():
                ressource = Ressource.__new__(Ressource)
                if not ressource.deserialize(ser):
                    continue
                char.ressourcen.append(ressource)
            ser.end() #ressourcen

        char.finanzenAnzeigen = False

    def pdfExportFilter(self, fields, params):
        wertNamen = ["0", "W4", "W6", "W8", "W10", "W12"]

        filtered = []
        for ressource in Wolke.Char.ressourcen:
            # hacky until we have a new charsheet
            if ressource.name == "Ansehen":
                fields["Ansehen"] = f"{wertNamen[ressource.wert]} ({ressource.kommentar})"
            elif ressource.name == "Stand":
                fields["Status"] = f"{wertNamen[ressource.wert]} ({ressource.kommentar})"
            else:
                filtered.append(ressource)
            

        for i in range(0, len(filtered)):
            ressource = filtered[i]
            fields[f"Ressource{i+1}Name"] = ressource.name
            fields[f"Ressource{i+1}Wert"] = wertNamen[ressource.wert]
            fields[f"Ressource{i+1}Kommentar"] = ressource.kommentar
            fields[f"Ressource{i+1}"] = f"{ressource.name}: {wertNamen[ressource.wert]} ({ressource.kommentar})"

        return fields

    def scriptsAvailableHook(self, scripts, params):
        context = params["context"]
        if context != ScriptContext.Charakter:
            return scripts

        for ressource in self.db.einstellungen["Ressourcen Plugin: Standardressourcen"].wert.keys():
            script = Script(f"{ressource} Modifikator", f"get{ressource}Mod", "Ressourcen")
            scripts.numberGetter[script.name] = script

            script = Script(f"{ressource} Modifikator setzen", f"set{ressource}Mod", "Ressourcen")
            script.beschreibung = "Der Modifikator der Ressource wird auf den neuen Wert gesetzt. Achtung: Modifikatoren werden damit je nach Scriptpriorität ignoriert."
            script.parameter.append(ScriptParameter("Modifikator", int))
            scripts.setters[script.name] = script

            script = Script(f"{ressource} Modifikator modifizieren", f"modify{ressource}", "Ressourcen")
            script.beschreibung = "Der Modifikator der Ressource wird um den angebenen Wert modifiziert."
            script.parameter.append(ScriptParameter("Modifikator", int))
            scripts.setters[script.name] = script
        return scripts