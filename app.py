
import streamlit as st
import pandas as pd
import torch
import tempfile
from sentence_transformers import SentenceTransformer, util
from job_matcher import prepare_data
from utils import extract_keywords
from resume_parser import parse_resume

# 🔧 Config
st.set_page_config(page_title="JobGenie – AI Job Assistant", layout="wide")
st.markdown("<h1 style='text-align: center; color: #6a0dad;'>🧞‍♂ JobGenie – Your AI Job Assistant</h1>", unsafe_allow_html=True)

# 🧠 Model (cached)
@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
model = load_model()

# 📂 Data (cached)
@st.cache_data
def load_data():
    return prepare_data()
df = load_data()

# 📄 Resume Upload
st.sidebar.header("📄 Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"])

resume_query = ""
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    parsed_data = parse_resume(temp_file_path)

    if parsed_data:
        name = parsed_data.get("name", "N/A")
        email = parsed_data.get("email", "N/A")
        phone = parsed_data.get("phone", "N/A")
        skills = parsed_data.get("skills", [])
        experience = parsed_data.get("total_experience", "N/A")

        st.sidebar.success("✅ Resume parsed successfully!")
        st.sidebar.markdown(f"**📧 Email:** {email}")
        st.sidebar.markdown(f"**📞 Phone:** {phone}")
        st.sidebar.markdown(f"**🛠 Skills Extracted:**")
        st.sidebar.write(", ".join(skills) if skills else "No skills detected")
        st.sidebar.markdown(f"**⌛ Experience:** {experience} years")
        resume_query = " ".join(skills)

# ✅ Input bar (standard Streamlit)
user_input = st.text_input("Enter your query", value=resume_query, key="custom_input")
final_query = user_input.strip()

# 🔍 Intent Classifier
def classify_intent(text):
    if not isinstance(text, str):
        return 'job_search'
    text = text.lower()
    if any(w in text for w in ['job', 'opening', 'position', 'apply', 'career', 'developer', 'engineer', 'data', 'analyst', 'internship']):
        return 'job_search'
    elif any(w in text for w in ['trend', 'trending', 'popular', 'top']):
        return 'trending'
    elif any(w in text for w in ['advice', 'suggest', 'recommend', 'help']):
        return 'career_advice'
    elif any(w in text for w in ['analytics', 'dashboard', 'usage']):
        return 'analytics'
    return 'job_search'

# 🧠 Match Jobs
def compute_match_scores(query, jobs_df, top_n=10):
    query_embedding = model.encode(query, convert_to_tensor=True)
    jobs_df = jobs_df.copy()
    jobs_df["combined_text"] = jobs_df["jtitle"].fillna('') + " " + jobs_df["jdescription"].fillna('') + " " + jobs_df["jkeywords"].fillna('')
    job_embeddings = model.encode(jobs_df["combined_text"].tolist(), convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, job_embeddings)[0]
    jobs_df["match_score"] = cosine_scores.cpu().numpy()
    jobs_df = jobs_df.sort_values("match_score", ascending=False).head(top_n)
    jobs_df["match_score_percent"] = (jobs_df["match_score"] * 100).round(2)
    return jobs_df

def show_colored_bar(score):
    color = "🟩" if score >= 42 else "🟨" if score >= 37 else "🟥"
    return f"{color} {score:.2f}%"

# 🤖 Handle User Query
if final_query:
    st.chat_message("user").write(final_query)
    intent = classify_intent(final_query)

    if intent == 'job_search':
        result_df = compute_match_scores(final_query, df)
        if result_df.empty:
            st.chat_message("assistant").write("🤔 Hmm, I couldn't find anything for that. Try rephrasing or being more specific!")
        else:
            st.chat_message("assistant").markdown("🎯 **Here are some jobs that match your interest:**")
            for _, row in result_df.iterrows():
                st.markdown(f"""
                <div style="background-color:#fffafd; padding:18px; border-left: 5px solid #6a0dad;
                            border-radius:10px; margin-bottom:16px; box-shadow: 0 4px 10px rgba(106, 13, 173, 0.1); transition: 0.3s;">
                    <h4 style="margin-bottom:8px;">🧾 {row['jtitle']}</h4>
                    <p><strong>📍 Location:</strong> {row['jlocation']}</p>
                    <p><strong>📅 Posted On:</strong> {row['jpostingdate']}</p>
                    <p><strong>📚 Qualification:</strong> {row['jqualification']}</p>
                    <p><strong>🗒 Description:</strong> {row['jdescription'][:250]}...</p>
                    <p><strong>💡 Keywords:</strong> {row['jkeywords']}</p>
                    <p><strong>📊 Match Score:</strong> {show_colored_bar(row['match_score_percent'])}</p>
                </div>
                """, unsafe_allow_html=True)

            trending = extract_keywords(" ".join(result_df['jdescription'].fillna('').tolist()))
            st.markdown("📈 **Trending Keywords from matched jobs:**")
            st.write(", ".join(set(trending[:10])))

    elif intent == 'trending':
        keywords = extract_keywords(" ".join(df['jdescription'].fillna('').tolist()))
        st.chat_message("assistant").write("🔥 Trending job-related keywords:")
        st.write(", ".join(set(keywords[:10])))

    elif intent == 'career_advice':
        tips = [
            "📄 Tailor your resume to every job you apply for.",
            "🔗 Engage with professionals on LinkedIn.",
            "📈 Take certifications in AI, Cloud, or Cybersecurity.",
            "💬 Practice behavioral questions using STAR format.",
            "🧠 Stay updated with job market trends.",
            "🚀 Contribute to projects and open-source."
        ]
        st.chat_message("assistant").write("💡 Here's a tip for you:")
        st.write(tips[torch.randint(0, len(tips), (1,)).item()])

    elif intent == 'analytics':
        st.markdown("📊 **Analytics Dashboard**")
        top_keywords = pd.Series(" ".join(df["jkeywords"].fillna("")).split()).value_counts().head(10)
        top_locations = df["jlocation"].value_counts().head(10)
        top_titles = df["jtitle"].value_counts().head(10)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📌 Top Keyword", top_keywords.index[0])
            st.bar_chart(top_keywords)
        with col2:
            st.metric("🌍 Top Location", top_locations.index[0])
            st.bar_chart(top_locations)
        with col3:
            st.metric("💼 Top Job Title", top_titles.index[0])
            st.bar_chart(top_titles)

    else:
        st.chat_message("assistant").write("🧠 Try asking for job searches, trends, career advice, or show analytics!")
