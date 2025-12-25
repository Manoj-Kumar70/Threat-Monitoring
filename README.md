# Clone the repository
git clone <repository-url>
cd threat-monitoring

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Run the server
python manage.py runserver
http://127.0.0.1:8000/api/dashboard/


API Endpoints List

POST /api/register       Register new user
POST /api/token          Login user
POST	/api/events/	     Admin	Ingest security event
GET	/api/events/	       Admin	List all events
POST	/api/alerts/	     Admin	Ingest security alert
GET	/api/alerts/	       Admin	List all alerts
PATCH	/api/alerts/{id}/	 Admin	Update alert status
