import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import random
import uuid

# Configure page
st.set_page_config(
    page_title="Premium Insurance Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Custom CSS for Modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .main {
        padding: 1rem 2rem;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Status Badges */
    .status-active {
        background: linear-gradient(45deg, #10b981, #059669);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .status-pending {
        background: linear-gradient(45deg, #f59e0b, #d97706);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }
    
    .status-approved {
        background: linear-gradient(45deg, #10b981, #059669);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .status-rejected {
        background: linear-gradient(45deg, #ef4444, #dc2626);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }
    
    /* Form Styling */
    .modern-form {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Alert Styling */
    .alert-success {
        background: linear-gradient(45deg, #d1fae5, #a7f3d0);
        color: #065f46;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(45deg, #dbeafe, #bfdbfe);
        color: #1e40af;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    /* Premium Card */
    .premium-card {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(251, 191, 36, 0.3);
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: white;
        border-radius: 10px 10px 0 0;
        padding: 0 2rem;
        font-weight: 500;
        border: 2px solid #e5e7eb;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Data Models
@dataclass
class User:
    id: str
    name: str
    email: str
    phone: str
    address: str
    date_of_birth: str
    aadhar_number: str
    pan_number: str
    created_date: str

@dataclass
class Policy:
    id: str
    policy_number: str
    type: str
    category: str
    premium_annual: float
    premium_monthly: float
    coverage_amount: float
    deductible: float
    status: str
    start_date: str
    end_date: str
    description: str
    user_id: str
    agent_id: str
    last_payment_date: str
    next_payment_due: str

@dataclass
class Claim:
    id: str
    claim_number: str
    amount_claimed: float
    amount_approved: float
    status: str
    priority: str
    description: str
    incident_date: str
    filed_date: str
    processed_date: str
    policy_id: str
    user_id: str
    documents: List[str]
    notes: str

@dataclass
class Payment:
    id: str
    amount: float
    payment_date: str
    payment_method: str
    status: str
    policy_id: str
    user_id: str
    transaction_id: str

@dataclass
class Agent:
    id: str
    name: str
    email: str
    phone: str
    designation: str
    policies_managed: int

@dataclass
class Activity:
    id: str
    type: str
    description: str
    timestamp: str
    user_id: str
    reference_id: str

# Initialize session state
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'users' not in st.session_state:
        st.session_state.users = get_sample_users()
    if 'policies' not in st.session_state:
        st.session_state.policies = get_sample_policies()
    if 'claims' not in st.session_state:
        st.session_state.claims = get_sample_claims()
    if 'payments' not in st.session_state:
        st.session_state.payments = get_sample_payments()
    if 'agents' not in st.session_state:
        st.session_state.agents = get_sample_agents()
    if 'activities' not in st.session_state:
        st.session_state.activities = get_sample_activities()

# Sample Data Generation
def get_sample_users():
    return [
        User("1", "Rajesh Kumar", "rajesh.kumar@email.com", "+91-9876543210", 
             "123 MG Road, Bangalore, Karnataka 560001", "1985-05-15", "1234-5678-9012", 
             "ABCDE1234F", "2023-01-15"),
        User("2", "Priya Sharma", "priya.sharma@email.com", "+91-9876543211", 
             "456 CP Road, Delhi, Delhi 110001", "1990-08-22", "2345-6789-0123", 
             "BCDEF2345G", "2023-02-20"),
        User("3", "Amit Patel", "amit.patel@email.com", "+91-9876543212", 
             "789 SG Highway, Ahmedabad, Gujarat 380001", "1988-12-10", "3456-7890-1234", 
             "CDEFG3456H", "2023-03-10")
    ]

def get_sample_agents():
    return [
        Agent("1", "Suresh Agrawal", "suresh.agent@insurance.com", "+91-9876500001", 
               "Senior Insurance Agent", 25),
        Agent("2", "Meera Joshi", "meera.agent@insurance.com", "+91-9876500002", 
               "Insurance Advisor", 18),
        Agent("3", "Karan Singh", "karan.agent@insurance.com", "+91-9876500003", 
               "Claims Specialist", 22)
    ]

def get_sample_policies():
    return [
        Policy("1", "MOTOR-2024-001", "Motor Insurance", "Vehicle", 25000.0, 2100.0, 
               800000.0, 5000.0, "Active", "2024-01-15", "2025-01-15", 
               "Comprehensive Car Insurance for Maruti Swift", "1", "1", 
               "2024-01-15", "2024-02-15"),
        Policy("2", "HEALTH-2024-001", "Health Insurance", "Medical", 18000.0, 1500.0, 
               500000.0, 2000.0, "Active", "2024-02-01", "2025-02-01", 
               "Family Health Insurance Plan", "1", "2", 
               "2024-02-01", "2024-03-01"),
        Policy("3", "HOME-2024-001", "Home Insurance", "Property", 15000.0, 1250.0, 
               2000000.0, 10000.0, "Active", "2024-03-10", "2025-03-10", 
               "Comprehensive Home Insurance", "1", "1", 
               "2024-03-10", "2024-04-10"),
        Policy("4", "TERM-2024-001", "Term Life Insurance", "Life", 12000.0, 1000.0, 
               1000000.0, 0.0, "Active", "2024-04-01", "2044-04-01", 
               "20-Year Term Life Insurance", "2", "3", 
               "2024-04-01", "2024-05-01"),
        Policy("5", "TRAVEL-2024-001", "Travel Insurance", "Travel", 3500.0, 300.0, 
               200000.0, 1000.0, "Active", "2024-05-15", "2024-11-15", 
               "International Travel Insurance", "3", "2", 
               "2024-05-15", "2024-06-15")
    ]

def get_sample_claims():
    return [
        Claim("1", "CLM-2024-001", 45000.0, 42000.0, "Approved", "High", 
              "Car accident - front bumper damage and engine repair", "2024-08-10", 
              "2024-08-12", "2024-08-20", "1", "1", 
              ["accident_report.pdf", "repair_estimate.jpg", "photos.zip"], 
              "Claim approved after investigation. Minor damage covered."),
        Claim("2", "CLM-2024-002", 25000.0, 0.0, "Under Review", "Medium", 
              "Hospitalization for appendix surgery", "2024-09-05", "2024-09-07", 
              "", "2", "1", 
              ["medical_bills.pdf", "discharge_summary.pdf"], 
              "Medical review in progress. Waiting for additional documents."),
        Claim("3", "CLM-2024-003", 8000.0, 8000.0, "Approved", "Low", 
              "Mobile phone screen damage during travel", "2024-09-20", 
              "2024-09-22", "2024-09-25", "5", "3", 
              ["purchase_invoice.jpg", "damage_photos.jpg"], 
              "Travel insurance claim approved for accidental damage."),
        Claim("4", "CLM-2024-004", 150000.0, 0.0, "Rejected", "Medium", 
              "Water damage to home electronics", "2024-08-25", "2024-08-28", 
              "2024-09-10", "3", "1", 
              ["damage_photos.zip", "purchase_receipts.pdf"], 
              "Claim rejected - damage caused by negligence, not covered under policy."),
        Claim("5", "CLM-2024-005", 12000.0, 0.0, "Pending", "Low", 
              "Dental treatment expenses", "2024-09-15", "2024-09-18", 
              "", "2", "1", 
              ["dental_bills.pdf", "treatment_plan.pdf"], 
              "Initial review completed. Awaiting final approval.")
    ]

def get_sample_payments():
    return [
        Payment("1", 25000.0, "2024-01-15", "Online Banking", "Completed", "1", "1", "TXN123456789"),
        Payment("2", 18000.0, "2024-02-01", "Credit Card", "Completed", "2", "1", "TXN123456790"),
        Payment("3", 15000.0, "2024-03-10", "UPI", "Completed", "3", "1", "TXN123456791"),
        Payment("4", 12000.0, "2024-04-01", "Net Banking", "Completed", "4", "2", "TXN123456792"),
        Payment("5", 3500.0, "2024-05-15", "Debit Card", "Completed", "5", "3", "TXN123456793")
    ]

def get_sample_activities():
    activities = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(50):
        activity_types = ["POLICY_CREATED", "PREMIUM_PAID", "CLAIM_FILED", "CLAIM_APPROVED", 
                         "POLICY_RENEWED", "DOCUMENT_UPLOADED", "PROFILE_UPDATED"]
        activity_type = random.choice(activity_types)
        
        descriptions = {
            "POLICY_CREATED": ["New motor insurance policy created", "Health insurance policy activated", "Home insurance coverage started"],
            "PREMIUM_PAID": ["Annual premium payment processed", "Monthly premium auto-debit successful", "Premium payment confirmed"],
            "CLAIM_FILED": ["New claim submitted for review", "Insurance claim filed successfully", "Claim documentation uploaded"],
            "CLAIM_APPROVED": ["Claim approved and processed", "Settlement amount credited", "Claim investigation completed"],
            "POLICY_RENEWED": ["Policy renewed for next term", "Auto-renewal processed", "Coverage extended successfully"],
            "DOCUMENT_UPLOADED": ["Policy documents uploaded", "Claim supporting documents added", "KYC documents verified"],
            "PROFILE_UPDATED": ["Profile information updated", "Contact details modified", "Address information changed"]
        }
        
        timestamp = base_date + timedelta(days=random.randint(0, 30), 
                                        hours=random.randint(0, 23), 
                                        minutes=random.randint(0, 59))
        
        activities.append(Activity(
            id=str(i+1),
            type=activity_type,
            description=random.choice(descriptions[activity_type]),
            timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            user_id=random.choice(["1", "2", "3"]),
            reference_id=f"REF-{i+1:04d}"
        ))
    
    return activities

# Authentication
def authenticate(email: str, password: str) -> Optional[User]:
    """Simple authentication - in production use proper auth"""
    demo_credentials = {
        "demo@insurance.com": "demo123",
        "rajesh.kumar@email.com": "rajesh123",
        "priya.sharma@email.com": "priya123",
        "amit.patel@email.com": "amit123"
    }
    
    if email in demo_credentials and password == demo_credentials[email]:
        # Find user by email
        for user in st.session_state.users:
            if user.email == email:
                return user
        # Return first user as demo
        return st.session_state.users[0]
    return None

# Helper Functions
def get_user_policies(user_id: str) -> List[Policy]:
    return [p for p in st.session_state.policies if p.user_id == user_id]

def get_user_claims(user_id: str) -> List[Claim]:
    return [c for c in st.session_state.claims if c.user_id == user_id]

def get_user_payments(user_id: str) -> List[Payment]:
    return [p for p in st.session_state.payments if p.user_id == user_id]

def get_user_activities(user_id: str) -> List[Activity]:
    return [a for a in st.session_state.activities if a.user_id == user_id]

def get_policy_by_id(policy_id: str) -> Optional[Policy]:
    return next((p for p in st.session_state.policies if p.id == policy_id), None)

def get_agent_by_id(agent_id: str) -> Optional[Agent]:
    return next((a for a in st.session_state.agents if a.id == agent_id), None)

def calculate_risk_score(user: User, policy_type: str) -> int:
    """Simple risk calculation for demo purposes"""
    base_score = 50
    
    # Age factor
    today = datetime.now()
    birth_date = datetime.strptime(user.date_of_birth, "%Y-%m-%d")
    age = today.year - birth_date.year
    
    if policy_type == "Motor Insurance":
        if age < 25:
            base_score += 20
        elif age > 60:
            base_score += 15
        else:
            base_score += 5
    elif policy_type == "Health Insurance":
        if age > 50:
            base_score += 25
        elif age > 35:
            base_score += 10
    
    return min(100, base_score)

# Login Page
def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Premium Insurance Management System</h1>
        <p>Complete Insurance Solutions for Individuals & Families</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="modern-form">', unsafe_allow_html=True)
        st.markdown("### 🔐 Secure Login Portal")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", 
                                value="demo@insurance.com", 
                                placeholder="Enter your registered email")
            password = st.text_input("🔒 Password", 
                                   type="password", 
                                   value="demo123", 
                                   placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                login_button = st.form_submit_button("🚀 Login to Dashboard", use_container_width=True)
            with col_btn2:
                forgot_btn = st.form_submit_button("🔄 Forgot Password?", use_container_width=True)
            
            if login_button:
                user = authenticate(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    st.success("✅ Login successful! Redirecting to dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please check your email and password.")
            
            if forgot_btn:
                st.info("🔄 Password reset link would be sent to your registered email address.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo credentials info
        st.markdown("""
        <div class="alert-info">
            <h4>🎭 Demo Account Access</h4>
            <strong>Email:</strong> demo@insurance.com<br>
            <strong>Password:</strong> demo123<br><br>
            <em>Use these credentials to explore the full-featured insurance management system</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Features showcase
        st.markdown("### ✨ System Features")
        
        col_feat1, col_feat2 = st.columns(2)
        
        with col_feat1:
            st.markdown("""
            **📋 Policy Management**
            - Create & manage policies
            - Premium calculations
            - Coverage analysis
            - Renewal tracking
            
            **💰 Claims Processing** 
            - File new claims
            - Track claim status
            - Document management
            - Settlement tracking
            """)
        
        with col_feat2:
            st.markdown("""
            **📊 Advanced Analytics**
            - Interactive dashboards
            - Financial insights
            - Risk assessment
            - Performance metrics
            
            **🔔 Smart Features**
            - Payment reminders
            - Activity timeline
            - Agent connectivity
            - Mobile-ready design
            """)

# Main Dashboard
def dashboard_page():
    user = st.session_state.current_user
    
    # Header
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="margin: 0;">🏠 Welcome back, {user.name}!</h2>
            <p style="margin: 0; opacity: 0.9;">Manage your insurance portfolio with ease</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_header2:
        if st.button("🚪 Secure Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
    
    # Get user data
    user_policies = get_user_policies(user.id)
    user_claims = get_user_claims(user.id)
    user_payments = get_user_payments(user.id)
    user_activities = get_user_activities(user.id)
    
    # Calculate comprehensive metrics
    active_policies = [p for p in user_policies if p.status == "Active"]
    total_annual_premium = sum(p.premium_annual for p in active_policies)
    total_coverage = sum(p.coverage_amount for p in active_policies)
    pending_claims = len([c for c in user_claims if c.status in ["Pending", "Under Review"]])
    approved_claims = len([c for c in user_claims if c.status == "Approved"])
    total_claims_value = sum(c.amount_approved for c in user_claims if c.status == "Approved")
    
    # Enhanced Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🏅 Active Policies",
            value=len(active_policies),
            delta=f"₹{total_annual_premium:,.0f} annual premium",
            help="Total number of active insurance policies"
        )
    
    with col2:
        st.metric(
            label="🛡️ Total Coverage",
            value=f"₹{total_coverage/100000:.1f}L",
            delta="Protected Amount",
            help="Total insurance coverage amount across all policies"
        )
    
    with col3:
        st.metric(
            label="📋 Claims Status",
            value=f"{pending_claims} Pending",
            delta=f"{approved_claims} Approved",
            help="Current status of insurance claims"
        )
    
    with col4:
        st.metric(
            label="💰 Claims Settled",
            value=f"₹{total_claims_value:,.0f}",
            delta="Total Received",
            help="Total amount received from approved claims"
        )
    
    with col5:
        savings_ratio = (total_claims_value / total_annual_premium * 100) if total_annual_premium > 0 else 0
        st.metric(
            label="📈 Savings Ratio",
            value=f"{savings_ratio:.1f}%",
            delta="Claims vs Premium",
            help="Ratio of claims received vs premiums paid"
        )
    
    st.divider()
    
    # Enhanced Tabbed Interface
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard Overview", 
        "🏠 Policy Management", 
        "💼 Claims Center", 
        "💳 Payments & Billing",
        "📈 Analytics & Reports",
        "👤 Profile & Settings"
    ])
    
    with tab1:
        show_dashboard_overview(user, user_policies, user_claims, user_activities)
    
    with tab2:
        show_policy_management(user, user_policies)
    
    with tab3:
        show_claims_center(user, user_claims)
    
    with tab4:
        show_payments_billing(user, user_payments, user_policies)
    
    with tab5:
        show_analytics_reports(user, user_policies, user_claims, user_payments)
    
    with tab6:
        show_profile_settings(user)

def show_dashboard_overview(user, user_policies, user_claims, user_activities):
    """Enhanced dashboard overview with comprehensive information"""
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📋 Policy Portfolio Overview")
        
        if user_policies:
            # Create enhanced policy dataframe
            policy_data = []
            for policy in user_policies:
                agent = get_agent_by_id(policy.agent_id)
                agent_name = agent.name if agent else "N/A"
                
                # Calculate days until renewal
                end_date = datetime.strptime(policy.end_date, "%Y-%m-%d")
                days_to_renewal = (end_date - datetime.now()).days
                
                policy_data.append({
                    "Policy": policy.policy_number,
                    "Type": policy.type,
                    "Premium (Annual)": f"₹{policy.premium_annual:,.0f}",
                    "Coverage": f"₹{policy.coverage_amount/100000:.1f}L",
                    "Status": policy.status,
                    "Days to Renewal": days_to_renewal,
                    "Agent": agent_name
                })
            
            df = pd.DataFrame(policy_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Policy type distribution chart
            st.subheader("📊 Policy Distribution")
            policy_types = [p.type for p in user_policies]
            type_counts = pd.Series(policy_types).value_counts()
            
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title="Insurance Portfolio by Type",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("🔍 No policies found. Consider getting your first insurance policy!")
    
    with col_right:
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🆕 Buy New Policy", use_container_width=True, type="primary"):
            st.balloons()
            st.success("🎉 New policy wizard would open here!")
        
        if st.button("📄 File New Claim", use_container_width=True):
            st.info("📋 Claims filing interface would appear here!")
        
        if st.button("💰 Make Payment", use_container_width=True):
            st.info("💳 Payment gateway would be integrated here!")
        
        if st.button("🔄 Renew Policy", use_container_width=True):
            st.info("🔄 Policy renewal process would start here!")
        
        st.divider()
        
        # Recent Activity Feed
        st.subheader("📢 Recent Activity")
        
        recent_activities = sorted(user_activities, key=lambda x: x.timestamp, reverse=True)[:8]
        
        for activity in recent_activities:
            # Activity type icons
            icons = {
                "POLICY_CREATED": "🆕",
                "PREMIUM_PAID": "💰",
                "CLAIM_FILED": "📋",
                "CLAIM_APPROVED": "✅",
                "POLICY_RENEWED": "🔄",
                "DOCUMENT_UPLOADED": "📎",
                "PROFILE_UPDATED": "👤"
            }
            
            icon = icons.get(activity.type, "📌")
            
            st.markdown(f"""
            <div style="padding: 0.8rem; margin: 0.5rem 0; background: linear-gradient(45deg, #f8fafc, #e2e8f0); 
                        border-radius: 8px; border-left: 3px solid #667eea;">
                <div style="display: flex; align-items: center; margin-bottom: 0.3rem;">
                    <span style="margin-right: 0.5rem; font-size: 1.2rem;">{icon}</span>
                    <strong style="color: #1f2937;">{activity.type.replace('_', ' ').title()}</strong>
                </div>
                <div style="color: #4b5563; font-size: 0.9rem; margin-bottom: 0.3rem;">
                    {activity.description}
                </div>
                <div style="color: #9ca3af; font-size: 0.8rem;">
                    📅 {activity.timestamp}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Important Notifications
        st.subheader("🔔 Important Notifications")
        
        # Check for upcoming renewals
        upcoming_renewals = []
        for policy in user_policies:
            end_date = datetime.strptime(policy.end_date, "%Y-%m-%d")
            days_to_renewal = (end_date - datetime.now()).days
            if 0 <= days_to_renewal <= 60:
                upcoming_renewals.append((policy, days_to_renewal))
        
        if upcoming_renewals:
            for policy, days in upcoming_renewals:
                if days <= 7:
                    st.error(f"🚨 {policy.type} policy expires in {days} days!")
                elif days <= 30:
                    st.warning(f"⚠️ {policy.type} policy expires in {days} days")
                else:
                    st.info(f"ℹ️ {policy.type} policy expires in {days} days")
        else:
            st.success("✅ All policies are up to date!")

def show_policy_management(user, user_policies):
    """Comprehensive policy management interface"""
    
    col_header1, col_header2 = st.columns([2, 1])
    
    with col_header1:
        st.subheader("🏠 Insurance Policy Management")
    
    with col_header2:
        if st.button("🆕 Create New Policy", type="primary"):
            show_new_policy_form(user)
    
    # Policy filters
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        policy_type_filter = st.selectbox(
            "Filter by Type",
            ["All Types"] + list(set(p.type for p in user_policies))
        )
    
    with col_filter2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All Status"] + list(set(p.status for p in user_policies))
        )
    
    with col_filter3:
        sort_by = st.selectbox(
            "Sort by",
            ["Policy Number", "Premium (Low to High)", "Premium (High to Low)", 
             "Coverage Amount", "Expiry Date"]
        )
    
    # Apply filters
    filtered_policies = user_policies
    if policy_type_filter != "All Types":
        filtered_policies = [p for p in filtered_policies if p.type == policy_type_filter]
    if status_filter != "All Status":
        filtered_policies = [p for p in filtered_policies if p.status == status_filter]
    
    # Apply sorting
    if sort_by == "Premium (Low to High)":
        filtered_policies.sort(key=lambda x: x.premium_annual)
    elif sort_by == "Premium (High to Low)":
        filtered_policies.sort(key=lambda x: x.premium_annual, reverse=True)
    elif sort_by == "Coverage Amount":
        filtered_policies.sort(key=lambda x: x.coverage_amount, reverse=True)
    elif sort_by == "Expiry Date":
        filtered_policies.sort(key=lambda x: x.end_date)
    
    st.divider()
    
    # Display policies
    if filtered_policies:
        for policy in filtered_policies:
            agent = get_agent_by_id(policy.agent_id)
            
            with st.container():
                # Policy card design
                col_icon, col_details, col_metrics, col_actions = st.columns([1, 3, 2, 2])
                
                with col_icon:
                    # Policy type icons
                    icons = {
                        "Motor Insurance": "🚗",
                        "Health Insurance": "🏥",
                        "Home Insurance": "🏠",
                        "Term Life Insurance": "❤️",
                        "Travel Insurance": "✈️"
                    }
                    icon = icons.get(policy.type, "📄")
                    
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); 
                                color: white; border-radius: 10px; margin-bottom: 1rem;">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div style="font-size: 0.8rem; font-weight: 500;">{policy.category}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_details:
                    status_class = "status-active" if policy.status == "Active" else "status-pending"
                    
                    st.markdown(f"""
                    <div style="padding: 1rem;">
                        <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{policy.type}</h4>
                        <p style="margin: 0; color: #4b5563;"><strong>Policy #:</strong> {policy.policy_number}</p>
                        <p style="margin: 0; color: #4b5563;"><strong>Description:</strong> {policy.description}</p>
                        <p style="margin: 0; color: #4b5563;"><strong>Agent:</strong> {agent.name if agent else 'N/A'}</p>
                        <div style="margin-top: 0.5rem;">
                            <span class="{status_class}">{policy.status}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_metrics:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem;">
                        <p style="margin: 0; color: #374151;"><strong>Annual Premium:</strong><br>₹{policy.premium_annual:,.0f}</p>
                        <p style="margin: 0; color: #374151;"><strong>Coverage:</strong><br>₹{policy.coverage_amount/100000:.1f}L</p>
                        <p style="margin: 0; color: #374151;"><strong>Deductible:</strong><br>₹{policy.deductible:,.0f}</p>
                        <p style="margin: 0; color: #374151;"><strong>Expires:</strong><br>{policy.end_date}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_actions:
                    st.markdown("<div style='padding-top: 1rem;'>", unsafe_allow_html=True)
                    
                    if st.button(f"📋 View Details", key=f"view_{policy.id}", use_container_width=True):
                        show_policy_details(policy)
                    
                    if st.button(f"🔄 Renew Policy", key=f"renew_{policy.id}", use_container_width=True):
                        st.info(f"🔄 Renewal process for {policy.policy_number} would start here!")
                    
                    if st.button(f"💰 Pay Premium", key=f"pay_{policy.id}", use_container_width=True):
                        st.success(f"💳 Payment gateway for {policy.policy_number} would open here!")
                    
                    if policy.status == "Active":
                        if st.button(f"⏸️ Suspend", key=f"suspend_{policy.id}", use_container_width=True, type="secondary"):
                            st.warning(f"⏸️ Policy {policy.policy_number} suspension process initiated!")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.divider()
    else:
        st.info("🔍 No policies match your current filters.")

def show_new_policy_form(user):
    """New policy creation form"""
    st.subheader("🆕 Create New Insurance Policy")
    
    with st.form("new_policy_form"):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            policy_type = st.selectbox(
                "Insurance Type *",
                ["Motor Insurance", "Health Insurance", "Home Insurance", 
                 "Term Life Insurance", "Travel Insurance", "Cyber Insurance"]
            )
            
            coverage_amount = st.number_input(
                "Coverage Amount (₹) *",
                min_value=100000,
                max_value=10000000,
                value=500000,
                step=50000
            )
            
            deductible = st.number_input(
                "Deductible Amount (₹)",
                min_value=0,
                max_value=50000,
                value=5000,
                step=1000
            )
        
        with col_form2:
            policy_duration = st.selectbox(
                "Policy Duration *",
                ["1 Year", "2 Years", "5 Years", "10 Years", "20 Years"]
            )
            
            payment_mode = st.selectbox(
                "Premium Payment *",
                ["Annual", "Semi-Annual", "Quarterly", "Monthly"]
            )
            
            agent_id = st.selectbox(
                "Select Agent *",
                options=[a.id for a in st.session_state.agents],
                format_func=lambda x: next(a.name for a in st.session_state.agents if a.id == x)
            )
        
        policy_description = st.text_area(
            "Policy Description",
            placeholder="Enter specific requirements or details for this policy..."
        )
        
        # Risk Assessment
        st.subheader("📊 Risk Assessment")
        risk_score = calculate_risk_score(user, policy_type)
        
        col_risk1, col_risk2, col_risk3 = st.columns(3)
        
        with col_risk1:
            st.metric("Risk Score", f"{risk_score}/100")
        
        with col_risk2:
            risk_level = "Low" if risk_score < 40 else "Medium" if risk_score < 70 else "High"
            st.metric("Risk Level", risk_level)
        
        with col_risk3:
            # Calculate premium based on risk
            base_premium = coverage_amount * 0.02  # 2% base rate
            risk_multiplier = 1 + (risk_score / 100) * 0.5
            estimated_premium = base_premium * risk_multiplier
            st.metric("Estimated Premium", f"₹{estimated_premium:,.0f}")
        
        # Terms and Conditions
        st.subheader("📋 Terms & Conditions")
        terms_accepted = st.checkbox("I accept the terms and conditions *")
        consent_marketing = st.checkbox("I consent to receive marketing communications")
        
        submitted = st.form_submit_button("🚀 Create Policy", type="primary", use_container_width=True)
        
        if submitted:
            if terms_accepted:
                # Generate new policy
                new_policy_id = str(len(st.session_state.policies) + 1)
                policy_number = f"{policy_type.split()[0].upper()}-2024-{len(st.session_state.policies) + 1:03d}"
                
                # Calculate dates
                start_date = datetime.now().strftime("%Y-%m-%d")
                duration_years = int(policy_duration.split()[0])
                end_date = (datetime.now() + timedelta(days=365 * duration_years)).strftime("%Y-%m-%d")
                
                # Calculate premiums
                annual_premium = estimated_premium
                payment_frequencies = {"Annual": 1, "Semi-Annual": 2, "Quarterly": 4, "Monthly": 12}
                frequency = payment_frequencies[payment_mode]
                premium_amount = annual_premium / frequency
                
                new_policy = Policy(
                    id=new_policy_id,
                    policy_number=policy_number,
                    type=policy_type,
                    category=policy_type.split()[0],
                    premium_annual=annual_premium,
                    premium_monthly=annual_premium / 12,
                    coverage_amount=coverage_amount,
                    deductible=deductible,
                    status="Pending Approval",
                    start_date=start_date,
                    end_date=end_date,
                    description=policy_description or f"Standard {policy_type} policy",
                    user_id=user.id,
                    agent_id=agent_id,
                    last_payment_date="",
                    next_payment_due=start_date
                )
                
                st.session_state.policies.append(new_policy)
                
                st.success(f"""
                ✅ **Policy Created Successfully!**
                
                **Policy Number:** {policy_number}  
                **Coverage Amount:** ₹{coverage_amount:,.0f}  
                **Annual Premium:** ₹{annual_premium:,.0f}  
                **Status:** Pending Approval
                
                You will receive a confirmation email shortly with policy documents.
                """)
                st.balloons()
                
                # Add activity
                activity = Activity(
                    id=str(len(st.session_state.activities) + 1),
                    type="POLICY_CREATED",
                    description=f"New {policy_type} policy created - {policy_number}",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_id=user.id,
                    reference_id=new_policy_id
                )
                st.session_state.activities.append(activity)
                
                st.rerun()
            else:
                st.error("❌ Please accept the terms and conditions to proceed.")

def show_policy_details(policy):
    """Detailed policy information modal"""
    st.subheader(f"📋 Policy Details: {policy.policy_number}")
    
    # Policy overview
    col_overview1, col_overview2 = st.columns(2)
    
    with col_overview1:
        st.markdown(f"""
        **Policy Information:**
        - **Type:** {policy.type}
        - **Category:** {policy.category}
        - **Status:** {policy.status}
        - **Policy Number:** {policy.policy_number}
        - **Description:** {policy.description}
        """)
    
    with col_overview2:
        st.markdown(f"""
        **Financial Details:**
        - **Annual Premium:** ₹{policy.premium_annual:,.0f}
        - **Monthly Premium:** ₹{policy.premium_monthly:,.0f}
        - **Coverage Amount:** ₹{policy.coverage_amount:,.0f}
        - **Deductible:** ₹{policy.deductible:,.0f}
        """)
    
    # Coverage timeline
    st.subheader("📅 Coverage Timeline")
    
    start_date = datetime.strptime(policy.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(policy.end_date, "%Y-%m-%d")
    current_date = datetime.now()
    
    # Calculate coverage progress
    total_days = (end_date - start_date).days
    elapsed_days = (current_date - start_date).days
    progress = min(100, max(0, (elapsed_days / total_days) * 100))
    
    st.progress(progress / 100)
    st.write(f"Coverage Progress: {progress:.1f}% ({elapsed_days} of {total_days} days)")
    
    col_dates1, col_dates2, col_dates3 = st.columns(3)
    
    with col_dates1:
        st.metric("Start Date", policy.start_date)
    
    with col_dates2:
        st.metric("End Date", policy.end_date)
    
    with col_dates3:
        days_remaining = (end_date - current_date).days
        st.metric("Days Remaining", days_remaining)
    
    # Agent information
    agent = get_agent_by_id(policy.agent_id)
    if agent:
        st.subheader("👤 Agent Information")
        
        col_agent1, col_agent2 = st.columns(2)
        
        with col_agent1:
            st.markdown(f"""
            **{agent.name}**  
            📧 {agent.email}  
            📞 {agent.phone}  
            🏢 {agent.designation}
            """)
        
        with col_agent2:
            st.metric("Policies Managed", agent.policies_managed)
            
            if st.button("📞 Contact Agent", key=f"contact_agent_{policy.id}"):
                st.info(f"📞 Contacting {agent.name}... (This would open a communication interface)")

def show_claims_center(user, user_claims):
    """Enhanced claims management center"""
    
    col_header1, col_header2 = st.columns([2, 1])
    
    with col_header1:
        st.subheader("💼 Claims Management Center")
    
    with col_header2:
        if st.button("📄 File New Claim", type="primary"):
            show_new_claim_form(user)
    
    # Claims statistics
    claims_stats = {
        "Total": len(user_claims),
        "Approved": len([c for c in user_claims if c.status == "Approved"]),
        "Pending": len([c for c in user_claims if c.status == "Pending"]),
        "Under Review": len([c for c in user_claims if c.status == "Under Review"]),
        "Rejected": len([c for c in user_claims if c.status == "Rejected"])
    }
    
    col_stat1, col_stat2, col_stat3, col_stat4, col_stat5 = st.columns(5)
    
    with col_stat1:
        st.metric("Total Claims", claims_stats["Total"])
    
    with col_stat2:
        st.metric("✅ Approved", claims_stats["Approved"], delta=None)
    
    with col_stat3:
        st.metric("⏳ Pending", claims_stats["Pending"])
    
    with col_stat4:
        st.metric("🔍 Under Review", claims_stats["Under Review"])
    
    with col_stat5:
        st.metric("❌ Rejected", claims_stats["Rejected"])
    
    st.divider()
    
    # Claims filter and sort
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All Status"] + list(set(c.status for c in user_claims))
        )
    
    with col_filter2:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["All Priority"] + list(set(c.priority for c in user_claims))
        )
    
    with col_filter3:
        sort_claims = st.selectbox(
            "Sort by",
            ["Filed Date (Latest)", "Filed Date (Oldest)", "Amount (High to Low)", "Amount (Low to High)"]
        )
    
    # Apply filters
    filtered_claims = user_claims
    
    if status_filter != "All Status":
        filtered_claims = [c for c in filtered_claims if c.status == status_filter]
    
    if priority_filter != "All Priority":
        filtered_claims = [c for c in filtered_claims if c.priority == priority_filter]
    
    # Apply sorting
    if sort_claims == "Filed Date (Latest)":
        filtered_claims.sort(key=lambda x: x.filed_date, reverse=True)
    elif sort_claims == "Filed Date (Oldest)":
        filtered_claims.sort(key=lambda x: x.filed_date)
    elif sort_claims == "Amount (High to Low)":
        filtered_claims.sort(key=lambda x: x.amount_claimed, reverse=True)
    elif sort_claims == "Amount (Low to High)":
        filtered_claims.sort(key=lambda x: x.amount_claimed)
    
    # Display claims
    if filtered_claims:
        for claim in filtered_claims:
            policy = get_policy_by_id(claim.policy_id)
            policy_name = f"{policy.type} - {policy.policy_number}" if policy else "Unknown Policy"
            
            # Status styling
            status_styles = {
                "Approved": "background: linear-gradient(45deg, #10b981, #059669); color: white;",
                "Pending": "background: linear-gradient(45deg, #f59e0b, #d97706); color: white;",
                "Under Review": "background: linear-gradient(45deg, #3b82f6, #2563eb); color: white;",
                "Rejected": "background: linear-gradient(45deg, #ef4444, #dc2626); color: white;"
            }
            
            # Priority styling
            priority_colors = {
                "High": "#ef4444",
                "Medium": "#f59e0b", 
                "Low": "#10b981"
            }
            
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
                           background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                    
                    <!-- Header -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0; color: #1f2937;">🎫 {claim.claim_number}</h4>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <span style="background-color: {priority_colors.get(claim.priority, '#6b7280')}; 
                                         color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem;">
                                {claim.priority} Priority
                            </span>
                            <span style="{status_styles.get(claim.status, 'background-color: #6b7280; color: white;')} 
                                         padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">
                                {claim.status}
                            </span>
                        </div>
                    </div>
                    
                    <!-- Content Grid -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                        <div>
                            <strong style="color: #374151;">Amount Claimed:</strong><br>
                            <span style="font-size: 1.2rem; color: #1f2937;">₹{claim.amount_claimed:,.0f}</span>
                        </div>
                        <div>
                            <strong style="color: #374151;">Amount Approved:</strong><br>
                            <span style="font-size: 1.2rem; color: #059669;">₹{claim.amount_approved:,.0f}</span>
                        </div>
                        <div>
                            <strong style="color: #374151;">Policy:</strong><br>
                            <span style="color: #4b5563;">{policy_name}</span>
                        </div>
                    </div>
                    
                    <!-- Description -->
                    <div style="margin-bottom: 1rem;">
                        <strong style="color: #374151;">Description:</strong><br>
                        <span style="color: #4b5563;">{claim.description}</span>
                    </div>
                    
                    <!-- Dates and Documents -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                        <div>
                            <strong style="color: #374151;">Incident Date:</strong><br>
                            <span style="color: #4b5563;">📅 {claim.incident_date}</span>
                        </div>
                        <div>
                            <strong style="color: #374151;">Filed Date:</strong><br>
                            <span style="color: #4b5563;">📋 {claim.filed_date}</span>
                        </div>
                        <div>
                            <strong style="color: #374151;">Documents:</strong><br>
                            <span style="color: #4b5563;">📎 {len(claim.documents)} files</span>
                        </div>
                    </div>
                    
                    <!-- Notes -->
                    {f'<div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 3px solid #667eea;"><strong style="color: #374151;">Notes:</strong><br><span style="color: #4b5563;">{claim.notes}</span></div>' if claim.notes else ''}
                    
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col_action1, col_action2, col_action3, col_action4, col_action5 = st.columns(5)
                
                with col_action1:
                    if st.button(f"👁️ View Details", key=f"view_claim_{claim.id}", use_container_width=True):
                        show_claim_details(claim)
                
                with col_action2:
                    if st.button(f"📎 Documents", key=f"docs_claim_{claim.id}", use_container_width=True):
                        show_claim_documents(claim)
                
                with col_action3:
                    if claim.status in ["Pending", "Under Review"]:
                        if st.button(f"📝 Update", key=f"update_claim_{claim.id}", use_container_width=True):
                            st.info(f"🔄 Claim update interface for {claim.claim_number} would open here!")
                
                with col_action4:
                    if st.button(f"📞 Contact", key=f"contact_claim_{claim.id}", use_container_width=True):
                        st.info(f"📞 Claims department contact for {claim.claim_number}")
                
                with col_action5:
                    if claim.status == "Approved":
                        if st.button(f"💰 Track Payment", key=f"payment_claim_{claim.id}", use_container_width=True):
                            st.success(f"💳 Payment tracking for ₹{claim.amount_approved:,.0f}")
                
                st.divider()
    else:
        st.info("🔍 No claims match your current filters.")
        
        # Encourage first claim if no claims exist
        if not user_claims:
            st.markdown("""
            <div class="alert-info">
                <h4>📋 No Claims Filed Yet</h4>
                <p>Great news! You haven't needed to file any insurance claims. When you do need to make a claim, 
                our streamlined process makes it easy:</p>
                <ul>
                    <li>✅ Quick online filing</li>
                    <li>📎 Digital document upload</li>
                    <li>🔄 Real-time status tracking</li>
                    <li>💰 Fast settlement processing</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_new_claim_form(user):
    """Enhanced new claim filing form"""
    st.subheader("📄 File New Insurance Claim")
    
    user_policies = get_user_policies(user.id)
    active_policies = [p for p in user_policies if p.status == "Active"]
    
    if not active_policies:
        st.error("❌ No active policies found. You need an active policy to file a claim.")
        return
    
    with st.form("new_claim_form"):
        # Policy selection
        st.subheader("🏠 Select Policy")
        selected_policy_id = st.selectbox(
            "Choose the policy for this claim *",
            options=[p.id for p in active_policies],
            format_func=lambda x: f"{next(p.type for p in active_policies if p.id == x)} - {next(p.policy_number for p in active_policies if p.id == x)}"
        )
        
        # Claim details
        st.subheader("📋 Claim Details")
        
        col_claim1, col_claim2 = st.columns(2)
        
        with col_claim1:
            incident_date = st.date_input(
                "Date of Incident *",
                max_value=datetime.now().date(),
                value=datetime.now().date()
            )
            
            claim_amount = st.number_input(
                "Claim Amount (₹) *",
                min_value=100.0,
                max_value=10000000.0,
                value=5000.0,
                step=100.0
            )
            
            priority = st.selectbox(
                "Priority Level *",
                ["Low", "Medium", "High"],
                help="High: Urgent medical/safety issues, Medium: Significant damage/loss, Low: Minor issues"
            )
        
        with col_claim2:
            # Get selected policy for coverage validation
            selected_policy = next(p for p in active_policies if p.id == selected_policy_id)
            
            st.info(f"""
            **Policy Coverage Information:**
            - **Coverage Amount:** ₹{selected_policy.coverage_amount:,.0f}
            - **Deductible:** ₹{selected_policy.deductible:,.0f}
            - **Net Coverage:** ₹{selected_policy.coverage_amount - selected_policy.deductible:,.0f}
            """)
            
            # Validate claim amount
            if claim_amount > selected_policy.coverage_amount:
                st.warning("⚠️ Claim amount exceeds policy coverage limit.")
            elif claim_amount < selected_policy.deductible:
                st.warning(f"⚠️ Claim amount is below deductible (₹{selected_policy.deductible:,.0f}). You may not receive payment.")
        
        # Incident description
        st.subheader("📝 Incident Description")
        incident_description = st.text_area(
            "Describe the incident in detail *",
            placeholder="Please provide a detailed description of what happened, when it occurred, and any relevant circumstances...",
            height=100
        )
        
        # Additional details based on policy type
        if selected_policy.type == "Motor Insurance":
            st.subheader("🚗 Vehicle Incident Details")
            col_vehicle1, col_vehicle2 = st.columns(2)
            
            with col_vehicle1:
                other_party_involved = st.checkbox("Other party involved?")
                police_report_filed = st.checkbox("Police report filed?")
            
            with col_vehicle2:
                vehicle_drivable = st.checkbox("Vehicle still drivable?")
                injuries_reported = st.checkbox("Any injuries reported?")
        
        elif selected_policy.type == "Health Insurance":
            st.subheader("🏥 Medical Incident Details")
            col_medical1, col_medical2 = st.columns(2)
            
            with col_medical1:
                hospital_name = st.text_input("Hospital/Clinic Name")
                doctor_name = st.text_input("Attending Doctor")
            
            with col_medical2:
                treatment_type = st.selectbox(
                    "Treatment Type",
                    ["Outpatient", "Inpatient", "Emergency", "Surgery", "Diagnostic"]
                )
                admission_required = st.checkbox("Hospital admission required?")
        
        elif selected_policy.type == "Home Insurance":
            st.subheader("🏠 Property Incident Details")
            damage_cause = st.selectbox(
                "Cause of Damage",
                ["Fire", "Water/Flood", "Theft/Burglary", "Natural Disaster", "Vandalism", "Other"]
            )
            emergency_repairs = st.checkbox("Emergency repairs needed?")
        
        # Document upload simulation
        st.subheader("📎 Supporting Documents")
        st.info("📋 **Required Documents:** Please prepare the following documents for upload:")
        
        if selected_policy.type == "Motor Insurance":
            required_docs = [
                "📄 Driving License", "🚗 Vehicle Registration", "📋 Police FIR (if applicable)",
                "📷 Accident Photos", "🔧 Repair Estimates", "🏥 Medical Bills (if injuries)"
            ]
        elif selected_policy.type == "Health Insurance":
            required_docs = [
                "🏥 Hospital Bills", "📋 Medical Reports", "💊 Prescription & Medicines",
                "🩺 Diagnostic Reports", "📄 Discharge Summary", "👨‍⚕️ Doctor's Certificate"
            ]
        elif selected_policy.type == "Home Insurance":
            required_docs = [
                "📷 Damage Photos", "🔨 Repair Estimates", "📋 Police Report (if theft)",
                "🧾 Purchase Receipts", "📄 Property Papers", "🌡️ Weather Report (if natural disaster)"
            ]
        else:
            required_docs = [
                "📄 Incident Report", "📷 Supporting Photos", "🧾 Bills/Receipts",
                "📋 Official Documents", "👥 Witness Statements"
            ]
        
        for i, doc in enumerate(required_docs):
            col_doc, col_status = st.columns([3, 1])
            with col_doc:
                st.write(doc)
            with col_status:
                uploaded = st.checkbox("✅", key=f"doc_{i}", help=f"Check when {doc} is ready")
        
        # Claim submission
        st.subheader("📋 Claim Submission")
        
        # Terms and declarations
        col_terms1, col_terms2 = st.columns(2)
        
        with col_terms1:
            declaration = st.checkbox(
                "I declare that the information provided is true and accurate *",
                help="False information may result in claim rejection"
            )
        
        with col_terms2:
            investigation_consent = st.checkbox(
                "I consent to claim investigation procedures *",
                help="This may include site visits, interviews, and document verification"
            )
        
        # Estimated processing time
        processing_time = {
            "Motor Insurance": "5-10 business days",
            "Health Insurance": "7-15 business days", 
            "Home Insurance": "10-20 business days",
            "Travel Insurance": "3-7 business days"
        }
        
        st.info(f"""
        **📅 Estimated Processing Time:** {processing_time.get(selected_policy.type, '7-14 business days')}
        
        **📞 Claim Support:** 1800-XXX-XXXX (24/7 helpline)
        
        **📧 Updates:** You'll receive SMS and email updates on your claim status.
        """)
        
        submitted = st.form_submit_button("🚀 Submit Claim", type="primary", use_container_width=True)
        
        if submitted:
            if declaration and investigation_consent and incident_description.strip():
                # Generate new claim
                new_claim_id = str(len(st.session_state.claims) + 1)
                claim_number = f"CLM-2024-{len(st.session_state.claims) + 1:03d}"
                current_time = datetime.now()
                
                # Simulate document list
                doc_count = len([i for i in range(len(required_docs)) if st.session_state.get(f"doc_{i}", False)])
                simulated_docs = [f"document_{i+1}.pdf" for i in range(doc_count)]
                
                new_claim = Claim(
                    id=new_claim_id,
                    claim_number=claim_number,
                    amount_claimed=claim_amount,
                    amount_approved=0.0,
                    status="Pending",
                    priority=priority,
                    description=incident_description,
                    incident_date=incident_date.strftime("%Y-%m-%d"),
                    filed_date=current_time.strftime("%Y-%m-%d"),
                    processed_date="",
                    policy_id=selected_policy_id,
                    user_id=user.id,
                    documents=simulated_docs,
                    notes="Initial claim review in progress."
                )
                
                st.session_state.claims.append(new_claim)
                
                # Add activity
                activity = Activity(
                    id=str(len(st.session_state.activities) + 1),
                    type="CLAIM_FILED",
                    description=f"New claim filed - {claim_number} for ₹{claim_amount:,.0f}",
                    timestamp=current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    user_id=user.id,
                    reference_id=new_claim_id
                )
                st.session_state.activities.append(activity)
                
                st.success(f"""
                ✅ **Claim Filed Successfully!**
                
                **Claim Number:** {claim_number}  
                **Claim Amount:** ₹{claim_amount:,.0f}  
                **Priority:** {priority}  
                **Status:** Pending Review
                
                📧 **Confirmation email sent to:** {user.email}  
                📱 **SMS sent to:** {user.phone}
                
                **Next Steps:**
                1. Upload required documents (if not done already)
                2. Our claims team will review within 24-48 hours
                3. You'll receive updates via SMS/email
                4. Investigation (if required) will be scheduled
                
                **📞 Questions?** Call our claims helpline: 1800-XXX-XXXX
                """)
                
                st.balloons()
                st.rerun()
            else:
                missing = []
                if not declaration:
                    missing.append("Declaration of truthfulness")
                if not investigation_consent:
                    missing.append("Investigation consent")
                if not incident_description.strip():
                    missing.append("Incident description")
                
                st.error(f"❌ Please complete the following required fields: {', '.join(missing)}")

def show_claim_details(claim):
    """Detailed claim view"""
    st.subheader(f"🎫 Claim Details: {claim.claim_number}")
    
    # Claim status timeline
    st.subheader("📅 Claim Timeline")
    
    # Status progression
    statuses = ["Pending", "Under Review", "Approved/Rejected"]
    current_status_index = 0
    
    if claim.status == "Under Review":
        current_status_index = 1
    elif claim.status in ["Approved", "Rejected"]:
        current_status_index = 2
    
    # Create progress visualization
    col_progress1, col_progress2, col_progress3 = st.columns(3)
    
    with col_progress1:
        status_color = "#10b981" if current_status_index >= 0 else "#e5e7eb"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background-color: {status_color}; 
                    color: white; border-radius: 8px;">
            📋 Filed<br>
            <small>{claim.filed_date}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col_progress2:
        status_color = "#10b981" if current_status_index >= 1 else "#e5e7eb"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background-color: {status_color}; 
                    color: white; border-radius: 8px;">
            🔍 Under Review<br>
            <small>{"In Progress" if current_status_index >= 1 else "Pending"}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col_progress3:
        if claim.status == "Approved":
            status_color = "#10b981"
            icon = "✅"
        elif claim.status == "Rejected":
            status_color = "#ef4444"
            icon = "❌"
        else:
            status_color = "#e5e7eb"
            icon = "⏳"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background-color: {status_color}; 
                    color: white; border-radius: 8px;">
            {icon} {claim.status}<br>
            <small>{claim.processed_date if claim.processed_date else "Pending"}</small>
        </div>
        """, unsafe_allow_html=True)

def show_claim_documents(claim):
    """Display claim documents"""
    st.subheader(f"📎 Documents for Claim: {claim.claim_number}")
    
    if claim.documents:
        st.write(f"**📋 {len(claim.documents)} document(s) uploaded:**")
        
        for i, doc in enumerate(claim.documents):
            col_doc, col_action = st.columns([3, 1])
            
            with col_doc:
                st.write(f"📄 {doc}")
            
            with col_action:
                if st.button(f"👁️ View", key=f"view_doc_{claim.id}_{i}"):
                    st.info(f"📄 Document viewer would open for {doc}")
    else:
        st.info("📭 No documents uploaded yet.")
        
        if st.button("📎 Upload Documents"):
            st.info("📤 Document upload interface would open here.")

def show_payments_billing(user, user_payments, user_policies):
    """Enhanced payments and billing interface"""
    
    st.subheader("💳 Payments & Billing Management")
    
    # Payment summary metrics
    total_paid = sum(p.amount for p in user_payments if p.status == "Completed")
    pending_payments = sum(p.premium_annual for p in user_policies 
                          if p.status == "Active" and datetime.now() > 
                          datetime.strptime(p.next_payment_due, "%Y-%m-%d"))
    
    col_pay1, col_pay2, col_pay3, col_pay4 = st.columns(4)
    
    with col_pay1:
        st.metric("💰 Total Paid", f"₹{total_paid:,.0f}")
    
    with col_pay2:
        st.metric("⏳ Pending Payments", f"₹{pending_payments:,.0f}")
    
    with col_pay3:
        completed_payments = len([p for p in user_payments if p.status == "Completed"])
        st.metric("✅ Completed", completed_payments)
    
    with col_pay4:
        next_payment_due = None
        for policy in user_policies:
            if policy.status == "Active":
                due_date = datetime.strptime(policy.next_payment_due, "%Y-%m-%d")
                if not next_payment_due or due_date < next_payment_due:
                    next_payment_due = due_date
        
        if next_payment_due:
            days_until = (next_payment_due - datetime.now()).days
            st.metric("📅 Next Due", f"{days_until} days")
        else:
            st.metric("📅 Next Due", "No payments due")
    
    st.divider()
    
    # Tabbed interface for payments
    pay_tab1, pay_tab2, pay_tab3, pay_tab4 = st.tabs([
        "💰 Make Payment", 
        "📜 Payment History", 
        "🔄 Auto-Pay Setup",
        "🧾 Download Receipts"
    ])
    
    with pay_tab1:
        show_payment_interface(user, user_policies)
    
    with pay_tab2:
        show_payment_history(user_payments, user_policies)
    
    with pay_tab3:
        show_autopay_setup(user, user_policies)
    
    with pay_tab4:
        show_receipt_download(user_payments)

def show_payment_interface(user, user_policies):
    """Enhanced payment interface"""
    st.subheader("💰 Make Premium Payment")
    
    # Get policies with upcoming payments
    due_policies = []
    for policy in user_policies:
        if policy.status == "Active":
            due_date = datetime.strptime(policy.next_payment_due, "%Y-%m-%d")
            days_until_due = (due_date - datetime.now()).days
            due_policies.append((policy, days_until_due))
    
    # Sort by due date
    due_policies.sort(key=lambda x: x[1])
    
    if due_policies:
        st.subheader("⚡ Upcoming Payments")
        
        for policy, days_until_due in due_policies[:3]:  # Show top 3 upcoming
            urgency_color = "#ef4444" if days_until_due <= 7 else "#f59e0b" if days_until_due <= 30 else "#10b981"
            
            col_policy_pay, col_amount_pay, col_action_pay = st.columns([2, 1, 1])
            
            with col_policy_pay:
                st.markdown(f"""
                <div style="padding: 1rem; border: 1px solid {urgency_color}; border-radius: 8px; margin: 0.5rem 0;">
                    <strong>{policy.type}</strong><br>
                    <small>Policy: {policy.policy_number}</small><br>
                    <small style="color: {urgency_color};">Due: {policy.next_payment_due} ({days_until_due} days)</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col_amount_pay:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <h4 style="margin: 0; color: #1f2937;">₹{policy.premium_annual:,.0f}</h4>
                    <small>Annual Premium</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col_action_pay:
                if st.button(f"💳 Pay Now", key=f"pay_now_{policy.id}", type="primary", use_container_width=True):
                    show_payment_gateway(policy)
    
    st.divider()
    
    # Manual payment selection
    st.subheader("🏦 Select Policy for Payment")
    
    with st.form("manual_payment_form"):
        selected_policy = st.selectbox(
            "Choose Policy",
            options=[p.id for p in user_policies if p.status == "Active"],
            format_func=lambda x: f"{next(p.type for p in user_policies if p.id == x)} - {next(p.policy_number for p in user_policies if p.id == x)}"
        )
        
        if selected_policy:
            policy = next(p for p in user_policies if p.id == selected_policy)
            
            # Payment options
            payment_type = st.radio(
                "Payment Type",
                ["Full Annual Premium", "Monthly Installment", "Custom Amount"],
                horizontal=True
            )
            
            if payment_type == "Full Annual Premium":
                payment_amount = policy.premium_annual
            elif payment_type == "Monthly Installment":
                payment_amount = policy.premium_monthly
            else:
                payment_amount = st.number_input(
                    "Enter Amount (₹)",
                    min_value=100.0,
                    max_value=policy.premium_annual,
                    value=policy.premium_monthly
                )
            
            # Payment method
            payment_method = st.selectbox(
                "Payment Method",
                ["Credit Card", "Debit Card", "Net Banking", "UPI", "Wallet"]
            )
            
            # Display payment summary
            st.subheader("💰 Payment Summary")
            
            col_summary1, col_summary2 = st.columns(2)
            
            with col_summary1:
                st.markdown(f"""
                **Policy Details:**
                - **Type:** {policy.type}
                - **Policy #:** {policy.policy_number}
                - **Coverage:** ₹{policy.coverage_amount:,.0f}
                """)
            
            with col_summary2:
                # Calculate processing fee
                processing_fee = payment_amount * 0.02  # 2% processing fee
                total_amount = payment_amount + processing_fee
                
                st.markdown(f"""
                **Payment Breakdown:**
                - **Premium Amount:** ₹{payment_amount:,.2f}
                - **Processing Fee:** ₹{processing_fee:,.2f}
                - **Total Amount:** ₹{total_amount:,.2f}
                """)
            
            # Terms
            terms_accepted = st.checkbox("I accept the payment terms and conditions")
            
            submitted = st.form_submit_button("🚀 Proceed to Payment", type="primary", use_container_width=True)
            
            if submitted and terms_accepted:
                # Simulate payment processing
                with st.spinner("Processing payment..."):
                    import time
                    time.sleep(2)  # Simulate processing time
                
                # Create payment record
                new_payment = Payment(
                    id=str(len(st.session_state.payments) + 1),
                    amount=total_amount,
                    payment_date=datetime.now().strftime("%Y-%m-%d"),
                    payment_method=payment_method,
                    status="Completed",
                    policy_id=selected_policy,
                    user_id=user.id,
                    transaction_id=f"TXN{random.randint(100000000, 999999999)}"
                )
                
                st.session_state.payments.append(new_payment)
                
                # Update policy payment dates
                for i, p in enumerate(st.session_state.policies):
                    if p.id == selected_policy:
                        st.session_state.policies[i] = Policy(
                            **{**asdict(p), 
                               'last_payment_date': datetime.now().strftime("%Y-%m-%d"),
                               'next_payment_due': (datetime.now() + timedelta(days=365 if payment_type == "Full Annual Premium" else 30)).strftime("%Y-%m-%d")
                            }
                        )
                        break
                
                st.success(f"""
                ✅ **Payment Successful!**
                
                **Transaction ID:** {new_payment.transaction_id}  
                **Amount Paid:** ₹{total_amount:,.2f}  
                **Payment Method:** {payment_method}  
                **Date:** {new_payment.payment_date}
                
                📧 **Receipt sent to:** {user.email}  
                📱 **SMS confirmation sent to:** {user.phone}
                
                Your policy is now updated and active!
                """)
                
                st.balloons()
                st.rerun()
            elif submitted and not terms_accepted:
                st.error("❌ Please accept the payment terms and conditions.")

def show_payment_gateway(policy):
    """Simulate payment gateway interface"""
    st.subheader(f"💳 Payment Gateway - {policy.policy_number}")
    
    with st.form("payment_gateway"):
        # Payment details
        st.markdown(f"""
        **Payment for:** {policy.type}  
        **Policy Number:** {policy.policy_number}  
        **Amount:** ₹{policy.premium_annual:,.2f}
        """)
        
        # Card details (simulation)
        card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
        
        col_exp, col_cvv = st.columns(2)
        with col_exp:
            expiry = st.text_input("MM/YY", placeholder="12/25")
        with col_cvv:
            cvv = st.text_input("CVV", type="password", placeholder="123")
        
        card_holder = st.text_input("Card Holder Name", placeholder="JOHN DOE")
        
        if st.form_submit_button("💳 Pay ₹{:,.2f}".format(policy.premium_annual), type="primary"):
            st.success("🎉 Payment processed successfully!")
            st.balloons()

def show_payment_history(user_payments, user_policies):
    """Payment history display"""
    st.subheader("📜 Payment History")
    
    if user_payments:
        # Create payment history dataframe
        payment_data = []
        for payment in sorted(user_payments, key=lambda x: x.payment_date, reverse=True):
            policy = get_policy_by_id(payment.policy_id)
            policy_name = f"{policy.type} - {policy.policy_number}" if policy else "N/A"
            
            payment_data.append({
                "Date": payment.payment_date,
                "Policy": policy_name,
                "Amount": f"₹{payment.amount:,.2f}",
                "Method": payment.payment_method,
                "Status": payment.status,
                "Transaction ID": payment.transaction_id
            })
        
        df = pd.DataFrame(payment_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Payment trends
        st.subheader("📊 Payment Trends")
        
        # Monthly payment chart
        payments_by_month = {}
        for payment in user_payments:
            month = payment.payment_date[:7]  # YYYY-MM
            payments_by_month[month] = payments_by_month.get(month, 0) + payment.amount
        
        if payments_by_month:
            months = list(payments_by_month.keys())
            amounts = list(payments_by_month.values())
            
            fig = px.line(
                x=months,
                y=amounts,
                title="📈 Monthly Premium Payments",
                labels={"x": "Month", "y": "Amount (₹)"}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 No payment history available.")

def show_autopay_setup(user, user_policies):
    """Auto-pay configuration"""
    st.subheader("🔄 Auto-Pay Configuration")
    
    st.info("""
    🤖 **Auto-Pay Benefits:**
    - Never miss a payment deadline
    - Avoid policy lapse due to non-payment
    - Get early payment discounts
    - Hassle-free premium management
    """)
    
    for policy in user_policies:
        if policy.status == "Active":
            with st.container():
                col_policy_auto, col_status_auto, col_action_auto = st.columns([2, 1, 1])
                
                with col_policy_auto:
                    st.markdown(f"""
                    **{policy.type}**  
                    Policy: {policy.policy_number}  
                    Premium: ₹{policy.premium_annual:,.0f}/year
                    """)
                
                with col_status_auto:
                    # Random auto-pay status for demo
                    autopay_enabled = random.choice([True, False])
                    status_color = "#10b981" if autopay_enabled else "#6b7280"
                    status_text = "✅ Enabled" if autopay_enabled else "⏸️ Disabled"
                    
                    st.markdown(f"""
                    <div style="text-align: center; color: {status_color}; font-weight: 500;">
                        {status_text}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_action_auto:
                    button_text = "⏸️ Disable" if autopay_enabled else "✅ Enable"
                    if st.button(button_text, key=f"autopay_{policy.id}", use_container_width=True):
                        new_status = "Disabled" if autopay_enabled else "Enabled"
                        st.success(f"🔄 Auto-pay {new_status.lower()} for {policy.policy_number}")
                
                st.divider()

def show_receipt_download(user_payments):
    """Receipt download interface"""
    st.subheader("🧾 Download Payment Receipts")
    
    if user_payments:
        st.write("Select payments to download receipts:")
        
        for payment in sorted(user_payments, key=lambda x: x.payment_date, reverse=True):
            col_receipt1, col_receipt2, col_receipt3 = st.columns([2, 1, 1])
            
            with col_receipt1:
                st.write(f"**{payment.payment_date}** - ₹{payment.amount:,.2f}")
                st.write(f"Transaction: {payment.transaction_id}")
            
            with col_receipt2:
                st.write(f"**{payment.payment_method}**")
                st.write(f"Status: {payment.status}")
            
            with col_receipt3:
                if st.button(f"📥 Download", key=f"download_{payment.id}", use_container_width=True):
                    st.success(f"📄 Receipt downloaded for transaction {payment.transaction_id}")
    else:
        st.info("📭 No payment receipts available.")

def show_analytics_reports(user, user_policies, user_claims, user_payments):
    """Comprehensive analytics and reporting"""
    
    st.subheader("📈 Insurance Analytics & Reports")
    
    # Key Performance Indicators
    st.subheader("🎯 Key Performance Indicators")
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
    
    # Calculate KPIs
    total_coverage = sum(p.coverage_amount for p in user_policies if p.status == "Active")
    total_premium_paid = sum(p.amount for p in user_payments if p.status == "Completed")
    total_claims_received = sum(c.amount_approved for c in user_claims if c.status == "Approved")
    claim_success_rate = len([c for c in user_claims if c.status == "Approved"]) / max(len(user_claims), 1) * 100
    insurance_utilization = (total_claims_received / total_premium_paid * 100) if total_premium_paid > 0 else 0
    
    with col_kpi1:
        st.metric("🛡️ Total Coverage", f"₹{total_coverage/100000:.1f}L")
    
    with col_kpi2:
        st.metric("💰 Premium Paid", f"₹{total_premium_paid:,.0f}")
    
    with col_kpi3:
        st.metric("✅ Claims Received", f"₹{total_claims_received:,.0f}")
    
    with col_kpi4:
        st.metric("📊 Claim Success Rate", f"{claim_success_rate:.1f}%")
    
    with col_kpi5:
        st.metric("📈 Insurance ROI", f"{insurance_utilization:.1f}%")
    
    st.divider()
    
    # Analytics tabs
    analytics_tab1, analytics_tab2, analytics_tab3, analytics_tab4 = st.tabs([
        "📊 Portfolio Analysis",
        "💰 Financial Analytics", 
        "📋 Claims Analytics",
        "📈 Trends & Insights"
    ])
    
    with analytics_tab1:
        show_portfolio_analysis(user_policies)
    
    with analytics_tab2:
        show_financial_analytics(user_payments, user_policies)
    
    with analytics_tab3:
        show_claims_analytics(user_claims, user_policies)
    
    with analytics_tab4:
        show_trends_insights(user, user_policies, user_claims, user_payments)

def show_portfolio_analysis(user_policies):
    """Portfolio analysis charts and insights"""
    st.subheader("📋 Insurance Portfolio Analysis")
    
    if user_policies:
        col_port1, col_port2 = st.columns(2)
        
        with col_port1:
            # Policy type distribution
            policy_types = [p.type for p in user_policies if p.status == "Active"]
            type_counts = pd.Series(policy_types).value_counts()
            
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title="🏠 Policy Distribution by Type",
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_port2:
            # Coverage distribution
            coverage_data = [(p.type, p.coverage_amount) for p in user_policies if p.status == "Active"]
            if coverage_data:
                types, coverages = zip(*coverage_data)
                
                fig = px.bar(
                    x=types,
                    y=coverages,
                    title="🛡️ Coverage Amount by Policy Type",
                    labels={"x": "Policy Type", "y": "Coverage Amount (₹)"},
                    color=types,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Premium vs Coverage Analysis
        st.subheader("💰 Premium vs Coverage Efficiency")
        
        efficiency_data = []
        for policy in user_policies:
            if policy.status == "Active":
                efficiency = (policy.coverage_amount / policy.premium_annual) if policy.premium_annual > 0 else 0
                efficiency_data.append({
                    "Policy Type": policy.type,
                    "Premium": policy.premium_annual,
                    "Coverage": policy.coverage_amount,
                    "Efficiency Ratio": efficiency,
                    "Policy Number": policy.policy_number
                })
        
        if efficiency_data:
            df_efficiency = pd.DataFrame(efficiency_data)
            
            fig = px.scatter(
                df_efficiency,
                x="Premium",
                y="Coverage",
                color="Policy Type",
                size="Efficiency Ratio",
                hover_data=["Policy Number"],
                title="📊 Premium vs Coverage Analysis",
                labels={"Premium": "Annual Premium (₹)", "Coverage": "Coverage Amount (₹)"}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Efficiency ranking
            st.subheader("🏆 Policy Efficiency Ranking")
            df_efficiency_sorted = df_efficiency.sort_values("Efficiency Ratio", ascending=False)
            
            for i, row in df_efficiency_sorted.iterrows():
                col_rank, col_details, col_ratio = st.columns([1, 3, 2])
                
                with col_rank:
                    rank = df_efficiency_sorted.index.get_loc(i) + 1
                    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                    st.markdown(f"<h3 style='text-align: center;'>{medal}</h3>", unsafe_allow_html=True)
                
                with col_details:
                    st.write(f"**{row['Policy Type']}** - {row['Policy Number']}")
                    st.write(f"Premium: ₹{row['Premium']:,.0f} | Coverage: ₹{row['Coverage']:,.0f}")
                
                with col_ratio:
                    st.metric("Efficiency Ratio", f"{row['Efficiency Ratio']:.0f}x")
    else:
        st.info("📭 No active policies for portfolio analysis.")

def show_financial_analytics(user_payments, user_policies):
    """Financial analytics and spending patterns"""
    st.subheader("💰 Financial Analytics")
    
    if user_payments:
        # Payment method analysis
        col_fin1, col_fin2 = st.columns(2)
        
        with col_fin1:
            payment_methods = [p.payment_method for p in user_payments]
            method_counts = pd.Series(payment_methods).value_counts()
            
            fig = px.pie(
                values=method_counts.values,
                names=method_counts.index,
                title="💳 Payment Methods Usage",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_fin2:
            # Monthly spending trend
            monthly_spending = {}
            for payment in user_payments:
                month = payment.payment_date[:7]
                monthly_spending[month] = monthly_spending.get(month, 0) + payment.amount
            
            if monthly_spending:
                months = sorted(monthly_spending.keys())
                amounts = [monthly_spending[month] for month in months]
                
                fig = px.line(
                    x=months,
                    y=amounts,
                    title="📈 Monthly Premium Spending",
                    markers=True,
                    labels={"x": "Month", "y": "Amount (₹)"}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Financial summary table
        st.subheader("📊 Financial Summary")
        
        summary_data = []
        for policy in user_policies:
            if policy.status == "Active":
                # Calculate payments for this policy
                policy_payments = [p for p in user_payments if p.policy_id == policy.id]
                total_paid = sum(p.amount for p in policy_payments)
                
                summary_data.append({
                    "Policy Type": policy.type,
                    "Policy Number": policy.policy_number,
                    "Annual Premium": f"₹{policy.premium_annual:,.0f}",
                    "Total Paid": f"₹{total_paid:,.0f}",
                    "Coverage": f"₹{policy.coverage_amount/100000:.1f}L",
                    "Cost per Lakh": f"₹{(policy.premium_annual / (policy.coverage_amount/100000)):,.0f}"
                })
        
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
        
        # Savings and investment recommendations
        st.subheader("💡 Financial Recommendations")
        
        total_annual_premium = sum(p.premium_annual for p in user_policies if p.status == "Active")
        
        col_rec1, col_rec2, col_rec3 = st.columns(3)
        
        with col_rec1:
            st.markdown("""
            <div style="background: linear-gradient(45deg, #10b981, #059669); color: white; padding: 1rem; border-radius: 10px;">
                <h4>💰 Premium Optimization</h4>
                <p>Consider bundling policies for 10-15% discount on total premiums.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_rec2:
            st.markdown("""
            <div style="background: linear-gradient(45deg, #3b82f6, #2563eb); color: white; padding: 1rem; border-radius: 10px;">
                <h4>🎯 Coverage Gap</h4>
                <p>Your coverage-to-income ratio looks optimal. Consider term life insurance.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_rec3:
            annual_savings = total_annual_premium * 0.1  # Assume 10% potential savings
            st.markdown(f"""
            <div style="background: linear-gradient(45deg, #f59e0b, #d97706); color: white; padding: 1rem; border-radius: 10px;">
                <h4>📈 Potential Savings</h4>
                <p>Switch to annual payments to save up to ₹{annual_savings:,.0f}/year.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No payment data available for financial analysis.")

def show_claims_analytics(user_claims, user_policies):
    """Claims analytics and patterns"""
    st.subheader("📋 Claims Analytics")
    
    if user_claims:
        # Claims status distribution
        col_claims1, col_claims2 = st.columns(2)
        
        with col_claims1:
            claim_statuses = [c.status for c in user_claims]
            status_counts = pd.Series(claim_statuses).value_counts()
            
            # Custom colors for claim statuses
            status_colors = {
                "Approved": "#10b981",
                "Pending": "#f59e0b", 
                "Under Review": "#3b82f6",
                "Rejected": "#ef4444"
            }
            
            colors = [status_colors.get(status, "#6b7280") for status in status_counts.index]
            
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="📊 Claims Status Distribution",
                color_discrete_sequence=colors
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_claims2:
            # Claims by policy type
            policy_types_claims = []
            for claim in user_claims:
                policy = get_policy_by_id(claim.policy_id)
                if policy:
                    policy_types_claims.append(policy.type)
            
            if policy_types_claims:
                type_counts = pd.Series(policy_types_claims).value_counts()
                
                fig = px.bar(
                    x=type_counts.index,
                    y=type_counts.values,
                    title="📋 Claims by Policy Type",
                    color=type_counts.values,
                    color_continuous_scale="Blues",
                    labels={"x": "Policy Type", "y": "Number of Claims"}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Claims timeline
        st.subheader("🕒 Claims Timeline Analysis")
        
        claims_timeline = []
        for claim in user_claims:
            claims_timeline.append({
                "Date": claim.filed_date,
                "Amount Claimed": claim.amount_claimed,
                "Amount Approved": claim.amount_approved,
                "Status": claim.status,
                "Processing Days": (datetime.now() - datetime.strptime(claim.filed_date, "%Y-%m-%d")).days
            })
        
        df_timeline = pd.DataFrame(claims_timeline)
        
        fig = px.scatter(
            df_timeline,
            x="Date",
            y="Amount Claimed",
            color="Status",
            size="Amount Approved",
            hover_data=["Processing Days"],
            title="💰 Claims Timeline - Amount vs Date",
            labels={"Amount Claimed": "Claimed Amount (₹)"}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Claims efficiency metrics
        st.subheader("📈 Claims Processing Efficiency")
        
        col_eff1, col_eff2, col_eff3, col_eff4 = st.columns(4)
        
        # Calculate metrics
        avg_processing_time = sum(
            (datetime.now() - datetime.strptime(c.filed_date, "%Y-%m-%d")).days 
            for c in user_claims if c.status in ["Approved", "Rejected"]
        ) / max(len([c for c in user_claims if c.status in ["Approved", "Rejected"]]), 1)
        
        approval_rate = len([c for c in user_claims if c.status == "Approved"]) / max(len(user_claims), 1) * 100
        
        total_claimed = sum(c.amount_claimed for c in user_claims)
        total_approved = sum(c.amount_approved for c in user_claims)
        settlement_ratio = (total_approved / total_claimed * 100) if total_claimed > 0 else 0
        
        avg_claim_size = sum(c.amount_claimed for c in user_claims) / max(len(user_claims), 1)
        
        with col_eff1:
            st.metric("⏱️ Avg Processing Time", f"{avg_processing_time:.0f} days")
        
        with col_eff2:
            st.metric("✅ Approval Rate", f"{approval_rate:.1f}%")
        
        with col_eff3:
            st.metric("💰 Settlement Ratio", f"{settlement_ratio:.1f}%")
        
        with col_eff4:
            st.metric("📊 Avg Claim Size", f"₹{avg_claim_size:,.0f}")
        
        # Claims recommendations
        st.subheader("💡 Claims Insights & Recommendations")
        
        recommendations = []
        
        if approval_rate < 70:
            recommendations.append("📋 Consider reviewing claim documentation quality to improve approval rates.")
        
        if avg_processing_time > 15:
            recommendations.append("⏱️ Processing time is higher than average. Consider following up on pending claims.")
        
        if settlement_ratio < 80:
            recommendations.append("💰 Settlement ratio could be improved. Review policy terms for better claims preparation.")
        
        if not recommendations:
            recommendations.append("🎉 Excellent claims performance! Your claims are processed efficiently.")
        
        for recommendation in recommendations:
            st.info(recommendation)
    
    else:
        st.info("📭 No claims data available for analysis.")
        
        st.markdown("""
        <div class="alert-info">
            <h4>📊 Claims Analytics Preview</h4>
            <p>Once you file claims, you'll see detailed analytics including:</p>
            <ul>
                <li>📈 Claims approval trends</li>
                <li>⏱️ Processing time analysis</li>
                <li>💰 Settlement patterns</li>
                <li>🎯 Policy-wise claim distribution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_trends_insights(user, user_policies, user_claims, user_payments):
    """Advanced trends and predictive insights"""
    st.subheader("📈 Trends & Predictive Insights")
    
    # Insurance portfolio health score
    st.subheader("🏥 Portfolio Health Score")
    
    # Calculate health score based on various factors
    health_factors = {
        "Policy Diversification": min(100, len(set(p.type for p in user_policies if p.status == "Active")) * 25),
        "Coverage Adequacy": min(100, sum(p.coverage_amount for p in user_policies if p.status == "Active") / 5000000 * 100),
        "Claims Efficiency": min(100, len([c for c in user_claims if c.status == "Approved"]) / max(len(user_claims), 1) * 100) if user_claims else 100,
        "Payment Consistency": 100 if user_payments else 0,
        "Risk Management": 100 - calculate_risk_score(user, "Overall")
    }
    
    overall_health = sum(health_factors.values()) / len(health_factors)
    
    # Health score gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = overall_health,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Portfolio Health Score"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Health factors breakdown
    col_health1, col_health2 = st.columns(2)
    
    with col_health1:
        st.subheader("📊 Health Factors Breakdown")
        
        factors_df = pd.DataFrame({
            "Factor": list(health_factors.keys()),
            "Score": list(health_factors.values())
        })
        
        fig = px.bar(
            factors_df,
            x="Score",
            y="Factor",
            orientation="h",
            title="Health Factor Scores",
            color="Score",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100]
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_health2:
        st.subheader("🎯 Improvement Recommendations")
        
        for factor, score in health_factors.items():
            if score < 70:
                if factor == "Policy Diversification":
                    st.warning(f"📋 {factor}: Consider adding different types of insurance coverage.")
                elif factor == "Coverage Adequacy":
                    st.warning(f"🛡️ {factor}: Your total coverage might be insufficient for your needs.")
                elif factor == "Claims Efficiency":
                    st.warning(f"📋 {factor}: Review claim filing procedures to improve success rate.")
                elif factor == "Payment Consistency":
                    st.warning(f"💰 {factor}: Set up auto-pay to ensure consistent premium payments.")
                elif factor == "Risk Management":
                    st.warning(f"⚠️ {factor}: Consider risk mitigation strategies to lower premium costs.")
            else:
                st.success(f"✅ {factor}: Excellent performance!")
    
    # Future projections
    st.subheader("🔮 Future Projections")
    
    col_proj1, col_proj2 = st.columns(2)
    
    with col_proj1:
        st.subheader("💰 Premium Projection (Next 5 Years)")
        
        # Project premium growth
        current_premium = sum(p.premium_annual for p in user_policies if p.status == "Active")
        inflation_rate = 0.06  # 6% annual inflation
        
        years = list(range(2024, 2030))
        projected_premiums = [current_premium * (1 + inflation_rate) ** (year - 2024) for year in years]
        
        fig = px.line(
            x=years,
            y=projected_premiums,
            title="Premium Growth Projection",
            markers=True,
            labels={"x": "Year", "y": "Annual Premium (₹)"}
        )
        fig.add_scatter(
            x=[2024],
            y=[current_premium],
            mode="markers",
            marker=dict(color="red", size=10),
            name="Current Premium"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_proj2:
        st.subheader("🎯 Savings Opportunities")
        
        # Calculate potential savings
        bundling_savings = current_premium * 0.15  # 15% bundling discount
        loyalty_discount = current_premium * 0.05   # 5% loyalty discount
        claim_free_bonus = current_premium * 0.10   # 10% no-claim bonus
        
        savings_data = {
            "Opportunity": ["Policy Bundling", "Loyalty Discount", "No-Claim Bonus", "Annual Payment"],
            "Potential Savings": [bundling_savings, loyalty_discount, claim_free_bonus, current_premium * 0.08]
        }
        
        fig = px.bar(
            savings_data,
            x="Opportunity",
            y="Potential Savings",
            title="Annual Savings Opportunities",
            color="Potential Savings",
            color_continuous_scale="Greens"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Market insights
    st.subheader("📊 Market Insights & Benchmarks")
    
    col_market1, col_market2, col_market3 = st.columns(3)
    
    with col_market1:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #3b82f6, #2563eb); color: white; padding: 1rem; border-radius: 10px;">
            <h4>📈 Industry Average</h4>
            <p><strong>Claim Ratio:</strong> 65%</p>
            <p><strong>Processing Time:</strong> 12 days</p>
            <p><strong>Premium Growth:</strong> 8% annually</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_market2:
        user_claim_ratio = len([c for c in user_claims if c.status == "Approved"]) / max(len(user_claims), 1) * 100 if user_claims else 0
        comparison = "Above" if user_claim_ratio > 65 else "Below" if user_claim_ratio < 65 else "At"
        
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #10b981, #059669); color: white; padding: 1rem; border-radius: 10px;">
            <h4>🎯 Your Performance</h4>
            <p><strong>Claim Ratio:</strong> {user_claim_ratio:.0f}%</p>
            <p><strong>Benchmark:</strong> {comparison} average</p>
            <p><strong>Status:</strong> {"Excellent" if comparison == "Above" else "Good" if comparison == "At" else "Needs Improvement"}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_market3:
        total_coverage = sum(p.coverage_amount for p in user_policies if p.status == "Active")
        coverage_category = "High" if total_coverage > 2000000 else "Medium" if total_coverage > 1000000 else "Basic"
        
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #f59e0b, #d97706); color: white; padding: 1rem; border-radius: 10px;">
            <h4>🛡️ Coverage Analysis</h4>
            <p><strong>Total Coverage:</strong> ₹{total_coverage/100000:.1f}L</p>
            <p><strong>Category:</strong> {coverage_category}</p>
            <p><strong>Recommendation:</strong> {"Well protected" if coverage_category == "High" else "Consider increasing"}</p>
        </div>
        """, unsafe_allow_html=True)

def show_profile_settings(user):
    """User profile and settings management"""
    
    st.subheader("👤 Profile & Account Settings")
    
    # Profile tabs
    profile_tab1, profile_tab2, profile_tab3, profile_tab4 = st.tabs([
        "👤 Personal Information",
        "🔔 Notifications",
        "🔐 Security Settings",
        "📱 Preferences"
    ])
    
    with profile_tab1:
        show_personal_information(user)
    
    with profile_tab2:
        show_notification_settings()
    
    with profile_tab3:
        show_security_settings()
    
    with profile_tab4:
        show_user_preferences()

def show_personal_information(user):
    """Personal information management"""
    st.subheader("👤 Personal Information")
    
    with st.form("profile_form"):
        col_profile1, col_profile2 = st.columns(2)
        
        with col_profile1:
            name = st.text_input("Full Name", value=user.name)
            email = st.text_input("Email Address", value=user.email)
            phone = st.text_input("Phone Number", value=user.phone)
            date_of_birth = st.date_input("Date of Birth", value=datetime.strptime(user.date_of_birth, "%Y-%m-%d").date())
        
        with col_profile2:
            address = st.text_area("Address", value=user.address, height=100)
            aadhar = st.text_input("Aadhar Number", value=user.aadhar_number)
            pan = st.text_input("PAN Number", value=user.pan_number)
        
        # Additional information
        st.subheader("📊 Additional Information")
        
        col_add1, col_add2 = st.columns(2)
        
        with col_add1:
            occupation = st.text_input("Occupation", value="Software Engineer")
            annual_income = st.number_input("Annual Income (₹)", value=1200000, min_value=0)
        
        with col_add2:
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
            dependents = st.number_input("Number of Dependents", value=2, min_value=0, max_value=10)
        
        if st.form_submit_button("💾 Update Profile", type="primary"):
            st.success("✅ Profile updated successfully!")
            st.balloons()

def show_notification_settings():
    """Notification preferences"""
    st.subheader("🔔 Notification Settings")
    
    st.write("**📧 Email Notifications**")
    
    col_email1, col_email2 = st.columns(2)
    
    with col_email1:
        st.checkbox("Policy renewal reminders", value=True)
        st.checkbox("Premium payment due", value=True)
        st.checkbox("Claim status updates", value=True)
        st.checkbox("New policy offers", value=False)
    
    with col_email2:
        st.checkbox("Payment confirmations", value=True)
        st.checkbox("Document expiry alerts", value=True)
        st.checkbox("Newsletter & updates", value=False)
        st.checkbox("Marketing communications", value=False)
    
    st.divider()
    
    st.write("**📱 SMS Notifications**")
    
    col_sms1, col_sms2 = st.columns(2)
    
    with col_sms1:
        st.checkbox("Payment confirmations (SMS)", value=True, key="sms_payment")
        st.checkbox("Claim approvals (SMS)", value=True, key="sms_claim")
    
    with col_sms2:
        st.checkbox("Policy renewals (SMS)", value=True, key="sms_renewal")
        st.checkbox("Emergency alerts (SMS)", value=True, key="sms_emergency")
    
    st.divider()
    
    st.write("**📲 Push Notifications**")
    
    push_enabled = st.toggle("Enable Push Notifications", value=True)
    
    if push_enabled:
        col_push1, col_push2 = st.columns(2)
        
        with col_push1:
            st.checkbox("Real-time claim updates", value=True, key="push_claim")
            st.checkbox("Payment reminders", value=True, key="push_payment")
        
        with col_push2:
            st.checkbox("Policy alerts", value=True, key="push_policy")
            st.checkbox("Special offers", value=False, key="push_offers")
    
    if st.button("💾 Save Notification Preferences", type="primary"):
        st.success("✅ Notification preferences saved!")

def show_security_settings():
    """Security and privacy settings"""
    st.subheader("🔐 Security & Privacy Settings")
    
    st.write("**🔒 Password Security**")
    
    with st.form("password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("🔄 Change Password"):
            if new_password == confirm_password:
                st.success("✅ Password changed successfully!")
            else:
                st.error("❌ Passwords do not match!")
    
    st.divider()
    
    st.write("**🔐 Two-Factor Authentication**")
    
    two_fa_enabled = st.toggle("Enable Two-Factor Authentication", value=False)
    
    if two_fa_enabled:
        st.info("📱 Two-factor authentication will be enabled for your account. You'll receive a setup SMS shortly.")
        
        if st.button("📲 Send Setup SMS"):
            st.success("📱 Setup SMS sent to your registered mobile number!")
    
    st.divider()
    
    st.write("**🛡️ Privacy Settings**")
    
    col_privacy1, col_privacy2 = st.columns(2)
    
    with col_privacy1:
        st.checkbox("Share data for better service", value=True)
        st.checkbox("Allow marketing communications", value=False)
    
    with col_privacy2:
        st.checkbox("Data analytics participation", value=True)
        st.checkbox("Third-party integrations", value=False)
    
    st.divider()
    
    st.write("**📊 Account Activity**")
    
    if st.button("📋 View Login History"):
        st.info("Login history would be displayed here showing recent access details.")
    
    if st.button("🔒 Lock Account"):
        st.warning("⚠️ This will temporarily lock your account. Contact support to unlock.")

def show_user_preferences():
    """User preferences and customization"""
    st.subheader("📱 User Preferences")
    
    st.write("**🎨 Display Settings**")
    
    col_display1, col_display2 = st.columns(2)
    
    with col_display1:
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Telugu", "Bengali"])
    
    with col_display2:
        currency_display = st.selectbox("Currency Display", ["₹ (Indian Rupee)", "$ (US Dollar)", "€ (Euro)"])
        date_format = st.selectbox("Date Format", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
    
    st.divider()
    
    st.write("**📊 Dashboard Preferences**")
    
    default_tab = st.selectbox(
        "Default Dashboard Tab",
        ["Dashboard Overview", "Policy Management", "Claims Center", "Payments & Billing"]
    )
    
    col_dash1, col_dash2 = st.columns(2)
    
    with col_dash1:
        st.checkbox("Show welcome message", value=True)
        st.checkbox("Display quick actions", value=True)
        st.checkbox("Show activity feed", value=True)
    
    with col_dash2:
        st.checkbox("Enable data refresh alerts", value=True)
        st.checkbox("Show policy expiry warnings", value=True)
        st.checkbox("Display premium trends", value=True)
    
    st.divider()
    
    st.write("**💰 Payment Preferences**")
    
    preferred_payment = st.selectbox(
        "Preferred Payment Method",
        ["Credit Card", "Debit Card", "Net Banking", "UPI", "Auto-Debit"]
    )
    
    payment_reminders = st.selectbox(
        "Payment Reminder Timing",
        ["7 days before", "15 days before", "30 days before", "Custom"]
    )
    
    auto_renew = st.checkbox("Enable auto-renewal for policies", value=True)
    
    st.divider()
    
    st.write("**📞 Communication Preferences**")
    
    preferred_contact = st.selectbox(
        "Preferred Contact Method",
        ["Email", "SMS", "Phone Call", "WhatsApp", "In-App Notification"]
    )
    
    contact_hours = st.selectbox(
        "Preferred Contact Hours",
        ["Anytime", "Business Hours (9 AM - 6 PM)", "Evenings (6 PM - 9 PM)", "Weekends Only"]
    )
    
    if st.button("💾 Save Preferences", type="primary"):
        st.success("✅ User preferences saved successfully!")
        st.balloons()

# Main Application
def main():
    """Main application entry point"""
    init_session_state()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()