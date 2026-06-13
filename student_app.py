import json
import streamlit as st
from abc import ABC, abstractmethod
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SchoolOS",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --ink: #0f0f0f;
    --cream: #f5f0e8;
    --accent: #e8572a;
    --accent2: #2a7ae8;
    --muted: #8a8680;
    --card: #ffffff;
    --border: #e2ddd6;
    --success: #2d9e6b;
    --danger: #d94040;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: var(--cream) !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.4rem 0;
}
[data-testid="stSidebar"] [data-baseweb="radio"] {
    gap: 0.3rem;
}

/* Main header */
.main-header {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    letter-spacing: -0.03em;
    line-height: 1;
    color: var(--ink);
    margin-bottom: 0;
}
.main-sub {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.3rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.accent-dot {
    color: var(--accent);
}

/* Section title */
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    border-left: 4px solid var(--accent);
    padding-left: 0.75rem;
    margin-bottom: 1.5rem;
    color: var(--ink);
}

/* Cards */
.stat-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}
.stat-number {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    line-height: 1;
    color: var(--ink);
}
.stat-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
}

/* Student / Teacher rows */
.person-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.person-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
}
.person-meta {
    font-size: 0.82rem;
    color: var(--muted);
    margin-top: 0.1rem;
}
.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.badge-student { background: #fff3ee; color: var(--accent); border: 1px solid #f5c9b8; }
.badge-teacher { background: #eef3ff; color: var(--accent2); border: 1px solid #b8c8f5; }
.badge-avg { background: #eefaf4; color: var(--success); border: 1px solid #b8e8d0; }

/* Divider */
.divider {
    border: none;
    border-top: 1.5px solid var(--border);
    margin: 1.5rem 0;
}

/* Form styling */
[data-testid="stForm"] {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 2rem 2rem 1.5rem;
}

/* Input overrides */
.stTextInput input, .stNumberInput input {
    border-radius: 8px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(232,87,42,0.12) !important;
}

/* Button */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    background: var(--ink) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.6rem !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
}

/* Success / Error messages */
.msg-success {
    background: #eefaf4;
    border-left: 4px solid var(--success);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-weight: 500;
    color: #1a6b47;
    margin: 0.8rem 0;
}
.msg-error {
    background: #fff0f0;
    border-left: 4px solid var(--danger);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-weight: 500;
    color: #8b1f1f;
    margin: 0.8rem 0;
}

/* Grade pill */
.grade-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #f5f0e8;
    border: 1.5px solid var(--border);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.83rem;
    font-weight: 600;
    margin: 0.2rem;
}

/* Top rule */
.top-rule {
    width: 100%;
    border: none;
    border-top: 3px solid var(--ink);
    margin-bottom: 1.8rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Data Layer ─────────────────────────────────────────────────────────────
DATABASE = "school_data.json"

def load_data():
    p = Path(DATABASE)
    if p.exists():
        content = p.read_text()
        if content.strip():
            return json.loads(content)
    return {"students": [], "teachers": []}

def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

def validate_email(email):
    return "@" in email and "." in email

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 2rem 0;'>
        <div style='font-family: Syne, sans-serif; font-weight: 800; font-size: 1.6rem; letter-spacing: -0.02em;'>
            School<span style='color: #e8572a;'>OS</span>
        </div>
        <div style='font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.5; margin-top: 0.2rem;'>
            Management System
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["Dashboard", "Register Student", "Register Teacher",
         "Add Grade", "Student Details", "Teacher Details"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #333; margin: 2rem 0 1.5rem;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.75rem; opacity:0.4; text-transform:uppercase; letter-spacing:0.08em;'>
        {len(data['students'])} Students · {len(data['teachers'])} Teachers
    </div>
    """, unsafe_allow_html=True)


# ─── DASHBOARD ──────────────────────────────────────────────────────────────
if nav == "Dashboard":
    st.markdown("""
    <div class='main-header'>School<span class='accent-dot'>OS</span></div>
    <div class='main-sub'>Management System</div>
    <hr class='top-rule' style='margin-top:1.2rem;'>
    """, unsafe_allow_html=True)

    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    all_grades = [m for s in data['students'] for m in s['grades'].values()]
    avg_school = sum(all_grades) / len(all_grades) if all_grades else 0

    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{len(data['students'])}</div>
            <div class='stat-label'>Students</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{len(data['teachers'])}</div>
            <div class='stat-label'>Teachers</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        total_grades = sum(len(s['grades']) for s in data['students'])
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{total_grades}</div>
            <div class='stat-label'>Grades Recorded</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number' style='color:#e8572a;'>{avg_school:.1f}</div>
            <div class='stat-label'>School Average</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<div class='section-title'>Recent Students</div>", unsafe_allow_html=True)
        if data['students']:
            for s in data['students'][-5:][::-1]:
                grades = s['grades']
                avg = sum(grades.values()) / len(grades) if grades else None
                avg_txt = f"{avg:.1f}" if avg is not None else "—"
                st.markdown(f"""
                <div class='person-card'>
                    <div>
                        <div class='person-name'>{s['name']}</div>
                        <div class='person-meta'>Roll #{s['roll_no']} · Age {s['age']}</div>
                    </div>
                    <div>
                        <span class='badge badge-avg'>avg {avg_txt}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#8a8680; font-size:0.9rem;'>No students registered yet.</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-title'>Faculty</div>", unsafe_allow_html=True)
        if data['teachers']:
            for t in data['teachers'][-5:][::-1]:
                st.markdown(f"""
                <div class='person-card'>
                    <div>
                        <div class='person-name'>{t['name']}</div>
                        <div class='person-meta'>ID: {t['emp_id']} · Age {t['age']}</div>
                    </div>
                    <span class='badge badge-teacher'>{t['subject']}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#8a8680; font-size:0.9rem;'>No teachers registered yet.</div>", unsafe_allow_html=True)


# ─── REGISTER STUDENT ───────────────────────────────────────────────────────
elif nav == "Register Student":
    st.markdown("<div class='main-header'>Register <span class='accent-dot'>Student</span></div>", unsafe_allow_html=True)
    st.markdown("<hr class='top-rule' style='margin-top:1rem;'>", unsafe_allow_html=True)

    with st.form("reg_student"):
        st.markdown("<div class='section-title'>Student Information</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
        with c2:
            age = st.number_input("Age", min_value=5, max_value=30, value=16)
            roll_no = st.text_input("Roll Number")

        submitted = st.form_submit_button("Register Student →")

    if submitted:
        if not name or not email or not roll_no:
            st.markdown("<div class='msg-error'>⚠ Please fill in all fields.</div>", unsafe_allow_html=True)
        elif not validate_email(email):
            st.markdown("<div class='msg-error'>⚠ Invalid email address.</div>", unsafe_allow_html=True)
        elif any(s['roll_no'] == roll_no for s in data['students']):
            st.markdown("<div class='msg-error'>⚠ A student with this roll number already exists.</div>", unsafe_allow_html=True)
        else:
            data['students'].append({
                "name": name, "age": age,
                "email": email, "roll_no": roll_no, "grades": {}
            })
            save_data(data)
            st.markdown(f"<div class='msg-success'>✓ {name} has been registered successfully.</div>", unsafe_allow_html=True)


# ─── REGISTER TEACHER ───────────────────────────────────────────────────────
elif nav == "Register Teacher":
    st.markdown("<div class='main-header'>Register <span class='accent-dot'>Teacher</span></div>", unsafe_allow_html=True)
    st.markdown("<hr class='top-rule' style='margin-top:1rem;'>", unsafe_allow_html=True)

    with st.form("reg_teacher"):
        st.markdown("<div class='section-title'>Teacher Information</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            subject = st.text_input("Subject")
        with c2:
            age = st.number_input("Age", min_value=21, max_value=70, value=35)
            emp_id = st.text_input("Employee ID")

        submitted = st.form_submit_button("Register Teacher →")

    if submitted:
        if not name or not email or not emp_id or not subject:
            st.markdown("<div class='msg-error'>⚠ Please fill in all fields.</div>", unsafe_allow_html=True)
        elif not validate_email(email):
            st.markdown("<div class='msg-error'>⚠ Invalid email address.</div>", unsafe_allow_html=True)
        elif any(t['emp_id'] == emp_id for t in data['teachers']):
            st.markdown("<div class='msg-error'>⚠ A teacher with this Employee ID already exists.</div>", unsafe_allow_html=True)
        else:
            data['teachers'].append({
                "name": name, "age": age,
                "email": email, "subject": subject, "emp_id": emp_id
            })
            save_data(data)
            st.markdown(f"<div class='msg-success'>✓ {name} has been registered successfully.</div>", unsafe_allow_html=True)


# ─── ADD GRADE ──────────────────────────────────────────────────────────────
elif nav == "Add Grade":
    st.markdown("<div class='main-header'>Add <span class='accent-dot'>Grade</span></div>", unsafe_allow_html=True)
    st.markdown("<hr class='top-rule' style='margin-top:1rem;'>", unsafe_allow_html=True)

    if not data['students']:
        st.markdown("<div class='msg-error'>⚠ No students registered yet. Register a student first.</div>", unsafe_allow_html=True)
    else:
        student_options = {f"{s['name']} (Roll #{s['roll_no']})": s['roll_no'] for s in data['students']}

        with st.form("add_grade"):
            st.markdown("<div class='section-title'>Grade Entry</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                selected = st.selectbox("Select Student", list(student_options.keys()))
            with c2:
                subject = st.text_input("Subject")
            with c3:
                marks = st.number_input("Marks", min_value=0.0, max_value=100.0, value=75.0, step=0.5)

            submitted = st.form_submit_button("Save Grade →")

        if submitted:
            if not subject:
                st.markdown("<div class='msg-error'>⚠ Subject name is required.</div>", unsafe_allow_html=True)
            else:
                roll_no = student_options[selected]
                for s in data['students']:
                    if s['roll_no'] == roll_no:
                        s['grades'][subject] = marks
                        save_data(data)
                        st.markdown(f"<div class='msg-success'>✓ Grade saved — {subject}: {marks}</div>", unsafe_allow_html=True)
                        break


# ─── STUDENT DETAILS ────────────────────────────────────────────────────────
elif nav == "Student Details":
    st.markdown("<div class='main-header'>Student <span class='accent-dot'>Details</span></div>", unsafe_allow_html=True)
    st.markdown("<hr class='top-rule' style='margin-top:1rem;'>", unsafe_allow_html=True)

    if not data['students']:
        st.markdown("<div class='msg-error'>⚠ No students registered yet.</div>", unsafe_allow_html=True)
    else:
        student_options = {f"{s['name']} (Roll #{s['roll_no']})": s for s in data['students']}
        selected = st.selectbox("Select Student", list(student_options.keys()))
        s = student_options[selected]
        grades = s['grades']
        avg = sum(grades.values()) / len(grades) if grades else 0

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number' style='font-size:1.8rem;'>{s['name']}</div>
                <div class='stat-label'>Full Name</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number'>{s['roll_no']}</div>
                <div class='stat-label'>Roll Number</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number'>{s['age']}</div>
                <div class='stat-label'>Age</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number' style='color:#e8572a;'>{avg:.1f}</div>
                <div class='stat-label'>Average Score</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.85rem; color:#8a8680;'>📧 {s['email']}</div>", unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Grades</div>", unsafe_allow_html=True)
        if grades:
            cols = st.columns(min(len(grades), 4))
            for idx, (subj, score) in enumerate(grades.items()):
                with cols[idx % 4]:
                    color = "#2d9e6b" if score >= 75 else "#e8572a" if score < 50 else "#2a7ae8"
                    st.markdown(f"""
                    <div class='stat-card' style='text-align:center;'>
                        <div class='stat-number' style='color:{color};'>{score:.0f}</div>
                        <div class='stat-label'>{subj}</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#8a8680;'>No grades recorded yet.</div>", unsafe_allow_html=True)


# ─── TEACHER DETAILS ────────────────────────────────────────────────────────
elif nav == "Teacher Details":
    st.markdown("<div class='main-header'>Teacher <span class='accent-dot'>Details</span></div>", unsafe_allow_html=True)
    st.markdown("<hr class='top-rule' style='margin-top:1rem;'>", unsafe_allow_html=True)

    if not data['teachers']:
        st.markdown("<div class='msg-error'>⚠ No teachers registered yet.</div>", unsafe_allow_html=True)
    else:
        teacher_options = {f"{t['name']} — {t['subject']}": t for t in data['teachers']}
        selected = st.selectbox("Select Teacher", list(teacher_options.keys()))
        t = teacher_options[selected]

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number' style='font-size:1.8rem;'>{t['name']}</div>
                <div class='stat-label'>Full Name</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number'>{t['emp_id']}</div>
                <div class='stat-label'>Employee ID</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number'>{t['age']}</div>
                <div class='stat-label'>Age</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-number' style='font-size:1.4rem; color:#2a7ae8;'>{t['subject']}</div>
                <div class='stat-label'>Subject</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.85rem; color:#8a8680;'>📧 {t['email']}</div>", unsafe_allow_html=True)