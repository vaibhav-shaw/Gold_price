import streamlit as st

# Page configuration
st.set_page_config(
    page_title="💎 Kanchan Jewellers",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load CSS styles
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load main styles
load_css('styles.css')

def calculate_final_cost(weight: float, metal_type: str, carats: int = None, rate_per_gram: float = 0, making_charges_percent: float = 14.0) -> dict:
    # Calculate base cost for given weight
    base_cost = weight * rate_per_gram
    
    # Calculate making charges with different discounts for gold and silver
    making_charges = base_cost * (making_charges_percent / 100)
    
    if metal_type == "Gold":
        discounted_making_charges = making_charges * 0.75  # 25% discount on making charges for gold
        discount_percent = "25%"
    else:  # Silver
        discounted_making_charges = making_charges * 0.50  # 50% discount on making charges for silver
        discount_percent = "50%"
    
    # Calculate the cost before GST
    cost_before_gst = base_cost + discounted_making_charges
    
    # Calculate GST (3% on the cost before GST)
    gst = cost_before_gst * 0.03
    
    # Calculate final cost with GST
    final_cost = cost_before_gst + gst
    
    # Prepare result with all parameters
    result = {
        "Weight (grams)": weight,
        "Metal Type": metal_type,
        "Rate per gram": rate_per_gram,
        "Base Cost": base_cost,
        "Making Charges": making_charges,
        "Discounted Making Charges": discounted_making_charges,
        "Discount": (making_charges - discounted_making_charges),
        "Discount Percent": discount_percent,
        "Cost Before GST": cost_before_gst,
        "GST (3%)": gst,
        "Final Cost": final_cost
    }
    
    # Add carat info for gold
    if metal_type == "Gold" and carats:
        result["Carats"] = carats
    
    return result

# No theme toggle needed

# Main interface
st.markdown('<h1 class="main-header">💎 Kanchan Jewellers</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Shuddhata Ki Pehchan</p>', unsafe_allow_html=True)

# Input section
st.subheader("Jewelry Details")

# Metal type selection
metal_type = st.selectbox(
    "Metal Type",
    ["Gold", "Silver"],
    index=0,
    help="Select the type of metal"
)

# User inputs with better styling
weight = st.number_input(
    "Weight (grams)",
    min_value=0.01,
    step=0.01,
    value=10.0,
    help="Enter the weight of jewelry in grams",
    key="weight_input"
)

# Default rates
default_gold_rates = {18: 10400, 22: 12100, 24: 13000}
default_silver_rate = 190

carats = None
rate_per_gram = 0

if metal_type == "Gold":
    carats = st.selectbox(
        "Carat Purity",
        [18, 22, 24],
        index=1,
        help="Select the purity of gold"
    )
    
    rate_per_gram = st.number_input(
        f"Gold Rate per gram ({carats}K)",
        min_value=0.0,
        step=100.0,
        value=float(default_gold_rates[carats]),
        help="Enter or adjust the current gold rate per gram",
        key=f"gold_rate_{carats}"
    )
    
    st.info(f"📈 Current rate for {carats}K gold: ₹{rate_per_gram:,.0f}/gram (₹{rate_per_gram*10:,.0f}/10g)")
    
else:  # Silver
    rate_per_10gram = st.number_input(
        "Silver Rate per 10 gram",
        min_value=0.0,
        step=100.0,
        value=float(default_silver_rate * 10),
        help="Enter or adjust the current silver rate per 10 grams",
        key="silver_rate"
    )
    
    # Convert back to per gram for calculation
    rate_per_gram = rate_per_10gram / 10
    
    st.info(f"📈 Current silver rate: ₹{rate_per_gram:,.0f}/gram (₹{rate_per_10gram:,.0f}/10g)")

making_charges_percent = st.number_input(
    "Making Charges (%)",
    min_value=0.0,
    step=0.1,
    value=14.0,
    help="Enter making charges percentage"
)
    
# Calculate button
calculate_clicked = st.button("Calculate Final Cost", use_container_width=True)

if calculate_clicked:
    result = calculate_final_cost(weight, metal_type, carats, rate_per_gram, making_charges_percent)
    if result:
        st.subheader("Price Calculation")
        
        # Professional metrics display
        st.metric(
            label="Final Amount",
            value=f"₹{result['Final Cost']:,.2f}",
            delta=f"Including GST: ₹{result['GST (3%)']:,.2f}"
        )
        
        st.metric(
            label="Discount Applied",
            value=f"₹{result['Discount']:,.2f}",
            delta=f"{result['Discount Percent']} off making charges"
        )
        
        # Detailed breakdown
        st.subheader("Price Breakdown")
        
        # Mobile-friendly breakdown display
        st.write(f"**Metal:** {result['Metal Type']}" + (f" ({result['Carats']}K)" if 'Carats' in result else ""))
        st.write(f"**Weight:** {result['Weight (grams)']} grams")
        st.write(f"**Rate:** ₹{result['Rate per gram']:,.0f}/gram")
        
        st.divider()
        
        st.write(f"**Base Cost:** ₹{result['Base Cost']:,.2f}")
        st.write(f"**Making Charges:** ₹{result['Making Charges']:,.2f}")
        st.write(f"**After Discount:** ₹{result['Discounted Making Charges']:,.2f}")
        st.write(f"**Before GST:** ₹{result['Cost Before GST']:,.2f}")
        st.write(f"**GST (3%):** ₹{result['GST (3%)']:,.2f}")
        
        st.divider()
        
        st.markdown(f"### **Final Amount: ₹{result['Final Cost']:,.2f}**")
else:
    st.info("👆 Enter the jewelry details and click 'Calculate Final Cost' to see the results")

# Sidebar with additional information
with st.sidebar:
    st.header("ℹ️ Information")
    
    st.markdown("### About Us")
    st.write("**Shuddhata Ki Pehchan - Kanchan Jewellers**")
    st.write("Your trusted partner for premium jewelry with transparent pricing and exceptional service during festive seasons.")
    
    st.markdown("### Features")
    st.write("• Gold & Silver calculations")
    st.write("• Editable metal rates")
    st.write("• Mobile-optimized interface")
    st.write("• 25% discount on gold making charges")
    st.write("• 50% discount on silver making charges")
    st.write("• GST included (3%)")
    st.write("• Multiple carat options for gold")
    
    st.markdown("### Support")
    st.write("For technical support, contact the development team.")
    
    st.markdown("---")
    st.markdown("**Developed by:** Vaibhav Shaw")
    st.markdown("**Version:** 2.1")
