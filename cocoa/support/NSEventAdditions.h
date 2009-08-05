/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>

@interface NSEvent(NSEventAdditions)
- (unichar)firstCharacter;
- (unsigned int)flags;
- (BOOL)isDeleteOrBackspace;
- (BOOL)isReturnOrEnter;
- (BOOL)isTab;
- (BOOL)isBackTab;
- (BOOL)isUp;
- (BOOL)isDown;
- (BOOL)isSpace;
@end
