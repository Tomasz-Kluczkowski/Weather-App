@echo off
REM activate virtual environment
call workon weather_app_32b_env
cls

:question
echo This will delete current build directory and all its contents.
set /p answer= Do you want to proceed (y/n)?
if /i "%answer%" == "y" goto proceed
if /i "%answer%" == "n" goto terminate
echo Incorrect input & goto question

:proceed
if exist ..\build_32bit (
    echo Deleting build directory.
    rmdir ..\build_32bit /s /q
)
echo Running cx_Freeze script.
start /wait python ..\Cx_Freeze_Configs\cx_setup_windows_32bit.py build -b ..\build_32bit
if %ERRORLEVEL% EQU 0 (

rmdir ..\build_32bit\exe.win32-3.6\Data\Scripts /s /q
rmdir ..\build_32bit\exe.win32-3.6\Data\Text_files /s /q
rmdir ..\build_32bit\exe.win32-3.6\Data\DLLs /s /q

goto success
) else (
echo Cx_Freeze build failed. Please check your cx_freeze setup file.
echo Exit status code: %ERRORLEVEL%
goto terminate
)

:success
echo Cx_Freeze build completed successfully
echo Starting Inno setup compilation.
start /wait iscc ..\Inno_Setup_Configs\inno_setup_windows_32bit.iss /O+
if %ERRORLEVEL% EQU 0 (
echo Inno setup compilation successul.
) else (
echo Inno setup compilation failed. Please check your setup script.
echo Exit status code: %ERRORLEVEL%
)

:terminate
pause
deactivate
