import os
import shutil
import datetime
import logging
import warnings

warnings.filterwarnings("ignore")

# Initialize logging
logging.basicConfig(filename='organize_files.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def organize_files(source_dir, organize_by='type'):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        logging.error(f"Source directory '{source_dir}' does not exist.")
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Create a dictionary to map file types to destination directories
    type_to_dir = {}

    # Iterate over files in the source directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Determine the file type (extension)
        file_type = filename.split('.')[-1].lower()

        # Handle files based on the chosen organization criteria
        if organize_by == 'type':
            # Organize by file type (extension)
            if file_type not in type_to_dir:
                type_to_dir[file_type] = os.path.join(source_dir, file_type)
                os.makedirs(type_to_dir[file_type], exist_ok=True)
            destination_dir = type_to_dir[file_type]
        elif organize_by == 'date':
            # Organize by file creation date
            try:
                creation_time = os.path.getctime(file_path)
                creation_date = datetime.date.fromtimestamp(creation_time)
                destination_dir = os.path.join(source_dir, str(creation_date))
                os.makedirs(destination_dir, exist_ok=True)
            except Exception as e:
                logging.error(f"Failed to organize '{filename}' by date: {str(e)}")
                print(f"Failed to organize '{filename}' by date: {str(e)}")
                continue
        else:
            logging.error("Invalid organization criteria. Use 'type' or 'date'.")
            print("Invalid organization criteria. Use 'type' or 'date'.")
            return

        # Move the file to the destination directory
        try:
            shutil.move(file_path, os.path.join(destination_dir, filename))
            logging.info(f"Moved '{filename}' to '{destination_dir}'")
            print(f"Moved '{filename}' to '{destination_dir}'")
        except Exception as e:
            logging.error(f"Failed to move '{filename}' to '{destination_dir}': {str(e)}")
            print(f"Failed to move '{filename}' to '{destination_dir}': {str(e)}")

if __name__ == "__main__":
    source_directory = input("Enter the source directory path: ")
    organization_criteria = input("Organize by 'type' or 'date': ").lower()

    if organization_criteria not in ['type', 'date']:
        logging.error("Invalid organization criteria. Use 'type' or 'date'.")
        print("Invalid organization criteria. Use 'type' or 'date'.")
    else:
        organize_files(source_directory, organization_criteria)

