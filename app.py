import streamlit as st

# Title and Text Display
st.title("Streamlit App Test")
st.write("This is a simple Streamlit app to test functionalities.")

# User Input with Checkbox
name = st.text_input("Enter your name:")

if st.checkbox("Show Greeting"):
  if name:
    st.write(f"Hello, {name}!")
  else:
    st.warning("Please enter your name first!")

# Selectbox for choosing a fruit
fruits = ["Apple", "Banana", "Orange"]
selected_fruit = st.selectbox("Select your favorite fruit:", fruits)

st.write(f"You selected: {selected_fruit}")

# Button Click Event
if st.button("Click me!"):
  st.balloons()  # Fun element to show a success message

# Display Code (Optional)
if st.checkbox("Show App Code"):
  st.code(open(__file__, 'r').read())