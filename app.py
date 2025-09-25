import streamlit as st
import pandas as pd
import json
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import List, Dict, Any
import os

# Configure page
st.set_page_config(
    page_title="Insurance Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .status-active {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    .status-pending {
        background-color: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    .status-approved {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class User:
    id: str
    name: str
    email: str
    phone: str
    address: str

@dataclass
class Policy:
    id: str
    policy_number: str
    type: str
    premium: float
    coverage: float
    status: str
    start_date: str
    end_date: str
    description: str
    user_id: str

@dataclass
class Claim:
    id: str
    claim_number: str
    amount: float
    status: str
    description: str
    incident_date: str
    filed_date: str
    policy_id: str
    user_id: str

@dataclass
class Activity:
    id: str
    type: str
    description: str
    timestamp: str
    user_id: str

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Sample data
USERS = [
    User("1", "John Doe", "john@example.com", "+1-555-0123", "123 Main St, Anytown, USA"),
    User("2", "Jane Smith", "jane@example.com", "+1-555-0124", "456 Oak Ave, Anytown, USA")
]

POLICIES = [
    Policy("1", "AUTO-2024-001", "Auto", 1200, 50000, "Active", "2024-01-15", "2025-01-15", "Comprehensive Auto Insurance", "1"),
    Policy("2", "HOME-2024-001", "Home", 800, 250000, "Active", "2024-03-01", "2025-03-01", "Homeowners Insurance", "1"),
    Policy("3", "LIFE-2024-001", "Life", 2400, 500000, "Active", "2024-02-10", "2025-02-10", "Term Life Insurance", "1"),
    Policy("4", "AUTO-2024-002", "Auto", 1100, 45000, "Active", "2024-04-01", "2025-04-01", "Standard Auto Insurance", "2")
]

CLAIMS = [
    Claim("1", "CLM-2024-001", 5000, "Approved", "Car accident repair - rear-end collision", "2024-08-10", "2024-08-15", "1", "1"),
    Claim("2", "CLM-2024-002", 1200, "Pending", "Water damage to basement from pipe burst", "2024-08-30", "2024-09-01", "2", "1"),
    Claim("3", "CLM-2024-003", 800, "Under Review", "Windshield replacement", "2024-09-10", "2024-09-12", "4", "2")
]

ACTIVITIES = [
    Activity("1", "POLICY_CREATED", "New Auto insurance policy created", "2024-01-15 10:00:00", "1"),
    Activity("2", "CLAIM_SUBMITTED", "Claim submitted for car accident", "2024-08-15 14:30:00", "1"),
    Activity("3", "CLAIM_APPROVED", "Claim CLM-2024-001 approved and processed", "2024-08-20 09:15:00", "1"),
    Activity("4", "POLICY_CREATED", "New Home insurance policy created", "2024-03-01 11:00:00", "1"),
    Activity("5", "CLAIM_SUBMITTED", "Claim submitted for water damage", "2024-09-01 16:00:00", "1")
]

def authenticate(email: str, password: str) -> User:
    """Simple authentication - in production use proper auth"""
    if email == "demo@insurance.com" and password == "demo":
        return USERS[0]
    return None

def get_user_policies(user_id: str) -> List[Policy]:
    return [p for p in POLICIES if p.user_id == user_id]

def get_user_claims(user_id: str) -> List[Claim]:
    return [c for c in CLAIMS if c.user_id == user_id]

def get_user_activities(user_id: str) -> List[Activity]:
    return [a for a in ACTIVITIES if a.user_id == user_id]

def get_policy_by_id(policy_id: str) -> Policy:
    return next((p for p in POLICIES if p.id == policy_id), None)

def login_page():
    """Login interface"""
    st.markdown('<h1 class="main-header">🏥 Insurance Management System</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Your Account")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", value="demo@insurance.com", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", value="demo", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_button:
                user = authenticate(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        # Demo credentials info
        st.info("""
        **🎭 Demo Credentials:**
        
        **Email:** demo@insurance.com  
        **Password:** demo
        
        *Click Login to access your insurance dashboard*
        """)
        
        # Features preview
        st.markdown("### ✨ What You Can Do:")
        col_feat1, col_feat2 = st.columns(2)
        
        with col_feat1:
            st.markdown("""
            - 📋 **Policy Management**
            - 💰 **Claims Tracking** 
            - 📊 **Dashboard Analytics**
            """)
        
        with col_feat2:
            st.markdown("""
            - 🔔 **Activity Timeline**
            - 📈 **Premium Overview**
            - 🏆 **Coverage Summary**
            """)

def dashboard_page():
    """Main dashboard interface"""
    user = st.session_state.current_user
    
    # Header
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown(f'<h1 class="main-header">🏥 Welcome back, {user.name}!</h1>', unsafe_allow_html=True)
    with col_header2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
    
    # Get user data
    user_policies = get_user_policies(user.id)
    user_claims = get_user_claims(user.id)
    user_activities = get_user_activities(user.id)
    
    # Calculate metrics
    total_premium = sum(p.premium for p in user_policies if p.status == "Active")
    total_coverage = sum(p.coverage for p in user_policies if p.status == "Active")
    pending_claims = len([c for c in user_claims if c.status in ["Pending", "Under Review"]])
    approved_claims = len([c for c in user_claims if c.status == "Approved"])
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏅 Active Policies",
            value=len([p for p in user_policies if p.status == "Active"]),
            delta="All current"
        )
    
    with col2:
        st.metric(
            label="💵 Annual Premium",
            value=f"${total_premium:,.0f}",
            delta=f"{len(user_policies)} policies"
        )
    
    with col3:
        st.metric(
            label="🛡️ Total Coverage",
            value=f"${total_coverage:,.0f}",
            delta="Protected"
        )
    
    with col4:
        st.metric(
            label="📋 Claims Status",
            value=f"{pending_claims} Pending",
            delta=f"{approved_claims} Approved"
        )
    
    st.divider()
    
    # Main content in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏠 Policies", "💼 Claims", "📈 Analytics"])
    
    with tab1:
        # Overview dashboard
        col_over1, col_over2 = st.columns([2, 1])
        
        with col_over1:
            st.subheader("📋 Policy Portfolio")
            
            # Create policy dataframe for display
            policy_df = pd.DataFrame([
                {
                    "Policy": p.policy_number,
                    "Type": p.type,
                    "Premium": f"${p.premium:,.0f}",
                    "Coverage": f"${p.coverage:,.0f}",
                    "Status": p.status,
                    "Expires": p.end_date
                }
                for p in user_policies
            ])
            
            if not policy_df.empty:
                # Style the dataframe
                styled_df = policy_df.style.apply(
                    lambda x: ['background-color: #d1fae5' if v == 'Active' 
                              else 'background-color: #fef3c7' if v == 'Pending' 
                              else '' for v in x], 
                    subset=['Status']
                )
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
            else:
                st.info("No policies found.")
        
        with col_over2:
            st.subheader("🎯 Quick Stats")
            
            # Policy type distribution
            if user_policies:
                policy_types = [p.type for p in user_policies]
                type_counts = pd.Series(policy_types).value_counts()
                
                fig = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Policy Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent activity
            st.subheader("📢 Recent Activity")
            recent_activities = sorted(user_activities, key=lambda x: x.timestamp, reverse=True)[:5]
            
            for activity in recent_activities:
                st.markdown(f"""
                <div style="padding: 0.5rem; margin: 0.5rem 0; background-color: #f3f4f6; border-radius: 5px;">
                    <strong>{activity.type.replace('_', ' ').title()}</strong><br>
                    <small>{activity.description}</small><br>
                    <small style="color: #6b7280;">{activity.timestamp}</small>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🏠 Your Insurance Policies")
        
        for policy in user_policies:
            with st.container():
                col_pol1, col_pol2, col_pol3 = st.columns([2, 1, 1])
                
                with col_pol1:
                    icon = "🚗" if policy.type == "Auto" else "🏠" if policy.type == "Home" else "❤️" if policy.type == "Life" else "📄"
                    st.markdown(f"""
                    ### {icon} {policy.type} Insurance
                    **Policy:** {policy.policy_number}  
                    **Description:** {policy.description}
                    """)
                
                with col_pol2:
                    status_color = "🟢" if policy.status == "Active" else "🟡"
                    st.markdown(f"""
                    **Status:** {status_color} {policy.status}  
                    **Premium:** ${policy.premium:,.0f}/year  
                    **Coverage:** ${policy.coverage:,.0f}
                    """)
                
                with col_pol3:
                    st.markdown(f"""
                    **Start:** {policy.start_date}  
                    **End:** {policy.end_date}  
                    **Duration:** Active
                    """)
                
                st.divider()
    
    with tab3:
        st.subheader("💼 Claims Management")
        
        if user_claims:
            for claim in user_claims:
                policy = get_policy_by_id(claim.policy_id)
                policy_name = f"{policy.type} - {policy.policy_number}" if policy else "Unknown Policy"
                
                # Status styling
                if claim.status == "Approved":
                    status_style = "background-color: #10b981; color: white;"
                elif claim.status == "Pending":
                    status_style = "background-color: #f59e0b; color: white;"
                elif claim.status == "Under Review":
                    status_style = "background-color: #3b82f6; color: white;"
                else:
                    status_style = "background-color: #6b7280; color: white;"
                
                st.markdown(f"""
                <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <h4 style="margin: 0; color: #1f2937;">🎫 {claim.claim_number}</h4>
                        <span style="{status_style} padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem;">
                            {claim.status}
                        </span>
                    </div>
                    <p><strong>Amount:</strong> ${claim.amount:,.0f}</p>
                    <p><strong>Description:</strong> {claim.description}</p>
                    <p><strong>Policy:</strong> {policy_name}</p>
                    <p><strong>Incident Date:</strong> {claim.incident_date} | <strong>Filed:</strong> {claim.filed_date}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No claims found. Great job staying safe!")
        
        # Add new claim form
        with st.expander("➕ File New Claim"):
            with st.form("new_claim"):
                st.subheader("Submit New Insurance Claim")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    claim_policy = st.selectbox(
                        "Select Policy",
                        options=[p.id for p in user_policies],
                        format_func=lambda x: f"{next(p.type for p in user_policies if p.id == x)} - {next(p.policy_number for p in user_policies if p.id == x)}"
                    )
                    claim_amount = st.number_input("Claim Amount ($)", min_value=0.0, value=1000.0)
                    incident_date = st.date_input("Incident Date")
                
                with col_form2:
                    claim_description = st.text_area("Description of Incident", placeholder="Describe what happened...")
                
                submitted = st.form_submit_button("🚀 Submit Claim")
                
                if submitted:
                    st.success(f"✅ Claim submitted successfully! You will receive a claim number via email shortly.")
                    st.balloons()
    
    with tab4:
        st.subheader("📈 Insurance Analytics")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Premium breakdown chart
            if user_policies:
                policy_data = pd.DataFrame([
                    {"Policy Type": p.type, "Annual Premium": p.premium, "Coverage": p.coverage}
                    for p in user_policies if p.status == "Active"
                ])
                
                fig = px.bar(
                    policy_data, 
                    x="Policy Type", 
                    y="Annual Premium",
                    title="📊 Annual Premium by Policy Type",
                    color="Policy Type",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            # Coverage analysis
            if user_policies:
                fig = px.bar(
                    policy_data, 
                    x="Policy Type", 
                    y="Coverage",
                    title="🛡️ Coverage Amount by Policy Type",
                    color="Policy Type",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Claims timeline
        if user_claims:
            st.subheader("🕒 Claims Timeline")
            
            claims_data = pd.DataFrame([
                {
                    "Date": claim.filed_date,
                    "Amount": claim.amount,
                    "Status": claim.status,
                    "Claim": claim.claim_number
                }
                for claim in user_claims
            ])
            
            fig = px.scatter(
                claims_data,
                x="Date",
                y="Amount",
                color="Status",
                size="Amount",
                hover_data=["Claim"],
                title="💰 Claims Over Time"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application logic"""
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
