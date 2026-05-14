import streamlit as st
import os
import pandas as pd
import plotly.express as plt

st.set_page_config(
    page_title="DAV Admin Panel",
    page_icon="🔐",
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

.login-box {
    padding: 25px;
    border-radius: 15px;
    background-color: #f5f7fb;
    border: 1px solid #dcdcdc;
}

</style>
""", unsafe_allow_html=True)


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


def logout():
    st.session_state.logged_in = False


st.title("🔐 DAV Public School Admin Panel")

st.markdown("""
<div style="
background-color:#e8f0fe;
padding:12px;
border-radius:15px;
width:fit-content;
font-weight:bold;
color:#0b3d91;
margin-bottom:20px;
">
📂 Student Enquiry Management System
</div>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    login = st.button("Login")

    st.markdown('</div>', unsafe_allow_html=True)



    if login:
        if user == "shriswarup" and pwd == "admin@123":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")
else:
    st.subheader("📋 Student Enquiry Records")

    file_name = "student_enquiries.csv"

    if os.path.exists(file_name):
        df = pd.read_csv(file_name)  # type: ignore
        st.dataframe(df, use_container_width=True)
        class_frequency = df["Class"].value_counts().sort_index()
        st.subheader("📊 Enquiries by Class")
        st.bar_chart(class_frequency)
# first one line chart reg_trend
        st.subheader("📈 Registration Trend")
        rgt = df["Date"].value_counts().reset_index()
        rgt.columns = ["Date", "Count"]
        rgt["Date"] = pd.to_datetime(rgt["Date"])
        rgt = rgt.sort_values("Date")
        st.line_chart(rgt.set_index("Date")["Count"])
#boy girl bar chart
        st.subheader("Boy/Girl Bar Chart")
        tot_bg = df["Gender"].value_counts().reset_index()
        tot_bg.columns = ["Gender", "Count"]
        st.bar_chart(tot_bg.set_index("Gender"))
#pie chart for boy girl ratio
        st.subheader("Boy/Girl Ratio")
        boy_girl = df["Gender"].value_counts().reset_index()
        boy_girl.columns = ["Gender", "Count"]
        fig = plt.pie(boy_girl, names="Gender", values="Count", color_discrete_sequence=plt.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            label="⬇ Download CSV",
            data=df.to_csv(index=False),
            file_name="student_enquiries.csv",
            mime="text/csv"
        )
    else:
        st.warning("No enquiry data available.")

    st.button("Logout", on_click=logout)
#hash for the pwd is not made because this is just a sample, thanks for reviewing till end :)))