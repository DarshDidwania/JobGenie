# JobGenie - Your AI Job Assistant 🧞‍♂️

JobGenie is an **AI-powered job search assistant** that helps users find their perfect job with ease.  
It allows you to **upload your resume, perform semantic job searches, discover trending job market keywords, and get personalized career advice** — all from a single intuitive interface.  

The application is built using **Streamlit** and leverages **Sentence Transformers** for powerful semantic search capabilities.

---

## ✨ Features

- 📄 **Resume Parsing**: Automatically extracts your name, email, phone number, and skills from PDF and DOCX resumes.  
- 🔍 **Semantic Job Search**: Find jobs that semantically match your query, rather than just keyword matches.  
- 💡 **Career Advice**: Get helpful tips on resume building, networking, and staying updated with market trends.  
- 📊 **Trending Keywords**: View the most popular keywords from job descriptions to help tailor your resume and search.  
- 📈 **Analytics Dashboard**: Visualize key job market data, including top keywords, locations, and job titles.  

---

## 🚀 Installation and Setup

1. Clone the Repository

```bash
git clone https://github.com/darshdidwania/jobgenie.git
cd jobgenie
```
2. Set Up the Python Environment
Install the required Python packages:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
3. Database Configuration
The application connects to a MySQL database to fetch job listings.
Update the DB_CONFIG dictionary in db.py with your database credentials:

```python
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "NewPassword",
    "database": "KSDC_Prod"
}
```
⚠️ The application expects a table named cleaned_job_posting to exist.

#### ▶️ Running the Application
Option A: Run Locally
Simply run the Streamlit app from your terminal:

```bash
streamlit run app.py
```
The application will open in your browser at http://localhost:8501

Option B: Run with Docker
You can also build and run the application inside a Docker container.

Build the Docker image:

```bash
docker build -t jobgenie .
```
Run the container:

```bash
docker run -p 8501:8501 jobgenie
```
The app will be accessible at http://localhost:8501

#### 📌 Tech Stack
Frontend: Streamlit

Backend: Python, FastAPI (for services)
Database: MySQL
AI/ML: Sentence Transformers, spaCy
Containerization: Docker

