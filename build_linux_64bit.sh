#!/bin/bash
@echo off
clear

function success {
echo Cx_Freeze build completed successfully.
#cd build/exe.linux-x86_64-3.5
# gvfs-set-attribute -t string Weather_App_64bit_launcher.sh metadata::custom-icon file:///app_icon96x96.ico

echo Creating archive for deployment.
#cd ../..
mv build/exe.linux-x86_64-3.5 build/Weather_App_Linux_64bit
cd build
tar -cvzf Weather_App_Linux_64bit.tar.gz Weather_App_Linux_64bit
read -rsp $'Press any key to continue...\n' -n 1 key
}


function proceed {
if [ -d build ] ; then
    echo Deleting build directory.
    rm -rf build
fi
echo Running cx_Freeze script.
python cx_setup_linux_64bit.py build &
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



