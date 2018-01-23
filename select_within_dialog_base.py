# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_within_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SelectWithinDialogBase(object):
    def setupUi(self, SelectWithinDialogBase):
        SelectWithinDialogBase.setObjectName("SelectWithinDialogBase")
        SelectWithinDialogBase.resize(312, 231)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SelectWithinDialogBase)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SelectWithinDialogBase)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.selectFromCombo = QgsMapLayerComboBox(SelectWithinDialogBase)
        self.selectFromCombo.setObjectName("selectFromCombo")
        self.verticalLayout.addWidget(self.selectFromCombo)
        self.label_2 = QtWidgets.QLabel(SelectWithinDialogBase)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.centroidRadioButton = QtWidgets.QRadioButton(SelectWithinDialogBase)
        self.centroidRadioButton.setChecked(True)
        self.centroidRadioButton.setObjectName("centroidRadioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(SelectWithinDialogBase)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.centroidRadioButton)
        self.horizontalLayout_2.addWidget(self.centroidRadioButton)
        self.pointonsurfaceRadioButton_2 = QtWidgets.QRadioButton(SelectWithinDialogBase)
        self.pointonsurfaceRadioButton_2.setObjectName("pointonsurfaceRadioButton_2")
        self.buttonGroup.addButton(self.pointonsurfaceRadioButton_2)
        self.horizontalLayout_2.addWidget(self.pointonsurfaceRadioButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_3 = QtWidgets.QLabel(SelectWithinDialogBase)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.selectWithCombo = QgsMapLayerComboBox(SelectWithinDialogBase)
        self.selectWithCombo.setObjectName("selectWithCombo")
        self.verticalLayout.addWidget(self.selectWithCombo)
        self.selectedFeaturesCheckbox = QtWidgets.QCheckBox(SelectWithinDialogBase)
        self.selectedFeaturesCheckbox.setChecked(True)
        self.selectedFeaturesCheckbox.setObjectName("selectedFeaturesCheckbox")
        self.verticalLayout.addWidget(self.selectedFeaturesCheckbox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.newSelectionRadioButton = QtWidgets.QRadioButton(SelectWithinDialogBase)
        self.newSelectionRadioButton.setChecked(True)
        self.newSelectionRadioButton.setObjectName("newSelectionRadioButton")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(SelectWithinDialogBase)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.newSelectionRadioButton)
        self.horizontalLayout_3.addWidget(self.newSelectionRadioButton)
        self.currentSelectionRadioButton = QtWidgets.QRadioButton(SelectWithinDialogBase)
        self.currentSelectionRadioButton.setObjectName("currentSelectionRadioButton")
        self.buttonGroup_2.addButton(self.currentSelectionRadioButton)
        self.horizontalLayout_3.addWidget(self.currentSelectionRadioButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.button_box = QtWidgets.QDialogButtonBox(SelectWithinDialogBase)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(SelectWithinDialogBase)
        self.button_box.rejected.connect(SelectWithinDialogBase.reject)
        self.button_box.accepted.connect(SelectWithinDialogBase.accept)
        QtCore.QMetaObject.connectSlotsByName(SelectWithinDialogBase)

    def retranslateUi(self, SelectWithinDialogBase):
        _translate = QtCore.QCoreApplication.translate
        SelectWithinDialogBase.setWindowTitle(_translate("SelectWithinDialogBase", "Select Within"))
        self.label.setText(_translate("SelectWithinDialogBase", "Select all features from:"))
        self.label_2.setText(_translate("SelectWithinDialogBase", "Where the:"))
        self.centroidRadioButton.setText(_translate("SelectWithinDialogBase", "Centroid"))
        self.pointonsurfaceRadioButton_2.setText(_translate("SelectWithinDialogBase", "Point on Surface"))
        self.label_3.setText(_translate("SelectWithinDialogBase", "Is within:"))
        self.selectedFeaturesCheckbox.setText(_translate("SelectWithinDialogBase", "Using selected features"))
        self.newSelectionRadioButton.setText(_translate("SelectWithinDialogBase", "Creating new selection"))
        self.currentSelectionRadioButton.setText(_translate("SelectWithinDialogBase", "Adding to current selection"))

from qgis.gui import QgsMapLayerComboBox
