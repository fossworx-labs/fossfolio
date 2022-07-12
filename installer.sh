pip install virtualenv
virtualenv venv 
source venv/bin/activate
pip install poetry 
poetry install
cd fossfolio
python3 build.py