# Created By: Virgil Dupras
# Created On: 2009-11-07
# Copyright 2012 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPen

from core.gui.bar_graph import PenID, BrushID
from .graph_view import GraphView

class BarGraphView(GraphView):
    DRAW_XAXIS_OVERLAY = False
    FLIP_COORDS = False
    
    def penForID(self, penId):
        if penId == PenID.Bar:
            return self.linePen
        elif penId == PenID.TodayLine:
            pen = QPen(self.linePen)
            pen.setColor(Qt.red)
            return pen
    
    def brushForID(self, brushId):
        if brushId == BrushID.NormalBar:
            return self.graphBrush
        elif brushId == BrushID.FutureBar:
            return self.graphFutureBrush
    
    def _drawGraph(self, painter, xFactor, yFactor):
        ds = self.dataSource
        self.current_painter = painter
        ds.draw(xFactor, yFactor)
        del self.current_painter
    
