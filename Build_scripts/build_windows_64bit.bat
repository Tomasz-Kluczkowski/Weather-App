@echo off
REM activate virtual environment
call workon weather_app_64b_env
cls

:question
echo This will delete current build directory and all its contents.
set /p answer= Do you want to proceed (y/n)?
if /i "%answer%" == "y" goto proceed
if /i "%answer%" == "n" goto terminate
echo Incorrect input & goto question

:proceed
if exist ..\build_64bit (
    echo Deleting build directory.
    rmdir ..\build_64bit /s /q
)
echo Running cx_Freeze script.
start /wait python ..\Cx_Freeze_Configs\cx_setup_windows_64bit.py build -b ..\build_64bit
if exist ..\build_64bit (
goto success
) else (
echo Cx_Freeze build failed. Please check your cx_freeze setup file.
goto terminate
)

:success
echo Cx_Freeze build completed successfully
echo Starting Inno setup compilation.
start /wait iscc ..\Inno_Setup_Configs\inno_setup_windows_64bit.iss /O+
if exist ..\build_64bit\Weather_App_Win_64bit_Setup.exe (
echo Inno setup compilation successul.
) else (
echo Inno setup compilation failed. Please check your setup script.
)

:terminate
pause
deactivate
