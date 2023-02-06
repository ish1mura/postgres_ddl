rm -rf "./build"
rm -rf "./dist"
rm -rf "./postgres_ddl.egg-info"
"python3" -m pip install --upgrade twine setuptools
"python3" "./setup.py" sdist bdist_wheel
"python3" -m twine upload dist/*
