# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SelectWithin
                                 A QGIS plugin
 Select centroid within and point of surface within
                              -------------------
        begin                : 2015-08-19
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Heikki Vesanto
        email                : heikki.vesanto@thinkwhere.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox, QProgressBar
from qgis.core import *
# Initialize Qt resources from file resources.py
import resource_rc
# Import the code for the dialog
from select_within_dialog import SelectWithinDialog
import os.path
from PyQt4.QtCore import *


class SelectWithin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SelectWithin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SelectWithinDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Select Within')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SelectWithin')
        self.toolbar.setObjectName(u'SelectWithin')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SelectWithin', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SelectWithin/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Select Within'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Select Within'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # Get list of vector layers
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        # Populate the UI with the list
        self.dlg.selectWithCombo.clear()
        self.dlg.selectFromCombo.clear()
        #Check there is at least one vector layer. Selecting within the same layer is fine.
        vlayer_count = 0
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                vlayer_count = vlayer_count + 1
                self.dlg.selectWithCombo.addItem( layer.name(), layer )
                self.dlg.selectFromCombo.addItem( layer.name(), layer )

        # Run the dialog event loop
        if vlayer_count > 0:
            # show the dialog
            self.dlg.show()
            result = self.dlg.exec_()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                "No vecor layers.", QMessageBox.Ok)
            result = 0
        # See if OK was pressed

        if result:
            # Get the two selected layers.
            index1 = self.dlg.selectWithCombo.currentIndex()
            selecting_layer = self.dlg.selectWithCombo.itemData(index1)
            index2 = self.dlg.selectFromCombo.currentIndex()
            select_from_layer = self.dlg.selectFromCombo.itemData(index2)

            # Either select with all features or just selected ones
            selected_test = self.dlg.selectedFeaturesCheckbox.isChecked()
            if selected_test == 1:
                selecting_feats = selecting_layer.selectedFeatures()
            else:
                selecting_feats_iterator = selecting_layer.getFeatures()
                selecting_feats = []
                for s_feat in selecting_feats_iterator:
                    selecting_feats.append(s_feat)

            select_from_feats = select_from_layer.getFeatures()

            # Check if point on surface or centroid is selected
            point_on_surface_test = self.dlg.pointonsurfaceRadioButton_2.isChecked()
            if point_on_surface_test == 1:
                point_on_surface = 1
            else:
                point_on_surface = 0

            centroids = []

            # Attempting to use a spatial index so not all centroids need to be created.
            spatial_index = QgsSpatialIndex()
            for f in selecting_feats:
                spatial_index.insertFeature(f)

            # Progress bar.
            progressMessageBar = self.iface.messageBar().createMessage("Creating selection points...")
            progress = QProgressBar()
            progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            progressMessageBar.layout().addWidget(progress)
            self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
            maximum_progress = select_from_layer.featureCount()
            progress.setMaximum(maximum_progress)
            i = 0

            # Create centroids for all features that intersect the bounding box of the selecting features
            for each_feat in select_from_feats:
                if spatial_index.intersects(each_feat.geometry().boundingBox()):
                    geom = each_feat.geometry()
                    if point_on_surface == 1:
                        centroid = geom.pointOnSurface()
                    else:
                        centroid = geom.centroid()
                    id = each_feat.id()
                    centroid_feat = QgsFeature(id)
                    centroid_feat.setGeometry(centroid)
                    centroids.append(centroid_feat)
                i = i + 1
                progress.setValue(i)

            to_select = []

            # Progress bar would not update for this procedure. Need to look into perhaps a new thread for it.
            for each_feat in selecting_feats:
                geom = each_feat.geometry()
                # Check if feature geometry is multipart
                # Credit to from Alexandre Neto at:
                # http://gis.stackexchange.com/questions/44799/how-to-transform-a-selected-multipart-feature-into-
                # singlepart-features-while-edi
                if geom.isMultipart():
                    multi_new_features = []
                    temp_feature = QgsFeature(each_feat)
                    # Create a new feature using the geometry of each part
                    for part in geom.asGeometryCollection():
                        temp_feature.setGeometry(part)
                        multi_new_features.append(QgsFeature(temp_feature))
                    # Splitting into single part allows for the parts to be indexed as well.
                    for multi_features in multi_new_features:
                        for each_centroid in centroids:
                            selecting = multi_features.geometry()
                            centroid = each_centroid.geometry()
                            # First do a bounding box check this speeds up the selection
                            # Bounding box with point search. I don't think a proper index would speed it up?
                            if centroid.intersects(selecting.boundingBox()):
                                if centroid.within(selecting):
                                    to_select.append(each_centroid.id())

                # If singlepart
                else:
                    for each_centroid in centroids:
                        selecting = each_feat.geometry()
                        centroid = each_centroid.geometry()
                        #
                        if centroid.within(selecting):
                            to_select.append(each_centroid.id())

            self.iface.messageBar().clearWidgets()

            # Clear selection if desired, default option adds to current selection
            if self.dlg.newSelectionRadioButton.isChecked() == 1:
                select_from_layer.removeSelection()

            select_from_layer.select(to_select)