# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SelectWithinDialog
                                 A QGIS plugin
 Select centroid within and point of surface within
                             -------------------
        begin                : 2015-08-19
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Heikki Vesanto
        email                : heikki.vesanto@gmail.com

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

from qgis.core import QgsMapLayerProxyModel

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'select_within_dialog_base.ui'))


class SelectWithinDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SelectWithinDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.selectFromCombo.setFilters(QgsMapLayerProxyModel.HasGeometry)
        self.selectWithCombo.setFilters(QgsMapLayerProxyModel.HasGeometry)

        self.mostlyWithinRadioButton.toggled.connect(self.where_mostly)
        self.centroidRadioButton.toggled.connect(self.where_centroid)
        self.pointonsurfaceRadioButton.toggled.connect(self.where_surface)
        self.poleOfInaccessibilityRadioButton.toggled.connect(self.where_point_of_inaccessability)

        self.selectWithCombo.layerChanged.connect(self.is_something_selected)

    def where_mostly(self):
        self.poiTolSpin.setEnabled(0)
        self.mostlySpin.setEnabled(1)
        self.noDissolveSelectWith.setEnabled(1)

    def where_centroid(self):
        self.poiTolSpin.setEnabled(0)
        self.mostlySpin.setEnabled(0)
        self.noDissolveSelectWith.setEnabled(0)
        self.noDissolveSelectWith.setChecked(0)

    def where_surface(self):
        self.poiTolSpin.setEnabled(0)
        self.mostlySpin.setEnabled(0)
        self.noDissolveSelectWith.setEnabled(0)
        self.noDissolveSelectWith.setChecked(0)

    def where_point_of_inaccessability(self):
        self.poiTolSpin.setEnabled(1)
        self.mostlySpin.setEnabled(0)
        self.noDissolveSelectWith.setEnabled(0)
        self.noDissolveSelectWith.setChecked(0)

    def is_something_selected(self):
        vlayer = self.selectWithCombo.currentLayer()
        if vlayer is not None:
            if not vlayer.selectedFeatures():
                self.selectedFeaturesCheckbox.setChecked(0)
                self.selectedFeaturesCheckbox.setEnabled(0)
                self.selectedFeaturesCheckbox.setToolTip("No features selected in layer")
            else:
                self.selectedFeaturesCheckbox.setEnabled(1)
                self.selectedFeaturesCheckbox.setToolTip("Use only selected features")
                # self.selectedfeats.setChecked(1)
        else:
            pass
