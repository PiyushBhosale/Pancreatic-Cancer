Pancreatic Cancer Prediction Web Application
Description

This web application predicts the likelihood of pancreatic cancer using a trained deep learning model. The system allows users to sign up, log in, and submit medical input data through a web interface to receive prediction results.

The backend is built using Django, and the machine learning model is integrated into the API to provide real-time predictions. The application ensures authenticated access before allowing users to perform analysis.

Setup Instructions

Follow the steps below to set up and run the project locally.

1. Clone the Repository
git clone https://github.com/PiyushBhosale/Pancreatic-Cancer.git
cd Pancreatic-Cancer
2. Create Virtual Environment
python -m venv myenv

Activate the environment:

Windows:

myenv\Scripts\activate

Mac/Linux:

source myenv/bin/activate
3. Install Dependencies
pip install -r requirements.txt

If requirements.txt is not available:

pip install django tensorflow numpy pandas
4. Apply Migrations
python manage.py makemigrations
python manage.py migrate
5. Create Superuser (Optional)
python manage.py createsuperuser
6. Run the Development Server
python manage.py runserver

The application will run at:

http://127.0.0.1:8000/
Signup Page

You can directly access the signup page using the link below:

http://127.0.0.1:5500/signup/

Copy and paste this link into your browser after running the server.
