# Google Sheets Clone

This project is a web-based application that replicates some basic functionalities of Google Sheets. It allows users to create, edit, and manipulate spreadsheets directly in their browser using **Streamlit**. The app provides various features for managing rows, columns, and cell data, as well as data formatting and mathematical operations.

---

## Features

### Spreadsheet Management
- Create an empty spreadsheet with customizable rows and columns.
- Add or remove rows and columns dynamically.

### Data Editing
- Editable DataFrame with live updates.
- Cell value types: `Text`, `Numeric`, `Date`.
- Trim, uppercase, or lowercase text in cells.
- Validate and convert non-numeric data to numeric where applicable.

### Data Analysis
- Calculate the sum and average of selected cell ranges.
- Highlight selected ranges in the spreadsheet.
- Apply conditional formatting based on cell values.

### Formatting Options
- Apply font styling (bold, italic, font size, font color) to cells.
- Trim whitespace from cell contents.
- Merge cells for better presentation.

### File Handling
- Save the spreadsheet as an Excel file (.xlsx) with a download option.
- Load a spreadsheet from an uploaded Excel file.

### Advanced Features
- Evaluate custom formulas using Python's `eval`.
- Apply cell formatting such as background color and borders.

---

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.7 or later
- pip

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/google-sheets-clone.git
   cd google-sheets-clone
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to the URL provided (usually `http://localhost:8501`).

---

## How to Use

1. **Create or Load a Spreadsheet**:
   - By default, a 5x5 spreadsheet is created when you launch the app.
   - You can upload an existing spreadsheet in `.xlsx` format.

2. **Edit Data**:
   - Click on any cell in the spreadsheet to edit its value.
   - Use the sidebar to set cell value types (e.g., Text, Numeric, Date).

3. **Add or Remove Rows/Columns**:
   - Use the sidebar buttons to add or remove rows and columns dynamically.

4. **Format Data**:
   - Apply font styling, text trimming, and case conversion using the options in the sidebar.

5. **Perform Calculations**:
   - Use the range selection inputs in the sidebar to calculate the sum or average of selected cells.

6. **Save or Load Files**:
   - Save the spreadsheet as an Excel file and download it.
   - Upload a new file to replace the current spreadsheet.

7. **Advanced Features**:
   - Use the formula evaluator to calculate custom values based on the spreadsheet data.
   - Apply conditional formatting to highlight cells based on conditions.

---

## File Structure

```plaintext
.
├── app.py                   # Main application file
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
```

---

## Dependencies

- `streamlit` - Web application framework for creating interactive apps.
- `pandas` - Data manipulation and analysis library.
- `numpy` - Numerical computing library.
- `xlsxwriter` - Used for creating Excel files.

Install these dependencies using the following command:
```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this project as per the terms of the license.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

---

## Author

Developed by [Prashanth K T](https://github.com/prashanthktgowda). If you have any questions, feel free to reach out!

---

## Acknowledgments

- Inspired by Google Sheets.
- Special thanks to the open-source community for their invaluable tools and libraries.

