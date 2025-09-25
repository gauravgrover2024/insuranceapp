import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import uuid
from typing import Dict, List
import json

# Configure page
st.set_page_config(
    page_title="CDrive Insurance Management",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, mobile-responsive design
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #C73E1D;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .app-header {
        background: var(--background-gradient);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
        color: white;
        text-align: center;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: var(--card-shadow);
        margin: 0.5rem 0;
        border-left: 4px solid var(--primary-color);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: bold;
        text-align: center;
        margin: 0.25rem;
    }
    
    .status-new { background-color: #e3f2fd; color: #1976d2; }
    .status-quote { background-color: #fff3e0; color: #f57c00; }
    .status-policy { background-color: #e8f5e8; color: #388e3c; }
    .status-closed { background-color: #fce4ec; color: #c2185b; }
    
    /* Step indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem 0.5rem;
        position: relative;
        min-width: 100px;
    }
    
    .step.active {
        color: var(--primary-color);
        font-weight: bold;
    }
    
    .step.completed {
        color: var(--success-color);
    }
    
    .step::after {
        content: '';
        position: absolute;
        top: 50%;
        right: -50%;
        width: 100%;
        height: 2px;
        background: #e0e0e0;
        z-index: -1;
    }
    
    .step:last-child::after {
        display: none;
    }
    
    .step.completed::after {
        background: var(--success-color);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .step-indicator {
            flex-direction: column;
        }
        
        .step::after {
            display: none;
        }
        
        .metric-card {
            margin: 0.25rem 0;
            padding: 1rem;
        }
    }
    
    /* Form styling */
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
    
    .stTextInput > div > div > input {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--background-gradient);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'current_user_role' not in st.session_state:
    st.session_state.current_user_role = 'Admin'
if 'current_case' not in st.session_state:
    st.session_state.current_case = {}
if 'case_step' not in st.session_state:
    st.session_state.case_step = 1

# Sample data for testing
def load_sample_data():
    if not st.session_state.cases:
        sample_cases = [
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Rajesh Kumar',
                'customer_phone': '+91-9876543210',
                'customer_email': 'rajesh.kumar@email.com',
                'insurance_type': 'Life Insurance',
                'coverage_amount': 1000000,
                'premium_amount': 25000,
                'status': 'Policy Issued',
                'created_date': datetime.now() - timedelta(days=15),
                'assigned_to': 'Priya Sharma',
                'follow_up_date': datetime.now() + timedelta(days=30),
                'documents': ['ID Proof', 'Income Proof', 'Medical Reports'],
                'step': 9
            },
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Anita Desai',
                'customer_phone': '+91-9876543211',
                'customer_email': 'anita.desai@email.com',
                'insurance_type': 'Health Insurance',
                'coverage_amount': 500000,
                'premium_amount': 15000,
                'status': 'Quote Generated',
                'created_date': datetime.now() - timedelta(days=5),
                'assigned_to': 'Amit Singh',
                'follow_up_date': datetime.now() + timedelta(days=3),
                'documents': ['ID Proof', 'Medical Records'],
                'step': 4
            },
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Mohammed Ali',
                'customer_phone': '+91-9876543212',
                'customer_email': 'mohammed.ali@email.com',
                'insurance_type': 'Vehicle Insurance',
                'coverage_amount': 300000,
                'premium_amount': 8000,
                'status': 'Documentation Pending',
                'created_date': datetime.now() - timedelta(days=2),
                'assigned_to': 'Sneha Patel',
                'follow_up_date': datetime.now() + timedelta(days=1),
                'documents': ['Vehicle Registration', 'Driver License'],
                'step': 5
            },
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Lakshmi Nair',
                'customer_phone': '+91-9876543213',
                'customer_email': 'lakshmi.nair@email.com',
                'insurance_type': 'Home Insurance',
                'coverage_amount': 2000000,
                'premium_amount': 35000,
                'status': 'New Lead',
                'created_date': datetime.now() - timedelta(days=1),
                'assigned_to': 'Rahul Verma',
                'follow_up_date': datetime.now() + timedelta(days=2),
                'documents': [],
                'step': 1
            },
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Suresh Reddy',
                'customer_phone': '+91-9876543214',
                'customer_email': 'suresh.reddy@email.com',
                'insurance_type': 'Travel Insurance',
                'coverage_amount': 100000,
                'premium_amount': 2500,
                'status': 'Case Closed',
                'created_date': datetime.now() - timedelta(days=30),
                'assigned_to': 'Neha Gupta',
                'follow_up_date': None,
                'documents': ['Passport', 'Visa', 'Travel Itinerary'],
                'step': 9
            }
        ]
        st.session_state.cases.extend(sample_cases)

