import streamlit as st

# Set the title of the app
st.title("Interactive Streamlit App")

# Create a slider
slider_value = st.slider("Select a number", 0, 100)

# Display the value of the slider
st.write(f"You selected {slider_value}")
