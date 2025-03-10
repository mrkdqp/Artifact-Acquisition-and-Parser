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

def acquire_live():
    acquired_hives = {}

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = os.path.join(os.getcwd(), "ExtractedFiles", timestamp)
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

def process_hives(base_folder):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = os.path.join(os.getcwd(), "ExtractedFiles", timestamp)
    os.makedirs(output_folder, exist_ok=True)
    
    hives = {}
    base_path = os.path.join(base_folder, "C")
    for hive, relative_path in HIVES.items():
        hive_path = os.path.join(base_path, relative_path)
        if os.path.exists(hive_path):
            hives[hive] = hive_path
        
    if not hives:
        print("No valid registry hives found in offline directory.")
        return
    
    for hive, path in hives.items():
        hive_output_dir = os.path.join(output_folder, hive)
        os.makedirs(hive_output_dir, exist_ok=True)
        parse_registry(path, hive_output_dir)
    
    merge_csvs(output_folder)

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: tool.exe <mode>")
        print("Modes: live, offline")
        return

    mode = sys.argv[1].strip().lower()
    
    if mode == "live":
        hives, output_dir = acquire_live()
        for hive, path in hives.items():
            if path:
                hive_output_dir = os.path.join(output_dir, hive)
                os.makedirs(hive_output_dir, exist_ok=True)
                parse_registry(path, hive_output_dir)
        merge_csvs(output_dir)
    elif mode == "offline":
        offline_folder = os.path.join(os.getcwd(), "OfflineFiles")
        process_hives(offline_folder)
    else:
        print("Invalid mode selected. Use 'live' or 'offline'.")

if __name__ == "__main__":
    main()