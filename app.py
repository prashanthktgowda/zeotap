import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

# Function to create an empty spreadsheet with default column names
def create_spreadsheet(rows, cols):
    return pd.DataFrame(np.zeros((rows, cols)), columns=[f"Col {i+1}" for i in range(cols)])

# Function to initialize cell types based on the data structure
def initialize_cell_types(data):
    return pd.DataFrame(
        [["Text"] * data.shape[1] for _ in range(data.shape[0])],
        columns=data.columns
    )

# Function to add a new row
def add_row(data):
    new_row = pd.Series([""] * data.shape[1], index=data.columns)
    return pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

# Function to remove a row
def remove_row(data):
    if data.shape[0] > 1:  # Ensure at least one row remains
        return data.iloc[:-1, :]
    return data

# Function to add a new column
def add_column(data):
    new_col_name = f"Col {data.shape[1] + 1}"
    data[new_col_name] = ""
    return data

# Function to remove a column
def remove_column(data):
    if data.shape[1] > 1:  # Ensure at least one column remains
        return data.iloc[:, :-1]
    return data

# Function to calculate the sum of selected cells
def calculate_sum(data, start_row, end_row, start_col, end_col):
    selected_data = data.iloc[start_row:end_row+1, start_col:end_col+1]
    numeric_data = selected_data.apply(pd.to_numeric, errors='coerce')
    return numeric_data.sum().sum()

# Function to calculate the average of selected cells
def calculate_average(data, start_row, end_row, start_col, end_col):
    selected_data = data.iloc[start_row:end_row+1, start_col:end_col+1]
    numeric_data = selected_data.apply(pd.to_numeric, errors='coerce')
    return numeric_data.mean().mean()

# Function to trim whitespace from all cells
def trim_data(data):
    return data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Function to convert all text to uppercase
def upper_case_data(data):
    return data.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Function to convert all text to lowercase
def lower_case_data(data):
    return data.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Function to validate numeric data
def validate_data(data):
    for col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    return data

# Function to save the spreadsheet to an Excel file
def save_data(data):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False)
        writer.save()
    return buffer

# Function to apply font styling to a cell
def apply_font_style(text, bold=False, italic=False, font_size=None, font_color=None):
    style = ""
    if bold:
        style += "font-weight: bold;"
    if italic:
        style += "font-style: italic;"
    if font_size:
        style += f"font-size: {font_size}px;"
    if font_color:
        style += f"color: {font_color};"
    return f'<span style="{style}">{text}</span>'

# Function to enforce cell value type
def enforce_cell_value_type(value, cell_type):
    if cell_type == "Text":
        return str(value)
    elif cell_type == "Numeric":
        try:
            return float(value)
        except ValueError:
            return None
    elif cell_type == "Date":
        try:
            return pd.to_datetime(value).date()
        except ValueError:
            return None
    else:
        return value

# Function to apply cell formatting (background color, borders)
def apply_cell_style(data, start_row, end_row, start_col, end_col, bg_color=None, border_color=None):
    styled_data = data.copy()
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            style = ""
            if bg_color:
                style += f"background-color: {bg_color};"
            if border_color:
                style += f"border: 1px solid {border_color};"
            styled_data.iat[row, col] = f'<div style="{style}">{data.iat[row, col]}</div>'
    return styled_data

# Function to apply conditional formatting
def apply_conditional_formatting(data, condition, value, highlight_color):
    styled_data = data.copy()
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            cell_value = data.iat[row, col]
            if condition == "greater_than" and cell_value > value:
                styled_data.iat[row, col] = f'<div style="background-color: {highlight_color};">{cell_value}</div>'
            elif condition == "less_than" and cell_value < value:
                styled_data.iat[row, col] = f'<div style="background-color: {highlight_color};">{cell_value}</div>'
            elif condition == "equal_to" and cell_value == value:
                styled_data.iat[row, col] = f'<div style="background-color: {highlight_color};">{cell_value}</div>'
    return styled_data

# Function to merge cells
def merge_cells(data, start_row, end_row, start_col, end_col):
    merged_value = data.iloc[start_row, start_col]
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            data.iat[row, col] = merged_value if row == start_row and col == start_col else ""
    return data

# Function to evaluate formulas
def evaluate_formula(data, formula):
    try:
        return eval(formula, {"__builtins__": None}, {"data": data})
    except Exception as e:
        return f"Error: {e}"

