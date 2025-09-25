# 🚗 CDrive Vehicle Insurance Management System

A comprehensive, modern vehicle insurance case management system built with Python and Streamlit. This enterprise-grade application handles the complete vehicle insurance lifecycle from lead generation to policy issuance and renewals.

## ✨ Features

### 🔐 Role-Based Access Control
- **Admin**: Complete system access, user management, analytics
- **Team Lead**: Team management, case assignment, team analytics  
- **Executive**: Case creation, follow-ups, personal performance tracking

### 📋 Complete 9-Step Vehicle Insurance Case Creation Workflow
1. **Customer Details** - Comprehensive customer information capture
2. **Vehicle Details** - Complete vehicle information with real Indian car makes/models
3. **Coverage Options** - Comprehensive vs Third Party with add-on covers
4. **Quote Generation** - Intelligent premium calculation with multiple plan options
5. **Documentation** - Vehicle-specific document collection and verification
6. **Policy Finalization** - Terms acceptance and executive assignment
7. **Payment Processing** - Multiple payment methods and secure processing
8. **Policy Issuance** - Automated policy generation with document delivery
9. **Follow-up Setup** - Automated scheduling for renewals and customer service

### 🚗 Comprehensive Vehicle Insurance Coverage
- **Third Party Insurance** - Legal compliance coverage
- **Comprehensive Insurance** - Complete protection including own damage
- **Add-on Covers**: Zero Depreciation, Engine Protection, Roadside Assistance, Key Replacement, Return to Invoice
- **IDV Calculation** - Automatic depreciation-based valuation
- **NCB Integration** - No Claim Bonus discount application

### 🏢 Indian Vehicle Data Integration
Complete database of Indian car manufacturers and models:
- **Maruti Suzuki**: Swift, Baleno, Brezza, Dzire, Ertiga, and 13+ models
- **Hyundai**: Creta, Venue, i20, Verna, Alcazar, and 9+ models  
- **Tata**: Nexon, Punch, Harrier, Safari, and 10+ models
- **Mahindra**: XUV700, Thar, Scorpio, Bolero, and 6+ models
- **Honda, Toyota, Kia, MG, Skoda** and 10+ more brands
- **Real-time Vehicle Valuation** based on make, model, year, and variant

### 📊 Advanced Analytics & Reporting
- Real-time dashboard with vehicle insurance metrics
- Policy status tracking and conversion rates
- Premium collection and vehicle type analytics
- Executive performance monitoring
- Vehicle brand and fuel type distribution charts

### 💼 Vehicle Insurance Specific Features
- **Registration Number Validation** - Indian vehicle registration format
- **Engine Capacity Tracking** - CC for petrol/diesel, kW for electric
- **Fuel Type Management** - Petrol, Diesel, CNG, Electric, Hybrid
- **RTO Location Tracking** - Regional transport office details
- **Previous Insurance Integration** - NCB calculation and transfer
- **Vehicle Inspection** - Photo requirements and damage assessment

### 🎨 Modern UI/UX Features
- **Mobile Responsive** - Optimized for all device sizes
- **Modern Design** - Gradient backgrounds, card layouts, animations
- **Professional Styling** - Clean, insurance industry appropriate interface
- **Indian Rupee (₹)** - Localized currency formatting
- **Interactive Components** - Hover effects, progress indicators, status badges

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Git account
- Streamlit Cloud account (for deployment)

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd cdrive-insurance-app
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access the application**
Open your browser to `http://localhost:8501`

### 🌐 Cloud Deployment

#### Option 1: Streamlit Cloud (Recommended)

1. **Create GitHub Repository**
   - Upload all files to a new GitHub repository
   - Ensure `app.py` and `requirements.txt` are in the root directory

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Set main file as `app.py`
   - Click "Deploy"

## 📱 Usage Guide

### Getting Started

1. **Select Your Role**
   - Use the dropdown at the top to switch between Admin, Team Lead, or Executive
   - Each role has different permissions and menu options

