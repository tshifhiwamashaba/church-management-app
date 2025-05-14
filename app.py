import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Ensure data folder and CSVs exist
data_files = {
    "members.csv": ["Name", "Phone", "Join_Date"],
    "finances.csv": ["Date", "Type", "Amount"],
    "cell_groups.csv": ["Group_Name", "Member_Name"],
    "events.csv": ["Event_Name", "Date"]
}
os.makedirs("data", exist_ok=True)
for file, cols in data_files.items():
    path = f"data/{file}"
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_csv(path, index=False)

st.title("📊 Church Management Dashboard")

# Sidebar Navigation
page = st.sidebar.selectbox("Select Page", [
    "Members", "Finances", "Cell Groups", "Events", "Dashboard"
])

# Load data
members = pd.read_csv("data/members.csv")
finances = pd.read_csv("data/finances.csv")
groups = pd.read_csv("data/cell_groups.csv")
events = pd.read_csv("data/events.csv")

# Members
if page == "Members":
    st.header("👥 Add a New Member")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    if st.button("Add Member"):
        if name and phone:
            new = pd.DataFrame([[name, phone, datetime.today().date()]], columns=["Name", "Phone", "Join_Date"])
            members = pd.concat([members, new], ignore_index=True)
            members.to_csv("data/members.csv", index=False)
            st.success("Member added!")
        else:
            st.warning("Please fill in all fields.")
    st.subheader("Current Members")
    st.dataframe(members)

# Finances
elif page == "Finances":
    st.header("💰 Record Financial Entry")
    f_type = st.selectbox("Type", ["Offering", "Tithe", "Other"])
    amount = st.number_input("Amount", min_value=0.0)
    if st.button("Add Finance"):
        if amount > 0:
            new = pd.DataFrame([[datetime.today().date(), f_type, amount]], columns=["Date", "Type", "Amount"])
            finances = pd.concat([finances, new], ignore_index=True)
            finances.to_csv("data/finances.csv", index=False)
            st.success("Finance recorded!")
        else:
            st.warning("Enter an amount.")
    st.subheader("Finance Records")
    st.dataframe(finances)

# Cell Groups
elif page == "Cell Groups":
    st.header("🧑‍🤝‍🧑 Assign to Cell Group")
    group = st.text_input("Group Name")
    member = st.selectbox("Member", members["Name"].tolist())
    if st.button("Assign Member"):
        if group:
            new = pd.DataFrame([[group, member]], columns=["Group_Name", "Member_Name"])
            groups = pd.concat([groups, new], ignore_index=True)
            groups.to_csv("data/cell_groups.csv", index=False)
            st.success("Member assigned!")
    st.subheader("Cell Group Assignments")
    st.dataframe(groups)

# Events
elif page == "Events":
    st.header("📅 Add New Event")
    event = st.text_input("Event Name")
    date = st.date_input("Event Date")
    if st.button("Add Event"):
        if event:
            new = pd.DataFrame([[event, date]], columns=["Event_Name", "Date"])
            events = pd.concat([events, new], ignore_index=True)
            events.to_csv("data/events.csv", index=False)
            st.success("Event added!")
    st.subheader("Upcoming Events")
    st.dataframe(events)

# Dashboard
elif page == "Dashboard":
    st.header("📈 Dashboard Summary")
    st.metric("Total Members", len(members))
    st.metric("Total Finance Entries", len(finances))
    st.metric("Cell Groups", len(groups["Group_Name"].unique()))
    st.metric("Upcoming Events", len(events[events["Date"] >= str(datetime.today().date())]))
    st.bar_chart(finances.groupby("Type")["Amount"].sum())
