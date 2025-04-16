import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "NewPassword",
    "database": "KSDC_Prod"
}

def fetch_jobs():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cleaned_job_posting")
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jobs
