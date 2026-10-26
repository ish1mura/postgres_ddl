rmdir /S /Q "./build"
rmdir /S /Q "./dist"
rmdir /S /Q "./postgres_ddl.egg-info"
"python.exe" "./setup.py" sdist bdist_wheel
"python.exe" -m twine upload dist/*
pause