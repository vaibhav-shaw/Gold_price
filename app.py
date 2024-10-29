import streamlit as st

def calculate_final_cost(weight: float, carats: int = 22, making_charges_percent: float = 14.0) -> dict:
    # Define rate per gram based on carat
    if carats == 24:
        rate_per_gram = 8175
    elif carats == 22:
        rate_per_gram = 7600
    elif carats == 18:
        rate_per_gram = 6540
    else:
        st.error("Unsupported carat value. Only 18, 22, and 24 carat rates are available.")
        return None
    
    # Calculate base cost for given weight
    base_cost = weight * rate_per_gram
    
    # Calculate making charges with 25% discount applied
    making_charges = base_cost * (making_charges_percent / 100)
    discounted_making_charges = making_charges * 0.75  # 25% discount on making charges
    
    # Calculate the cost before GST
    cost_before_gst = base_cost + discounted_making_charges
    
    # Calculate GST (3% on the cost before GST)
    gst = cost_before_gst * 0.03
    
    # Calculate final cost with GST
    final_cost = cost_before_gst + gst
    
    # Prepare result with all parameters
    result = {
        "Weight (grams)": weight,
        "Carats": carats,
        "Rate per gram": rate_per_gram,
        "Base Cost": base_cost,
        "Making Charges": making_charges,
        "Discounted Making Charges": discounted_making_charges,
        "Discount": (making_charges - discounted_making_charges),
        "Cost Before GST": cost_before_gst,
        "GST (3%)": gst,
        "Final Cost": final_cost
    }
    
    return result

# Streamlit interface
st.title("Jewelry Cost Calculator")

# User input
weight = st.number_input("Enter weight in grams:", min_value=0.01, step=0.01, value=0.02)
carats = st.selectbox("Select carat value:", [18, 22, 24], index=1)
making_charges_percent = st.number_input("Enter making charges (%):", min_value=0.0, step=0.1, value=14.0)

if st.button("Calculate"):
    result = calculate_final_cost(weight, carats, making_charges_percent)
    if result:
        st.subheader("Calculation Results:")
        for key, value in result.items():
            if isinstance(value, float):
                st.write(f"{key}: {round(value, 2)}")
            else:
                st.write(f"{key}: {value}")
