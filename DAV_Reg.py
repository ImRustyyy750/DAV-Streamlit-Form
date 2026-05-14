import streamlit as st
import os
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Inquiry Form - DAV Public School",
    page_icon="📝",
    layout="centered"
)

st.markdown("""
<style>

.stButton > button {
    background-color: #1f77b4;
    color: white;
    border-radius: 12px;
    height: 45px;
    width: 100%;
    font-size: 16px;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: red;
    color: white;
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

left_col, right_col = st.columns([1, 1])

with left_col:
    st.title("Welcome to Excellence at DAV Public School")
    st.markdown("""
    **Empowering young minds with knowledge, discipline, creativity,  
    and values for a brighter tomorrow.**
    """)
    
    st.markdown("""
<div style="
background-color:#e8f0fe;
padding:12px;
border-radius:15px;
width:fit-content;
font-weight:bold;
color:#0b3d91;
margin-top:10px;
">
🎓 Admissions Open 2026-27
</div>
""", unsafe_allow_html=True)

with right_col:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwmH1vNzArzjmKqO_H_ZAY3fxw0yJIVmHhjQ&s",
        width=380
    )

st.divider()

# School Details

st.subheader("About School")

st.markdown("""
At DAV Public School, we believe education is the foundation of a successful and meaningful life.

Our mission is to nurture confident, compassionate, and responsible individuals through academic excellence and holistic development.

With experienced faculty, modern infrastructure, and a student-centered approach, we create an environment where every child can discover their true potential.
""")

st.divider()

# Main Part

st.subheader("Student Enquiry Form")

st.write("Please fill in the details below. Our team will contact you soon.")

name = st.text_input("Full Name")

col1, col2 = st.columns(2)

with col1:
    student_class = st.selectbox(
        "Class",
        [str(i) for i in range(1, 13)]
    )

with col2:
    section = st.selectbox(
        "Section",
        ["A", "B", "C", "D", "E", "F"]
    )

gender = st.radio(
    "Gender",
    ["Male", "Female"],
    horizontal=True
)

mobile = st.text_input("Mobile Number")
email = st.text_input("Email Address")
message = st.text_area("Message")

# ---------------- SUBMIT ----------------

if st.button("Submit Enquiry"):

    # Validation
    if name.strip() == "":
        st.error("Name cannot be empty.")

    elif mobile.strip() == "":
        st.error("Mobile number cannot be empty.")

    elif not mobile.isdigit():
        st.error("Mobile number should contain only digits.")

    elif len(mobile) != 10:
        st.error("Mobile number must be 10 digits.")

    elif email.strip() == "":
        st.error("Email cannot be empty.")

    elif message.strip() == "":
        st.error("Message cannot be empty.")

    else:

        filename = "student_enquiries.csv"

        # New form data
        data = {
            "Name": [name],
            "Class": [student_class],
            "Section": [section],
            "Gender": [gender],
            "Mobile": [mobile],
            "Email": [email],
            "Message": [message],
            "Date": [date.today()]
        }

        new_df = pd.DataFrame(data)

        # Check for any duplicates, strip and lower to avoid space and case issues

        if os.path.exists(filename):

            existing_df = pd.read_csv(filename)

            duplicate = (
                (existing_df["Name"].str.strip().str.lower() == name.strip().lower()) &
                (existing_df["Class"].astype(str) == str(student_class)) &
                (existing_df["Section"].str.strip().str.lower() == section.strip().lower())
            ).any()

            if duplicate:
                st.error("This student has already submitted an enquiry for the selected class and section.")

            else:
                new_df.to_csv(
                    filename,
                    mode='a',
                    header=False,
                    index=False
                )

                st.success("Enquiry submitted successfully!")
                st.balloons()

        else:
            # If file is not present, this will create new csv
            new_df.to_csv(filename, index=False)

            st.success("Enquiry submitted successfully!")
            st.balloons()

st.markdown("---")
st.markdown("Made with ❤️ by Shriswarup")