# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/license_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(713, 478)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.widget = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.lic_layout = QtWidgets.QVBoxLayout(self.widget)
        self.lic_layout.setObjectName("lic_layout")
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_button = QtWidgets.QPushButton(Dialog)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.decline_button = QtWidgets.QPushButton(Dialog)
        self.decline_button.setDefault(True)
        self.decline_button.setObjectName("decline_button")
        self.horizontalLayout.addWidget(self.decline_button)
        self.accept_button = QtWidgets.QPushButton(Dialog)
        self.accept_button.setDefault(False)
        self.accept_button.setFlat(False)
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout.addWidget(self.accept_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.accept_button.clicked.connect(Dialog.on_accepted)
        self.close_button.clicked.connect(Dialog.close)
        self.decline_button.clicked.connect(Dialog.on_rejected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Fluedit license"))
        self.label.setText(_translate("Dialog", "FluEdit Licenses"))
        self.close_button.setText(_translate("Dialog", "Close"))
        self.decline_button.setText(_translate("Dialog", "I Decline"))
        self.accept_button.setText(_translate("Dialog", "I Accept"))


