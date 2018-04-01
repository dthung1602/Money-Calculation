#!/usr/bin/env bash
export GAE_SDK_ROOT='/home/hung/opt/google-cloud-sdk/platform/google_appengine'
export PROJECT_ROOT='/media/hung/DATA1/PYTHON/Workspace/MoneyCalculation'
export PYTHONPATH=`which python`
export PYTHONPATH=${GAE_SDK_ROOT}:${PROJECT_ROOT}:${PYTHONPATH}
export PICKLE_FILE='pickle_file.dat'
export PYTHONUNBUFFERED='true'

echo "Start downloading old data ..."
export GOOGLE_APPLICATION_CREDENTIALS='../../../GoogleAppEngine/WebApp-546d92efe094.json'
export APP_ID='webapp-173414'
python download.py

if [[ $? != 0 ]]; then
    echo -e "\n\nUpgrading stopped"
    exit 1
fi

echo -e "\nStart uploading new data ..."
export GOOGLE_APPLICATION_CREDENTIALS='../remote_api/MoneyCalculation-557f48420bfc.json'
export APP_ID='money-calculation-m1522'
python upload.py

if [[ $? != 0 ]]; then
    echo -e "\n\nUpgrading stopped"
    exit 2
else
    echo -e "\nDone!"
    exit 0
fi