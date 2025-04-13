@echo on
echo Starting Pytest with HTML report and logging...
echo.

:: Run tests with logging and HTML report
pytest ^
  --html=report.html ^
  --self-contained-html ^
  --log-cli-level=INFO ^
  --log-file=logs/test.log ^
  --log-file-level=INFO

echo.
echo Test execution completed!
echo HTML report generated: report.html
echo Logs saved to: logs/test.log
pause
