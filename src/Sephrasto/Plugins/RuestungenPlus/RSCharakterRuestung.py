# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RSCharakterRuestung.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QGridLayout, QGroupBox,
    QLabel, QLayout, QLineEdit, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_formAusruestung(object):
    def setupUi(self, formAusruestung):
        if not formAusruestung.objectName():
            formAusruestung.setObjectName(u"formAusruestung")
        formAusruestung.resize(971, 735)
        formAusruestung.setMinimumSize(QSize(802, 0))
        self.verticalLayout = QVBoxLayout(formAusruestung)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(formAusruestung)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 969, 733))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.gbRstungen = QGroupBox(self.scrollAreaWidgetContents)
        self.gbRstungen.setObjectName(u"gbRstungen")
        self.verticalLayout_3 = QVBoxLayout(self.gbRstungen)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.Ruestungen = QGridLayout()
        self.Ruestungen.setObjectName(u"Ruestungen")
        self.Ruestungen.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_3 = QLabel(self.gbRstungen)
        self.label_3.setObjectName(u"label_3")

        self.Ruestungen.addWidget(self.label_3, 1, 5, 1, 1)

        self.label_2 = QLabel(self.gbRstungen)
        self.label_2.setObjectName(u"label_2")

        self.Ruestungen.addWidget(self.label_2, 1, 0, 1, 1)

        self.editGesamtName = QLineEdit(self.gbRstungen)
        self.editGesamtName.setObjectName(u"editGesamtName")

        self.Ruestungen.addWidget(self.editGesamtName, 1, 1, 1, 1)

        self.label = QLabel(self.gbRstungen)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.Ruestungen.addWidget(self.label, 2, 0, 1, 2)

        self.labelRS = QLabel(self.gbRstungen)
        self.labelRS.setObjectName(u"labelRS")
        self.labelRS.setFont(font)
        self.labelRS.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Ruestungen.addWidget(self.labelRS, 0, 3, 1, 1)

        self.labelRName = QLabel(self.gbRstungen)
        self.labelRName.setObjectName(u"labelRName")
        self.labelRName.setFont(font)

        self.Ruestungen.addWidget(self.labelRName, 0, 1, 1, 1)

        self.labelPunkte = QLabel(self.gbRstungen)
        self.labelPunkte.setObjectName(u"labelPunkte")
        self.labelPunkte.setFont(font)
        self.labelPunkte.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Ruestungen.addWidget(self.labelPunkte, 0, 4, 1, 1)

        self.spinGesamtBE = QSpinBox(self.gbRstungen)
        self.spinGesamtBE.setObjectName(u"spinGesamtBE")
        self.spinGesamtBE.setMinimumSize(QSize(44, 0))
        self.spinGesamtBE.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinGesamtBE.setReadOnly(False)
        self.spinGesamtBE.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.spinGesamtBE.setMaximum(999)

        self.Ruestungen.addWidget(self.spinGesamtBE, 1, 2, 1, 1)

        self.spinGesamtRS = QSpinBox(self.gbRstungen)
        self.spinGesamtRS.setObjectName(u"spinGesamtRS")
        self.spinGesamtRS.setMinimumSize(QSize(44, 0))
        self.spinGesamtRS.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinGesamtRS.setReadOnly(True)
        self.spinGesamtRS.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinGesamtRS.setMaximum(999)

        self.Ruestungen.addWidget(self.spinGesamtRS, 1, 3, 1, 1)

        self.labelBE = QLabel(self.gbRstungen)
        self.labelBE.setObjectName(u"labelBE")
        self.labelBE.setMinimumSize(QSize(35, 0))
        self.labelBE.setFont(font)
        self.labelBE.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Ruestungen.addWidget(self.labelBE, 0, 2, 1, 1)

        self.spinGesamtPunkte = QSpinBox(self.gbRstungen)
        self.spinGesamtPunkte.setObjectName(u"spinGesamtPunkte")
        self.spinGesamtPunkte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinGesamtPunkte.setReadOnly(True)
        self.spinGesamtPunkte.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinGesamtPunkte.setMaximum(9999)

        self.Ruestungen.addWidget(self.spinGesamtPunkte, 1, 4, 1, 1)


        self.verticalLayout_3.addLayout(self.Ruestungen)

        self.labelHinweis = QLabel(self.gbRstungen)
        self.labelHinweis.setObjectName(u"labelHinweis")
        self.labelHinweis.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.labelHinweis)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)


        self.verticalLayout_2.addWidget(self.gbRstungen)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(formAusruestung)

        QMetaObject.connectSlotsByName(formAusruestung)
    # setupUi

    def retranslateUi(self, formAusruestung):
        formAusruestung.setWindowTitle(QCoreApplication.translate("formAusruestung", u"Form", None))
        self.scrollArea.setProperty(u"class", QCoreApplication.translate("formAusruestung", u"transparent", None))
        self.gbRstungen.setTitle("")
        self.label_3.setText("")
        self.label_2.setText(QCoreApplication.translate("formAusruestung", u"Gesamte R\u00fcstung", None))
#if QT_CONFIG(tooltip)
        self.editGesamtName.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("formAusruestung", u"Zonen", None))
        self.label.setProperty(u"class", QCoreApplication.translate("formAusruestung", u"h4", None))
#if QT_CONFIG(tooltip)
        self.labelRS.setToolTip(QCoreApplication.translate("formAusruestung", u"R\u00fcstungsschutz", None))
#endif // QT_CONFIG(tooltip)
        self.labelRS.setText(QCoreApplication.translate("formAusruestung", u"RS", None))
        self.labelRS.setProperty(u"class", QCoreApplication.translate("formAusruestung", u"h4", None))
        self.labelRName.setText(QCoreApplication.translate("formAusruestung", u"Name", None))
        self.labelRName.setProperty(u"class", QCoreApplication.translate("formAusruestung", u"h4", None))
        self.labelPunkte.setText(QCoreApplication.translate("formAusruestung", u"ZRW", None))
        self.labelPunkte.setProperty(u"class", QCoreApplication.translate("formAusruestung", u"h4", None))
#if QT_CONFIG(tooltip)
        self.spinGesamtBE.setToolTip(QCoreApplication.translate("formAusruestung", u"Die R\u00fcstungswerte werden automatisch aus allen Slots berechnet.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinGesamtRS.setToolTip(QCoreApplication.translate("formAusruestung", u"Die R\u00fcstungswerte werden automatisch aus allen Slots berechnet.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.labelBE.setToolTip(QCoreApplication.translate("formAusruestung", u"Behinderung", None))
#endif // QT_CONFIG(tooltip)
        self.labelBE.setText(QCoreApplication.translate("formAusruestung", u"BE", None))
        self.labelBE.setProperty(u"class", QCoreApplication.translate("formAusruestung", u"h4", None))
        self.labelHinweis.setText(QCoreApplication.translate("formAusruestung", u"Hinweis: Nur R\u00fcstung 1 wird zur Berechnung der WS* usw. verwendet.", None))
    # retranslateUi

