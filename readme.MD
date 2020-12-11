
### Get Started

_**Note:** To install the dependencies of the project make sure Python 3 is installed._

### Installation

Setup project environment using virtualenv.

For Linux
```
python3 -m venv env
source env/bin/activate
```

For Windows
```
python3 -m venv env
source ./env/Scripts/activate
```

Install project dependencies using pip. 

```
pip install -r requirements.txt
```

Navigate to the project folder. Migrate the models and run the development server.

```
cd registration
python manage.py migrate
python manage.py runserver
```
