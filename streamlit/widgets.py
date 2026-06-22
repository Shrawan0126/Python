import streamlit as st
import pandas as pd

st.title("Streamlit Text Input")

name = st.text_input("Enter your name : ")

age = st.slider("Select your age : ",0,100,25)

st.write(f"Your age is : {age}")

options = ["Python", "Java", "C++", "JavaScript"]
choice = st.selectbox("Choose your favorite language : ", options)
st.write(f"You selected {choice}.")

if name:
    st.write(f"Hello, {name}!")

data = {
    "name" : ["John", "Alice", "Bob", "Eve"],
    "age" : [30, 25, 35, 28],
    "city" : ["New York", "Los Angeles", "Chicago", "Houston"]
}

df = pd.DataFrame(data)
df.to_csv("sample_data.csv", index=False)
st.write(df)


uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"]) 

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)