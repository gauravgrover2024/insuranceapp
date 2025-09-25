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
    page_title="CDrive Vehicle Insurance Management",
    page_icon="🚗",
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

# Indian Car Make and Model Data
CAR_DATA = {
    'Maruti Suzuki': [
        'Swift', 'Baleno', 'Alto K10', 'WagonR', 'Dzire', 'Brezza', 'Victoris', 
        'Ertiga', 'S-Presso', 'Celerio', 'Fronx', 'Grand Vitara', 'XL6', 
        'Ignis', 'Jimny', 'Invicto', 'Ciaz', 'Eeco'
    ],
    'Hyundai': [
        'Creta', 'Venue', 'Exter', 'Grand i10 Nios', 'i20', 'Aura', 'Verna', 
        'Alcazar', 'Creta Electric', 'i20 N Line', 'Creta N Line', 'Tucson', 
        'Venue N Line', 'Ioniq 5'
    ],
    'Tata': [
        'Nexon', 'Punch', 'Tiago', 'Altroz', 'Harrier', 'Curvv', 'Safari', 
        'Punch EV', 'Nexon EV', 'Harrier EV', 'Tiago EV', 'Tigor', 
        'Curvv EV', 'Tiago NRG', 'Tigor EV'
    ],
    'Mahindra': [
        'XUV700', 'Thar', 'Scorpio N', 'Scorpio Classic', 'XUV400', 'Bolero', 
        'Bolero Neo', 'XUV 3XO', 'BE 6e', 'XEV 9e', 'Marazzo'
    ],
    'Kia': [
        'Seltos', 'Sonet', 'Carens', 'EV6', 'EV9', 'Syros', 'Carens Clavis EV'
    ],
    'Honda': [
        'City', 'Amaze', 'City Hybrid', 'Elevate', 'CR-V'
    ],
    'Toyota': [
        'Innova Crysta', 'Fortuner', 'Urban Cruiser Hyryder', 'Glanza', 
        'Rumion', 'Land Cruiser', 'Hilux', 'Camry', 'Vellfire'
    ],
    'MG': [
        'Hector', 'Astor', 'ZS EV', 'Comet EV', 'Windsor EV', 'Hector Plus',
        'Gloster'
    ],
    'Skoda': [
        'Kushaq', 'Slavia', 'Kodiaq', 'Superb', 'Octavia'
    ],
    'Volkswagen': [
        'Taigun', 'Virtus', 'Tiguan', 'T-Roc'
    ],
    'Nissan': [
        'Magnite', 'X-Trail'
    ],
    'Renault': [
        'Kiger', 'Triber', 'Kwid'
    ],
    'Jeep': [
        'Compass', 'Meridian', 'Avenger'
    ],
    'Citroen': [
        'C3', 'C5 Aircross', 'C3 Aircross', 'eC3'
    ],
    'BYD': [
        'Atto 3', 'Seal'
    ]
}

# Vehicle Insurance Sample Data
def load_sample_data():
    if not st.session_state.cases:
        sample_cases = [
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Rajesh Kumar',
                'customer_phone': '+91-9876543210',
                'customer_email': 'rajesh.kumar@email.com',
                'vehicle_make': 'Maruti Suzuki',
                'vehicle_model': 'Swift',
                'vehicle_variant': 'VXi',
                'vehicle_year': 2020,
                'registration_number': 'MH12AB1234',
                'vehicle_type': 'Hatchback',
                'fuel_type': 'Petrol',
                'engine_capacity': '1197cc',
                'vehicle_value': 800000,
                'coverage_type': 'Comprehensive',
                'premium_amount': 15000,
                'status': 'Policy Issued',
                'created_date': datetime.now() - timedelta(days=15),
                'assigned_to': 'Priya Sharma',
                'follow_up_date': datetime.now() + timedelta(days=330),
                'policy_number': 'VEH-2024-001',
                'documents': ['RC Copy', 'Driving License', 'Previous Policy', 'Photos'],
                'step': 9
            },
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Anita Desai',
                'customer_phone': '+91-9876543211',
                'customer_email': 'anita.desai@email.com',
                'vehicle_make': 'Hyundai',
                'vehicle_model': 'Creta',
                'vehicle_variant': 'SX',
                'vehicle_year': 2023,
                'registration_number': 'DL08CB5678',
                'vehicle_type': 'SUV',
                'fuel_type': 'Diesel',
                'engine_capacity': '1493cc',
                'vehicle_value': 1500000,
                'coverage_type': 'Comprehensive',
                'premium_amount': 22000,
                'status': 'Quote Generated',
                'created_date': datetime.now() - timedelta(days=5),
                'assigned_to': 'Amit Singh',
                'follow_up_date': datetime.now() + timedelta(days=3),
                'documents': ['RC Copy', 'Driving License'],
                'step': 4
            },
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Mohammed Ali',
                'customer_phone': '+91-9876543212',
                'customer_email': 'mohammed.ali@email.com',
                'vehicle_make': 'Tata',
                'vehicle_model': 'Nexon',
                'vehicle_variant': 'XZ Plus',
                'vehicle_year': 2022,
                'registration_number': 'KA03MN9012',
                'vehicle_type': 'SUV',
                'fuel_type': 'Electric',
                'engine_capacity': 'Electric',
                'vehicle_value': 1200000,
                'coverage_type': 'Comprehensive',
                'premium_amount': 18000,
                'status': 'Documentation Pending',
                'created_date': datetime.now() - timedelta(days=2),
                'assigned_to': 'Sneha Patel',
                'follow_up_date': datetime.now() + timedelta(days=1),
                'documents': ['RC Copy', 'Driving License'],
                'step': 5
            },
            {
                'id': str(uuid.uuid4()),
                'customer_name': 'Lakshmi Nair',
                'customer_phone': '+91-9876543213',
                'customer_email': 'lakshmi.nair@email.com',
                'vehicle_make': 'Mahindra',
                'vehicle_model': 'XUV700',
                'vehicle_variant': 'AX7',
                'vehicle_year': 2024,
                'registration_number': 'TN22PQ3456',
                'vehicle_type': 'SUV',
                'fuel_type': 'Petrol',
                'engine_capacity': '1998cc',
                'vehicle_value': 2200000,
                'coverage_type': 'Comprehensive',
                'premium_amount': 28000,
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
                'vehicle_make': 'Honda',
                'vehicle_model': 'City',
                'vehicle_variant': 'V',
                'vehicle_year': 2019,
                'registration_number': 'AP09RS7890',
                'vehicle_type': 'Sedan',
                'fuel_type': 'Petrol',
                'engine_capacity': '1498cc',
                'vehicle_value': 900000,
                'coverage_type': 'Third Party',
                'premium_amount': 8000,
                'status': 'Policy Expired',
                'created_date': datetime.now() - timedelta(days=30),
                'assigned_to': 'Neha Gupta',
                'follow_up_date': None,
                'policy_number': 'VEH-2023-045',
                'documents': ['RC Copy', 'Driving License', 'Previous Policy', 'Photos'],
                'step': 9
            }
        ]
        st.session_state.cases.extend(sample_cases)

