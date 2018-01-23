@ECHO OFF
@RD /S /Q .\SelectWithin
mkdir SelectWithin
xcopy *.py .\SelectWithin\
xcopy *.svg .\SelectWithin\
xcopy *.png .\SelectWithin\
xcopy *.txt .\SelectWithin\
xcopy *.qrc .\SelectWithin\
xcopy *.ui .\SelectWithin\
