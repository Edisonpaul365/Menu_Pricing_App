import streamlit as st
import pandas as pd

# Initialize an empty DataFrame for ingredients
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Ingredient', 'Quantity (grams/units)', 'Price per kg/unit', 'Type', 'Price'])

# Function to calculate price for both per kg and per unit
def calculate_price(row):
    if row['Type'] == 'kg':
        return (row['Price per kg/unit'] / 1000) * row['Quantity (grams/units)']
    elif row['Type'] == 'unit':
        return row['Price per kg/unit'] * row['Quantity (grams/units)']

# Main Streamlit app
st.title("Recipe Cost Calculator")

# Tabs
tab1, tab2 = st.tabs(["Overview & Total Price", "Add/Remove Ingredients"])

# Tab 1: Overview & Total Price
with tab1:
    st.header("Ingredients, Quantities, Prices, and Total Price")
    
    if not st.session_state.df.empty:
        # Auto-calculate price for each ingredient
        st.session_state.df['Price'] = st.session_state.df.apply(calculate_price, axis=1)
        
        # Display the ingredients and their details
        st.table(st.session_state.df[['Ingredient', 'Quantity (grams/units)', 'Price per kg/unit', 'Type', 'Price']])
        
        # Calculate and display the total price
        total_price = st.session_state.df['Price'].sum()
        st.write(f"**Total Price: {total_price}**")
        
        # Remove an ingredient
        ingredient_to_remove = st.selectbox("Select ingredient to remove", st.session_state.df['Ingredient'])
        if st.button("Remove Ingredient"):
            st.session_state.df = st.session_state.df[st.session_state.df['Ingredient'] != ingredient_to_remove]
            st.success(f"Removed {ingredient_to_remove}!")
            st.experimental_rerun()  # Force rerun to reflect changes immediately
    else:
        st.write("No ingredients added yet. Please add ingredients in the next tab.")

# Tab 2: Add/Remove Ingredients
with tab2:
    st.header("Add New Ingredient")
    
    new_ingredient = st.text_input("Ingredient Name")
    new_quantity = st.number_input("Quantity (grams/units)", value=0.0)
    
    # Price type (kg or unit)
    price_type = st.selectbox("Select price type", ['kg', 'unit'])
    
    if price_type == 'kg':
        new_price_per_kg = st.number_input("Price per kg", value=0.0)
    else:
        new_price_per_kg = st.number_input("Price per unit", value=0.0)
    
    if st.button("Add Ingredient"):
        if new_ingredient:
            # Add the new ingredient to the DataFrame
            new_row = pd.DataFrame({
                'Ingredient': [new_ingredient], 
                'Quantity (grams/units)': [new_quantity], 
                'Price per kg/unit': [new_price_per_kg], 
                'Type': [price_type],  # 'kg' or 'unit'
                'Price': [0]  # Price will be calculated automatically
            })
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success("Ingredient added!")
            st.experimental_rerun()  # Force rerun to immediately update prices
        else:
            st.error("Please enter an ingredient name.")

# Display the DataFrame (for debugging purposes if needed)
st.write("Current Data:", st.session_state.df)