# Load sample data
load_sample_data()

# Header
st.markdown("""
<div class="app-header">
    <h1>🚗 CDrive Vehicle Insurance Management System</h1>
    <p>Comprehensive Vehicle Insurance • Case Management • Analytics</p>
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
    st.markdown("## 🚗 Vehicle Insurance Dashboard")
    
    # Key metrics
    total_cases = len(st.session_state.cases)
    active_cases = len([c for c in st.session_state.cases if c['status'] not in ['Policy Expired', 'Policy Issued']])
    total_premium = sum([c['premium_amount'] for c in st.session_state.cases])
    avg_case_value = total_premium / total_cases if total_cases > 0 else 0
    
    # Vehicle Insurance specific metrics
    comprehensive_policies = len([c for c in st.session_state.cases if c.get('coverage_type') == 'Comprehensive'])
    total_vehicle_value = sum([c.get('vehicle_value', 0) for c in st.session_state.cases])
    
    # Metrics cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--primary-color); margin: 0;">Total Policies</h3>
            <h2 style="margin: 0.5rem 0 0 0;">{}</h2>
        </div>
        """.format(total_cases), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--secondary-color); margin: 0;">Active Policies</h3>
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
            <h3 style="color: var(--success-color); margin: 0;">Comprehensive</h3>
            <h2 style="margin: 0.5rem 0 0 0;">{}</h2>
        </div>
        """.format(comprehensive_policies), unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--primary-color); margin: 0;">Insured Value</h3>
            <h2 style="margin: 0.5rem 0 0 0;">₹{:,.0f}L</h2>
        </div>
        """.format(total_vehicle_value/100000), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Policies by Status")
        if st.session_state.cases:
            status_counts = pd.DataFrame(st.session_state.cases)['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, 
                        color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
            fig.update_layout(showlegend=True, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🚗 Vehicle Brands")
        if st.session_state.cases:
            brand_counts = pd.DataFrame(st.session_state.cases)['vehicle_make'].value_counts()
            fig = px.bar(x=brand_counts.index, y=brand_counts.values,
                        color_discrete_sequence=['#667eea'])
            fig.update_layout(showlegend=False, height=300, xaxis_title="Vehicle Brand", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    # Vehicle type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚙 Vehicle Types")
        if st.session_state.cases:
            type_counts = pd.DataFrame(st.session_state.cases)['vehicle_type'].value_counts()
            fig = px.pie(values=type_counts.values, names=type_counts.index,
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
            fig.update_layout(showlegend=True, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⛽ Fuel Types")
        if st.session_state.cases:
            fuel_counts = pd.DataFrame(st.session_state.cases)['fuel_type'].value_counts()
            fig = px.bar(x=fuel_counts.index, y=fuel_counts.values,
                        color_discrete_sequence=['#FF9F43'])
            fig.update_layout(showlegend=False, height=300, xaxis_title="Fuel Type", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent cases table
    st.markdown("### 📋 Recent Vehicle Insurance Cases")
    if st.session_state.cases:
        recent_cases = sorted(st.session_state.cases, key=lambda x: x['created_date'], reverse=True)[:5]
        
        for case in recent_cases:
            status_class = {
                'New Lead': 'status-new',
                'Quote Generated': 'status-quote', 
                'Policy Issued': 'status-policy',
                'Policy Expired': 'status-closed',
                'Documentation Pending': 'status-new'
            }.get(case['status'], 'status-new')
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h4 style="margin: 0; color: var(--primary-color);">{case['customer_name']}</h4>
                        <p style="margin: 0.25rem 0; color: #666;">{case['vehicle_make']} {case['vehicle_model']} ({case['vehicle_year']}) • ₹{case['premium_amount']:,.0f}</p>
                        <p style="margin: 0.25rem 0; color: #888; font-size: 0.9rem;">{case['registration_number']} • {case['coverage_type']}</p>
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
    st.markdown("## ➕ Create New Vehicle Insurance Case")
    
    # Case creation steps
    steps = [
        "Customer Details",
        "Vehicle Details", 
        "Coverage Options",
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
    st.markdown("### 🚗 Step 2: Vehicle Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Vehicle Make
        vehicle_make = st.selectbox(
            "Vehicle Make *",
            list(CAR_DATA.keys()),
            index=list(CAR_DATA.keys()).index(st.session_state.current_case.get('vehicle_make', list(CAR_DATA.keys())[0]))
        )
        
        # Vehicle Model (depends on make)
        available_models = CAR_DATA.get(vehicle_make, [])
        vehicle_model = st.selectbox(
            "Vehicle Model *",
            available_models,
            index=available_models.index(st.session_state.current_case.get('vehicle_model', available_models[0])) if st.session_state.current_case.get('vehicle_model') in available_models else 0
        )
        
        # Vehicle Variant
        variants = ["Base", "Mid", "Top", "LXi", "VXi", "ZXi", "S", "SX", "SX(O)", "E", "S+", "XE", "XM", "XT", "XZ", "XZ+"]
        vehicle_variant = st.selectbox(
            "Vehicle Variant",
            variants,
            index=variants.index(st.session_state.current_case.get('vehicle_variant', 'S')) if st.session_state.current_case.get('vehicle_variant') in variants else 0
        )
        
        # Manufacturing Year
        current_year = datetime.now().year
        vehicle_year = st.selectbox(
            "Manufacturing Year *",
            list(range(current_year, current_year - 25, -1)),
            index=list(range(current_year, current_year - 25, -1)).index(st.session_state.current_case.get('vehicle_year', current_year - 2)) if st.session_state.current_case.get('vehicle_year') in list(range(current_year, current_year - 25, -1)) else 2
        )
        
        # Registration Number
        registration_number = st.text_input(
            "Registration Number *",
            value=st.session_state.current_case.get('registration_number', ''),
            placeholder="e.g. MH12AB1234"
        )
    
    with col2:
        # Vehicle Type
        vehicle_types = ["Hatchback", "Sedan", "SUV", "MUV/MPV", "Coupe", "Convertible", "Pickup Truck", "Van"]
        vehicle_type = st.selectbox(
            "Vehicle Type *",
            vehicle_types,
            index=vehicle_types.index(st.session_state.current_case.get('vehicle_type', 'Hatchback')) if st.session_state.current_case.get('vehicle_type') in vehicle_types else 0
        )
        
        # Fuel Type  
        fuel_types = ["Petrol", "Diesel", "CNG", "Electric", "Hybrid", "LPG"]
        fuel_type = st.selectbox(
            "Fuel Type *",
            fuel_types,
            index=fuel_types.index(st.session_state.current_case.get('fuel_type', 'Petrol')) if st.session_state.current_case.get('fuel_type') in fuel_types else 0
        )
        
        # Engine Capacity
        if fuel_type == "Electric":
            engine_capacity = st.selectbox("Power", ["Electric", "50kW", "100kW", "150kW", "200kW+"])
        else:
            engine_capacity = st.text_input(
                "Engine Capacity",
                value=st.session_state.current_case.get('engine_capacity', ''),
                placeholder="e.g. 1197cc"
            )
        
        # Vehicle Value
        vehicle_value = st.number_input(
            "Current Vehicle Value (₹) *",
            min_value=50000,
            max_value=50000000,
            value=st.session_state.current_case.get('vehicle_value', 500000),
            step=25000
        )
        
        # RTO Location
        rto_location = st.text_input(
            "RTO Location",
            value=st.session_state.current_case.get('rto_location', ''),
            placeholder="e.g. Mumbai Central"
        )
    
    # Previous Insurance Details
    st.markdown("#### Previous Insurance Details")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        has_previous_insurance = st.checkbox(
            "Has Previous Insurance",
            value=st.session_state.current_case.get('has_previous_insurance', False)
        )
    
    with col2:
        if has_previous_insurance:
            previous_insurer = st.text_input(
                "Previous Insurer",
                value=st.session_state.current_case.get('previous_insurer', '')
            )
    
    with col3:
        if has_previous_insurance:
            ncb_percentage = st.selectbox(
                "No Claim Bonus (%)",
                [0, 20, 25, 35, 45, 50],
                index=[0, 20, 25, 35, 45, 50].index(st.session_state.current_case.get('ncb_percentage', 0))
            )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step2_prev'):
            st.session_state.case_step = 1
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step2_next'):
            if vehicle_make and vehicle_model and vehicle_year and registration_number and vehicle_value:
                st.session_state.current_case.update({
                    'vehicle_make': vehicle_make,
                    'vehicle_model': vehicle_model,
                    'vehicle_variant': vehicle_variant,
                    'vehicle_year': vehicle_year,
                    'registration_number': registration_number.upper(),
                    'vehicle_type': vehicle_type,
                    'fuel_type': fuel_type,
                    'engine_capacity': engine_capacity,
                    'vehicle_value': vehicle_value,
                    'rto_location': rto_location,
                    'has_previous_insurance': has_previous_insurance,
                    'previous_insurer': previous_insurer if has_previous_insurance else '',
                    'ncb_percentage': ncb_percentage if has_previous_insurance else 0
                })
                st.session_state.case_step = 3
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")

def render_coverage_requirements_step():
    st.markdown("### 🛡️ Step 3: Insurance Coverage Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Coverage Type
        coverage_types = ["Third Party", "Comprehensive"]
        coverage_type = st.selectbox(
            "Coverage Type *",
            coverage_types,
            index=coverage_types.index(st.session_state.current_case.get('coverage_type', 'Comprehensive'))
        )
        
        if coverage_type == "Comprehensive":
            st.info("Comprehensive coverage includes third-party liability, own damage, theft, and natural calamities")
        else:
            st.warning("Third Party coverage only covers damage to third parties. Own damage not covered.")
        
        # Deductible (only for comprehensive)
        if coverage_type == "Comprehensive":
            deductible_amounts = [0, 1000, 2500, 5000, 7500, 10000, 15000]
            deductible = st.selectbox(
                "Voluntary Deductible (₹)",
                deductible_amounts,
                index=deductible_amounts.index(st.session_state.current_case.get('deductible', 0))
            )
            st.info("Higher deductible = Lower premium")
        else:
            deductible = 0
    
    with col2:
        # Policy Duration
        policy_durations = ["1 Year", "2 Years", "3 Years"]
        policy_duration = st.selectbox(
            "Policy Duration *",
            policy_durations,
            index=policy_durations.index(st.session_state.current_case.get('policy_duration', '1 Year'))
        )
        
        # IDV (Insured Declared Value) - Auto calculated but can be adjusted
        vehicle_value = st.session_state.current_case.get('vehicle_value', 500000)
        vehicle_year = st.session_state.current_case.get('vehicle_year', datetime.now().year)
        
        # Calculate depreciation-adjusted IDV
        current_year = datetime.now().year
        age = current_year - vehicle_year
        depreciation_rates = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20, 5: 25}
        depreciation = depreciation_rates.get(age, 30 + (age - 5) * 5)  # 5% additional per year after 5 years
        suggested_idv = vehicle_value * (100 - depreciation) / 100
        
        idv = st.number_input(
            f"IDV - Insured Declared Value (₹)",
            min_value=int(suggested_idv * 0.8),
            max_value=int(suggested_idv * 1.2),
            value=int(suggested_idv),
            step=5000,
            help=f"Suggested IDV based on {age} year old vehicle with {depreciation}% depreciation"
        )
    
    # Add-on Covers (only for comprehensive)
    if coverage_type == "Comprehensive":
        st.markdown("#### Add-on Covers")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            zero_depreciation = st.checkbox(
                "Zero Depreciation Cover",
                value=st.session_state.current_case.get('zero_depreciation', False),
                help="No depreciation deduction on parts during claim settlement"
            )
            
            engine_protect = st.checkbox(
                "Engine Protection Cover",
                value=st.session_state.current_case.get('engine_protect', False),
                help="Covers damage due to water ingress, oil leakage"
            )
        
        with col2:
            roadside_assistance = st.checkbox(
                "24x7 Roadside Assistance",
                value=st.session_state.current_case.get('roadside_assistance', False),
                help="Towing, battery jumpstart, flat tire assistance"
            )
            
            consumables_cover = st.checkbox(
                "Consumables Cover",
                value=st.session_state.current_case.get('consumables_cover', False),
                help="Covers engine oil, brake oil, other consumables"
            )
        
        with col3:
            key_replacement = st.checkbox(
                "Key Replacement Cover",
                value=st.session_state.current_case.get('key_replacement', False),
                help="Covers cost of key/lock replacement if lost"
            )
            
            return_invoice = st.checkbox(
                "Return to Invoice Cover",
                value=st.session_state.current_case.get('return_invoice', False),
                help="Pay invoice value in case of total loss/theft"
            )
    
    # Driver Details
    st.markdown("#### Driver Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        driver_age = st.selectbox(
            "Primary Driver Age",
            ["18-25 years", "26-35 years", "36-50 years", "50+ years"],
            index=["18-25 years", "26-35 years", "36-50 years", "50+ years"].index(st.session_state.current_case.get('driver_age', '26-35 years'))
        )
    
    with col2:
        driving_experience = st.selectbox(
            "Driving Experience",
            ["< 1 year", "1-3 years", "3-5 years", "5+ years"],
            index=["< 1 year", "1-3 years", "3-5 years", "5+ years"].index(st.session_state.current_case.get('driving_experience', '1-3 years'))
        )
    
    with col3:
        any_claim = st.checkbox(
            "Any claim in last 3 years?",
            value=st.session_state.current_case.get('any_claim', False)
        )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step3_prev'):
            st.session_state.case_step = 2
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step3_next'):
            coverage_data = {
                'coverage_type': coverage_type,
                'deductible': deductible,
                'policy_duration': policy_duration,
                'idv': idv,
                'driver_age': driver_age,
                'driving_experience': driving_experience,
                'any_claim': any_claim
            }
            
            if coverage_type == "Comprehensive":
                coverage_data.update({
                    'zero_depreciation': zero_depreciation,
                    'engine_protect': engine_protect,
                    'roadside_assistance': roadside_assistance,
                    'consumables_cover': consumables_cover,
                    'key_replacement': key_replacement,
                    'return_invoice': return_invoice
                })
            
            st.session_state.current_case.update(coverage_data)
            st.session_state.case_step = 4
            st.rerun()

def render_quote_generation_step():
    st.markdown("### 💵 Step 4: Vehicle Insurance Quote Generation")
    
    # Get current case data
    case = st.session_state.current_case
    idv = case.get('idv', 500000)
    coverage_type = case.get('coverage_type', 'Comprehensive')
    vehicle_type = case.get('vehicle_type', 'Hatchback')
    fuel_type = case.get('fuel_type', 'Petrol')
    driver_age = case.get('driver_age', '26-35 years')
    ncb_percentage = case.get('ncb_percentage', 0)
    deductible = case.get('deductible', 0)
    
    # Base premium calculation for vehicle insurance
    if coverage_type == "Third Party":
        # Third party rates based on engine capacity
        engine_capacity = case.get('engine_capacity', '1197cc')
        if fuel_type == "Electric":
            base_premium = 3000
        elif 'cc' in str(engine_capacity):
            cc = int(''.join(filter(str.isdigit, str(engine_capacity))))
            if cc <= 1000:
                base_premium = 2072
            elif cc <= 1500:
                base_premium = 3221
            else:
                base_premium = 7890
        else:
            base_premium = 3221
    else:
        # Comprehensive insurance calculation
        base_rate = 0.025  # 2.5% of IDV
        
        # Vehicle type multiplier
        vehicle_multipliers = {
            'Hatchback': 1.0,
            'Sedan': 1.1,
            'SUV': 1.3,
            'MUV/MPV': 1.2,
            'Coupe': 1.4,
            'Convertible': 1.5,
            'Pickup Truck': 1.1,
            'Van': 1.1
        }
        
        # Fuel type multiplier
        fuel_multipliers = {
            'Petrol': 1.0,
            'Diesel': 1.05,
            'CNG': 0.95,
            'Electric': 0.9,
            'Hybrid': 0.95,
            'LPG': 0.95
        }
        
        # Driver age multiplier
        age_multipliers = {
            '18-25 years': 1.3,
            '26-35 years': 1.0,
            '36-50 years': 0.95,
            '50+ years': 1.1
        }
        
        base_premium = idv * base_rate * vehicle_multipliers.get(vehicle_type, 1.0) * fuel_multipliers.get(fuel_type, 1.0) * age_multipliers.get(driver_age, 1.0)
        
        # Apply NCB discount
        base_premium = base_premium * (100 - ncb_percentage) / 100
        
        # Apply voluntary deductible discount
        if deductible > 0:
            deductible_discount = min(deductible / 10000 * 5, 15)  # Max 15% discount
            base_premium = base_premium * (100 - deductible_discount) / 100
    
    # Generate quote options
    quotes = []
    
    if coverage_type == "Third Party":
        quotes.append({
            'name': 'Third Party Only',
            'premium': base_premium,
            'features': [
                'Third Party Liability Coverage',
                'Legal Compliance',
                'Covers injury/death to third parties',
                'Property damage to third parties'
            ],
            'coverage_amount': 'Unlimited Third Party Liability'
        })
    else:
        # Basic Comprehensive
        basic_premium = base_premium
        quotes.append({
            'name': 'Basic Comprehensive',
            'premium': basic_premium,
            'features': [
                'Own Damage Coverage',
                'Third Party Liability',
                'Theft Protection',
                'Natural Calamity Coverage'
            ],
            'coverage_amount': f'IDV: ₹{idv:,}'
        })
        
        # Standard Comprehensive with add-ons
        standard_premium = basic_premium * 1.25
        standard_features = [
            'Own Damage Coverage',
            'Third Party Liability', 
            'Theft Protection',
            'Natural Calamity Coverage',
            '24x7 Roadside Assistance',
            'Engine Protection Cover'
        ]
        if case.get('roadside_assistance'): standard_features.append('✓ Selected: Roadside Assistance')
        if case.get('engine_protect'): standard_features.append('✓ Selected: Engine Protection')
        
        quotes.append({
            'name': 'Standard Comprehensive',
            'premium': standard_premium,
            'features': standard_features,
            'coverage_amount': f'IDV: ₹{idv:,}'
        })
        
        # Premium Comprehensive with all add-ons
        premium_premium = basic_premium * 1.6
        premium_features = [
            'Own Damage Coverage',
            'Third Party Liability',
            'Theft Protection', 
            'Natural Calamity Coverage',
            '24x7 Roadside Assistance',
            'Engine Protection Cover',
            'Zero Depreciation Cover',
            'Consumables Cover',
            'Key Replacement Cover',
            'Return to Invoice Cover'
        ]
        
        # Mark selected add-ons
        if case.get('zero_depreciation'): premium_features.append('✓ Selected: Zero Depreciation')
        if case.get('consumables_cover'): premium_features.append('✓ Selected: Consumables')
        if case.get('key_replacement'): premium_features.append('✓ Selected: Key Replacement')
        if case.get('return_invoice'): premium_features.append('✓ Selected: Return to Invoice')
        
        quotes.append({
            'name': 'Premium Comprehensive',
            'premium': premium_premium,
            'features': premium_features,
            'coverage_amount': f'IDV: ₹{idv:,}'
        })
    
    st.markdown("#### Available Vehicle Insurance Quotes")
    
    # Display vehicle summary
    vehicle_info = f"{case.get('vehicle_make', '')} {case.get('vehicle_model', '')} {case.get('vehicle_variant', '')} ({case.get('vehicle_year', '')})"
    st.info(f"🚗 **Vehicle:** {vehicle_info} | **Registration:** {case.get('registration_number', '')} | **IDV:** ₹{idv:,}")
    
    selected_quote = None
    for i, quote in enumerate(quotes):
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{quote['name']}**")
                st.markdown(f"*{quote['coverage_amount']}*")
                for feature in quote['features'][:6]:  # Show first 6 features
                    if '✓ Selected:' in feature:
                        st.markdown(f"🟢 {feature}")
                    else:
                        st.markdown(f"• {feature}")
                if len(quote['features']) > 6:
                    with st.expander("View all features"):
                        for feature in quote['features'][6:]:
                            if '✓ Selected:' in feature:
                                st.markdown(f"🟢 {feature}")
                            else:
                                st.markdown(f"• {feature}")
            
            with col2:
                st.markdown(f"**Annual Premium: ₹{quote['premium']:,.0f}**")
                if case.get('policy_duration') == '2 Years':
                    st.markdown(f"2-Year Premium: ₹{quote['premium'] * 1.85:,.0f}")
                elif case.get('policy_duration') == '3 Years': 
                    st.markdown(f"3-Year Premium: ₹{quote['premium'] * 2.7:,.0f}")
                
                if ncb_percentage > 0:
                    st.markdown(f"🎉 NCB Discount: {ncb_percentage}% applied")
                if deductible > 0:
                    st.markdown(f"💰 Voluntary Deductible: ₹{deductible}")
            
            with col3:
                if st.button(f"Select", key=f'quote_{i}'):
                    selected_quote = quote
                    st.session_state.current_case['selected_quote'] = quote
                    st.session_state.current_case['premium_amount'] = quote['premium']
                    st.success(f"{quote['name']} selected!")
    
    if 'selected_quote' in st.session_state.current_case:
        st.success(f"✅ Selected: {st.session_state.current_case['selected_quote']['name']} - ₹{st.session_state.current_case['premium_amount']:,.0f}/year")
    
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
    st.markdown("### 📄 Step 5: Vehicle Insurance Document Collection")
    
    # Required documents for vehicle insurance
    required_docs = [
        'Registration Certificate (RC)',
        'Valid Driving License',
        'Previous Insurance Policy',
        'Vehicle Photos (4 angles)',
        'Identity Proof (Aadhar/Passport)',
        'Address Proof',
        'Pollution Under Control (PUC) Certificate'
    ]
    
    # Additional documents based on case specifics
    additional_docs = []
    
    # If commercial vehicle
    vehicle_type = st.session_state.current_case.get('vehicle_type', 'Hatchback')
    if 'commercial' in vehicle_type.lower():
        additional_docs.extend(['Commercial License', 'Fitness Certificate'])
    
    # If financed vehicle
    is_financed = st.checkbox("Is this vehicle financed/on loan?")
    if is_financed:
        additional_docs.extend(['Loan Agreement', 'NOC from Financier'])
        st.session_state.current_case['is_financed'] = True
    
    # If first-time buyer (no previous insurance)
    has_previous_insurance = st.session_state.current_case.get('has_previous_insurance', False)
    if not has_previous_insurance:
        additional_docs = [doc for doc in additional_docs if 'Previous Insurance' not in doc]
        required_docs = [doc for doc in required_docs if 'Previous Insurance' not in doc]
        additional_docs.append('Vehicle Invoice/Bill of Sale')
    
    all_docs = required_docs + additional_docs
    
    st.markdown(f"#### Required Documents for Vehicle Insurance")
    
    # Vehicle details summary
    vehicle_info = f"{st.session_state.current_case.get('vehicle_make', '')} {st.session_state.current_case.get('vehicle_model', '')} ({st.session_state.current_case.get('vehicle_year', '')})"
    reg_no = st.session_state.current_case.get('registration_number', '')
    st.info(f"🚗 **Vehicle:** {vehicle_info} | **Registration:** {reg_no}")
    
    collected_docs = []
    col1, col2 = st.columns(2)
    
    for i, doc in enumerate(all_docs):
        with col1 if i % 2 == 0 else col2:
            if st.checkbox(f"{doc}", key=f'doc_{doc}'):
                collected_docs.append(doc)
                
            # Special instructions for specific documents
            if doc == 'Vehicle Photos (4 angles)' and doc in collected_docs:
                st.caption("📸 Required: Front, Rear, Left Side, Right Side")
            elif doc == 'Registration Certificate (RC)' and doc in collected_docs:
                st.caption("📋 Both sides of RC required")
            elif doc == 'Valid Driving License' and doc in collected_docs:
                st.caption("🪪 Valid DL of primary driver")
    
    # Document upload simulation
    st.markdown("#### Document Upload")
    uploaded_files = st.file_uploader(
        "Upload Vehicle Insurance Documents", 
        accept_multiple_files=True,
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Upload scanned copies or photos of required documents"
    )
    
    if uploaded_files:
        st.success(f"📎 Uploaded {len(uploaded_files)} document(s)")
        for file in uploaded_files:
            file_size = len(file.read()) / 1024  # Size in KB
            st.markdown(f"• **{file.name}** ({file_size:.1f} KB)")
    
    # Document verification checklist
    st.markdown("#### Document Verification Checklist")
    verification_items = [
        "RC matches vehicle details entered",
        "DL is valid and not expired", 
        "Vehicle photos are clear and show damage (if any)",
        "Previous policy shows NCB eligibility",
        "All documents are clearly readable"
    ]
    
    verified_items = []
    for item in verification_items:
        if st.checkbox(item, key=f'verify_{item}'):
            verified_items.append(item)
    
    # Document status
    completion_rate = len(collected_docs) / len(all_docs) * 100
    verification_rate = len(verified_items) / len(verification_items) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents Collected", f"{len(collected_docs)}/{len(all_docs)}")
        st.progress(completion_rate / 100)
    
    with col2:
        st.metric("Verification Complete", f"{len(verified_items)}/{len(verification_items)}")
        st.progress(verification_rate / 100)
    
    # Document status summary
    if completion_rate == 100:
        st.success("✅ All required documents collected!")
    elif completion_rate >= 80:
        st.warning(f"⚠️ {completion_rate:.0f}% documents collected - Almost complete!")
    else:
        st.error(f"❌ Only {completion_rate:.0f}% documents collected - More documents needed")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step5_prev'):
            st.session_state.case_step = 4
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step5_next'):
            st.session_state.current_case.update({
                'documents': collected_docs,
                'verified_items': verified_items,
                'is_financed': is_financed,
                'document_completion_rate': completion_rate
            })
            st.session_state.case_step = 6
            st.rerun()

def render_policy_finalization_step():
    st.markdown("### ✅ Step 6: Vehicle Insurance Policy Finalization")
    
    # Summary of case details
    case = st.session_state.current_case
    
    st.markdown("#### Vehicle Insurance Policy Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Customer Information**")
        st.markdown(f"• **Name:** {case.get('customer_name', 'N/A')}")
        st.markdown(f"• **Phone:** {case.get('customer_phone', 'N/A')}")
        st.markdown(f"• **Email:** {case.get('customer_email', 'N/A')}")
        
        st.markdown("**Vehicle Details**")
        vehicle_info = f"{case.get('vehicle_make', 'N/A')} {case.get('vehicle_model', 'N/A')} {case.get('vehicle_variant', '')}"
        st.markdown(f"• **Vehicle:** {vehicle_info}")
        st.markdown(f"• **Year:** {case.get('vehicle_year', 'N/A')}")
        st.markdown(f"• **Registration:** {case.get('registration_number', 'N/A')}")
        st.markdown(f"• **Fuel Type:** {case.get('fuel_type', 'N/A')}")
        st.markdown(f"• **Engine:** {case.get('engine_capacity', 'N/A')}")
    
    with col2:
        st.markdown("**Insurance Coverage**")
        st.markdown(f"• **Coverage Type:** {case.get('coverage_type', 'N/A')}")
        st.markdown(f"• **IDV:** ₹{case.get('idv', 0):,.0f}")
        st.markdown(f"• **Policy Duration:** {case.get('policy_duration', 'N/A')}")
        if case.get('deductible', 0) > 0:
            st.markdown(f"• **Voluntary Deductible:** ₹{case.get('deductible'):,.0f}")
        
        st.markdown("**Premium Information**")
        if 'selected_quote' in case:
            st.markdown(f"• **Plan:** {case['selected_quote']['name']}")
        st.markdown(f"• **Annual Premium:** ₹{case.get('premium_amount', 0):,.0f}")
        
        # Calculate premium for multi-year policies
        duration = case.get('policy_duration', '1 Year')
        if duration == '2 Years':
            total_premium = case.get('premium_amount', 0) * 1.85
            st.markdown(f"• **2-Year Premium:** ₹{total_premium:,.0f}")
        elif duration == '3 Years':
            total_premium = case.get('premium_amount', 0) * 2.7  
            st.markdown(f"• **3-Year Premium:** ₹{total_premium:,.0f}")
    
    # Add-on covers summary
    if case.get('coverage_type') == 'Comprehensive':
        st.markdown("**Add-on Covers Selected**")
        addons = []
        if case.get('zero_depreciation'): addons.append('Zero Depreciation Cover')
        if case.get('engine_protect'): addons.append('Engine Protection Cover')
        if case.get('roadside_assistance'): addons.append('24x7 Roadside Assistance')
        if case.get('consumables_cover'): addons.append('Consumables Cover')
        if case.get('key_replacement'): addons.append('Key Replacement Cover')
        if case.get('return_invoice'): addons.append('Return to Invoice Cover')
        
        if addons:
            for addon in addons:
                st.markdown(f"• ✅ {addon}")
        else:
            st.markdown("• No add-on covers selected")
    
    # NCB and discounts
    if case.get('ncb_percentage', 0) > 0:
        st.markdown(f"**No Claim Bonus:** {case.get('ncb_percentage')}% discount applied")
    
    # Documentation status
    st.markdown("**Documentation Status**")
    docs = case.get('documents', [])
    completion_rate = case.get('document_completion_rate', 0)
    st.markdown(f"• **Documents Collected:** {len(docs)} ({completion_rate:.0f}% complete)")
    
    if completion_rate >= 80:
        for doc in docs[:5]:  # Show first 5 documents
            st.markdown(f"  ✓ {doc}")
        if len(docs) > 5:
            st.markdown(f"  ... and {len(docs) - 5} more documents")
    
    # Important policy terms
    st.markdown("#### Important Policy Terms & Conditions")
    
    terms = [
        f"Policy covers vehicle {case.get('registration_number', '')} for {case.get('coverage_type', 'Comprehensive').lower()} insurance",
        f"Insured Declared Value (IDV) is ₹{case.get('idv', 0):,}",
        "Premium must be paid before policy inception",
        "Policy is subject to terms and conditions of the insurance company",
        "Claims must be intimated within 48 hours of incident"
    ]
    
    if case.get('deductible', 0) > 0:
        terms.append(f"Voluntary deductible of ₹{case.get('deductible'):,} applies to own damage claims")
    
    if case.get('coverage_type') == 'Third Party':
        terms.append("Policy covers ONLY third party liability - own damage not covered")
    
    for term in terms:
        st.markdown(f"• {term}")
    
    # Terms and conditions acceptance
    terms_accepted = st.checkbox("I have read and agree to the terms and conditions of the vehicle insurance policy")
    
    # Executive assignment
    st.markdown("#### Assignment")
    executives = ["Priya Sharma", "Amit Singh", "Sneha Patel", "Rahul Verma", "Neha Gupta", "Rohit Kumar", "Kavita Jain"]
    assigned_to = st.selectbox("Assign to Executive", executives)
    
    # Pre-policy checklist
    st.markdown("#### Pre-Policy Issuance Checklist")
    checklist_items = [
        "Vehicle details verified from RC",
        "Customer identity confirmed",
        "Premium calculation reviewed",
        "Add-on covers confirmed with customer",
        "Payment method confirmed"
    ]
    
    completed_checks = []
    for item in checklist_items:
        if st.checkbox(item, key=f'check_{item}'):
            completed_checks.append(item)
    
    all_checks_done = len(completed_checks) == len(checklist_items)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Previous", key='step6_prev'):
            st.session_state.case_step = 5
            st.rerun()
    with col3:
        if st.button("Next Step →", key='step6_next'):
            if terms_accepted and all_checks_done:
                st.session_state.current_case.update({
                    'assigned_to': assigned_to,
                    'terms_accepted': True,
                    'pre_policy_checks': completed_checks
                })
                st.session_state.case_step = 7
                st.rerun()
            else:
                if not terms_accepted:
                    st.error("Please accept the terms and conditions")
                if not all_checks_done:
                    st.error("Please complete all pre-policy checklist items")

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
    st.markdown("### 🚗 Step 8: Vehicle Insurance Policy Issuance")
    
    case = st.session_state.current_case
    
    # Generate policy number
    if 'policy_number' not in case:
        policy_number = f"VEH-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.cases) + 1:04d}"
        st.session_state.current_case['policy_number'] = policy_number
    
    st.markdown("#### Vehicle Insurance Policy Generated Successfully! 🎉")
    
    # Policy certificate display
    st.markdown("""
    <div style="border: 2px solid #2E86AB; border-radius: 10px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); margin: 20px 0;">
        <h3 style="text-align: center; color: #2E86AB; margin: 0;">🚗 VEHICLE INSURANCE POLICY CERTIFICATE</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Policy Information**")
        st.markdown(f"• **Policy Number:** {case.get('policy_number')}")
        st.markdown(f"• **Issue Date:** {datetime.now().strftime('%d %b %Y')}")
        st.markdown(f"• **Effective Date:** {datetime.now().strftime('%d %b %Y')}")
        
        # Calculate policy end date based on duration
        duration = case.get('policy_duration', '1 Year')
        if duration == '1 Year':
            end_date = datetime.now() + timedelta(days=365)
        elif duration == '2 Years':
            end_date = datetime.now() + timedelta(days=730)
        elif duration == '3 Years':
            end_date = datetime.now() + timedelta(days=1095)
        else:
            end_date = datetime.now() + timedelta(days=365)
            
        st.markdown(f"• **Expiry Date:** {end_date.strftime('%d %b %Y')}")
        
        st.markdown("**Vehicle Details**")
        vehicle_info = f"{case.get('vehicle_make', '')} {case.get('vehicle_model', '')} {case.get('vehicle_variant', '')}"
        st.markdown(f"• **Vehicle:** {vehicle_info}")
        st.markdown(f"• **Year:** {case.get('vehicle_year', 'N/A')}")
        st.markdown(f"• **Registration:** {case.get('registration_number', 'N/A')}")
        st.markdown(f"• **Engine:** {case.get('engine_capacity', 'N/A')}")
        st.markdown(f"• **Fuel Type:** {case.get('fuel_type', 'N/A')}")
    
    with col2:
        st.markdown("**Coverage Summary**")
        st.markdown(f"• **Coverage Type:** {case.get('coverage_type', 'Comprehensive')}")
        st.markdown(f"• **IDV (Insured Declared Value):** ₹{case.get('idv', 0):,.0f}")
        if case.get('deductible', 0) > 0:
            st.markdown(f"• **Voluntary Deductible:** ₹{case.get('deductible'):,.0f}")
        
        st.markdown("**Premium Details**")
        st.markdown(f"• **Annual Premium:** ₹{case.get('premium_amount', 0):,.0f}")
        if case.get('ncb_percentage', 0) > 0:
            st.markdown(f"• **NCB Applied:** {case.get('ncb_percentage')}%")
        
        # Next premium due calculation
        next_due = datetime.now() + timedelta(days=365)
        st.markdown(f"• **Next Premium Due:** {next_due.strftime('%d %b %Y')}")
        
        st.markdown("**Customer Details**")
        st.markdown(f"• **Policyholder:** {case.get('customer_name', 'N/A')}")
        st.markdown(f"• **Contact:** {case.get('customer_phone', 'N/A')}")
        st.markdown(f"• **Email:** {case.get('customer_email', 'N/A')}")
    
    # Add-on covers (if any)
    if case.get('coverage_type') == 'Comprehensive':
        addons = []
        if case.get('zero_depreciation'): addons.append('Zero Depreciation Cover')
        if case.get('engine_protect'): addons.append('Engine Protection Cover')
        if case.get('roadside_assistance'): addons.append('24x7 Roadside Assistance')
        if case.get('consumables_cover'): addons.append('Consumables Cover')
        if case.get('key_replacement'): addons.append('Key Replacement Cover')
        if case.get('return_invoice'): addons.append('Return to Invoice Cover')
        
        if addons:
            st.markdown("**Add-on Covers Included**")
            for addon in addons:
                st.markdown(f"• ✅ {addon}")
    
    # Important policy information
    st.markdown("#### 🔔 Important Policy Information")
    st.info("""
    **Key Points to Remember:**
    • Keep this policy number safe for all future communications
    • Claims must be intimated within 48 hours of incident
    • Policy documents will be sent to your registered email
    • Premium payment receipt will be generated separately
    • For claims assistance: Call 1800-XXX-XXXX (24x7)
    """)
    
    # Policy document generation
    st.markdown("#### Policy Document Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📄 Download Policy PDF", key='download_policy'):
            st.success("Policy PDF downloaded!")
            st.balloons()
    with col2:
        if st.button("📧 Email to Customer", key='email_policy'):
            st.success(f"Policy emailed to {case.get('customer_email')}")
    with col3:
        if st.button("📱 SMS Confirmation", key='sms_policy'):
            st.success(f"SMS sent to {case.get('customer_phone')}")
    with col4:
        if st.button("🖨️ Print Policy", key='print_policy'):
            st.success("Policy sent to printer")
    
    # Generate insurance card
    st.markdown("#### 🪪 Digital Insurance Card")
    
    # Create a mock insurance card
    st.markdown(f"""
    <div style="
        border: 2px solid #2E86AB; 
        border-radius: 10px; 
        padding: 15px; 
        background: white;
        width: 400px;
        margin: 10px auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-family: monospace;
    ">
        <div style="text-align: center; font-weight: bold; color: #2E86AB; margin-bottom: 10px;">
            🚗 VEHICLE INSURANCE CARD
        </div>
        <div style="font-size: 12px;">
            <strong>Policy:</strong> {case.get('policy_number', '')}<br>
            <strong>Vehicle:</strong> {case.get('registration_number', '')}<br>
            <strong>Valid:</strong> {datetime.now().strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}<br>
            <strong>IDV:</strong> ₹{case.get('idv', 0):,.0f}<br>
            <strong>Coverage:</strong> {case.get('coverage_type', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📱 Generate Digital Card", key='digital_card'):
        st.success("Digital insurance card generated and sent to customer's mobile")
    
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
    st.markdown("## 🚗 Manage Vehicle Insurance Cases")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All"] + list(set([case['status'] for case in st.session_state.cases])))
    
    with col2:
        make_filter = st.selectbox("Filter by Vehicle Make",
                                 ["All"] + list(set([case.get('vehicle_make', 'Unknown') for case in st.session_state.cases])))
    
    with col3:
        assigned_filter = st.selectbox("Filter by Executive",
                                     ["All"] + list(set([case['assigned_to'] for case in st.session_state.cases])))
    
    with col4:
        coverage_filter = st.selectbox("Filter by Coverage", 
                                     ["All", "Comprehensive", "Third Party"])
    
    # Apply filters
    filtered_cases = st.session_state.cases.copy()
    
    if status_filter != "All":
        filtered_cases = [case for case in filtered_cases if case['status'] == status_filter]
    
    if make_filter != "All":
        filtered_cases = [case for case in filtered_cases if case.get('vehicle_make') == make_filter]
    
    if assigned_filter != "All":
        filtered_cases = [case for case in filtered_cases if case['assigned_to'] == assigned_filter]
        
    if coverage_filter != "All":
        filtered_cases = [case for case in filtered_cases if case.get('coverage_type') == coverage_filter]
    
    # Cases table
    if filtered_cases:
        st.markdown(f"### Found {len(filtered_cases)} vehicle insurance case(s)")
        
        for i, case in enumerate(filtered_cases):
            # Prepare vehicle info
            vehicle_info = f"{case.get('vehicle_make', 'Unknown')} {case.get('vehicle_model', 'Unknown')} ({case.get('vehicle_year', 'Unknown')})"
            coverage_info = case.get('coverage_type', 'Unknown')
            if case.get('idv'):
                coverage_info += f" - IDV: ₹{case.get('idv'):,.0f}"
            
            with st.expander(f"🚗 {case['customer_name']} - {vehicle_info} - {case['status']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Customer Details**")
                    st.markdown(f"• **Name:** {case['customer_name']}")
                    st.markdown(f"• **Phone:** {case['customer_phone']}")
                    st.markdown(f"• **Email:** {case['customer_email']}")
                    
                    st.markdown("**Vehicle Details**") 
                    st.markdown(f"• **Make/Model:** {case.get('vehicle_make', 'N/A')} {case.get('vehicle_model', 'N/A')}")
                    st.markdown(f"• **Year:** {case.get('vehicle_year', 'N/A')}")
                    st.markdown(f"• **Registration:** {case.get('registration_number', 'N/A')}")
                    st.markdown(f"• **Fuel Type:** {case.get('fuel_type', 'N/A')}")
                
                with col2:
                    st.markdown("**Insurance Details**")
                    st.markdown(f"• **Coverage:** {case.get('coverage_type', 'N/A')}")
                    if case.get('idv'):
                        st.markdown(f"• **IDV:** ₹{case.get('idv'):,.0f}")
                    st.markdown(f"• **Premium:** ₹{case['premium_amount']:,.0f}")
                    if case.get('policy_number'):
                        st.markdown(f"• **Policy Number:** {case.get('policy_number')}")
                    
                    # Add-on covers
                    addons = []
                    if case.get('zero_depreciation'): addons.append('Zero Dep')
                    if case.get('engine_protect'): addons.append('Engine Cover')
                    if case.get('roadside_assistance'): addons.append('RSA')
                    if addons:
                        st.markdown(f"• **Add-ons:** {', '.join(addons)}")
                
                with col3:
                    st.markdown("**Case Status**")
                    st.markdown(f"• **Status:** {case['status']}")
                    st.markdown(f"• **Assigned to:** {case['assigned_to']}")
                    st.markdown(f"• **Created:** {case['created_date'].strftime('%d %b %Y')}")
                    if case.get('follow_up_date'):
                        st.markdown(f"• **Follow-up:** {case['follow_up_date'].strftime('%d %b %Y')}")
                    
                    # Document status
                    docs = case.get('documents', [])
                    completion = case.get('document_completion_rate', 0)
                    st.markdown(f"• **Documents:** {len(docs)} items ({completion:.0f}% complete)")
                
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
                    if st.button("📄 Policy", key=f"policy_{i}"):
                        if case.get('policy_number'):
                            st.success(f"Policy {case.get('policy_number')} details displayed")
                        else:
                            st.warning("Policy not yet issued")
    else:
        st.info("No vehicle insurance cases found matching the selected filters.")

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