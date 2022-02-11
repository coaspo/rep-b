@echo on
call ./venv/Scripts/activate.bat
set PYTHONPATH=.
pytest tests/
if ERRORLEVEL 1 (
	set errorflag=1
)
call ./venv/Scripts/deactivate.bat
if ERRORLEVEL 1 (
	echo. & echo    Tests have failed - cannot do check-in & echo.
	pause
	exit 1
)
@echo on
git add *
git status
echo.
set /p msg=Enter commit msg: 
git commit -m "%msg%"
git push origin br1
pause