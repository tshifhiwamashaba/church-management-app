import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Ensure data folder and CSVs exist
data_files = {
    "members.csv": ["Name", "Phone", "Gender", "Age", "Address", "Join_Date"],
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

# Add Month and Week Columns
members['Month'] = pd.to_datetime(members['Join_Date']).dt.to_period('M')
members['Week'] = pd.to_datetime(members['Join_Date']).dt.strftime('%Y-%U')

finances['Month'] = pd.to_datetime(finances['Date']).dt.to_period('M')
finances['Week'] = pd.to_datetime(finances['Date']).dt.strftime('%Y-%U')

# Members
if page == "Members":
    st.header("👥 Add or Edit a Member")
    
    member_to_edit = st.selectbox("Select a member to edit", members["Name"].tolist())
    if member_to_edit:
        member = members[members["Name"] == member_to_edit].iloc[0]
        # Edit member details
        name = st.text_input("Full Name", value=member["Name"])
        phone = st.text_input("Phone Number", value=member["Phone"])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(member["Gender"]))
        age = st.number_input("Age", min_value=0, max_value=100, value=member["Age"])
        address = st.text_area("Address", value=member["Address"])
        join_date = st.date_input("Join Date", value=pd.to_datetime(member["Join_Date"]).date())
        
        if st.button("Save Changes"):
            if name and phone and age > 0 and address:
                updated_member = pd.DataFrame([[name, phone, gender, age, address, join_date]], columns=["Name", "Phone", "Gender", "Age", "Address", "Join_Date"])
                members.loc[members["Name"] == member_to_edit, ["Name", "Phone", "Gender", "Age", "Address", "Join_Date"]] = updated_member.iloc[0]
                members.to_csv("data/members.csv", index=False)
                st.success("Member details updated!")
            else:
                st.warning("Please fill in all fields.")
    else:
        # Add new member details
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=0, max_value=100)
        address = st.text_area("Address")
        join_date = st.date_input("Join Date")
        
        if st.button("Save New Member"):
            if name and phone and age > 0 and address:
                new_member = pd.DataFrame([[name, phone, gender, age, address, join_date]], columns=["Name", "Phone", "Gender", "Age", "Address", "Join_Date"])
                members = pd.concat([members, new_member], ignore_index=True)
                members.to_csv("data/members.csv", index=False)
                st.success("New member added!")
            else:
                st.warning("Please fill in all fields.")
    
    st.subheader("Current Members")
    st.dataframe(members)

    # Group members by month or week
    group_by = st.selectbox("Group by", ["Month", "Week"])
    if group_by == "Month":
        month_counts = members.groupby('Month').size()
        st.write(month_counts)
    elif group_by == "Week":
        week_counts = members.groupby('Week').size()
        st.write(week_counts)

# Finances
elif page == "Finances":
    st.header("💰 Record or Edit Financial Entry")
    
    finance_to_edit = st.selectbox("Select a finance entry to edit", finances["Date"].tolist())
    if finance_to_edit:
        finance = finances[finances["Date"] == finance_to_edit].iloc[0]
        # Edit finance entry details
        f_type = st.selectbox("Type", ["Offering", "Tithe", "Other"], index=["Offering", "Tithe", "Other"].index(finance["Type"]))
        amount = st.number_input("Amount", min_value=0.0, value=finance["Amount"])
        date = st.date_input("Date", value=pd.to_datetime(finance["Date"]).date())
        
        if st.button("Save Changes"):
            if amount > 0:
                updated_finance = pd.DataFrame([[date, f_type, amount]], columns=["Date", "Type", "Amount"])
                finances.loc[finances["Date"] == finance_to_edit, ["Date", "Type", "Amount"]] = updated_finance.iloc[0]
                finances.to_csv("data/finances.csv", index=False)
                st.success("Finance entry updated!")
            else:
                st.warning("Enter a valid amount.")
    else:
        # Add new finance entry
        f_type = st.selectbox("Type", ["Offering", "Tithe", "Other"])
        amount = st.number_input("Amount", min_value=0.0)
        date = st.date_input("Date")
        
        if st.button("Save Finance Entry"):
            if amount > 0:
                new_finance = pd.DataFrame([[date, f_type, amount]], columns=["Date", "Type", "Amount"])
                finances = pd.concat([finances, new_finance], ignore_index=True)
                finances.to_csv("data/finances.csv", index=False)
                st.success("New finance entry added!")
            else:
                st.warning("Please enter a valid amount.")
    
    st.subheader("Finance Records")
    st.dataframe(finances)

    # Group finances by month or week
    group_by = st.selectbox("Group by", ["Month", "Week"], key="finances")
    if group_by == "Month":
        month_sums = finances.groupby('Month')['Amount'].sum()
        st.write(month_sums)
    elif group_by == "Week":
        week_sums = finances.groupby('Week')['Amount'].sum()
        st.write(week_sums)

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
