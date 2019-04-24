# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/editor_cfg.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(563, 406)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.language_box = QtWidgets.QComboBox(Form)
        self.language_box.setObjectName("language_box")
        self.language_box.addItem("")
        self.language_box.addItem("")
        self.language_box.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.language_box)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.text_direction_box = QtWidgets.QComboBox(Form)
        self.text_direction_box.setObjectName("text_direction_box")
        self.text_direction_box.addItem("")
        self.text_direction_box.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.text_direction_box)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Language"))
        self.language_box.setItemText(0, _translate("Form", "en_US"))
        self.language_box.setItemText(1, _translate("Form", "en_UK"))
        self.language_box.setItemText(2, _translate("Form", "ru_RU"))
        self.label_2.setText(_translate("Form", "Text Direction"))
        self.text_direction_box.setItemText(0, _translate("Form", "Right-to-left"))
        self.text_direction_box.setItemText(1, _translate("Form", "Left-to-right"))


