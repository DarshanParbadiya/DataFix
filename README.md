# DataFix : Excel Processing System - Documentation

## 1. Overview
The **Excel Processing System** is an enterprise-level Python application designed to process Excel files dynamically. It supports:
- Data validation using **Pandera**
- Data cleansing (removing empty & duplicate rows)
- Configurable field validation rules
- Date formatting based on a user-defined format
- SQL script generation from processed data
- Batch processing of multiple files

This system is highly **scalable**, **configurable**, and supports **new templates** without requiring code changes.

---

## 2. Project Structure
```
├── ExcelProcessor/
│   ├── config.yaml
│   ├── main.py
│   ├── logs/
│   │   ├── process.log
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── excel_reader.py
│   │   ├── data_cleaner.py
│   │   ├── validator.py
│   │   ├── formatter.py
│   │   ├── sql_generator.py
│   │   ├── batch_processor.py
│   │   ├── logger.py
│   ├── tests/
│   │   ├── test_validator.py
│   │   ├── test_cleaner.py
│   ├── output/
│   ├── input/
```

---

## 3. Configuration - `config.yaml`
The `config.yaml` file defines templates, validation rules, and settings.

```yaml
templates:
  template_1:
    input_columns:
      - "SSM NAME"
      - "EAP CASE REFERENCE NUMBER"
      - "NEW EAP START DATE"
      - "ADDITIONAL NOTES (if needed)"
    output_columns:
      - "SSM NAME"
      - "EAP CASE REFERENCE NUMBER"
      - "NEW EAP START DATE"
      - "ADDITIONAL NOTES (if needed)"
    mandatory_fields:
      - "SSM NAME"
      - "EAP CASE REFERENCE NUMBER"
    date_fields:
      - "NEW EAP START DATE"
    sql_template: "INSERT INTO eap_data (ssm_name, case_ref, start_date, notes) VALUES (?, ?, ?, ?);"
    field_rules:
      "SSM NAME":
        datatype: "string"
        validation:
          min_length: 3
      "EAP CASE REFERENCE NUMBER":
        datatype: "integer"
        validation:
          min_value: 1000
          max_value: 999999
      "NEW EAP START DATE":
        datatype: "date"
      "ADDITIONAL NOTES (if needed)":
        datatype: "string"
        validation:
          max_length: 255

settings:
  date_format: "dd-mm-yy"
  logging_level: "INFO"
  batch_processing: true
```

---

## 4. Main Processing Flow (`main.py`)
The `main.py` file orchestrates the processing of Excel files:

1. Reads the **Excel file** and identifies the matching template.
2. Cleans the data by removing empty and duplicate rows.
3. Validates fields using **Pandera** based on `config.yaml`.
4. Formats date fields according to the configured format.
5. Generates an SQL script from the validated data.
6. Saves both the cleaned file and SQL script in the `output/` directory.

```python
if __name__ == "__main__":
    input_folder = "input"
    for file in os.listdir(input_folder):
        if file.endswith(".xlsx"):
            process_file(os.path.join(input_folder, file))
```

---

## 5. Module Breakdown
### 5.1 `excel_reader.py`
- Reads Excel files dynamically.
- Identifies the correct template based on column names.

### 5.2 `data_cleaner.py`
- Removes duplicate and empty rows.
- Ensures mandatory fields are present.

### 5.3 `validator.py`
- Uses **Pandera** to enforce field-level data validation.
- Applies checks for **string length, numeric ranges, and date format**.

### 5.4 `formatter.py`
- Converts date fields to the configured format.

### 5.5 `sql_generator.py`
- Converts cleaned and validated data into **SQL insert statements**.

### 5.6 `logger.py`
- Handles **error logging** and system activity tracking.

---

## 6. Testing Suite (`tests/`)
We use **pytest** for testing individual modules.

### Example Test Case - `test_cleaner.py`
```python
def test_cleaner_removes_duplicates():
    data = {"SSM NAME": ["John Doe", "John Doe"], "EAP CASE REFERENCE NUMBER": [1234, 1234]}
    df = pd.DataFrame(data)
    cleaned_df = DataCleaner.clean_data(df, CONFIG["templates"]["template_1"])
    assert len(cleaned_df) == 1
```

Run tests with:
```bash
pytest tests/
```

---

## 7. Error Handling & Logging
- All errors are logged in `logs/process.log`.
- **Example log entry:**
```log
2025-02-27 10:15:32 - INFO - Processing file: input/sample1.xlsx
2025-02-27 10:15:35 - ERROR - Validation failed for field 'EAP CASE REFERENCE NUMBER'.
```

---

## 8. Deployment & Usage
### **Requirements**
- Python 3.8+
- Required Libraries:
```bash
pip install pandas openpyxl yaml pandera pytest
```

### **How to Run**
1. Place Excel files inside `input/`.
2. Run the program:
```bash
python main.py
```
3. Processed files will be saved in `output/`.

---

## 9. Future Enhancements
🚀 **Possible upgrades:**
- Add a **CLI Interface** for user-friendly execution.
- Implement a **GUI application** for non-technical users.
- Enable **database connectivity** for direct data insertion.

Would you like any modifications to this documentation? 🚀

