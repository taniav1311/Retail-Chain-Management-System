import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import date

DB_PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Niraj@2005',
    'host': 'localhost',
    'port': '5432'
}

def get_conn():
    return psycopg2.connect(**DB_PARAMS)

# Custom CSS styling
st.markdown("""
<style>
    .title {
        color: #2E86C1;
        font-weight: bold;
        font-size: 48px;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-header {
        color: #117A65;
        font-size: 24px;
        font-weight: bold;
        margin-top: 40px;
        margin-bottom: 10px;
    }
    .success-msg {
        color: #28a745;
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
    }
    .error-msg {
        color: #dc3545;
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
    }
    .info-msg {
        color: #117A65;
        font-size: 20px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Retail Chain Management System</div>', unsafe_allow_html=True)

# Session state for employee ID
if 'emp_id' not in st.session_state:
    st.session_state.emp_id = None

# Departments related to selling goods
departments = [
    "Sales",
    "Retail",
    "Distribution",
    "Customer Service",
    "Marketing"
]

# --- EMPLOYEE PERSONAL INFO ---
st.markdown('<div class="section-header">Employee Personal Info</div>', unsafe_allow_html=True)

name = st.text_input("Name", placeholder="Enter employee's full name")
dept = st.selectbox("Department", departments)

if st.button("Confirm Employee Info"):
    if not name.strip() or not dept.strip():
        st.markdown('<p class="error-msg">Please enter both Name and Department</p>', unsafe_allow_html=True)
    else:
        with st.spinner("Searching or adding employee..."):
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM EmployeeBasic WHERE LOWER(name)=LOWER(%s) AND LOWER(department)=LOWER(%s)",
                    (name, dept)
                )
                result = cur.fetchone()
                if result:
                    st.markdown(f'<p class="success-msg">Employee found with ID: {result[0]}</p>', unsafe_allow_html=True)
                    st.session_state.emp_id = result[0]
                else:
                    cur.execute(
                        "INSERT INTO EmployeeBasic (name, department) VALUES (%s, %s) RETURNING id",
                        (name, dept)
                    )
                    emp_id = cur.fetchone()[0]
                    conn.commit()
                    st.markdown(f'<p class="success-msg">New employee added with ID: {emp_id}</p>', unsafe_allow_html=True)
                    st.session_state.emp_id = emp_id

st.markdown("---")

# List of 50 shoe products for product selection
shoe_products = [
    "Running Shoes", "Sneakers", "Loafers", "Formal Shoes", "Casual Shoes", "Basketball Shoes",
    "Tennis Shoes", "Sandals", "Flip Flops", "High Heels", "Wedges", "Boots", "Chelsea Boots",
    "Chukka Boots", "Hiking Boots", "Work Boots", "Slip-Ons", "Moccasins", "Oxford Shoes",
    "Derby Shoes", "Monk Strap Shoes", "Ballet Flats", "Espadrilles", "Clogs", "Boat Shoes",
    "Trail Running Shoes", "Cross Trainers", "Skate Shoes", "Golf Shoes", "Cycling Shoes",
    "Soccer Cleats", "Baseball Cleats", "Water Shoes", "School Shoes", "Dance Shoes",
    "Combat Boots", "Rain Boots", "Snow Boots", "Platform Shoes", "Mary Janes",
    "Loafer Slippers", "Horsebit Loafers", "Gladiator Sandals", "Toe Ring Sandals", "Ankle Boots",
    "Sock Sneakers", "Leather Sneakers", "Canvas Sneakers", "Slip-resistant Shoes", "Climbing Shoes"
]

# --- PAYROLL AND SALES SECTIONS ---
if st.session_state.emp_id:
    st.markdown(f'<div class="section-header">Payroll and Sales details for Employee ID: {st.session_state.emp_id}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Employee Payroll", expanded=True):
            # Query for existing payroll details
            with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT salary, bank_info FROM EmployeePayroll WHERE id=%s", (st.session_state.emp_id,))
                payroll_row = cur.fetchone()

            if payroll_row:
                st.markdown(f"<b>Salary:</b> {payroll_row['salary']}", unsafe_allow_html=True)
                st.markdown(f"<b>Bank Info:</b> {payroll_row['bank_info']}", unsafe_allow_html=True)
                st.markdown('<p class="info-msg">Payroll already exists and cannot be edited.</p>', unsafe_allow_html=True)
            else:
                salary = st.number_input("Salary", min_value=0.0, step=1000.0, help="Enter employee monthly Salary", key="salary")
                bank_info = st.text_input("Bank Info", placeholder="Bank Account or Branch details", key="bank_info")
                if st.button("Submit Payroll"):
                    with st.spinner("Saving Payroll info..."):
                        with get_conn() as conn, conn.cursor() as cur:
                            cur.execute(
                                "INSERT INTO EmployeePayroll (id, salary, bank_info) VALUES (%s, %s, %s)",
                                (st.session_state.emp_id, salary, bank_info)
                            )
                            st.success("Payroll info added")
                            conn.commit()

    with col2:
        with st.expander("Sales Record", expanded=True):
            store = st.selectbox("Select Store Location", ["Store A", "Store B"], key="store")
            product = st.selectbox("Product Name", shoe_products, key="product")
            quantity = st.number_input("Quantity", min_value=1, step=1, key="quantity")
            sale_dt = st.date_input("Sale Date", date.today(), key="sale_date")
            if st.button("Submit Sale Record"):
                if not product:
                    st.markdown('<p class="error-msg">Please select a product</p>', unsafe_allow_html=True)
                else:
                    with st.spinner("Saving sale record..."):
                        with get_conn() as conn, conn.cursor() as cur:
                            # Always insert a new record, not updating existing
                            cur.execute(
                                "INSERT INTO Sales (store_location, product_name, quantity, sale_date, employee_id) VALUES (%s, %s, %s, %s, %s)",
                                (store, product, quantity, sale_dt, st.session_state.emp_id)
                            )
                            st.markdown('<p class="success-msg">New sale record inserted</p>', unsafe_allow_html=True)
                            conn.commit()
else:
    st.markdown('<p class="info-msg">Please enter employee personal info above to proceed with Payroll and Sales operations.</p>', unsafe_allow_html=True)

# --- VIEW DATA (sidebar) ---
st.sidebar.header("View Data")
view_choice = st.sidebar.selectbox("Select Data to View", ["Employee Full Info", "All Sales Records"])

with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
    if view_choice == "Employee Full Info":
        cur.execute("SELECT * FROM EmployeeFull ORDER BY id")
        records = cur.fetchall()
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df)
        else:
            st.info("No records found.")
    else:
        # Show sales records with employee name first, without sale_id column
        cur.execute("""
            SELECT 
                e.name AS employee_name,
                s.store_location, 
                s.product_name, 
                s.quantity, 
                s.sale_date
            FROM Sales s
            JOIN EmployeeBasic e ON s.employee_id = e.id
            ORDER BY s.sale_date DESC
        """)
        records = cur.fetchall()
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df)
        else:
            st.info("No records found.")