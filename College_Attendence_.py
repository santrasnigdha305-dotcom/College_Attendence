import os
import streamlit as st
import pymysql

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Student Attendance System",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>

/* ===== Main Background ===== */
section[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1f2d1a, #2f3e1f, #3f4f2a) !important;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141d10, #1f2d1a) !important;
}

/* ===== Text ===== */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: #e6f0dc !important;
}

/* ===== Inputs ===== */
input, textarea, select {
    background-color: #141d10 !important;
    color: #f0f5e6 !important;
    border: 1px solid #a3b18a !important;
    border-radius: 6px !important;
}

/* ===== Buttons ===== */
button {
    background: linear-gradient(90deg, #6b8e23, #7c9a2f, #8fae3c) !important;
    color: #0f1a0a !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    border: none !important;
}

/* ===== Button Hover ===== */
button:hover {
    background: linear-gradient(90deg, #556b2f, #6b8e23, #7c9a2f) !important;
    color: #ffffff !important;
}

/* ===== Alerts ===== */
div[data-testid="stAlert"] {
    background-color: #141d10 !important;
    color: #e6f0dc !important;
    border: 1px solid #a3b18a !important;
}

</style>
""", unsafe_allow_html=True)





# --------------------------------------------------
# COVER IMAGE (OPTIONAL)
# --------------------------------------------------

image_path = "C:/Users/santr/Desktop/Data_base/college.webp"
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("Cover image not found")



# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

try:
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="collage_attendance"
    )
    cursor = con.cursor()

    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            grade VARCHAR(20)
        )
    """)

    # Create attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            date DATE,
            status ENUM('Present','Absent'),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    con.commit()
    cursor.close()

    st.success("Database connected successfully!")

except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()



# --------------------------------------------------
# SIDEBAR MENU
# --------------------------------------------------

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Add Students",
        "Student Details",
        "Attendance",
        "Attendance Report",
        "Delete Student"
    ]
)



# --------------------------------------------------
# HOME PAGE (COVER PAGE)
# --------------------------------------------------

if menu == "Home":
    st.title("College Attendance System")

    st.write("Welcome to the College Attendance System")
    st.write("Built using **Python, Streamlit & MySQL**")

    st.image(
        r"C:\Users\santr\Desktop\Data_base\Attendence.jpeg",
        caption="College Attendance System",
        width=400
    )

    st.subheader("Features")
    st.write("""
    ✔ Add New Students  
    ✔ View Student Details  
    ✔ Mark Attendance  
    ✔ View Attendance Reports  
    ✔ Delete Student   
    """)
    st.write(
        "This smart attendance management system helps teachers "
        "to manage student records and attendance efficiently. "
        "It reduces paperwork and provides quick access to attendance reports."
    )
    
    st.write("student attendance management made easy!")
    


# --------------------------------------------------
# ADD STUDENTS
# ------------------------------------------------__
elif menu == "Add Students":
    st.title("Add New Student")

    name = st.text_input("Student Name")
    age = st.number_input("Student Age", min_value=1, max_value=100)
    grade = st.text_input("Student Grade")
    
    if st.button("Add Student"):
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
            (name, age, grade)
        )
        con.commit()
        cursor.close()
        st.success("Student added successfully!")
        



# --------------------------------------------------
# STUDENT DETAILS
# --------------------------------------------------

elif menu == "Student Details":
    st.title("Student Details")

    cursor = con.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        st.info("No students found.")
    else:
        for row in rows:
            st.write(
                f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Grade: {row[3]}"
            )



# --------------------------------------------------
# ATTENDANCE
# --------------------------------------------------

elif menu == "Attendance":
    st.title("Mark Attendance")

    cursor = con.cursor()
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    for i, student in enumerate(students, start=1):
        student_id = student[0]
        student_name = student[1]

        st.subheader(f"{i}. 👤 {student_name}")

        status = st.radio(
            "Status",
            ["Present", "Absent"],
            key=f"status_{student_id}"
        )

        if st.button("Submit Attendance", key=f"btn_{student_id}"):
            cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (%s, CURDATE(), %s)",
                (student_id, status)
            )
            con.commit()
            st.success(f"{student_name} marked {status}")

        st.divider()

    cursor.close()




# --------------------------------------------------
# ATTENDANCE REPORT
# --------------------------------------------------

elif menu == "Attendance Report":
    st.title("Attendance Report")

    cursor = con.cursor()
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        st.info("No attendance records found.")
    else:
        for row in rows:
            st.write(
                f"ID: {row[0]} | Student ID: {row[1]} | Date: {row[2]} | Status: {row[3]}"
            )



# --------------------------------------------------
# DELETE STUDENT (FIXED)
# --------------------------------------------------



elif menu == "Delete Student":
    st.title("Delete Student Record")

    cursor = con.cursor()
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    if not students:
        st.warning("No students available to delete.")
    else:
        selected_student = st.selectbox(
            "Select Student to Delete",
            students,
            format_func=lambda x: f"ID {x[0]} - {x[1]}"
        )

        student_id = selected_student[0]

        if st.button("Delete Student"):
            cursor.execute(
                "DELETE FROM attendance WHERE student_id = %s",
                (student_id,)
            )

            cursor.execute(
                "DELETE FROM students WHERE id = %s",
                (student_id,)
            )

            con.commit()
            cursor.close()

            st.success("Student deleted successfully!")
            st.rerun()



# ---------------------CLOSE CONNECTION ON EXIST--------------------------------
#----------------------------------------------------------------------------


import streamlit as st
import mysql.connector

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="attendance"
    )

# Clear cache when needed
st.cache_resource.clear()


# --------------------------------------------------