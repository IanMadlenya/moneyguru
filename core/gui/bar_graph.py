# Created By: Virgil Dupras
# Created On: 2008-07-06
# Copyright 2012 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from datetime import date, timedelta

from hscommon.geometry import Rect, Point

from ..model.date import DateRange, MonthRange, YearToDateRange
from .graph import Graph

class PenID:
    Axis = 1
    Bar = 2
    TodayLine = 3

class BrushID:
    NormalBar = 1
    FutureBar = 2

class BarGraph(Graph):
    # BarGraph's data point is (float x1, float x2, float past_value, float future_value).
    #--- Virtual
    def _currency(self):
        return None
    
    def _get_cash_flow(self, date_range):
        return 0
    
    #--- Override
    def compute_data(self):
        def monthly_period(start_date):
            return MonthRange(start_date)
        
        def weekly_period(start_date):
            first_weekday = self.document.first_weekday
            weekday = start_date.weekday()
            if weekday < first_weekday:
                weekday += 7
            diff = weekday - first_weekday
            period_start = start_date - timedelta(diff)
            period_end = period_start + timedelta(6)
            return DateRange(period_start, period_end)
        
        TODAY = date.today()
        date_range = self.document.date_range
        self._data = []
        self._min_date = date_range.start
        self._max_date = date_range.end
        period_getter = monthly_period if date_range.days >= 100 else weekly_period
        current_date = date_range.start
        while current_date <= date_range.end:
            period = period_getter(current_date)
            if isinstance(date_range, YearToDateRange): # we don't overflow in YTD
                period.end = min(period.end, self._max_date)
            self._min_date = min(period.start, self._min_date)
            self._max_date = max(period.end + timedelta(1), self._max_date)
            current_date = period.end + timedelta(1)
            if TODAY in period:
                past_amount = float(self._get_cash_flow(period.past))
                future_amount = float(self._get_cash_flow(period.future))
            else:
                amount = float(self._get_cash_flow(period))
                if TODAY > period.end: # all in the past
                    past_amount = amount
                    future_amount = 0
                else: # all in the future
                    future_amount = amount
                    past_amount = 0
            if past_amount + future_amount:
                left = self._offset_xpos(period.start.toordinal())
                # we want a 1 day period to have a width of 1
                right = self._offset_xpos(period.end.toordinal() + 1)
                padding = (right - left) / 5
                self._data.append((left + padding, right - padding, past_amount, future_amount))
    
    def compute_x_axis(self):
        Graph.compute_x_axis(self)
        self._xmin = self._offset_xpos(self._min_date.toordinal())
        self._xmax = self._offset_xpos(self._max_date.toordinal())
    
    def yrange(self):
        if self._data:
            ymin = min(0, min(min(h1, h2, h1+h2) for x1, x2, h1, h2 in self._data))
            ymax = max(0, max(max(h1, h2, h1+h2) for x1, x2, h1, h2 in self._data))
            return (ymin, ymax)
        else:
            return (0, 1)
    
    def draw(self, xfactor, yfactor):
        for x1, x2, h1, h2 in self.data:
            x1 *= xfactor
            x2 *= xfactor
            h1 *= yfactor
            h2 *= yfactor
            
            # Compute and fill past and future rectangles
            different_side = (h1 >= 0) != (h2 >= 0)
            past_rect = Rect(x1, 0, x2-x1, abs(h1))
            if h2:
                future_height = abs(h2 if different_side else h2-h1)
            else:
                future_height = 0
            future_rect = Rect(x1, 0, x2-x1, future_height)
            if h1 >= 0:
                past_rect.bottom = h1
            else:
                past_rect.top = h1
            if h2 >= 0:
                future_rect.bottom = h2
            else:
                future_rect.top = h2            
            self.view.draw_rect(past_rect, None, BrushID.NormalBar)
            self.view.draw_rect(future_rect, None, BrushID.FutureBar)
            
            # Compute and draw rect lines
            union = past_rect.united(future_rect)
            if (union.top < 0) and (union.bottom > 0): # we draw 4 sides instead of 3
                self.view.draw_rect(union, PenID.Bar, None)
            else:
                # One of bottom and top is 0. Use the other one. We're working with floats here,
                # comparison with 0 are hazardous, so I'm avoiding them.
                h = union.top if abs(union.top) >= abs(union.bottom) else union.bottom
                points = [Point(x1, 0), Point(x1, h), Point(x2, h), Point(x2, 0)]
                self.view.draw_polygon(points, PenID.Bar, None)
            
            
            # draw red line
            if (h1 != 0) and (h2 != 0):
                lineY = 0 if different_side else h1
                # XXX Under Qt, the red line is overshoadowed by the horizontal axis line when lineY == 0
                self.view.draw_line(Point(x1, lineY), Point(x2, lineY), PenID.TodayLine)
    
    @property
    def title(self):
        return ''
    
    @property
    def currency(self):
        return self._currency()
    
    #--- Event Handlers
    first_weekday_changed = Graph._data_changed
