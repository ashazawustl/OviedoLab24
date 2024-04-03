@echo off
title MERFISH Data Processing - Python Virtual Env

REM Create virtual environment
python -m venv venv

REM Print out the command to install the required packages if first time running
echo If this is the first time running this script, run the following command to install the required packages:
echo pip install -r requirements.txt
echo:
echo Or to manually install the required packages:
echo pip install pandas anndata scipy
echo:
echo:


REM Activate virtual environment
cmd /k venv\Scripts\activate
