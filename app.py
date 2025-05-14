import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Load data
finances = pd.read_csv("data/finances.csv")

# Finances
st.header("💰 Record or Edit Financial Entry")

# Select a finance entry to edit or leave blank to add new
finance_to_edit = st.selectbox("Select a finance entry to edit or leave blank to add new", [""] + finances["Date"].tolist())

# If a finance entry is selected, pre-populate the details
if finance_to_edit:
    finance = finances[finances["Date"] == finance_to_edit].iloc[0]
    f_type = st.selectbox("Type", ["Offering", "Tithe", "Other"], index=["Offering", "Tithe", "Other"].index(finance["Type"]))
    amount = st.number_input("Amount", min_value=0.0, value=finance["Amount"])
    date = st.date_input("Date", value=pd.to_datetime(finance["Date"]).date())
else:
    # If no finance entry is selected, allow entering details for a new entry
    f_type = st.selectbox("Type", ["Offering", "Tithe", "Other"])
    amount = st.number_input("Amount", min_value=0.0)
    date = st.date_input("Date")

if st.button("Save Finance Entry"):
    if amount > 0:
        # If editing an existing finance entry, update the row
        if finance_to_edit:
            updated_finance = pd.DataFrame([[date, f_type, amount]], columns=["Date", "Type", "Amount"])
            finances.loc[finances["Date"] == finance_to_edit, ["Date", "Type", "Amount"]] = updated_finance.iloc[0]
            finances.to_csv("data/finances.csv", index=False)
            st.success("Finance entry updated!")
        else:
            # If adding a new finance entry, append the row
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
    # Add Month column if it's not already present
    if 'Month' not in finances.columns:
        finances['Month'] = pd.to_datetime(finances['Date']).dt.to_period('M')
    month_sums = finances.groupby('Month')['Amount'].sum()
    st.write(month_sums)
elif group_by == "Week":
    # Add Week column if it's not already present
    if 'Week' not in finances.columns:
        finances['Week'] = pd.to_datetime(finances['Date']).dt.strftime('%Y-%U')
    week_sums = finances.groupby('Week')['Amount'].sum()
    st.write(week_sums)
