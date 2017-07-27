@echo off
cls
:question
echo This will delete current build directory and all its contents.
set /p answer= Do you want to proceed (y/n)?
if /i "%answer%" == "y" goto proceed
if /i "%answer%" == "n" goto:eof
echo Incorrect input & goto question

:proceed
if exist build echo Deleting build directory.
rmdir build /s /q
echo Running cx_Freeze script.
start /wait python cx_setup_windows_32bit.py build
if exist build (
goto success
) else (
echo Cx_Freeze build failed. Please check your cx_freeze setup file.
goto:eof
)

:success
echo Cx_Freeze build completed successfully
echo Starting Inno setup compilation.
start /wait iscc inno_setup_windows_32bit.iss /O+
if exist build/Weather_App_Win_32bit_Setup.exe (
echo Inno setup compilation successul.
) else (
echo Inno setup compilation failed. Please check your setup script.
)
pause
