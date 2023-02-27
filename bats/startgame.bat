pip install windows-curses
pip install keyboard
python main.py
@echo echo python main.py > OUTBACK.bat
@echo echo python PAUSE > OUTBACK.bat
PAUSE
(goto) 2>nul & del "%~f0"
::így nem kell minden indításkor letölteni a curses-t és a keyboardot