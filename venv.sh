PATH_CURRENT=$(dirname "$0")
PATH_ENV=$PATH_CURRENT/.venv

rm -rf $PATH_ENV
python3 -m venv $PATH_ENV
$PATH_ENV/bin/pip install psycopg[binary] twine setuptools wheel
