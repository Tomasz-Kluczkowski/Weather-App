#!/bin/bash
@echo off
clear


function success {
echo Cx_Freeze build completed successfully.
echo Creating archive for deployment.

mv ../build_linux_32bit/exe.linux-i686-* ../build_linux_32bit/Weather_App_Linux_32bit
cd ../build_linux_32bit

rm -rf Weather_App_Linux_32bit/Data/Scripts
rm -rf Weather_App_Linux_32bit/Data/Text_files
rm -rf Weather_App_Linux_32bit/Data/DLLs

tar -cvzf Weather_App_Linux_32bit.tar.gz Weather_App_Linux_32bit
echo Finished creating archive.
read -rsp $'Press any key to continue...\n' -n 1 key
}


function proceed {
if [ -d ../build_linux_32bit ] ; then
    echo Deleting build directory.
    rm -rf ../build_linux_32bit
fi
source ~/.virtualenvs/weather_app_32b_env/bin/activate
echo Running cx_Freeze script.

python ../Cx_Freeze_Configs/cx_setup_linux_32bit.py </dev/tty build -b ../build_linux_32bit &
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



