# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/memoirs_search_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MemoirsSearchDialog(object):
    def setupUi(self, MemoirsSearchDialog):
        MemoirsSearchDialog.setObjectName("MemoirsSearchDialog")
        MemoirsSearchDialog.resize(400, 300)
        self.formLayout = QtWidgets.QFormLayout(MemoirsSearchDialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(MemoirsSearchDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(MemoirsSearchDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.plainTextEdit)
        self.listWidget = QtWidgets.QListWidget(MemoirsSearchDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.listWidget)
        self.label_2 = QtWidgets.QLabel(MemoirsSearchDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.retranslateUi(MemoirsSearchDialog)
        self.plainTextEdit.textChanged.connect(MemoirsSearchDialog.on_text_changed)
        QtCore.QMetaObject.connectSlotsByName(MemoirsSearchDialog)

    def retranslateUi(self, MemoirsSearchDialog):
        _translate = QtCore.QCoreApplication.translate
        MemoirsSearchDialog.setWindowTitle(_translate("MemoirsSearchDialog", "Dialog"))
        self.label.setText(_translate("MemoirsSearchDialog", "Message:"))
        self.label_2.setText(_translate("MemoirsSearchDialog", "Result:"))


