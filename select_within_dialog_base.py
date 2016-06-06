# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_within_dialog_base.ui'
#
# Created: Mon Jun 06 21:48:05 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SelectWithinDialogBase(object):
    def setupUi(self, SelectWithinDialogBase):
        SelectWithinDialogBase.setObjectName(_fromUtf8("SelectWithinDialogBase"))
        SelectWithinDialogBase.resize(312, 231)
        self.horizontalLayout = QtGui.QHBoxLayout(SelectWithinDialogBase)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(SelectWithinDialogBase)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.selectFromCombo = QgsMapLayerComboBox(SelectWithinDialogBase)
        self.selectFromCombo.setObjectName(_fromUtf8("selectFromCombo"))
        self.verticalLayout.addWidget(self.selectFromCombo)
        self.label_2 = QtGui.QLabel(SelectWithinDialogBase)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.centroidRadioButton = QtGui.QRadioButton(SelectWithinDialogBase)
        self.centroidRadioButton.setChecked(True)
        self.centroidRadioButton.setObjectName(_fromUtf8("centroidRadioButton"))
        self.buttonGroup = QtGui.QButtonGroup(SelectWithinDialogBase)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.centroidRadioButton)
        self.horizontalLayout_2.addWidget(self.centroidRadioButton)
        self.pointonsurfaceRadioButton_2 = QtGui.QRadioButton(SelectWithinDialogBase)
        self.pointonsurfaceRadioButton_2.setObjectName(_fromUtf8("pointonsurfaceRadioButton_2"))
        self.buttonGroup.addButton(self.pointonsurfaceRadioButton_2)
        self.horizontalLayout_2.addWidget(self.pointonsurfaceRadioButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_3 = QtGui.QLabel(SelectWithinDialogBase)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.selectWithCombo = QgsMapLayerComboBox(SelectWithinDialogBase)
        self.selectWithCombo.setObjectName(_fromUtf8("selectWithCombo"))
        self.verticalLayout.addWidget(self.selectWithCombo)
        self.selectedFeaturesCheckbox = QtGui.QCheckBox(SelectWithinDialogBase)
        self.selectedFeaturesCheckbox.setChecked(True)
        self.selectedFeaturesCheckbox.setObjectName(_fromUtf8("selectedFeaturesCheckbox"))
        self.verticalLayout.addWidget(self.selectedFeaturesCheckbox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.newSelectionRadioButton = QtGui.QRadioButton(SelectWithinDialogBase)
        self.newSelectionRadioButton.setChecked(True)
        self.newSelectionRadioButton.setObjectName(_fromUtf8("newSelectionRadioButton"))
        self.buttonGroup_2 = QtGui.QButtonGroup(SelectWithinDialogBase)
        self.buttonGroup_2.setObjectName(_fromUtf8("buttonGroup_2"))
        self.buttonGroup_2.addButton(self.newSelectionRadioButton)
        self.horizontalLayout_3.addWidget(self.newSelectionRadioButton)
        self.currentSelectionRadioButton = QtGui.QRadioButton(SelectWithinDialogBase)
        self.currentSelectionRadioButton.setObjectName(_fromUtf8("currentSelectionRadioButton"))
        self.buttonGroup_2.addButton(self.currentSelectionRadioButton)
        self.horizontalLayout_3.addWidget(self.currentSelectionRadioButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.button_box = QtGui.QDialogButtonBox(SelectWithinDialogBase)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.verticalLayout.addWidget(self.button_box)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(SelectWithinDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectWithinDialogBase.reject)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectWithinDialogBase.accept)
        QtCore.QMetaObject.connectSlotsByName(SelectWithinDialogBase)

    def retranslateUi(self, SelectWithinDialogBase):
        SelectWithinDialogBase.setWindowTitle(_translate("SelectWithinDialogBase", "Select Within", None))
        self.label.setText(_translate("SelectWithinDialogBase", "Select all features from:", None))
        self.label_2.setText(_translate("SelectWithinDialogBase", "Where the:", None))
        self.centroidRadioButton.setText(_translate("SelectWithinDialogBase", "Centroid", None))
        self.pointonsurfaceRadioButton_2.setText(_translate("SelectWithinDialogBase", "Point on Surface", None))
        self.label_3.setText(_translate("SelectWithinDialogBase", "Is within:", None))
        self.selectedFeaturesCheckbox.setText(_translate("SelectWithinDialogBase", "Using selected features", None))
        self.newSelectionRadioButton.setText(_translate("SelectWithinDialogBase", "Creating new selection", None))
        self.currentSelectionRadioButton.setText(_translate("SelectWithinDialogBase", "Adding to current selection", None))

from qgsmaplayercombobox import QgsMapLayerComboBox
