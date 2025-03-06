# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RSDatenbankEditRuestung.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(491, 312)
        self.verticalLayout_3 = QVBoxLayout(dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 471, 292))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setMinimumSize(QSize(110, 0))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)

        self.leName = QLineEdit(self.scrollAreaWidgetContents)
        self.leName.setObjectName(u"leName")
        self.leName.setMinimumSize(QSize(300, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leName)

        self.labelKategorie = QLabel(self.scrollAreaWidgetContents)
        self.labelKategorie.setObjectName(u"labelKategorie")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelKategorie)

        self.comboKategorie = QComboBox(self.scrollAreaWidgetContents)
        self.comboKategorie.setObjectName(u"comboKategorie")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboKategorie)

        self.labelZRS = QLabel(self.scrollAreaWidgetContents)
        self.labelZRS.setObjectName(u"labelZRS")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelZRS)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.sbZRS = QSpinBox(self.scrollAreaWidgetContents)
        self.sbZRS.setObjectName(u"sbZRS")
        self.sbZRS.setMinimumSize(QSize(50, 0))
        self.sbZRS.setMaximumSize(QSize(16777215, 16777215))
        self.sbZRS.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.sbZRS.setMaximum(9999)

        self.horizontalLayout_7.addWidget(self.sbZRS)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.labelEigenschaften = QLabel(self.scrollAreaWidgetContents)
        self.labelEigenschaften.setObjectName(u"labelEigenschaften")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelEigenschaften)

        self.teEigenschaften = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.teEigenschaften.setObjectName(u"teEigenschaften")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.teEigenschaften)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.leName, self.comboKategorie)

        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Taverne - R\u00fcstung bearbeiten...", None))
        self.labelName.setText(QCoreApplication.translate("dialog", u"Name", None))
        self.labelKategorie.setText(QCoreApplication.translate("dialog", u"Kategorie", None))
        self.labelZRS.setText(QCoreApplication.translate("dialog", u"ZRW", None))
        self.labelEigenschaften.setText(QCoreApplication.translate("dialog", u"Eigenschaften", None))
    # retranslateUi

