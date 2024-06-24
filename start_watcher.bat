@echo off
cd /d "C:\path\quicksavePDF"
start python watcher.py "C:\path to directory you want to make pdf autosaves for" --watch_duration 3600
