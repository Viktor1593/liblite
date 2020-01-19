@echo off
set "ui_name=liblite_ui"
SET rootPath=%~dp0
set "infile=%rootPath%%ui_name%.ui"
set "outfile=%rootPath%%ui_name%.py"

pyuic5 -x %infile% -o %outfile%


set "ui_name=read_book_ui"
set "infile=%rootPath%%ui_name%.ui"
set "outfile=%rootPath%%ui_name%.py"

pyuic5 -x %infile% -o %outfile%