2. **Dashboard Overview**
   - View key metrics: total policies, active policies, premium collections
   - Monitor vehicle types and fuel type distribution
   - Review recent vehicle insurance cases

3. **Creating New Vehicle Insurance Cases**
   - Navigate to "Create New Case" from the sidebar
   - Follow the 9-step guided workflow for vehicle insurance
   - Select from comprehensive Indian vehicle database
   - Configure coverage options and add-ons

### 🚗 Vehicle Insurance Features

#### Comprehensive Coverage Options
- **IDV Calculation**: Automatic depreciation-based vehicle valuation
- **Add-on Covers**: Zero depreciation, engine protection, roadside assistance
- **NCB Integration**: Automatic no-claim bonus calculation
- **Multi-year Policies**: 1, 2, or 3-year policy options

#### Indian Market Specific
- **Registration Validation**: Supports all Indian state RTO formats
- **Vehicle Database**: Complete database of Indian car models with variants
- **Fuel Type Support**: Petrol, Diesel, CNG, Electric, Hybrid, LPG
- **Regional Pricing**: State-wise premium variations

## 🔧 Technical Architecture

### Built With
- **Frontend**: Streamlit with custom CSS/HTML
- **Backend**: Python with pandas for data management
- **Visualization**: Plotly for interactive charts
- **Data**: Comprehensive Indian vehicle database
- **Styling**: Custom CSS with mobile-first responsive design

### Key Technical Features
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Calculations**: Live premium computation and IDV calculation
- **Modular Architecture**: Clean separation of vehicle insurance logic
- **Data Validation**: Comprehensive vehicle and insurance data validation
- **Performance Optimized**: Efficient vehicle data lookup and premium calculation

## 💾 Sample Data

The application comes pre-loaded with realistic vehicle insurance sample data:
- 5 sample vehicle insurance cases across different vehicle types
- Various policy statuses and coverage types
- Sample customer information with Indian names and phone numbers
- Realistic premium calculations based on vehicle values
- Document tracking examples for vehicle insurance

## 🚗 Vehicle Insurance Business Logic

### Premium Calculation Engine
- **Third Party Rates**: Based on engine capacity as per Indian regulations
- **Comprehensive Rates**: IDV-based calculation with multiple factors
- **Vehicle Type Multipliers**: Different rates for hatchback, sedan, SUV
- **Driver Age Factors**: Age-based risk adjustment
- **NCB Discounts**: No Claim Bonus percentage application
- **Add-on Pricing**: Individual add-on cover premium calculation

### Coverage Types
1. **Third Party Only**
   - Legal compliance coverage
   - Fixed rates based on engine capacity
   - Covers third-party injury/death and property damage

2. **Comprehensive Coverage**
   - Own damage + third party coverage
   - Theft and natural calamity protection
   - Optional add-on covers
   - IDV-based premium calculation

## 📈 Insurance Analytics

The system tracks and displays:
- Vehicle insurance penetration by brand
- Fuel type distribution in policies
- Coverage type preferences (Comprehensive vs Third Party)
- Premium collection by vehicle category
- Policy renewal rates and customer retention

## 🛠️ Customization

### Adding New Vehicle Models
1. Update the `CAR_DATA` dictionary in `app.py`
2. Add new manufacturers and their models
3. System automatically includes them in dropdowns

### Modifying Premium Calculations
- Adjust base rates in the premium calculation functions
- Add new factors like city-wise rates
- Implement dynamic pricing based on market conditions

## 🔮 Future Enhancements

Planned features for vehicle insurance:
- **Digital Policy Cards**: QR code-based policy verification
- **Claim Management**: End-to-end claims processing workflow  
- **Vehicle Inspection**: Photo-based damage assessment
- **API Integration**: Real-time vehicle valuation APIs
- **WhatsApp Integration**: Policy delivery and customer communication
- **Telematics Integration**: Usage-based insurance (UBI) support

## 📝 License

This vehicle insurance management system is developed by MiniMax Agent for enterprise insurance operations.

---

**Ready to revolutionize your vehicle insurance operations? Get started today!** 🚗✨