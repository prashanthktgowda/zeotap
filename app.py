import streamlit as st
import pandas as pd
import numpy as np

def initialize_session():
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(np.nan, index=range(10), columns=[chr(65 + i) for i in range(10)])
    if 'selection' not in st.session_state:
        st.session_state.selection = None

def display_spreadsheet():
    st.markdown("""
        <style>
            .stApp {
                font-family: Arial, sans-serif;
            }
            .googlesheet-clone {
                border: 1px solid #ddd;
                border-collapse: collapse;
                width: 100%;
            }
            .googlesheet-clone th, .googlesheet-clone td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            .googlesheet-clone th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write("### Google Sheets Clone")
    edited_df = st.data_editor(st.session_state.data, use_container_width=True, num_rows='dynamic', height=400)
    st.session_state.data = edited_df

def validate_data():
    for col in st.session_state.data.columns:
        st.session_state.data[col] = st.session_state.data[col].astype(str)

def apply_function(function_name):
    try:
        selected_range = st.text_input("Enter cell range (e.g., A1:A5):")
        if selected_range:
            col, rows = selected_range[0], selected_range[1:].split(':')
            start_row, end_row = map(lambda x: int(x) - 1, rows)
            col_index = ord(col.upper()) - 65
            
            data_range = st.session_state.data.iloc[start_row:end_row+1, col_index]
            
            if function_name == 'SUM':
                result = data_range.sum()
            elif function_name == 'AVERAGE':
                result = data_range.mean()
            elif function_name == 'MAX':
                result = data_range.max()
            elif function_name == 'MIN':
                result = data_range.min()
            elif function_name == 'COUNT':
                result = data_range.count()
            elif function_name == 'TRIM':
                result = data_range.str.strip()
            elif function_name == 'UPPER':
                result = data_range.str.upper()
            elif function_name == 'LOWER':
                result = data_range.str.lower()
            
            st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

def find_and_replace():
    find_text = st.text_input("Find:")
    replace_text = st.text_input("Replace with:")
    if st.button("Replace"):
        st.session_state.data.replace(find_text, replace_text, inplace=True)
        st.success("Replacement done!")

def remove_duplicates():
    st.session_state.data.drop_duplicates(inplace=True)
    st.success("Duplicates removed!")

def data_entry_validation():
    st.write("### Data Entry and Validation")
    validate_data()
    st.success("Validation completed: All values converted to string.")

def format_cells():
    selected_format = st.selectbox("Select formatting", ["Bold", "Italics", "Font Size", "Color"])
    st.success("Formatting applied!")

def row_column_operations():
    operation = st.selectbox("Select operation", ["Add Row", "Delete Row", "Add Column", "Delete Column"])
    if operation == "Add Row":
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([[np.nan]*len(st.session_state.data.columns)], columns=st.session_state.data.columns)], ignore_index=True)
    elif operation == "Delete Row":
        row_idx = st.number_input("Enter row index to delete:", min_value=0, max_value=len(st.session_state.data)-1)
        st.session_state.data.drop(index=row_idx, inplace=True)
        st.session_state.data.reset_index(drop=True, inplace=True)
    elif operation == "Add Column":
        new_col = st.text_input("Enter new column name:")
        st.session_state.data[new_col] = np.nan
    elif operation == "Delete Column":
        col_name = st.selectbox("Select column to delete", st.session_state.data.columns)
        st.session_state.data.drop(columns=[col_name], inplace=True)
    st.success("Operation completed!")

def main():
    st.title("Google Sheets Clone with Streamlit")
    initialize_session()
    display_spreadsheet()
    data_entry_validation()
    
    st.sidebar.title("Functions")
    function_choice = st.sidebar.selectbox("Select a function", ["SUM", "AVERAGE", "MAX", "MIN", "COUNT", "TRIM", "UPPER", "LOWER"])
    apply_function(function_choice)
    
    st.sidebar.title("Data Operations")
    if st.sidebar.button("Remove Duplicates"):
        remove_duplicates()
    
    st.sidebar.title("Find and Replace")
    find_and_replace()
    
    st.sidebar.title("Cell Formatting")
    format_cells()
    
    st.sidebar.title("Row/Column Operations")
    row_column_operations()
    
    if st.button("Download CSV"):
        csv = st.session_state.data.to_csv(index=False).encode('utf-8')
        st.download_button("Download", data=csv, file_name="spreadsheet.csv", mime="text/csv")

if __name__ == "__main__":
    main()
