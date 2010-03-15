/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "PyGUI.h"

@interface PyDateRangeSelector : PyGUI {}
- (void)selectPrevDateRange;
- (void)selectNextDateRange;
- (void)selectTodayDateRange;
- (void)selectMonthRange;
- (void)selectQuarterRange;
- (void)selectYearRange;
- (void)selectYearToDateRange;
- (void)selectRunningYearRange;
- (void)selectAllTransactionsRange;
- (void)selectCustomDateRange;
- (NSString *)display;
- (BOOL)canNavigate;
@end