CURRENTLY EXPERIENCING DEPLOYMENT ISSUES WILL FIX SOON
# Financial-App-Development-with-Streamlit
As per requirements for assignment # 2 of programming for finance by Dr. Usama Arshad

# Budget Tracker App 💰📈

**Course Name:** AF3005 – Programming for Finance  
**Instructor Name:** Dr. Usama Arshad  
**Developed by:** [Your Name]  

## 📌 App Overview

A Streamlit-based interactive budgeting application that helps users:
- Track income and expenses with detailed categorization
- Visualize financial health through real-time metrics
- Analyze balance trends over time with an interactive chart
- Manage transactions with add/delete functionality

Key Features:
✔ Income vs. Expense tracking  
✔ Automatic balance calculation  
✔ Transaction history with filtering  
✔ Visual trend analysis  
✔ Responsive web interface  

🚀 Google Colab Setup
For quick testing without local installation:

Open Google Colab

Upload the budget_tracker.py file

Run these commands in separate cells:
# Installation cell
!pip install streamlit pandas matplotlib pyngrok

# Execution cell
!streamlit run budget_tracker.py &>/dev/null&
from pyngrok import ngrok
public_url = ngrok.connect(port='8501')
print("Access your app at:", public_url)
