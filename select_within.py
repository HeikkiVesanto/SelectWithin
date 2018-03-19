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
from __future__ import absolute_import
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, Qt, QCoreApplication, QVariant
# QCoreApplication, QVariant
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QProgressBar
from qgis.PyQt.QtGui import QIcon
from qgis.core import *
from qgis.utils import *
# Initialize Qt resources from file resources.py required for icon
from . import resource_rc
# Import the code for the dialog
from .select_within_dialog import SelectWithinDialog
import os.path


class SelectWithin(object):
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

    def create_progress_bar(self, message, size):
        progress_message_bar = self.iface.messageBar().createMessage(message)
        progress_b = QProgressBar()
        progress_b.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        progress_message_bar.layout().addWidget(progress_b)
        self.iface.messageBar().pushWidget(progress_message_bar)
        progress_b.setMaximum(size)
        return progress_b

    def clear_progress_bar(self):
        self.iface.messageBar().clearWidgets()

    def count_vertices(self, geom, typ):
        # Count vertices
        n = None
        if typ == "Point":
            if geom.isMultipart():  # new part for multipolylines
                vertices = geom.asMultiPoint()
                n = 0
                for v in vertices:
                    n += 1
            else:
                n = 1
        if typ == "LineString":
            if geom.isMultipart():  # new part for multipolylines
                vertices = geom.asMultiPolyline()
                n = 0
                for v in vertices:
                    n += len(v)
            else:
                vertices = geom.asPolyline()
                n = len(vertices)
        if typ == "Polygon":
            n = 0
            if geom.isMultipart():
                polygons = geom.asMultiPolygon()
            else:
                polygons = [geom.asPolygon()]
            for polygon in polygons:
                for ring in polygon:
                    n += len(ring)
        if n:
            return n
        else:
            return None

    def create_centroids(self, select_f_l, sp_index, cen_type, max_feats, poit):
        centroids = []
        progress = self.create_progress_bar("Creating selection points...", max_feats)
        i = 0
        # Create centroids for all features that intersect the bounding box of the selecting features
        for each_feat in select_f_l:
            if sp_index:
                if sp_index.intersects(each_feat.geometry().boundingBox()):
                    centroid_feat = self.centroid_point(each_feat, cen_type, poit)
                    centroids.append(centroid_feat)
                i = i + 1
                progress.setValue(i)
            else:
                # No index, or not supported
                centroid_feat = self.centroid_point(each_feat, cen_type, poit)
                centroids.append(centroid_feat)
                i = i + 1
                progress.setValue(i)
        self.clear_progress_bar()
        return centroids

    def centroid_point(self, feat, cen_type, poit):
        geom = feat.geometry()
        if cen_type == "point_on_surface":
            centroid = geom.pointOnSurface()
        elif cen_type == "centroid":
            centroid = geom.centroid()
        elif cen_type == "pole_of_inaccessibility":
            centroid = geom.poleOfInaccessibility(poit)[0]
        else:
            centroid = None
        centroid_feat = QgsFeature(feat.id())
        centroid_feat.setGeometry(centroid)
        return centroid_feat

    def dissolve_feats(self, input_feats):
        # Function to dissolve input features so select within, works on the layer, rather than individual features
        feats = []
        # Create and empty list of features and add all features to it.
        # We use feature 0 later and this ensures it exits.
        for each_feat in input_feats:
            feats.append(each_feat)
        # Do not run if geometry is empty, produce an error instead.
        if len(feats) > 0:
            # Need to create empty geometry to hold the dissolved features, we use the first feature to seed it.
            # Combine require a non-empty geometry to work (I could not get it to work).
            feat = feats[0]
            dissolved_geom = feat.geometry()

            # Run through the features and dissolve them all.
            for each_feat in feats:
                geom = each_feat.geometry()
                dissolved_geom = geom.combine(dissolved_geom)
            return_f = QgsFeature()
            return_f.setGeometry(dissolved_geom)
            self.iface.messageBar().clearWidgets()
            return return_f
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                                "No features to dissolve.", QMessageBox.Ok)
            return input_feats

    def run(self):
        """Run method that performs all the real work"""
        # Get list of vector layers
        layers = list(QgsProject.instance().mapLayers().values())

        # Check there is at least one vector layer. Selecting within the same layer is fine.
        vlayer_count = 0
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                vlayer_count = vlayer_count + 1
        # Run the dialog event loop
        if vlayer_count > 0:
            # show the dialog
            self.dlg.show()
            self.dlg.is_something_selected()
            result = self.dlg.exec_()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                                "No vector layers.", QMessageBox.Ok)
            result = 0
        # See if OK was pressed

        if result and self.dlg.selectWithCombo.currentLayer() and self.dlg.selectFromCombo.currentLayer():
            # Get the two selected layers.
            selecting_layer = self.dlg.selectWithCombo.currentLayer()
            select_from_layer = self.dlg.selectFromCombo.currentLayer()

            # Either select with all features or just selected ones
            if self.dlg.selectedFeaturesCheckbox.isChecked():
                selecting_feats = selecting_layer.selectedFeatures()
            else:
                selecting_feats_iterator = selecting_layer.getFeatures()
                selecting_feats = []
                for s_feat in selecting_feats_iterator:
                    selecting_feats.append(s_feat)

            select_from_feats = select_from_layer.getFeatures()

            # Asssign variables
            point_style = False
            per_style = False
            dissolve_selecting = 0
            cen_style = None
            poi_tol = 1.0

            if self.dlg.pointonsurfaceRadioButton.isChecked():
                point_style = True
                cen_style = "point_on_surface"
            elif self.dlg.centroidRadioButton.isChecked():
                point_style = True
                cen_style = "centroid"
            elif self.dlg.poleOfInaccessibilityRadioButton.isChecked():
                point_style = True
                cen_style = "pole_of_inaccessibility"
                poi_tol = self.dlg.poiTolSpin.value()
            elif self.dlg.mostlyWithinRadioButton.isChecked():
                # Percentage within was selected
                per_within = self.dlg.mostlySpin.value()
                dissolve_selecting = 1
                if self.dlg.noDissolveSelectWith.isChecked():
                    dissolve_selecting = 0
                per_style = True
            else:
                QMessageBox.warning(self.iface.mainWindow(), "Warning",
                                    "No select style selected.", QMessageBox.Ok)
                result = 0

            # Check if advanced settings ticked:
            no_select_from_index = self.dlg.noIndexSelectFrom.isChecked()
            no_select_with_index = self.dlg.noIndexSelectWith.isChecked()

            to_select = []

            if point_style:
                # Attempting to use a spatial index so not all centroids need to be created.
                if no_select_with_index:
                    spatial_index_selecting = None
                    self.iface.messageBar().pushInfo("Notice",
                                                     "Spatial index on select with layer not created. "
                                                     "Performance reduced.")
                else:
                    spatial_index_selecting = QgsSpatialIndex()
                    for f in selecting_feats:
                        spatial_index_selecting.insertFeature(f)
                    # If index creation fails then run without.
                    if spatial_index_selecting.refs() < 1:
                        spatial_index_selecting = None
                        self.iface.messageBar().pushInfo("Error",
                                                         "Spatial index on select with layer not created. "
                                                         "Performance reduced.")

                centroids = self.create_centroids(select_from_feats, spatial_index_selecting, cen_style,
                                                  select_from_layer.featureCount(), poi_tol)

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
            elif per_style:
                if no_select_from_index:
                    spatial_index_select_from = None
                    self.iface.messageBar().pushInfo("Notice",
                                                     "Spatial index on select from layer not created. "
                                                     "Performance reduced.")
                else:
                    spatial_index_select_from = QgsSpatialIndex(select_from_feats)
                    # If index creation fails then run without.
                    if spatial_index_select_from.refs() < 1:
                        spatial_index_select_from = None
                        self.iface.messageBar().pushInfo("Error",
                                                         "Spatial index on select from layer not created. "
                                                         "Performance reduced.")
                # Percentage selecting
                # Loop through all features that are being selected
                # Do a bounding box check if it intersects
                # Check if intersects
                # If so, check area of selection feature
                # Do an intersection
                # Check percentage of intersection
                # Select if over n percent

                if dissolve_selecting == 1:
                    self.iface.messageBar().pushInfo("Notice",
                                                     "Dissolving features.")
                    selecting_feats_dis = self.dissolve_feats(selecting_feats)
                    # We are iterating later, so if only one feature is returned,
                    # switch it to a list
                    selecting_feats = []
                    selecting_feats.append(selecting_feats_dis)

                # Progress bar is broken
                # progress = self.create_progress_bar("Selecting features {}% within..."
                # .format(per_within), selecting_feats.featureCount())

                i = 0

                # Need some notice of running, but this is not useful.
                # GUI freezes and message is displayed after completion.
                # self.iface.messageBar().pushInfo("Notice",
                #                                 "Selecting features.")

                for selecting_feat in selecting_feats:
                    if spatial_index_select_from:
                        intersecting = spatial_index_select_from.intersects(selecting_feat.geometry().boundingBox())
                    else:
                        intersecting = []
                        for feat in select_from_feats:
                            if feat.geometry().intersects(selecting_feat.geometry()):
                                intersecting.append(feat.id())
                    for bb_match in intersecting:
                        # Use index and get feature using the index
                        iterator = select_from_layer.getFeatures(QgsFeatureRequest().setFilterFid(bb_match))
                        # Grab only feature in the feature request
                        select_from_feat = next(iterator)
                        if select_from_feat.geometry().intersects(selecting_feat.geometry()):
                            # The logic from now on will vary with different geometry types
                            sf_type = select_from_feat.geometry().wkbType()
                            # Point:
                            if sf_type in [1, 1001, 2001, 3001]:
                                # Point
                                # Point 1, PointZ 1001, PointM = 2001, PointZM = 3001
                                to_select.append(select_from_feat.id())
                                # Point is easy, if it intersects the selecting feature it is 100% in it.
                                # So just select it. Selecting feature type does not matter.
                            # MultiPoint:
                            elif sf_type in [4, 1004, 2004, 3004]:
                                # MultiPoint
                                # I want to count the number of points in the intersection geometry and compare the
                                # count to the original geometry. If the intersecting points are more than twice the
                                # original, then select.
                                overlap_area = select_from_feat.geometry().intersection(
                                    selecting_feat.geometry())
                                if self.count_vertices(overlap_area, "Point") >= (
                                            self.count_vertices(select_from_feat.geometry(), "Point") *
                                            (per_within / 100.0)):
                                    to_select.append(select_from_feat.id())
                            # Line or Multiline
                            elif sf_type in [2, 1002, 2002, 3002, 5, 1005, 2005, 3005]:
                                # LineString or Multiline
                                sw_type = selecting_feat.geometry().wkbType()
                                # Intersecting point:
                                # If line has only 2 vertexes and intersects
                                if sw_type in [1, 1001, 2001, 3001]:
                                    # Already intersects just need point count test:
                                    if self.count_vertices(select_from_feat.geometry(), "LineString") == 2:
                                        to_select.append(select_from_feat.id())
                                elif sw_type in [4, 1004, 2004, 3004]:
                                    # If count of intersecting part points,
                                    # is bigger than count of line part vertexes/2
                                    overlap_area = select_from_feat.geometry().intersection(
                                        selecting_feat.geometry())
                                    if self.count_vertices(overlap_area, "Point") >= (
                                                self.count_vertices(select_from_feat.geometry(), "LineString")
                                                * (per_within / 100.0)):
                                        to_select.append(select_from_feat.id())
                                elif sw_type in [2, 1002, 2002, 3002, 5, 1005, 2005, 3005, 3, 1003, 2003, 3003,
                                                 6, 1006, 2006, 3006]:
                                    # If intersecting line is longer than the original line/2
                                    # If intersecting two lines, need to check that output
                                    # is a line, else no intersect.
                                    overlap_area = select_from_feat.geometry().intersection(
                                        selecting_feat.geometry())
                                    if overlap_area is not None:
                                        if overlap_area.wkbType() in [2, 1002, 2002, 3002, 5, 1005, 2005, 3005]:
                                            if overlap_area.length() >= select_from_feat.geometry().length()\
                                                    * (per_within / 100.0):
                                                to_select.append(select_from_feat.id())
                                else:
                                    self.iface.messageBar().pushInfo("Error",
                                                                     "Select with geometry type {} not supported"
                                                                     .format(sf_type))
                            # Polygon or Multipolygon
                            elif sf_type in [3, 1003, 2003, 3003, 6, 1006, 2006, 3006]:
                                # Polygon or Multipolygon
                                sw_type = selecting_feat.geometry().wkbType()
                                if sw_type in [1, 1001, 2001, 3001]:
                                    pass
                                    # Polygon cannot mostly be inside a point
                                elif sw_type in [4, 1004, 2004, 3004]:
                                    # If count of intersecting part points,
                                    # is bigger than count of polygon part vertexes/2
                                    overlap_area = select_from_feat.geometry().intersection(
                                        selecting_feat.geometry())
                                    if self.count_vertices(overlap_area, "Point") >= (
                                                self.count_vertices(select_from_feat.geometry(), "Polygon") *
                                                (per_within / 100.0)):
                                        to_select.append(select_from_feat.id())
                                elif sw_type in [2, 1002, 2002, 3002, 5, 1005, 2005, 3005]:
                                    # If count of intersecting vertexes,
                                    # is bigger than count of polygon part vertexes/2
                                    # This is broken, you would have to conver the polygon to points first for this to
                                    # work properly.
                                    overlap_area = select_from_feat.geometry().intersection(
                                        selecting_feat.geometry())
                                    if self.count_vertices(overlap_area, "Polyline") >= (
                                                self.count_vertices(select_from_feat.geometry(), "Polygon") *
                                                (per_within / 100.0)):
                                        to_select.append(select_from_feat.id())
                                    self.iface.messageBar().pushInfo("Error",
                                                                     "Line and polygon intersection is "
                                                                     "not implemented correctly")
                                elif sw_type in [3, 1003, 2003, 3003, 6, 1006, 2006, 3006]:
                                    # If intersection polygon size is larger than original part size/2
                                    overlap_area = select_from_feat.geometry().intersection(
                                        selecting_feat.geometry())
                                    if overlap_area is not None:
                                        if overlap_area.area() >= select_from_feat.geometry().area() * \
                                                (per_within / 100.0):
                                            to_select.append(select_from_feat.id())
                                else:
                                    self.iface.messageBar().pushInfo("Error",
                                                                     "Select with geometry type {} not supported. "
                                                                     "Select from type {}.".format(sf_type, sw_type))
                            else:
                                self.iface.messageBar().pushInfo("Error", "Select from geometry "
                                                                 "type {} not supported".format(sf_type))
                                """
                                Other geometry types not handled:
                                GeometryCollection = 7,
                                CircularString = 8,
                                CompoundCurve = 9,
                                CurvePolygon = 10,
                                MultiCurve = 11,
                                MultiSurface = 12,
                                Triangle = 17,
                                TriangleZ = 1017,
                                GeometryCollectionZ = 1007,
                                CircularStringZ = 1008,
                                CompoundCurveZ = 1009,
                                CurvePolygonZ = 1010,
                                MultiCurveZ = 1011,
                                MultiSurfaceZ = 1012,
                                TriangleM = 2017,
                                GeometryCollectionM = 2007,
                                CircularStringM = 2008,
                                CompoundCurveM = 2009,
                                CurvePolygonM = 2010,
                                MultiCurveM = 2011,
                                MultiSurfaceM = 2012,
                                GeometryCollectionZM = 3007,
                                CircularStringZM = 3008,
                                CompoundCurveZM = 3009,
                                CurvePolygonZM = 3010,
                                MultiCurveZM = 3011,
                                MultiSurfaceZM = 3012,
                                TriangleZM = 3017,"""
                    # progress.setValue(i)
                    i += 1
            else:
                self.iface.messageBar().pushInfo("Error",
                                                 "No style selected.")

            # self.clear_progress_bar()

            # Clear selection if desired, default option adds to current selection
            if self.dlg.newSelectionRadioButton.isChecked() == 1:
                select_from_layer.removeSelection()

            self.iface.messageBar().pushSuccess("Success",
                                                "Select Within Done.")
            select_from_layer.select(to_select)
