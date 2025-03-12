import sys
import os
import csv
import subprocess
import pandas as pd
from datetime import datetime
from regipy.registry import RegistryHive

RECMD = r"RECmd.exe"
BATCH_FILE = r"BatchExamples\\DFIRBatch.reb"

HIVES = {
    "SAM": "Windows\\System32\\config\\SAM",
    "SECURITY": "Windows\\System32\\config\\SECURITY",
    "SOFTWARE": "Windows\\System32\\config\\SOFTWARE",
    "SYSTEM": "Windows\\System32\\config\\SYSTEM",
    "NTUSER": "Users\\Default\\NTUSER.DAT"
}

def get_next_folder_number():
    extracted_files_path = os.path.join(os.getcwd(), "ExtractedFiles")
    if not os.path.exists(extracted_files_path):
        return 1

    existing_folders = [int(folder) for folder in os.listdir(extracted_files_path) if folder.isdigit()]
    return max(existing_folders) + 1 if existing_folders else 1

def acquire_live():
    acquired_hives = {}

    folder_number = get_next_folder_number()
    output_folder = os.path.join(os.getcwd(), "ExtractedFiles", str(folder_number))
    os.makedirs(output_folder, exist_ok=True)

    kape_path = r"KAPE\\kape.exe"
    kape_cmd = f'"{kape_path}" --tsource C: --tdest "{output_folder}" --target RegistryHives'

    try:
        result = subprocess.run(kape_cmd, shell=True, check=True)
        if result.returncode == 0:
            print(f"KAPE successfully acquired Registry hives and saved them to {output_folder}")

            base_path = os.path.join(output_folder, "C")
            for hive, relative_path in HIVES.items():
                hive_path = os.path.join(base_path, relative_path)
                acquired_hives[hive] = hive_path if os.path.exists(hive_path) else None

            for hive, path in acquired_hives.items():
                if path:
                    print(f"{hive} acquired successfully at {os.path.relpath(path, os.getcwd())}.")
                else:
                    print(f"{hive} not found.")
        else:
            print("Failed to acquire hives with KAPE. Check KAPE installation and permissions.")
    except subprocess.CalledProcessError:
        print("Failed to run KAPE command. Ensure KAPE is correctly configured.")

    return acquired_hives, output_folder

def parse_registry(hive_path, output_folder):
    command = f'{RECMD} -f "{hive_path}" --csv "{output_folder}" --bn "{BATCH_FILE}"'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully parsed {hive_path} and saved output to {output_folder}")
    except subprocess.CalledProcessError:
        print(f"Failed to parse {hive_path}. Check if RECmd is correctly configured.")

def merge_csvs(output_dir):
    all_dfs = []
    for hive_dir in os.listdir(output_dir):
        hive_dir_path = os.path.join(output_dir, hive_dir)
        if os.path.isdir(hive_dir_path):
            for file in os.listdir(hive_dir_path):
                file_path = os.path.join(hive_dir_path, file)
                if file.endswith('.csv'):
                    df = pd.read_csv(file_path)
                    df.insert(0, 'Hive', hive_dir)
                    all_dfs.append(df)

    if not all_dfs:
        print("No CSV files found to merge.")
        return

    combined_df = pd.concat(all_dfs, ignore_index=True)
    merged_csv_path = os.path.join(output_dir, 'merged_registry.csv')
    combined_df.to_csv(merged_csv_path, index=False)
    print(f"Merged CSVs saved to {merged_csv_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: tool.exe <mode>")
        print("Modes: live, offline")
        return

    mode = sys.argv[1].strip().lower()

    if mode == "live":
        action = input("Choose action: (1) Acquire hives, (2) Parse and merge hives, (3) Both: ")
        if action == "1":
            acquire_live()
        elif action == "2":
            folder_number = input("Enter the folder number inside ExtractedFiles to parse: ")
            parse_folder = os.path.join(os.getcwd(), "ExtractedFiles", folder_number)
            hives = {hive: os.path.join(parse_folder, "C", relative_path) for hive, relative_path in HIVES.items()}

            for hive, path in hives.items():
                if os.path.exists(path):
                    hive_output_dir = os.path.join(parse_folder, hive)
                    os.makedirs(hive_output_dir, exist_ok=True)
                    parse_registry(path, hive_output_dir)

            merge_csvs(parse_folder)
        elif action == "3":
            hives, output_dir = acquire_live()
            for hive, path in hives.items():
                if path:
                    hive_output_dir = os.path.join(output_dir, hive)
                    os.makedirs(hive_output_dir, exist_ok=True)
                    parse_registry(path, hive_output_dir)
            merge_csvs(output_dir)
        else:
            print("Invalid choice.")
    elif mode == "offline":
        offline_folder = os.path.join(os.getcwd(), "OfflineFiles")  # Original hive files
        folder_number = get_next_folder_number()  # Creates a new subfolder number for parsed files
        extracted_folder = os.path.join(os.getcwd(), "ExtractedFiles", str(folder_number))
        os.makedirs(extracted_folder, exist_ok=True)  # Folder to store parsed files

        hives = {hive: os.path.join(offline_folder, "C", relative_path) for hive, relative_path in HIVES.items()}

        for hive, path in hives.items():
            if os.path.exists(path):
                hive_output_dir = os.path.join(extracted_folder, hive)  # Parsed files go in ExtractedFiles
                os.makedirs(hive_output_dir, exist_ok=True)
                parse_registry(path, hive_output_dir)

        # After parsing, merge the results from ExtractedFiles folder and save them back to the same folder
        merge_csvs(extracted_folder)
    else:
        print("Invalid mode selected. Use 'live'.")


if __name__ == "__main__":
    main()
