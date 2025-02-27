import os
import sys
import traceback
from modules.config_loader import CONFIG
from modules.excel_reader import ExcelReader
from modules.data_cleaner import DataCleaner
from modules.validator import Validator
from modules.formatter import Formatter
from modules.sql_generator import SQLGenerator
from modules.logger import Logger

class ExcelProcessor:
    """Main class to orchestrate Excel processing pipeline."""
    
    def __init__(self):
        self.input_folder = "input"
        self.output_folder = "output"
        os.makedirs(self.output_folder, exist_ok=True)

    def process_file(self, file_path):
        """Process a single Excel file through all pipeline stages."""
        try:
            Logger.log_info(f"Processing file: {file_path}")

            df, template = ExcelReader.load_excel(file_path)
            df = DataCleaner.clean_data(df, template)
            df = Validator.validate(df, template)
            df = Formatter.format_dates(df, template)

            # Save cleaned file
            output_path = os.path.join(self.output_folder, os.path.basename(file_path))
            df.to_excel(output_path, index=False)
            Logger.log_info(f"Cleaned file saved: {output_path}")

            # Generate and save SQL script
            sql_statements = SQLGenerator.generate_sql(df, template)
            sql_output_path = output_path.replace(".xlsx", ".sql")
            with open(sql_output_path, "w") as sql_file:
                sql_file.write("\n".join(sql_statements))
            
            Logger.log_info(f"SQL script saved: {sql_output_path}")

        except Exception as e:
            Logger.log_error(f"Error processing {file_path}: {str(e)}")
            Logger.log_error(traceback.format_exc())

    def run(self):
        """Run the processor on all Excel files in the input folder."""
        if not os.path.exists(self.input_folder):
            Logger.log_error(f"Input folder '{self.input_folder}' not found.")
            sys.exit(1)

        files = [f for f in os.listdir(self.input_folder) if f.endswith(".xlsx")]
        if not files:
            Logger.log_warning("No Excel files found in the input directory.")
            return

        if CONFIG["settings"].get("batch_processing", False):
            Logger.log_info("Batch processing enabled.")
            for file in files:
                self.process_file(os.path.join(self.input_folder, file))
        else:
            Logger.log_info("Processing files one by one.")
            for file in files:
                self.process_file(os.path.join(self.input_folder, file))

if __name__ == "__main__":
    processor = ExcelProcessor()
    processor.run()
