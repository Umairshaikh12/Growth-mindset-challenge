# name = "umair"
# age = 30
# price = 20.5
# a = None
# print("My name is :" , name )
# print("My age is: " , age)
# print(type(name))
# print(type(age))
# print(type(price))
# print(type(a))

# num = 40
# num = 45
# sum = num + num
# print(sum)

# a = 2
# b = 3
# text = "@"
# print(a*text*b)

# name = input("name:")
# age = (input("age:"))
# price = (input("price:"))

# A = int (input("A : "))
# G = input ("M/F:")
# if ((A == 1 or A == 2) and G == "M"):
#     print("fee is 100")
# elif (A == 3 or A == 4 or G == "F"):
#     print("fee is 200")
# elif (A == 5 and G == "M"):
#     print("fee is 300")
# else:
#     print("no fee")

# food = input("food:")
# eat = "yes" if food == "cake" else "no"
# print(eat)

# food = input("food:")
# print("delicious") if food == "cake" else print("not delicious")


import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter and Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# Enable multiple file uploads
files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        # Fill missing values
        if st.checkbox(f"Fill missing values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values filled with mean")
            st.dataframe(df.head())

        # Column selection
        selected_columns = st.multiselect(f"Select columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show chart if numeric data exists
        if st.checkbox(f"Show chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File format selection
        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "xlsx"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime_type = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("Download file", file_name=new_name, data=output, mime=mime_type)

            st.success("Processing Complete")


        
 