import streamlit as st
from recommender import recommend_faculty

st.set_page_config(page_title="Faculty Finder", layout="wide")

# ---------- Advanced Styling ----------
st.markdown("""
<style>
/* Background Gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2f7 0%, #dbeafe 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.header {
    text-align:center;
    padding:40px 10px;
    background: linear-gradient(90deg, #1f4e79, #3b82f6);
    border-radius:12px;
    margin-bottom:30px;
    animation: fadeInDown 1s ease-in-out;
}
.header h1 {
    color:white;
    margin-bottom:5px;
}
.header p {
    color:#e0f2fe;
}

/* Search box */
.stTextInput>div>div>input {
    border-radius:8px;
    border:1px solid #93c5fd;
}

/* Grid Layout */
.grid-container {
    display:grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap:25px;
    animation: fadeIn 1.2s ease-in-out;
}

/* Card */
.card {
    background:white;
    border-radius:14px;
    padding:20px;
    box-shadow:0 8px 20px rgba(0,0,0,0.08);
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    min-height:340px;
    transition:all 0.3s ease;
    position:relative;
    overflow:hidden;
}
.card:hover {
    transform:translateY(-6px);
    box-shadow:0 12px 30px rgba(0,0,0,0.15);
}

/* Decorative gradient strip */
.card::before {
    content:"";
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:6px;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
}

/* Name */
.name {
    color:#1e3a8a;
    font-size:19px;
    font-weight:600;
}

/* Role */
.role {
    color:#64748b;
    font-size:14px;
    margin-bottom:8px;
}

/* Bio */
.bio {
    font-size:14px;
    color:#475569;
    margin:10px 0;
    flex-grow:1;
}

/* Email */
.email {
    font-size:14px;
    color:#334155;
}

/* View Profile Button (TEXT COLOR ONLY) */
.button-link {
    text-decoration:none;
    color:#2563eb;
    font-weight:600;
    font-size:14px;
    margin-top:12px;
    display:inline-block;
    transition:color 0.2s ease;
}
.button-link:hover {
    color:#1d4ed8;
    text-decoration:underline;
}

/* Animations */
@keyframes fadeIn {
    from {opacity:0;}
    to {opacity:1;}
}
@keyframes fadeInDown {
    from {opacity:0; transform:translateY(-20px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="header">
    <h1>🎓 Faculty Finder</h1>
    <p>Find the right faculty based on research, expertise, or academic background</p>
</div>
""", unsafe_allow_html=True)

# ---------- Search ----------
query = st.text_input("🔍 Search by name, research topic, or university")

if query:
    results = recommend_faculty(query)

    if results.empty:
        st.warning("No matching faculty found.")
    else:
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)

        for _, row in results.iterrows():
            bio_words = row["bio"].split()[:20]
            short_bio = " ".join(bio_words) + "..."

            profile_url = f"https://www.daiict.ac.in/{row['faculty_type'].lower().replace(' ', '-')}/{row['name'].lower().replace(' ', '-')}"

            st.markdown(f"""
                <div class="card">
                    <div>
                        <div class="name">{row['name']}</div>
                        <div class="role">{row['faculty_type']}</div>
                        <div><b>Education:</b> {row['education']}</div>
                        <div><b>Research:</b> {row['specialization_list']}</div>
                        <div class="bio">{short_bio}</div>
                        <div class="email">📧 {row['email']}</div>
                    </div>
                    <a class="button-link" href="{profile_url}" target="_blank">View Profile →</a>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
