#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS=./tools/remote_api/MoneyCalculation-557f48420bfc.json
./tools/remote_api/remote_api_shell.py -s money-calculation-m1522.appspot.com
