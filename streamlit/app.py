import streamlit as st
import pandas as pd
import numpy as np

## Title of the app
st.title("Hello Streamlit")

## Display a simple text
st.write("This is a simple Streamlit app to demonstrate basic features.")

## create a simple dataframe
df = pd.DataFrame({
    'First Column': [1, 2, 3, 4],
    'Second Column': [10, 20, 30, 40]
})

## Display the dataframe
st.write("Here is the dataframe:")
st.dataframe(df)

## Create a simple line chart
chart_data = pd.DataFrame(
    np.random.randn(20,3), columns = ['a', 'b', 'c']
)
st.line_chart(chart_data)