# Main function to run the Streamlit app
def main():
    st.title("Google Sheets Clone")

    # Create or load the spreadsheet
    if 'data' not in st.session_state:
        st.session_state.data = create_spreadsheet(5, 5)  # Default size: 5x5

    # Initialize cell types if not already done
    if 'cell_types' not in st.session_state:
        st.session_state.cell_types = initialize_cell_types(st.session_state.data)

    # Add/Remove Rows and Columns
    st.sidebar.header("Add/Remove Rows and Columns")
    if st.sidebar.button("Add Row"):
        st.session_state.data = add_row(st.session_state.data)
        st.session_state.cell_types = add_row(st.session_state.cell_types)
        st.write("Row added successfully!")

    if st.sidebar.button("Remove Row"):
        st.session_state.data = remove_row(st.session_state.data)
        st.session_state.cell_types = remove_row(st.session_state.cell_types)
        st.write("Row removed successfully!")

    if st.sidebar.button("Add Column"):
        st.session_state.data = add_column(st.session_state.data)
        st.session_state.cell_types = add_column(st.session_state.cell_types)
        st.write("Column added successfully!")

    if st.sidebar.button("Remove Column"):
        st.session_state.data = remove_column(st.session_state.data)
        st.session_state.cell_types = remove_column(st.session_state.cell_types)
        st.write("Column removed successfully!")

    # Font styling options
    st.sidebar.header("Font Styling")
    bold = st.sidebar.checkbox("Bold")
    italic = st.sidebar.checkbox("Italic")
    font_size = st.sidebar.number_input("Font Size", min_value=1, value=12)
    font_color = st.sidebar.color_picker("Font Color", "#000000")

    # Display the editable DataFrame (only the first 100 rows and columns for performance)
    st.session_state.data = st.data_editor(st.session_state.data.iloc[:100, :100], key="spreadsheet")

    # Allow users to select cell value types
    st.sidebar.header("Cell Value Types")
    selected_col = st.sidebar.selectbox("Select Column", st.session_state.data.columns)
    selected_row = st.sidebar.number_input("Select Row", min_value=0, max_value=st.session_state.data.shape[0]-1, value=0)
    cell_type = st.sidebar.selectbox("Select Cell Type", ["Text", "Numeric", "Date"])

    if st.sidebar.button("Set Cell Type"):
        st.session_state.cell_types.at[selected_row, selected_col] = cell_type
        st.write(f"Cell ({selected_row}, {selected_col}) set to {cell_type}.")

    # Apply font styling to selected cells
    if st.sidebar.button("Apply Font Styling"):
        styled_data = st.session_state.data.applymap(
            lambda x: apply_font_style(x, bold, italic, font_size, font_color)
        )
        st.session_state.styled_data = styled_data
        st.write("Font styling applied!")

    # Enforce cell value types
    for row in range(st.session_state.data.shape[0]):
        for col in st.session_state.data.columns:
            cell_value = st.session_state.data.at[row, col]
            cell_type = st.session_state.cell_types.at[row, col]
            st.session_state.data.at[row, col] = enforce_cell_value_type(cell_value, cell_type)

    # Allow users to select a range of cells for SUM and AVERAGE
    st.sidebar.header("Select Range for SUM/AVERAGE")
    start_row = st.sidebar.number_input("Start Row", min_value=0, max_value=st.session_state.data.shape[0]-1, value=0)
    end_row = st.sidebar.number_input("End Row", min_value=0, max_value=st.session_state.data.shape[0]-1, value=st.session_state.data.shape[0]-1)
    start_col = st.sidebar.number_input("Start Column", min_value=0, max_value=st.session_state.data.shape[1]-1, value=0)
    end_col = st.sidebar.number_input("End Column", min_value=0, max_value=st.session_state.data.shape[1]-1, value=st.session_state.data.shape[1]-1)

    # Highlight selected cells
    st.sidebar.header("Highlight Selected Cells")
    if st.sidebar.button("Highlight Selected Range"):
        st.session_state.highlighted_range = (start_row, end_row, start_col, end_col)
        st.write(f"Selected range: Rows {start_row} to {end_row}, Columns {start_col} to {end_col}")

    # Mathematical Functions
    st.sidebar.header("Mathematical Functions")
    if st.sidebar.button("Calculate Sum for Selected Range"):
        sum_result = calculate_sum(st.session_state.data, start_row, end_row, start_col, end_col)
        st.session_state.sum_result = sum_result
        st.write(f"Sum of selected cells: {sum_result}")

    if st.sidebar.button("Calculate Average for Selected Range"):
        avg_result = calculate_average(st.session_state.data, start_row, end_row, start_col, end_col)
        st.session_state.avg_result = avg_result
        st.write(f"Average of selected cells: {avg_result}")

    # Data Quality Functions
    st.sidebar.header("Data Quality Functions")
    if st.sidebar.button("Trim Data"):
        st.session_state.data = trim_data(st.session_state.data)
        st.write("Data trimmed successfully!")

    if st.sidebar.button("Convert to UPPERCASE"):
        st.session_state.data = upper_case_data(st.session_state.data)
        st.write("Data converted to UPPERCASE!")

    if st.sidebar.button("Convert to lowercase"):
        st.session_state.data = lower_case_data(st.session_state.data)
        st.write("Data converted to lowercase!")

    if st.sidebar.button("Validate Data"):
        st.session_state.data = validate_data(st.session_state.data)
        st.write("Data validated. Non-numeric values have been replaced with NaN.")

    # Save and Load Spreadsheet
    st.sidebar.header("Save/Load Spreadsheet")
    if st.sidebar.button("Save Spreadsheet"):
        buffer = save_data(st.session_state.data)
        st.sidebar.download_button(
            label="Download Spreadsheet",
            data=buffer,
            file_name="spreadsheet.xlsx",
            mime="application/vnd.ms-excel"
        )

    uploaded_file = st.sidebar.file_uploader("Upload a spreadsheet", type=["xlsx"])
    if uploaded_file is not None:
        uploaded_data = pd.read_excel(uploaded_file)
        st.session_state.data = uploaded_data
        st.session_state.cell_types = initialize_cell_types(uploaded_data)  # Reinitialize cell types
        st.write("Spreadsheet loaded successfully!")

    # Display the styled spreadsheet
    st.markdown("### Styled Spreadsheet")
    if 'styled_data' in st.session_state:
        st.write(st.session_state.styled_data.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.write(st.session_state.data.to_html(escape=False), unsafe_allow_html=True)

    # Display SUM and AVERAGE results at the bottom of the sheet
    if 'sum_result' in st.session_state:
        st.markdown(f"**Sum of selected cells:** {st.session_state.sum_result}")

    if 'avg_result' in st.session_state:
        st.markdown(f"**Average of selected cells:** {st.session_state.avg_result}")

# Run the app
if __name__ == "__main__":
    main()
