#!/bin/bash
@echo off
clear


function success {
echo Cx_Freeze build completed successfully.
pause
}


function proceed {
if [ -d build ] ; then
    echo Deleting build directory.
    rm -rf build
fi
echo Running cx_Freeze script.
python cx_setup_linux_32bit.py build &
wait
if [ -d build ] ; then
    success
else
echo Cx_Freeze build failed. Please check your cx_freeze setup file.
exit 1
fi
}


function question {
clear
echo This will delete current build directory and all its contents.
read -p "Do you want to proceed (y/n)?" answer

if [ "${answer,,}" = "y" ] ; then
    echo Proceeding.
    proceed

elif [ "${answer,,}" = "n" ] ; then
    exit 0

else
    echo Incorrect input
    question
fi
}


question



