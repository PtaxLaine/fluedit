# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/editor.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName("Editor")
        Editor.resize(813, 561)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Editor)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabWidget = QtWidgets.QTabWidget(Editor)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(self.tab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.create_message_button = QtWidgets.QPushButton(self.layoutWidget)
        self.create_message_button.setObjectName("create_message_button")
        self.verticalLayout.addWidget(self.create_message_button)
        self.messages_list = QtWidgets.QListWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messages_list.sizePolicy().hasHeightForWidth())
        self.messages_list.setSizePolicy(sizePolicy)
        self.messages_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.messages_list.setObjectName("messages_list")
        self.verticalLayout.addWidget(self.messages_list)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.fliter_box = QtWidgets.QComboBox(self.layoutWidget)
        self.fliter_box.setObjectName("fliter_box")
        self.fliter_box.addItem("")
        self.fliter_box.addItem("")
        self.fliter_box.addItem("")
        self.fliter_box.addItem("")
        self.fliter_box.addItem("")
        self.fliter_box.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fliter_box)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.verticalLayout.addLayout(self.formLayout)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.original_message_edit = QtWidgets.QTextEdit(self.layoutWidget1)
        self.original_message_edit.setReadOnly(True)
        self.original_message_edit.setObjectName("original_message_edit")
        self.verticalLayout_2.addWidget(self.original_message_edit)
        self.layoutWidget2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.is_draft_box = QtWidgets.QCheckBox(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.is_draft_box.sizePolicy().hasHeightForWidth())
        self.is_draft_box.setSizePolicy(sizePolicy)
        self.is_draft_box.setObjectName("is_draft_box")
        self.horizontalLayout.addWidget(self.is_draft_box)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.translited_message_edit = QtWidgets.QTextEdit(self.layoutWidget2)
        self.translited_message_edit.setAcceptRichText(False)
        self.translited_message_edit.setObjectName("translited_message_edit")
        self.verticalLayout_4.addWidget(self.translited_message_edit)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_8.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_8.addWidget(self.lineEdit)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_8.addWidget(self.lineEdit_2)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_8.addWidget(self.label_5)
        self.listView = QtWidgets.QListView(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setObjectName("listView")
        self.verticalLayout_8.addWidget(self.listView)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.comments_edit = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.comments_edit.sizePolicy().hasHeightForWidth())
        self.comments_edit.setSizePolicy(sizePolicy)
        self.comments_edit.setObjectName("comments_edit")
        self.verticalLayout_8.addWidget(self.comments_edit)
        self.verticalLayout_3.addWidget(self.splitter_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.tab_playground_layout = QtWidgets.QVBoxLayout()
        self.tab_playground_layout.setObjectName("tab_playground_layout")
        self.verticalLayout_9.addLayout(self.tab_playground_layout)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tab_config_layout = QtWidgets.QVBoxLayout()
        self.tab_config_layout.setObjectName("tab_config_layout")
        self.verticalLayout_6.addLayout(self.tab_config_layout)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_5.addWidget(self.tabWidget)

        self.retranslateUi(Editor)
        self.tabWidget.setCurrentIndex(0)
        self.is_draft_box.stateChanged['int'].connect(Editor.on_draft_box_changed)
        self.comments_edit.textChanged.connect(Editor.on_comment_changed)
        self.translited_message_edit.textChanged.connect(Editor.on_message_changed)
        self.create_message_button.clicked.connect(Editor.add_message)
        self.fliter_box.currentTextChanged['QString'].connect(Editor.on_fliter_changed)
        self.messages_list.currentRowChanged['int'].connect(Editor.on_current_row_changed)
        self.tabWidget.currentChanged['int'].connect(Editor.on_tab_changed)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        _translate = QtCore.QCoreApplication.translate
        Editor.setWindowTitle(_translate("Editor", "Form"))
        self.create_message_button.setText(_translate("Editor", "Create message"))
        self.messages_list.setSortingEnabled(True)
        self.fliter_box.setItemText(0, _translate("Editor", "None"))
        self.fliter_box.setItemText(1, _translate("Editor", "Drafts"))
        self.fliter_box.setItemText(2, _translate("Editor", "Untranslated"))
        self.fliter_box.setItemText(3, _translate("Editor", "Translated"))
        self.fliter_box.setItemText(4, _translate("Editor", "With comments"))
        self.fliter_box.setItemText(5, _translate("Editor", "Without comments"))
        self.label_7.setText(_translate("Editor", "Filter"))
        self.label.setText(_translate("Editor", "Original message"))
        self.original_message_edit.setPlaceholderText(_translate("Editor", "undefined"))
        self.label_2.setText(_translate("Editor", "Translited message"))
        self.is_draft_box.setText(_translate("Editor", "Draft"))
        self.label_3.setText(_translate("Editor", "Filename"))
        self.lineEdit.setPlaceholderText(_translate("Editor", "undefined"))
        self.label_4.setText(_translate("Editor", "File position"))
        self.lineEdit_2.setPlaceholderText(_translate("Editor", "undefined"))
        self.label_5.setText(_translate("Editor", "Translition memory"))
        self.label_6.setText(_translate("Editor", "Comments"))
        self.comments_edit.setPlaceholderText(_translate("Editor", "tape comment here"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Editor", "Editor"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Editor", "Playground"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Editor", "Configuration"))


