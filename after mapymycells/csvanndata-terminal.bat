@echo off
title MERFISH Data Processing - Python Virtual Env

REM Create virtual environment
python -m venv csvanndata

REM Print out the command to install the required packages if first time running
echo If this is the first time running this script, run the following command to install the required packages:
echo pip install -r requirements2.txt
echo:
echo Or to manually install the required packages:
echo pip install scanpy anndata scipy
echo:
echo:


REM Activate virtual environment
cmd /k csvanndata\Scripts\activate
