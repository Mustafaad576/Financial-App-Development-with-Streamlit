import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount', 'Description'])

def add_transaction(date, trans_type, category, amount, description):
    new_transaction = pd.DataFrame([[date, trans_type, category, amount, description]],
                                columns=['Date', 'Type', 'Category', 'Amount', 'Description'])
    st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)

def calculate_summary():
    summary = {}
    if not st.session_state.transactions.empty:
        income = st.session_state.transactions[st.session_state.transactions['Type'] == 'Income']['Amount'].sum()
        expenses = st.session_state.transactions[st.session_state.transactions['Type'] == 'Expense']['Amount'].sum()
        balance = income - expenses
        summary['Total Income'] = income
        summary['Total Expenses'] = expenses
        summary['Balance'] = balance
    return summary

def plot_balance_trend():
    if not st.session_state.transactions.empty:
        df = st.session_state.transactions.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        df['Balance_Impact'] = df.apply(lambda x: x['Amount'] if x['Type'] == 'Income' else -x['Amount'], axis=1)
        df['Cumulative_Balance'] = df['Balance_Impact'].cumsum()
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['Date'], df['Cumulative_Balance'], marker='o', color='#4CAF50', linewidth=2)
        ax.fill_between(df['Date'], df['Cumulative_Balance'], color='#4CAF50', alpha=0.1)
        ax.set_title('Balance Trend Over Time', pad=20)
        ax.set_xlabel('Date')
        ax.set_ylabel('Balance ($)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter('${x:,.0f}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    return None

def main():
    st.title("💰 Personal Budget Tracker")
    
    with st.sidebar:
        st.header("Add New Transaction")
        trans_date = st.date_input("Date", datetime.today())
        trans_type = st.radio("Type", ["Income", "Expense"])
        trans_category = st.selectbox("Category", 
                                   ["Salary", "Freelance", "Investment"] if trans_type == "Income" 
                                   else ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Other"])
        trans_amount = st.number_input("Amount", min_value=0.0, step=0.01)
        trans_description = st.text_input("Description")
        
        if st.button("Add Transaction"):
            if trans_amount > 0:
                add_transaction(trans_date, trans_type, trans_category, trans_amount, trans_description)
                st.success("Transaction added!")
            else:
                st.error("Amount must be > 0")

    col1, col2, col3 = st.columns(3)
    summary = calculate_summary()
    if summary:
        col1.metric("Total Income", f"${summary['Total Income']:,.2f}")
        col2.metric("Total Expenses", f"${summary['Total Expenses']:,.2f}")
        col3.metric("Balance", f"${summary['Balance']:,.2f}", 
                   delta_color="inverse" if summary['Balance'] < 0 else "normal")
    else:
        col1.write("No transactions yet")
        col2.write("No transactions yet")
        col3.write("No transactions yet")

    st.header("Balance Trend")
    if trend_fig := plot_balance_trend():
        st.pyplot(trend_fig)
    else:
        st.info("Add transactions to see trend")

    st.header("Transaction History")
    if not st.session_state.transactions.empty:
        st.dataframe(st.session_state.transactions.sort_values('Date', ascending=False))
        rows_to_delete = st.multiselect("Select transactions to delete", st.session_state.transactions.index)
        if st.button("Delete Selected"):
            st.session_state.transactions = st.session_state.transactions.drop(rows_to_delete)
            st.success("Deleted!")
    else:
        st.info("No transactions yet")

if __name__ == '__main__':
    main()
