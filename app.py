import streamlit as st
import pandas as pd
import numpy as np

# --- Initialize session state ---
if "spreadsheet" not in st.session_state:
    # Default 5x5 empty DataFrame
    st.session_state.spreadsheet = pd.DataFrame(
        [["" for _ in range(5)] for _ in range(5)], columns=list("ABCDE")
    )
if "styles" not in st.session_state:
    # A dictionary to store font styles for specific cell ranges
    st.session_state.styles = {}

# --- Helper Functions ---
def perform_operation(data, operation, range_start, range_end):
    try:
        # Map column letters to DataFrame column indices
        col_map = {chr(65 + i): i for i in range(len(data.columns))}  # A -> 0, B -> 1, etc.
        start_row, start_col = int(range_start[1:]) - 1, col_map[range_start[0]]
        end_row, end_col = int(range_end[1:]) - 1, col_map[range_end[0]]

        # Extract the range of data
        subrange = data.iloc[start_row:end_row + 1, start_col:end_col + 1]
        subrange_numeric = subrange.apply(pd.to_numeric, errors="coerce")  # Convert to numeric

        # Perform the specified operation
        if operation == "SUM":
            return subrange_numeric.sum().sum()
        elif operation == "AVERAGE":
            return subrange_numeric.mean().mean()
        elif operation == "MAX":
            return subrange_numeric.max().max()
        elif operation == "MIN":
            return subrange_numeric.min().min()
        elif operation == "COUNT":
            return subrange_numeric.count().sum()
        else:
            return "Invalid operation"
    except Exception as e:
        return f"Error: {e}"

def apply_data_quality_function(df, operation, find_text=None, replace_text=None):
    if operation == "TRIM":
        return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    elif operation == "UPPER":
        return df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    elif operation == "LOWER":
        return df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    elif operation == "REMOVE_DUPLICATES":
        return df.drop_duplicates()
    elif operation == "FIND_AND_REPLACE" and find_text and replace_text:
        return df.replace(find_text, replace_text, regex=True)
    return df


def apply_styles_to_dataframe(df, styles):
    """Apply font styles to a DataFrame using HTML rendering."""
    styled_df = df.style

    for (range_start, range_end), style in styles.items():
        # Map range
        col_map = {chr(65 + i): i for i in range(len(df.columns))}  # A -> 0, B -> 1, etc.
        start_row, start_col = int(range_start[1:]) - 1, col_map[range_start[0]]
        end_row, end_col = int(range_end[1:]) - 1, col_map[range_end[0]]

        # Iterate through the specified range and apply styles
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                styled_df = styled_df.applymap(
                    lambda _: (
                        f"color: {style['font_color']}; "
                        f"font-size: {style['font_size']}px; "
                        f"font-weight: {style['font_style']};"
                    ),
                    subset=(df.index[row], df.columns[col]),
                )
    return styled_df



# --- App Layout ---
st.title("Google Sheets Mimic - Streamlit")

st.sidebar.header("Features")
save_file = st.sidebar.button("Save File")
load_file = st.sidebar.file_uploader("Load Spreadsheet", type=["xlsx"])
data_quality = st.sidebar.selectbox(
    "Data Quality Functions", ["None", "TRIM", "UPPER", "LOWER", "REMOVE_DUPLICATES", "FIND_AND_REPLACE"]
)

# Editable spreadsheet
st.write("### Editable Spreadsheet")
edited_spreadsheet = st.data_editor(
    st.session_state.spreadsheet, num_rows="dynamic", use_container_width=True
)
st.session_state.spreadsheet = edited_spreadsheet

# --- Data Quality Functions ---
if data_quality != "None":
    if data_quality == "FIND_AND_REPLACE":
        find_text = st.text_input("Find Text")
        replace_text = st.text_input("Replace Text")
        if st.button("Apply Find and Replace"):
            st.session_state.spreadsheet = apply_data_quality_function(
                st.session_state.spreadsheet, data_quality, find_text, replace_text
            )
    else:
        st.session_state.spreadsheet = apply_data_quality_function(
            st.session_state.spreadsheet, data_quality
        )

# --- Mathematical Functions ---
st.write("### Mathematical Functions")

# Dropdown for selecting operation
operation = st.selectbox(
    "Select Operation",
    ["SUM", "AVERAGE", "MAX", "MIN", "COUNT"]
)

# Input range for operation
range_start = st.text_input("Enter Start Cell (e.g., A1)", value="A1")
range_end = st.text_input("Enter End Cell (e.g., B3)", value="B3")

# Automatically calculate result when data changes
if operation and range_start and range_end:
    result = perform_operation(st.session_state.spreadsheet, operation, range_start, range_end)
    st.success(f"Result of {operation} from {range_start} to {range_end}: {result}")

# --- Font Style Features ---
st.write("### Font Styling Options")

# Font size, color, and style inputs
font_size = st.number_input("Font Size (in px)", min_value=8, max_value=36, value=12, step=1)
font_color = st.color_picker("Font Color", value="#000000")
font_style = st.selectbox("Font Style", ["normal", "bold", "italic"])

# Apply styles to a range
if st.button("Apply Font Style"):
    st.session_state.styles[(range_start, range_end)] = {
        "font_size": font_size,
        "font_color": font_color,
        "font_style": font_style,
    }
    st.success(f"Font style applied to range {range_start}:{range_end}")

# Render styled DataFrame
st.write("### Styled Spreadsheet (Preview)")
styled_df = apply_styles_to_dataframe(st.session_state.spreadsheet, st.session_state.styles)
st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

# --- Save and Load ---
if save_file:
    # Save to Excel
    file_name = st.text_input("Enter file name", value="spreadsheet.xlsx")
    st.session_state.spreadsheet.to_excel(file_name, index=False)
    st.success(f"Spreadsheet saved successfully as {file_name}!")

if load_file:
    try:
        st.session_state.spreadsheet = pd.read_excel(load_file)
        st.success("Spreadsheet loaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")

# --- Bonus Features ---
st.write("### Bonus Features")
if st.button("Create Chart (Sum by Columns)"):
    chart_data = st.session_state.spreadsheet.apply(pd.to_numeric, errors="coerce").sum()
    st.bar_chart(chart_data)
