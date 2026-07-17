set -o errexit

# install dependencies
pip install -r requirements.txt

#  Collect static files
python manage.py collectstatic --no-input
    
#  makemigrations and migrate
python manage.py makemigrations

python manage.py migrate