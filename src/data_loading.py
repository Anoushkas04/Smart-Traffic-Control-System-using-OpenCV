import zipfile
from pathlib import Path

# --- Configuration ---
# This script assumes it is executed from:
# ~/Projects/Labs/cvLab/traffic-control/src/

# 1. Input File Location (ZIP file containing 25 images)
# We use the absolute path provided by the user.
# NOTE: Assumes the ZIP file is actually named 'untitled folder.zip' at the specified location.
ZIP_FILE_PATH_STR = "/Users/raman/Downloads/untitled folder.zip" 

# 2. Output Directory Location (This path remains relative to the user's home directory ~)
OUTPUT_RELATIVE_PATH = Path("Projects") / "Labs" / "cvLab" / "traffic-control" / "data" / "raw_templates"

# --- Path Setup ---

# Determine the user's home directory (~)
HOME_DIR = Path.home()

# Full path to the input ZIP file (resolved from the string)
# If the user's path already starts with /Users/raman, we can convert it directly.
ZIP_PATH = Path(ZIP_FILE_PATH_STR) 

# Full path to the target output directory
OUTPUT_DIR = HOME_DIR / OUTPUT_RELATIVE_PATH

# --- Main Extraction Logic ---

def extract_images_from_zip(zip_path: Path, output_dir: Path):
    """
    Extracts all contents from the ZIP archive directly into the specified output directory.
    """
    print("--- Image Extraction Tool ---")
    print(f"ZIP Source: {zip_path}")
    print(f"Destination: {output_dir}")

    # 1. Check if the input file exists
    if not zip_path.is_file():
        print(f"\nERROR: ZIP file not found at {zip_path}")
        print("Please check the absolute path and ensure the file is correctly named and located.")
        return

    # 2. Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nTarget directory ready: {output_dir}")

    # 3. Perform the extraction
    try:
        print(f"Attempting to extract all images from {zip_path.name}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # zip_ref.extractall() extracts all members to the target path.
            zip_ref.extractall(output_dir)
            
            # Count the files extracted for confirmation
            extracted_count = len([f for f in output_dir.iterdir() if f.is_file()])
            
            print(f"\nSUCCESS: Extracted {extracted_count} file(s) into the required directory.")
            
    except zipfile.BadZipFile:
        print(f"ERROR: The file at {zip_path} is not a valid ZIP archive.")
        print("Please ensure the file is a compressed .zip archive.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during extraction: {e}")
        return


if __name__ == "__main__":
    # Note: We now use the absolute path provided by the user directly.
    # If the user is not 'raman', Path.home() might conflict with /Users/raman/.
    # For safety, we use the literal path string provided.
    if "raman" not in ZIP_FILE_PATH_STR and HOME_DIR.name != "raman":
        print("\nWARNING: The absolute path specified contains 'raman', but this may not match the current user's home directory. Proceeding with the literal path.")
        
    extract_images_from_zip(ZIP_PATH, OUTPUT_DIR)