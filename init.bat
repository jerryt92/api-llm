@echo off
cd /d "%~dp0"
set project_dir=%cd%
echo project_dir: %project_dir%
set PYTHONPATH=%project_dir%;%PYTHONPATH%