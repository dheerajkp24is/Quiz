import streamlit as st

st.set_page_config(page_title="Quizminia", page_icon="❓", layout="centered")

# Center the logo using columns
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("logo.png", width=300)

st.markdown(
    "<h1 style='text-align:center;'>Welcome to Quizminia</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;'>Test Your Knowledge 🚀</h4>",
    unsafe_allow_html=True
)

st.markdown("""
<style>

/* ============================= */
/* MAIN BACKGROUND */
/* ============================= */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #ffffff;
}

/* ============================= */
/* SIDEBAR */
/* ============================= */
section[data-testid="stSidebar"] {
    background: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Sidebar radio buttons */
section[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Active selected sidebar item */
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
    background: #2563eb !important;
    padding: 8px;
    border-radius: 8px;
}

/* ============================= */
/* HEADINGS */
/* ============================= */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

/* ============================= */
/* RADIO BUTTONS */
/* ============================= */
div[role="radiogroup"] label {
    color: #ffffff !important;
    font-weight: 500;
}

/* ============================= */
/* SELECTBOX */
/* ============================= */
div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

/* Dropdown menu */
ul[role="listbox"] {
    background-color: #1e293b !important;
    color: #ffffff !important;
}

/* ============================= */
/* INPUT FIELDS */
/* ============================= */
input {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

/* ============================= */
/* BUTTONS */
/* ============================= */
.stButton>button {
    background: linear-gradient(45deg, #2563eb, #3b82f6);
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    background: linear-gradient(45deg, #1d4ed8, #2563eb);
    transform: scale(1.03);
}

/* ============================= */
/* GENERAL TEXT FIX */
/* ============================= */
html, body, [class*="css"] {
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)
import mysql.connector
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
from streamlit_autorefresh import st_autorefresh


# -------------------------------
# MySQL Connection (XAMPP)
# -------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="quiz_application"
)
cursor = conn.cursor()
# -------------------------------
# Generate PDF Certificate   👈 PASTE HERE
# -------------------------------
from reportlab.lib import colors
from reportlab.platypus import Image

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def generate_certificate(username, score, total, category, start_time, end_time):
    file_name = f"certificate_{username}.pdf"

    width = 2000
    height = 1414

    c = canvas.Canvas(file_name, pagesize=(width, height))

    # Background Image
    bg_image = os.path.join(os.getcwd(), "certificate.png")

    if os.path.exists(bg_image):
        c.drawImage(bg_image, 0, 0, width=width, height=height)

    # Font
    font_path = os.path.join(os.getcwd(), "EdwardianScriptITC.ttf")

    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("Edwardian", font_path))
        c.setFont("Edwardian", 140)
    else:
        c.setFont("Helvetica-Bold", 80)
    c.setFillColorRGB(1, 0.84, 0)  # gold color
    c.drawCentredString(width / 2, height / 2, username)

    # Username only
    c.drawCentredString(width / 2, height / 2, username)

    c.save()

    return file_name


# -------------------------------
# Session State
# -------------------------------
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "login_type" not in st.session_state:
    st.session_state.login_type = None
if "username" not in st.session_state:
    st.session_state.username = None
if "user_page" not in st.session_state:
    st.session_state.user_page = "home"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# -------------------------------
# Title
# -------------------------------
st.title("Quiz Application")

# =====================================================
# HOME PAGE
# =====================================================
if st.session_state.login_type is None:
    col1, col2, col3 = st.columns(3)
    if col1.button("Admin Login"):
        st.session_state.login_type = "admin"
    if col2.button("User Login"):
        st.session_state.login_type = "user"
    if col3.button("Register"):
        st.session_state.login_type = "register"

# =====================================================
# ADMIN LOGIN
# =====================================================
elif st.session_state.login_type == "admin" and st.session_state.username is None:
    st.subheader("Admin Login")
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")
    if st.button("Login as Admin"):
        cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result and result[2] == password:
            st.session_state.username = username
            st.success("Admin Login Successful")
            st.rerun()
        else:
            st.error("Invalid Admin Credentials")

# =====================================================
# USER LOGIN
# =====================================================
elif st.session_state.login_type == "user" and st.session_state.username is None:
    st.subheader("User Login")
    username = st.text_input("User Username")
    password = st.text_input("User Password", type="password")
    if st.button("Login as User"):
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()
        if user:
            st.session_state.username = username
            st.success("User Login Successful")
            st.rerun()
        else:
            st.error("Invalid User Credentials")

# =====================================================
# USER REGISTRATION
# =====================================================
elif st.session_state.login_type == "register":
    st.subheader("User Registration")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register User"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif new_username == "" or new_password == "":
            st.warning("Please fill all fields")
        else:
            cursor.execute("SELECT * FROM users WHERE username=%s", (new_username,))
            existing_user = cursor.fetchone()
            if existing_user:
                st.error("Username already exists")
            else:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (new_username, new_password)
                )
                conn.commit()
                st.success("Registration Successful! Please login.")
                st.session_state.login_type = None
                st.rerun()

# =====================================================
# ADMIN DASHBOARD
# =====================================================
elif st.session_state.login_type == "admin":
    st.success(f"Welcome Admin: {st.session_state.username}")
    menu = st.sidebar.selectbox(
        "Admin Menu",
        ["Add Question", "View Questions", "Edit/Delete Question", "Leaderboard"]
    )

    if menu == "Add Question":
        st.subheader("➕ Add New Question")
        st.info(f"Questions Added This Session: {st.session_state.question_count}")
        with st.form("add_question_form"):
            category = st.selectbox(
                "Select Category",
                ["General Knowledge", "Physics", "Chemistry", "Biology", "Computer Basics", "History"]
            )
            q = st.text_input("Enter Question")
            col1, col2 = st.columns(2)
            with col1:
                o1 = st.text_input("Option 1")
                o2 = st.text_input("Option 2")
            with col2:
                o3 = st.text_input("Option 3")
                o4 = st.text_input("Option 4")
            correct_option = st.selectbox(
                "Select Correct Option",
                ["Option 1", "Option 2", "Option 3", "Option 4"]
            )
            submitted = st.form_submit_button("Save Question")
        if submitted:
            if q and o1 and o2 and o3 and o4:
                option_map = {"Option 1": o1, "Option 2": o2, "Option 3": o3, "Option 4": o4}
                ans = option_map[correct_option]
                cursor.execute(
                    "INSERT INTO questions (question, option1, option2, option3, option4, answer, category) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (q, o1, o2, o3, o4, ans, category)
                )
                conn.commit()
                st.session_state.question_count += 1
                st.success("✅ Question Added Successfully!")
                st.rerun()
            else:
                st.warning("⚠ Please fill all fields")

    elif menu == "View Questions":
        cursor.execute("SELECT * FROM questions")
        data = cursor.fetchall()
        for row in data:
            st.write(f"Q: {row[1]}")
            st.write(f"Correct Answer: {row[6]}")
            st.write("-------------------")

    elif menu == "Edit/Delete Question":
        st.subheader("✏ Edit / Delete Question")
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        if questions:
            question_dict = {f"Q{q[0]} - {q[1]}": q for q in questions}
            selected = st.selectbox(
                "Select Question to Edit/Delete",
                list(question_dict.keys())
            )
            selected_q = question_dict[selected]
            new_question = st.text_input("Question", selected_q[1])
            col1, col2 = st.columns(2)
            with col1:
                new_o1 = st.text_input("Option 1", selected_q[2])
                new_o2 = st.text_input("Option 2", selected_q[3])
            with col2:
                new_o3 = st.text_input("Option 3", selected_q[4])
                new_o4 = st.text_input("Option 4", selected_q[5])
            correct_option = st.selectbox("Correct Option", ["Option 1", "Option 2", "Option 3", "Option 4"])
            option_map = {"Option 1": new_o1, "Option 2": new_o2, "Option 3": new_o3, "Option 4": new_o4}
            if st.button("Update Question"):
                new_answer = option_map[correct_option]
                cursor.execute(
                    "UPDATE questions SET question=%s, option1=%s, option2=%s, option3=%s, option4=%s, answer=%s WHERE id=%s",
                    (new_question, new_o1, new_o2, new_o3, new_o4, new_answer, selected_q[0])
                )
                conn.commit()
                st.success("✅ Question Updated Successfully!")
                st.rerun()
            if st.button("Delete Question"):
                cursor.execute("DELETE FROM questions WHERE id=%s", (selected_q[0],))
                conn.commit()
                st.success("🗑 Question Deleted Successfully!")
                st.rerun()
        else:
            st.warning("No questions available.")

    elif menu == "Leaderboard":
        st.subheader("🏆 Leaderboard")

        cursor.execute("""
            SELECT username, MAX(score) AS best_score
            FROM scores
            GROUP BY username
            ORDER BY best_score DESC
        """)
        leaderboard = cursor.fetchall()

        if leaderboard:

            medals = ["🥇", "🥈", "🥉"]

            for i, row in enumerate(leaderboard):
                username = row[0]
                score = row[1]

                # 🏆 Rank 1 Animated Trophy
                if i == 0:
                    st.markdown("""
                    <style>
                    @keyframes bounce {
                        0%, 100% { transform: translateY(0); }
                        50% { transform: translateY(-10px); }
                    }
                    .trophy {
                        font-size: 50px;
                        animation: bounce 1s infinite;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(90deg, gold, orange);
                            padding:15px;
                            border-radius:15px;
                            text-align:center;
                            margin-bottom:10px;">
                            <div class="trophy">🏆</div>
                            <h2>{medals[0]} {username}</h2>
                            <h3>{score} Points</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # 🥈 2nd and 🥉 3rd Place Trophy Cards
                elif i < 3:

                    trophy_icon = "🥈" if i == 1 else "🥉"

                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(90deg,#1e293b,#334155);
                            padding:15px;
                            border-radius:15px;
                            text-align:center;
                            margin-bottom:10px;
                            border:2px solid #3b82f6;
                        ">
                            <div style="font-size:40px;">{trophy_icon}</div>
                            <h3>{username}</h3>
                            <p>{score} Points</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Other Ranks
                else:
                    st.write(f"{i + 1}. {username} - {score} Points")

        else:
            st.warning("No scores available yet.")



# =====================================================
# USER DASHBOARD
# =====================================================
elif st.session_state.login_type == "user":
    st.success(f"Welcome User: {st.session_state.username}")

    if st.session_state.user_page == "home":
        st.title("🏠 Welcome to Quizminia")
        st.markdown("""
            ### 🎯 About Quizminia
            - Improve knowledge
            - Practice category-wise questions
            - Prepare for exams
            - Track performance
            Click Start Quiz to begin!
        """)
        if st.button("🚀 Start Quiz"):
            st.session_state.user_page = "category"
            st.rerun()

    elif st.session_state.user_page == "category":
        st.subheader("📚 Select Category")
        category = st.selectbox(
            "Choose Category",
            ["General Knowledge", "Physics", "Chemistry", "Biology", "Computer Basics", "History"]
        )
        if st.button("Start Now"):
            st.session_state.balloon_shown = False
            st.session_state.selected_category = category
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.q_start_time = time.time()
            st.session_state.user_page = "quiz"
            st.rerun()

    elif st.session_state.user_page == "quiz":
        # Refresh timer only while quiz is running
        cursor.execute(
            "SELECT * FROM questions WHERE category=%s",
            (st.session_state.selected_category,)
        )
        questions = cursor.fetchall()
        if st.session_state.current_q < len(questions):
            st_autorefresh(interval=1000, key="quiz_timer")
        if not questions:
            st.warning("No questions in this category.")
            st.stop()

        total_questions = len(questions)
        question_time = 15  # seconds per question

        # If quiz finished
        if st.session_state.current_q >= total_questions:
            cursor.execute(
                "INSERT INTO scores (username, score, total) VALUES (%s, %s, %s)",
                (st.session_state.username, st.session_state.score, total_questions)
            )
            conn.commit()

            st.success("🎉 Quiz Finished!")
            st.success(f"Your Final Score: {st.session_state.score}/{total_questions}")
            if "balloon_shown" not in st.session_state:
                st.balloons()
                st.session_state.balloon_shown = True

            # Show certificate button
            # 🎯 Minimum passing condition
            min_marks = int(total_questions * 0.75)

            if st.session_state.score >= min_marks:

                st.success("🎉 You are eligible for certificate!")

                # Generate Certificate Button
                # Generate certificate
                if "certificate_ready" not in st.session_state:
                    st.session_state.certificate_ready = False

                if st.button("🎓 Generate Certificate"):
                    pdf_file = generate_certificate(
                        username=st.session_state.username,
                        score=st.session_state.score,
                        total=total_questions,
                        category=st.session_state.selected_category,
                        start_time=datetime.fromtimestamp(st.session_state.q_start_time),
                        end_time=datetime.now()
                    )

                    st.session_state.certificate_file = pdf_file
                    st.session_state.certificate_ready = True

                if st.session_state.certificate_ready:
                    with open(st.session_state.certificate_file, "rb") as f:
                        st.download_button(
                            "⬇ Download Certificate",
                            data=f.read(),
                            file_name=st.session_state.certificate_file,
                            mime="application/pdf"
                        )

            else:
                st.error(f"❌ You need at least {min_marks}/{total_questions} to get certificate.")

            # 2️⃣ Back to Home Button
            if st.button("🏠 Back to Home"):
                st.session_state.user_page = "home"
                st.session_state.selected_category = None
                del st.session_state.current_q
                del st.session_state.score
                st.rerun()

            st.stop()

        # Current question
        q = questions[st.session_state.current_q]

        # TIMER
        elapsed = time.time() - st.session_state.q_start_time
        remaining = question_time - elapsed
        progress_percentage = max(0, int((remaining / question_time) * 100))
        color = "#28a745" if progress_percentage > 60 else "#fd7e14" if progress_percentage > 30 else "#dc3545"

        st.markdown(f"### Q{st.session_state.current_q + 1}. {q[1]}")

        # Disable answer if time is over
        disabled = remaining <= 0
        answer = st.radio(
            "Select your answer:",
            [q[2], q[3], q[4], q[5]],
            key=f"question_{q[0]}",
            disabled=disabled
        )

        st.markdown(f"""
            <div style="
                width: 100%;
                background-color: #e0e0e0;
                border-radius: 10px;
                height: 20px;">
                <div style="
                    width: {progress_percentage}%;
                    background-color: {color};
                    height: 100%;
                    border-radius: 10px;
                    transition: width 1s linear;">
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.caption(f"Time Remaining: {int(remaining)} seconds")

        # Auto move to next question when timer ends
        if remaining <= 0:
            selected_answer = st.session_state.get(f"question_{q[0]}", None)
            if selected_answer == q[6]:
                st.session_state.score += 1
            st.session_state.current_q += 1
            st.session_state.q_start_time = time.time()
            st.rerun()

        # NEXT BUTTON (manual)
        if st.button("Next ➡", disabled=disabled):
            selected_answer = st.session_state.get(f"question_{q[0]}", None)
            if selected_answer == q[6]:
                st.session_state.score += 1
            st.session_state.current_q += 1
            st.session_state.q_start_time = time.time()
            st.rerun()

# =====================================================
# LOGOUT
# =====================================================
if st.session_state.username is not None:
    if st.sidebar.button("Logout"):
        st.session_state.login_type = None
        st.session_state.username = None
        st.session_state.user_page = "home"
        st.session_state.selected_category = None
        st.rerun()
