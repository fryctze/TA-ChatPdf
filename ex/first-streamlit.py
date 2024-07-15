import streamlit as st
import numpy as np

# Title and description for your app
st.title("Hello World! ")
st.text("This is a simple Streamlit app.")

# Displaying text
name = st.text_input("Enter your name:")
st.write("Hello,", name)

# Checkbox for user interaction
if st.checkbox("Show image"):
    st.image("path/to/your/image.jpg")

# Displaying data
data = {"A": 1, "B": 2, "C": 3}
st.write("Here's some data:")
st.json(data)

# Simple chart example
x = np.linspace(0.0, 5.0, 100)
y = np.sin(x)
st.line_chart(y)
