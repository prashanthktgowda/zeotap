# Google Sheets Clone

## Overview
This project is a web-based spreadsheet application that closely mimics the UI and functionalities of Google Sheets. It allows users to enter and manipulate data using various mathematical and data quality functions while maintaining a familiar spreadsheet interface.

## Features

### Spreadsheet Interface:
- Google Sheets-like UI with toolbar and formula bar.
- Supports drag functionality for cell content and selections.
- Cell dependencies are maintained for formula updates.
- Basic cell formatting (bold, italics, font size, color).
- Adding, deleting, and resizing rows and columns.

### Mathematical Functions:
- Supports operations like:
  - **SUM**
  - **AVERAGE**
  - **MAX**
  - **MIN**
  - **COUNT**

### Data Quality Functions:
- Functions include:
  - **TRIM**: Removes leading and trailing spaces.
  - **UPPER**: Converts text to uppercase.
  - **LOWER**: Converts text to lowercase.
  - **REMOVE_DUPLICATES**: Removes duplicate rows from the spreadsheet.
  - **FIND_AND_REPLACE**: Finds and replaces specified text.

### Data Entry and Validation:
- Support for text, numbers, and dates.
- Basic validation checks for numeric inputs.

### Additional Features:
- Data export to CSV.
- Interactive data manipulation with Streamlit UI.

## Tech Stack

### 1. Frontend: **Streamlit**
#### Why Streamlit?
- Provides an easy and efficient way to build interactive web applications.
- Built-in support for data visualization and user-friendly widgets.
- Allows rapid prototyping with minimal code.

### 2. Backend: **Pandas** (for data handling)
#### Why Pandas?
- Provides robust data manipulation and analysis capabilities.
- Efficiently handles spreadsheet-like operations.
- Supports data cleaning, transformations, and calculations.

### 3. Data Storage: **Session State (Streamlit)**
#### Why Session State?
- Allows temporary storage of data within the user's session.
- Eliminates the need for an external database, keeping it lightweight.

## Data Structures Used

### 1. **Pandas DataFrame**:
- Used to store and manipulate spreadsheet data.
- Provides indexing and column management.

### 2. **NumPy Arrays**:
- Used to initialize data with NaN values.
- Enables efficient numerical operations.

### 3. **Python Dictionaries**:
- Utilized for managing user sessions and state variables.

## How to Run

### Install dependencies:
```bash
pip install streamlit pandas numpy
```

### Run the application:
```bash
streamlit run app.py
```

### Open the provided URL in your browser to interact with the application.

## Future Improvements
- Support for complex formulas (absolute/relative references).
- Enhanced charting and visualization features.
- Integration with cloud storage solutions for persistence.

## Author
Developed by **Prashanth K T**.

