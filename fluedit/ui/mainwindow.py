# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qt/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 770)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setObjectName("layout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 20))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAbout = QtWidgets.QMenu(self.menuHelp)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCreate = QtWidgets.QAction(MainWindow)
        self.actionCreate.setObjectName("actionCreate")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionAboutQt = QtWidgets.QAction(MainWindow)
        self.actionAboutQt.setObjectName("actionAboutQt")
        self.actionAboutFluEdit = QtWidgets.QAction(MainWindow)
        self.actionAboutFluEdit.setObjectName("actionAboutFluEdit")
        self.actionLicense = QtWidgets.QAction(MainWindow)
        self.actionLicense.setObjectName("actionLicense")
        self.actionPython = QtWidgets.QAction(MainWindow)
        self.actionPython.setObjectName("actionPython")
        self.actionFluent = QtWidgets.QAction(MainWindow)
        self.actionFluent.setObjectName("actionFluent")
        self.menuOpen.addAction(self.actionOpen)
        self.menuOpen.addAction(self.actionCreate)
        self.menuOpen.addAction(self.actionSave)
        self.menuOpen.addAction(self.actionSave_as)
        self.menuAbout.addAction(self.actionAboutQt)
        self.menuAbout.addAction(self.actionAboutFluEdit)
        self.menuAbout.addAction(self.actionPython)
        self.menuAbout.addAction(self.actionFluent)
        self.menuHelp.addAction(self.menuAbout.menuAction())
        self.menuHelp.addAction(self.actionLicense)
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuOpen.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionCreate.setText(_translate("MainWindow", "Create"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionAboutQt.setText(_translate("MainWindow", "Qt"))
        self.actionAboutFluEdit.setText(_translate("MainWindow", "FluEdit"))
        self.actionLicense.setText(_translate("MainWindow", "License"))
        self.actionPython.setText(_translate("MainWindow", "Python"))
        self.actionFluent.setText(_translate("MainWindow", "Fluent"))