# Load sample data
load_sample_data()

# Header
st.markdown("""
<div class="app-header">
    <h1>🏢 CDrive Insurance Management System</h1>
    <p>Comprehensive Case Management • Analytics • Renewals</p>
</div>
""", unsafe_allow_html=True)

# Role selection
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.session_state.current_user_role = st.selectbox(
        "👤 Current User Role",
        ['Admin', 'Team Lead', 'Executive'],
        index=['Admin', 'Team Lead', 'Executive'].index(st.session_state.current_user_role),
        key='role_selector'
    )

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    # Role-based menu options
    if st.session_state.current_user_role == 'Admin':
        menu_options = [
            "📊 Dashboard", 
            "➕ Create New Case", 
            "📋 Manage Cases", 
            "👥 User Management",
            "🔄 Renewal Management",
            "📈 Analytics & Reports"
        ]
    elif st.session_state.current_user_role == 'Team Lead':
        menu_options = [
            "📊 Dashboard",
            "➕ Create New Case",
            "📋 Team Cases",
            "👥 Assign Cases",
            "📈 Team Analytics"
        ]
    else:  # Executive
        menu_options = [
            "📊 Dashboard",
            "➕ Create New Case", 
            "📋 My Cases",
            "📅 Follow-ups",
            "📈 My Performance"
        ]
    
    selected_page = st.selectbox("Select Page", menu_options, key='page_selector')

