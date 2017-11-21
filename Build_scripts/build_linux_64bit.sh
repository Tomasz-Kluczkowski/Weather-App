#!/bin/bash

@echo off
clear

function success {
echo Cx_Freeze build completed successfully.
#cd build/exe.linux-x86_64-3.5
# gvfs-set-attribute -t string Weather_App_64bit_launcher.sh metadata::custom-icon file:///app_icon96x96.ico

echo Creating archive for deployment.
#cd ../..
mv ../build_linux_64bit/exe.linux-x86_64-* ../build_linux_64bit/Weather_App_Linux_64bit
cd ../build_linux_64bit
tar -cvzf Weather_App_Linux_64bit.tar.gz Weather_App_Linux_64bit
echo Finished creating archive.
read -rsp $'Press any key to continue...\n' -n 1 key
}


function proceed {

if [ -d ../build_linux_64bit ] ; then
    echo Deleting build directory.
    rm -rf ../build_linux_64bit
fi
source ~/.virtualenvs/weather_app_64b_env/bin/activate
echo Running cx_Freeze script.

python ../Cx_Freeze_Configs/cx_setup_linux_64bit.py build -b ../build_linux_64bit &
pid=$!
wait ${pid}
status=$?

if [ ${status} -eq 0 ] ; then
    deactivate
    success
else
echo Cx_Freeze build failed. Please check your cx_freeze setup file.
echo "Exit status code: ${status}"
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



