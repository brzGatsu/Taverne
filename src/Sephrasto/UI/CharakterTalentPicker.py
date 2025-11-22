# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CharakterTalentPicker.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QScrollArea, QSizePolicy,
    QSpacerItem, QSplitter, QTableWidget, QTableWidgetItem,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(758, 522)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelTip = QLabel(Dialog)
        self.labelTip.setObjectName(u"labelTip")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTip.sizePolicy().hasHeightForWidth())
        self.labelTip.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.labelTip, 0, 0, 1, 1)

        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.listTalente = QTableWidget(self.splitter)
        if (self.listTalente.columnCount() < 1):
            self.listTalente.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.listTalente.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.listTalente.setObjectName(u"listTalente")
        self.listTalente.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.listTalente.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.listTalente.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.listTalente.setShowGrid(False)
        self.listTalente.setRowCount(0)
        self.splitter.addWidget(self.listTalente)
        self.listTalente.horizontalHeader().setHighlightSections(False)
        self.listTalente.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.listTalente.verticalHeader().setVisible(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 379, 448))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelKommentar = QLabel(self.scrollAreaWidgetContents)
        self.labelKommentar.setObjectName(u"labelKommentar")

        self.gridLayout_2.addWidget(self.labelKommentar, 7, 0, 1, 1)

        self.plainText = QTextBrowser(self.scrollAreaWidgetContents)
        self.plainText.setObjectName(u"plainText")
        self.plainText.setFrameShape(QFrame.Shape.StyledPanel)

        self.gridLayout_2.addWidget(self.plainText, 8, 0, 1, 3)

        self.labelInfo = QLabel(self.scrollAreaWidgetContents)
        self.labelInfo.setObjectName(u"labelInfo")
        self.labelInfo.setMinimumSize(QSize(0, 18))
        font = QFont()
        font.setItalic(True)
        self.labelInfo.setFont(font)
        self.labelInfo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelInfo, 5, 2, 1, 1)

        self.labelName = QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setMinimumSize(QSize(0, 20))
        font1 = QFont()
        font1.setBold(True)
        self.labelName.setFont(font1)

        self.gridLayout_2.addWidget(self.labelName, 5, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 9, 0, 1, 1)

        self.textKommentar = QLineEdit(self.scrollAreaWidgetContents)
        self.textKommentar.setObjectName(u"textKommentar")

        self.gridLayout_2.addWidget(self.textKommentar, 7, 1, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMaximumSize(QSize(16777215, 16777215))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        QWidget.setTabOrder(self.scrollArea, self.textKommentar)
        QWidget.setTabOrder(self.textKommentar, self.plainText)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Taverne - Talente w\u00e4hlen...", None))
        self.labelTip.setText(QCoreApplication.translate("Dialog", u"Ein Talent lohnt sich ab...", None))
        ___qtablewidgetitem = self.listTalente.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Talent", None));
        self.labelKommentar.setText(QCoreApplication.translate("Dialog", u"Kommentar:", None))
        self.labelInfo.setText(QCoreApplication.translate("Dialog", u"Spezialtalent", None))
        self.labelInfo.setProperty(u"class", QCoreApplication.translate("Dialog", u"italic", None))
        self.labelName.setText(QCoreApplication.translate("Dialog", u"Talentname", None))
        self.labelName.setProperty(u"class", QCoreApplication.translate("Dialog", u"h4", None))
    # retranslateUi