# Main content area
def render_dashboard():
    st.markdown("## 📊 Dashboard")
    
    # Key metrics
    total_cases = len(st.session_state.cases)
    active_cases = len([c for c in st.session_state.cases if c['status'] not in ['Case Closed', 'Policy Issued']])
    total_premium = sum([c['premium_amount'] for c in st.session_state.cases])
    avg_case_value = total_premium / total_cases if total_cases > 0 else 0
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--primary-color); margin: 0;">Total Cases</h3>
            <h2 style="margin: 0.5rem 0 0 0;">{}</h2>
        </div>
        """.format(total_cases), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--secondary-color); margin: 0;">Active Cases</h3>
            <h2 style="margin: 0.5rem 0 0 0;">{}</h2>
        </div>
        """.format(active_cases), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--accent-color); margin: 0;">Total Premium</h3>
            <h2 style="margin: 0.5rem 0 0 0;">₹{:,.0f}</h2>
        </div>
        """.format(total_premium), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--success-color); margin: 0;">Avg Case Value</h3>
            <h2 style="margin: 0.5rem 0 0 0;">₹{:,.0f}</h2>
        </div>
        """.format(avg_case_value), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Cases by Status")
        if st.session_state.cases:
            status_counts = pd.DataFrame(st.session_state.cases)['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, 
                        color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
            fig.update_layout(showlegend=True, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏷️ Insurance Types")
        if st.session_state.cases:
            type_counts = pd.DataFrame(st.session_state.cases)['insurance_type'].value_counts()
            fig = px.bar(x=type_counts.index, y=type_counts.values,
                        color_discrete_sequence=['#667eea'])
            fig.update_layout(showlegend=False, height=300, xaxis_title="Insurance Type", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent cases table
    st.markdown("### 📋 Recent Cases")
    if st.session_state.cases:
        recent_cases = sorted(st.session_state.cases, key=lambda x: x['created_date'], reverse=True)[:5]
        
        for case in recent_cases:
            status_class = {
                'New Lead': 'status-new',
                'Quote Generated': 'status-quote', 
                'Policy Issued': 'status-policy',
                'Case Closed': 'status-closed'
            }.get(case['status'], 'status-new')
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h4 style="margin: 0; color: var(--primary-color);">{case['customer_name']}</h4>
                        <p style="margin: 0.25rem 0; color: #666;">{case['insurance_type']} • ₹{case['premium_amount']:,.0f}</p>
                    </div>
                    <div style="text-align: right;">
                        <span class="status-badge {status_class}">{case['status']}</span>
                        <p style="margin: 0.25rem 0; color: #666; font-size: 0.8rem;">
                            {case['created_date'].strftime('%d %b %Y')}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_case_creation():
    st.markdown("## ➕ Create New Case")
    
    # Case creation steps
    steps = [
        "Customer Details",
        "Insurance Type", 
        "Coverage Requirements",
        "Quote Generation",
        "Documentation",
        "Policy Finalization",
        "Payment Processing", 
        "Policy Issuance",
        "Follow-up Setup"
    ]
    
    # Step indicator
    st.markdown(f"""
    <div class="step-indicator">
        {" ".join([f'<div class="step {"active" if i+1 == st.session_state.case_step else "completed" if i+1 < st.session_state.case_step else ""}"><span>{i+1}</span><br><small>{step}</small></div>' for i, step in enumerate(steps)])}
    </div>
    """, unsafe_allow_html=True)
    
    # Step content
    if st.session_state.case_step == 1:
        render_customer_details_step()
    elif st.session_state.case_step == 2:
        render_insurance_type_step()
    elif st.session_state.case_step == 3:
        render_coverage_requirements_step()
    elif st.session_state.case_step == 4:
        render_quote_generation_step()
    elif st.session_state.case_step == 5:
        render_documentation_step()
    elif st.session_state.case_step == 6:
        render_policy_finalization_step()
    elif st.session_state.case_step == 7:
        render_payment_processing_step()
    elif st.session_state.case_step == 8:
        render_policy_issuance_step()
    elif st.session_state.case_step == 9:
        render_followup_setup_step()

def render_customer_details_step():
    st.markdown("### 👤 Step 1: Customer Details")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name *", 
                                        value=st.session_state.current_case.get('customer_name', ''))
            customer_phone = st.text_input("Phone Number *", 
                                         value=st.session_state.current_case.get('customer_phone', ''))
            customer_email = st.text_input("Email Address *",
                                         value=st.session_state.current_case.get('customer_email', ''))
        
        with col2:
            customer_dob = st.date_input("Date of Birth",
                                       value=st.session_state.current_case.get('customer_dob', date.today() - timedelta(days=365*30)))
            customer_occupation = st.text_input("Occupation",
                                              value=st.session_state.current_case.get('customer_occupation', ''))
            customer_address = st.text_area("Address",
                                          value=st.session_state.current_case.get('customer_address', ''))
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Next Step →", key='step1_next'):
            if customer_name and customer_phone and customer_email:
                st.session_state.current_case.update({
                    'customer_name': customer_name,
                    'customer_phone': customer_phone,
                    'customer_email': customer_email,
                    'customer_dob': customer_dob,
                    'customer_occupation': customer_occupation,
                    'customer_address': customer_address
                })
                st.session_state.case_step = 2
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")

def render_insurance_type_step():
    st.markdown("### 🏷️ Step 2: Insurance Type Selection")
    
    insurance_types = [
        "Life Insurance",
        "Health Insurance", 
        "Vehicle Insurance",
        "Home Insurance",
        "Travel Insurance",
        "Business Insurance"
    ]
    
    selected_type = st.selectbox("Select Insurance Type *",
                                insurance_types,
                                index=insurance_types.index(st.session_state.current_case.get('insurance_type', insurance_types[0])))
    
    # Type-specific details
    if selected_type == "Life Insurance":
        col1, col2 = st.columns(2)
        with col1:
            policy_term = st.selectbox("Policy Term", ["10 Years", "15 Years", "20 Years", "25 Years", "30 Years"])
            premium_paying_term = st.selectbox("Premium Paying Term", ["5 Years", "10 Years", "15 Years", "20 Years"])
        with col2:
            nominee_name = st.text_input("Nominee Name")
            nominee_relation = st.text_input("Nominee Relation")
    
    elif selected_type == "Health Insurance":
        col1, col2 = st.columns(2)
        with col1:
            family_size = st.selectbox("Family Size", ["Individual", "2 Members", "3 Members", "4 Members", "5+ Members"])
            pre_existing = st.selectbox("Pre-existing Conditions", ["None", "Diabetes", "Hypertension", "Heart Disease", "Other"])
        with col2:
            preferred_hospital = st.text_input("Preferred Hospital Network")
            room_type = st.selectbox("Room Type Preference", ["General Ward", "Semi-Private", "Private", "Suite"])
    
    elif selected_type == "Vehicle Insurance":
        col1, col2 = st.columns(2)
        with col1:
            vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Commercial Vehicle"])
            vehicle_make = st.text_input("Vehicle Make")
        with col2:
            vehicle_model = st.text_input("Vehicle Model")
            vehicle_year = st.selectbox("Manufacturing Year", list(range(datetime.now().year, datetime.now().year - 20, -1)))
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step2_prev'):
            st.session_state.case_step = 1
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step2_next'):
            st.session_state.current_case['insurance_type'] = selected_type
            st.session_state.case_step = 3
            st.rerun()

def render_coverage_requirements_step():
    st.markdown("### 💰 Step 3: Coverage Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        coverage_amount = st.number_input("Coverage Amount (₹) *",
                                        min_value=10000,
                                        max_value=10000000,
                                        value=st.session_state.current_case.get('coverage_amount', 500000),
                                        step=50000)
        
        deductible = st.selectbox("Deductible Amount (₹)",
                                [0, 5000, 10000, 25000, 50000])
    
    with col2:
        policy_duration = st.selectbox("Policy Duration",
                                     ["1 Year", "2 Years", "3 Years", "5 Years"])
        
        premium_frequency = st.selectbox("Premium Payment Frequency",
                                       ["Annually", "Semi-Annually", "Quarterly", "Monthly"])
    
    # Additional coverage options
    st.markdown("#### Additional Coverage Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        critical_illness = st.checkbox("Critical Illness Cover")
        accidental_death = st.checkbox("Accidental Death Benefit")
    
    with col2:
        disability_cover = st.checkbox("Disability Coverage")
        waiver_premium = st.checkbox("Waiver of Premium")
    
    with col3:
        maternity_cover = st.checkbox("Maternity Coverage")
        dental_optical = st.checkbox("Dental & Optical")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step3_prev'):
            st.session_state.case_step = 2
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step3_next'):
            st.session_state.current_case.update({
                'coverage_amount': coverage_amount,
                'deductible': deductible,
                'policy_duration': policy_duration,
                'premium_frequency': premium_frequency
            })
            st.session_state.case_step = 4
            st.rerun()

def render_quote_generation_step():
    st.markdown("### 💵 Step 4: Quote Generation")
    
    # Calculate premium based on coverage and type
    coverage = st.session_state.current_case.get('coverage_amount', 500000)
    insurance_type = st.session_state.current_case.get('insurance_type', 'Life Insurance')
    
    # Premium calculation logic
    base_rates = {
        'Life Insurance': 0.025,
        'Health Insurance': 0.030,
        'Vehicle Insurance': 0.015,
        'Home Insurance': 0.012,
        'Travel Insurance': 0.025,
        'Business Insurance': 0.020
    }
    
    base_premium = coverage * base_rates.get(insurance_type, 0.025)
    
    # Generate multiple quote options
    quotes = [
        {
            'name': 'Basic Plan',
            'premium': base_premium * 0.8,
            'features': ['Basic Coverage', 'Standard Benefits', '24/7 Support']
        },
        {
            'name': 'Standard Plan', 
            'premium': base_premium,
            'features': ['Enhanced Coverage', 'Additional Benefits', '24/7 Support', 'Cashless Network']
        },
        {
            'name': 'Premium Plan',
            'premium': base_premium * 1.3,
            'features': ['Comprehensive Coverage', 'Premium Benefits', '24/7 Support', 'Cashless Network', 'Global Coverage']
        }
    ]
    
    st.markdown("#### Available Quote Options")
    
    selected_quote = None
    for i, quote in enumerate(quotes):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{quote['name']}**")
                for feature in quote['features']:
                    st.markdown(f"• {feature}")
            
            with col2:
                st.markdown(f"**Annual Premium: ₹{quote['premium']:,.0f}**")
                st.markdown(f"Monthly: ₹{quote['premium']/12:,.0f}")
            
            with col3:
                if st.button(f"Select", key=f'quote_{i}'):
                    selected_quote = quote
                    st.session_state.current_case['selected_quote'] = quote
                    st.session_state.current_case['premium_amount'] = quote['premium']
                    st.success(f"{quote['name']} selected!")
    
    if 'selected_quote' in st.session_state.current_case:
        st.success(f"Selected: {st.session_state.current_case['selected_quote']['name']} - ₹{st.session_state.current_case['premium_amount']:,.0f}/year")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step4_prev'):
            st.session_state.case_step = 3
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step4_next'):
            if 'selected_quote' in st.session_state.current_case:
                st.session_state.case_step = 5
                st.rerun()
            else:
                st.error("Please select a quote option")

def render_documentation_step():
    st.markdown("### 📄 Step 5: Document Collection")
    
    insurance_type = st.session_state.current_case.get('insurance_type', 'Life Insurance')
    
    # Required documents based on insurance type
    required_docs = {
        'Life Insurance': ['ID Proof', 'Address Proof', 'Income Proof', 'Medical Reports', 'Passport Size Photos'],
        'Health Insurance': ['ID Proof', 'Address Proof', 'Medical Records', 'Salary Slips', 'Passport Size Photos'],
        'Vehicle Insurance': ['Vehicle Registration', 'Driver License', 'Previous Policy', 'Vehicle Photos', 'ID Proof'],
        'Home Insurance': ['Property Documents', 'ID Proof', 'Address Proof', 'Property Valuation', 'Property Photos'],
        'Travel Insurance': ['Passport', 'Visa', 'Travel Itinerary', 'ID Proof', 'Ticket Bookings'],
        'Business Insurance': ['Business Registration', 'Financial Statements', 'ID Proof', 'Property Documents', 'Tax Returns']
    }
    
    docs_needed = required_docs.get(insurance_type, ['ID Proof', 'Address Proof'])
    
    st.markdown(f"#### Required Documents for {insurance_type}")
    
    collected_docs = []
    for doc in docs_needed:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"• {doc}")
        with col2:
            if st.checkbox("Collected", key=f'doc_{doc}'):
                collected_docs.append(doc)
    
    # Document upload simulation
    st.markdown("#### Document Upload")
    uploaded_files = st.file_uploader(
        "Upload Documents", 
        accept_multiple_files=True,
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Upload scanned copies or photos of required documents"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} document(s)")
        for file in uploaded_files:
            st.markdown(f"📎 {file.name}")
    
    # Document status
    completion_rate = len(collected_docs) / len(docs_needed) * 100
    st.progress(completion_rate / 100)
    st.markdown(f"Documentation Complete: {completion_rate:.0f}%")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step5_prev'):
            st.session_state.case_step = 4
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step5_next'):
            st.session_state.current_case['documents'] = collected_docs
            st.session_state.case_step = 6
            st.rerun()

def render_policy_finalization_step():
    st.markdown("### ✅ Step 6: Policy Finalization")
    
    # Summary of case details
    case = st.session_state.current_case
    
    st.markdown("#### Policy Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Customer Information**")
        st.markdown(f"• **Name:** {case.get('customer_name', 'N/A')}")
        st.markdown(f"• **Phone:** {case.get('customer_phone', 'N/A')}")
        st.markdown(f"• **Email:** {case.get('customer_email', 'N/A')}")
        
        st.markdown("**Policy Details**")
        st.markdown(f"• **Type:** {case.get('insurance_type', 'N/A')}")
        st.markdown(f"• **Coverage:** ₹{case.get('coverage_amount', 0):,.0f}")
        st.markdown(f"• **Duration:** {case.get('policy_duration', 'N/A')}")
    
    with col2:
        st.markdown("**Premium Information**")
        if 'selected_quote' in case:
            st.markdown(f"• **Plan:** {case['selected_quote']['name']}")
        st.markdown(f"• **Annual Premium:** ₹{case.get('premium_amount', 0):,.0f}")
        st.markdown(f"• **Payment Mode:** {case.get('premium_frequency', 'Annually')}")
        
        st.markdown("**Documentation Status**")
        docs = case.get('documents', [])
        st.markdown(f"• **Documents Collected:** {len(docs)}")
        for doc in docs:
            st.markdown(f"  ✓ {doc}")
    
    # Policy terms and conditions
    st.markdown("#### Terms & Conditions")
    terms_accepted = st.checkbox("I have read and agree to the terms and conditions")
    
    # Executive assignment
    st.markdown("#### Assignment")
    executives = ["Priya Sharma", "Amit Singh", "Sneha Patel", "Rahul Verma", "Neha Gupta"]
    assigned_to = st.selectbox("Assign to Executive", executives)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step6_prev'):
            st.session_state.case_step = 5
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step6_next'):
            if terms_accepted:
                st.session_state.current_case['assigned_to'] = assigned_to
                st.session_state.current_case['terms_accepted'] = True
                st.session_state.case_step = 7
                st.rerun()
            else:
                st.error("Please accept the terms and conditions")

def render_payment_processing_step():
    st.markdown("### 💳 Step 7: Payment Processing")
    
    case = st.session_state.current_case
    premium = case.get('premium_amount', 0)
    frequency = case.get('premium_frequency', 'Annually')
    
    # Payment amount calculation
    payment_amounts = {
        'Annually': premium,
        'Semi-Annually': premium / 2,
        'Quarterly': premium / 4,
        'Monthly': premium / 12
    }
    
    payment_amount = payment_amounts.get(frequency, premium)
    
    st.markdown(f"#### Payment Due: ₹{payment_amount:,.0f} ({frequency})")
    
    # Payment methods
    payment_method = st.selectbox(
        "Select Payment Method",
        ["Credit Card", "Debit Card", "Net Banking", "UPI", "Bank Transfer", "Cheque"]
    )
    
    if payment_method in ["Credit Card", "Debit Card"]:
        col1, col2 = st.columns(2)
        with col1:
            card_number = st.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
            cardholder_name = st.text_input("Cardholder Name")
        with col2:
            expiry_date = st.text_input("Expiry (MM/YY)", placeholder="MM/YY")
            cvv = st.text_input("CVV", type="password", max_chars=3)
    
    elif payment_method == "UPI":
        upi_id = st.text_input("UPI ID", placeholder="example@paytm")
    
    elif payment_method == "Bank Transfer":
        bank_name = st.text_input("Bank Name")
        account_number = st.text_input("Account Number")
        ifsc_code = st.text_input("IFSC Code")
    
    elif payment_method == "Cheque":
        cheque_number = st.text_input("Cheque Number")
        bank_name = st.text_input("Bank Name")
        cheque_date = st.date_input("Cheque Date", value=date.today())
    
    # Payment processing simulation
    if st.button("Process Payment", key='process_payment'):
        with st.spinner("Processing payment..."):
            import time
            time.sleep(2)
            st.success("Payment processed successfully!")
            st.session_state.current_case['payment_status'] = 'Completed'
            st.session_state.current_case['payment_method'] = payment_method
            st.session_state.current_case['payment_amount'] = payment_amount
            st.session_state.current_case['payment_date'] = datetime.now()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step7_prev'):
            st.session_state.case_step = 6
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step7_next'):
            if case.get('payment_status') == 'Completed':
                st.session_state.case_step = 8
                st.rerun()
            else:
                st.error("Please complete the payment processing")

def render_policy_issuance_step():
    st.markdown("### 📋 Step 8: Policy Issuance")
    
    case = st.session_state.current_case
    
    # Generate policy number
    if 'policy_number' not in case:
        policy_number = f"CDR-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.cases) + 1:04d}"
        st.session_state.current_case['policy_number'] = policy_number
    
    st.markdown("#### Policy Generated Successfully! 🎉")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Policy Details**")
        st.markdown(f"• **Policy Number:** {case.get('policy_number')}")
        st.markdown(f"• **Issue Date:** {datetime.now().strftime('%d %b %Y')}")
        st.markdown(f"• **Effective Date:** {datetime.now().strftime('%d %b %Y')}")
        
        # Calculate policy end date
        duration = case.get('policy_duration', '1 Year')
        years = int(duration.split()[0])
        end_date = datetime.now() + timedelta(days=365 * years)
        st.markdown(f"• **Expiry Date:** {end_date.strftime('%d %b %Y')}")
    
    with col2:
        st.markdown("**Coverage Summary**")
        st.markdown(f"• **Sum Insured:** ₹{case.get('coverage_amount', 0):,.0f}")
        st.markdown(f"• **Annual Premium:** ₹{case.get('premium_amount', 0):,.0f}")
        st.markdown(f"• **Payment Mode:** {case.get('premium_frequency', 'Annually')}")
        st.markdown(f"• **Next Premium Due:** {(datetime.now() + timedelta(days=365)).strftime('%d %b %Y')}")
    
    # Policy document generation
    st.markdown("#### Policy Documents")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Download Policy", key='download_policy'):
            st.success("Policy document downloaded!")
    with col2:
        if st.button("📧 Email to Customer", key='email_policy'):
            st.success(f"Policy emailed to {case.get('customer_email')}")
    with col3:
        if st.button("📱 SMS Confirmation", key='sms_policy'):
            st.success(f"SMS sent to {case.get('customer_phone')}")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step8_prev'):
            st.session_state.case_step = 7
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step8_next'):
            st.session_state.current_case['status'] = 'Policy Issued'
            st.session_state.case_step = 9
            st.rerun()

def render_followup_setup_step():
    st.markdown("### 📅 Step 9: Follow-up Setup")
    
    case = st.session_state.current_case
    
    st.markdown("#### Congratulations! Policy Created Successfully 🎉")
    
    # Follow-up scheduling
    st.markdown("#### Schedule Follow-up Activities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Customer Follow-up**")
        customer_followup = st.date_input(
            "Customer Satisfaction Call",
            value=datetime.now().date() + timedelta(days=7)
        )
        
        st.markdown("**Renewal Reminder**")
        renewal_reminder = st.date_input(
            "Renewal Reminder Date",
            value=datetime.now().date() + timedelta(days=335)  # 30 days before expiry
        )
    
    with col2:
        st.markdown("**Payment Follow-up**")
        if case.get('premium_frequency') != 'Annually':
            next_payment = st.date_input(
                "Next Premium Due",
                value=datetime.now().date() + timedelta(days=30)
            )
        
        st.markdown("**Service Follow-up**")
        service_check = st.date_input(
            "Service Check Date",
            value=datetime.now().date() + timedelta(days=90)
        )
    
    # Additional notes
    follow_up_notes = st.text_area(
        "Follow-up Notes",
        placeholder="Any specific instructions or notes for follow-up activities..."
    )
    
    # Complete case creation
    if st.button("🏁 Complete Case Creation", key='complete_case'):
        # Finalize case data
        final_case = {
            **st.session_state.current_case,
            'id': str(uuid.uuid4()),
            'created_date': datetime.now(),
            'follow_up_date': customer_followup,
            'renewal_date': renewal_reminder,
            'follow_up_notes': follow_up_notes,
            'step': 9,
            'status': 'Policy Issued'
        }
        
        # Add to cases list
        st.session_state.cases.append(final_case)
        
        # Reset case creation
        st.session_state.current_case = {}
        st.session_state.case_step = 1
        
        st.success("Case created successfully!")
        st.balloons()
        
        # Show case summary
        with st.expander("📋 Case Summary", expanded=True):
            st.json(final_case, expanded=False)
        
        if st.button("Create Another Case"):
            st.rerun()

def render_manage_cases():
    st.markdown("## 📋 Manage Cases")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All"] + list(set([case['status'] for case in st.session_state.cases])))
    
    with col2:
        type_filter = st.selectbox("Filter by Type",
                                 ["All"] + list(set([case['insurance_type'] for case in st.session_state.cases])))
    
    with col3:
        assigned_filter = st.selectbox("Filter by Executive",
                                     ["All"] + list(set([case['assigned_to'] for case in st.session_state.cases])))
    
    with col4:
        date_range = st.selectbox("Date Range", ["All", "Today", "This Week", "This Month"])
    
    # Apply filters
    filtered_cases = st.session_state.cases.copy()
    
    if status_filter != "All":
        filtered_cases = [case for case in filtered_cases if case['status'] == status_filter]
    
    if type_filter != "All":
        filtered_cases = [case for case in filtered_cases if case['insurance_type'] == type_filter]
    
    if assigned_filter != "All":
        filtered_cases = [case for case in filtered_cases if case['assigned_to'] == assigned_filter]
    
    # Cases table
    if filtered_cases:
        st.markdown(f"### Found {len(filtered_cases)} case(s)")
        
        for i, case in enumerate(filtered_cases):
            with st.expander(f"Case: {case['customer_name']} - {case['insurance_type']} - {case['status']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Customer Details**")
                    st.markdown(f"• Name: {case['customer_name']}")
                    st.markdown(f"• Phone: {case['customer_phone']}")
                    st.markdown(f"• Email: {case['customer_email']}")
                
                with col2:
                    st.markdown("**Policy Details**")
                    st.markdown(f"• Type: {case['insurance_type']}")
                    st.markdown(f"• Coverage: ₹{case['coverage_amount']:,.0f}")
                    st.markdown(f"• Premium: ₹{case['premium_amount']:,.0f}")
                
                with col3:
                    st.markdown("**Case Status**")
                    st.markdown(f"• Status: {case['status']}")
                    st.markdown(f"• Assigned to: {case['assigned_to']}")
                    st.markdown(f"• Created: {case['created_date'].strftime('%d %b %Y')}")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("📝 Edit", key=f"edit_{i}"):
                        st.info("Edit functionality would open case details for modification")
                with col2:
                    if st.button("👥 Reassign", key=f"reassign_{i}"):
                        st.info("Reassignment dialog would open here")
                with col3:
                    if st.button("📞 Follow-up", key=f"followup_{i}"):
                        st.info("Follow-up scheduling dialog would open here")
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        st.error("Are you sure you want to delete this case?")
    else:
        st.info("No cases found matching the selected filters.")

# Main page routing
if "Dashboard" in selected_page:
    render_dashboard()
elif "Create New Case" in selected_page:
    render_case_creation()
elif "Manage Cases" in selected_page or "Team Cases" in selected_page or "My Cases" in selected_page:
    render_manage_cases()
elif "Analytics" in selected_page:
    st.markdown("## 📈 Analytics & Reports")
    st.info("Advanced analytics dashboard would be implemented here with detailed charts, KPIs, and export options.")
elif "User Management" in selected_page:
    st.markdown("## 👥 User Management")
    st.info("User management interface for creating, editing, and managing user accounts and roles.")
elif "Renewal Management" in selected_page:
    st.markdown("## 🔄 Renewal Management") 
    st.info("Renewal tracking and management system with automated alerts and assignment workflows.")
else:
    render_dashboard()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "© 2025 CDrive Insurance Management System • Powered by MiniMax Agent"
    "</div>", 
    unsafe_allow_html=True
)