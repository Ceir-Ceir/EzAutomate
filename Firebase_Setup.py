import firebase_admin
from firebase_admin import credentials, firestore

# Path to the service account key JSON file
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"

# Initialize Firebase app
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Helper functions for Firestore operations
def get_users():
    """
    Fetch all users from the Firestore 'users' collection.
    """
    users_ref = db.collection('users')
    users = users_ref.stream()
    return [user.to_dict() for user in users]

def get_jobs():
    """
    Fetch all jobs from the Firestore 'jobs' collection.
    """
    jobs_ref = db.collection('jobs')
    jobs = jobs_ref.stream()
    return [job.to_dict() for job in jobs]

def add_job(job_data):
    """
    Add a new job to the Firestore 'jobs' collection.
    """
    jobs_ref = db.collection('jobs')
    jobs_ref.add(job_data)
