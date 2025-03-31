Sure! Here's an updated version of the instructions, incorporating the artifact acquisition and REGISTRY hives analysis, as well as the requirement to create an `OfflineFiles` folder for offline mode:

---

## Artifact Acquisition & REGISTRY Hive Analysis

This tool is designed to help with artifact acquisition and the analysis of REGISTRY hives, commonly used in digital forensics or incident response. It extracts relevant files and data from the system, analyzes registry hives, and provides output that can be further examined.

### How to Run the Code

You can run the code in two ways: **Python** or **.exe**. Below are the steps for each method.

---

### 1. Run Python Code

#### Prerequisites:
- Ensure that Python is installed on your system.
- Dependencies for the tool must be installed. Refer to the project’s `requirements.txt` for the required packages.

#### Steps:

1. **Run Command Prompt as Administrator**  
   Open Command Prompt with Administrator privileges.

2. **Navigate to the Project Directory**  
   Use `cd` to change to the directory where you saved this GitHub repository folder.

3. **Run the Script**  
   You can choose to run the script either **live** or **offline**:
   - **To run live**:  
     ```
     python tool.py live
     ```
   - **To run offline**:  
     ```
     python tool.py offline
     ```

   **Important**: For **offline mode**, you must create a folder named `OfflineFiles` (you can change the folder name in the code if needed). This folder should contain the output from KAPE (Kroll Artifact Parser and Extractor) or any previous acquisition data that is required for offline analysis.

4. **Find the Output**  
   After the script has finished running, the output will be located in the `ExtractedFiles` directory. This directory will contain all the files and analysis results.

---

### 2. Run .exe File

#### Prerequisites:
- Ensure that you have the `.exe` file, which can be found in the `dist` folder.

#### Steps:

1. **Run Command Prompt as Administrator**  
   Open Command Prompt with Administrator privileges.

2. **Navigate to the `dist` Folder**  
   Use `cd` to change to the `dist` folder, which is located within the GitHub project directory.

3. **Run the .exe File**  
   You can choose to run the `.exe` either **live** or **offline**:
   - **To run live**:  
     ```
     tool2.exe live
     ```
   - **To run offline**:  
     ```
     tool2.exe offline
     ```

   **Important**: For **offline mode**, ensure that you have the `OfflineFiles` folder, containing the output from KAPE or similar acquisitions, in place.

4. **Find the Output**  
   The output will be located in the `ExtractedFiles` directory.

---

### Notes:
- **Dependencies**: Before running either method, make sure all dependencies are installed. You can do this by running `pip install -r requirements.txt` from the project directory.
- **Offline Mode Folder**: If using **offline mode**, ensure that the `OfflineFiles` folder (or the folder name defined in the code) is properly populated with relevant data from KAPE or a similar tool.
- **Logs**: If any issues arise during execution, check the logs in the `ExtractedFiles` folder for debugging information.

---

This tool will acquire and analyze artifact data, including REGISTRY hives, from the specified system. The results will help with further analysis and forensic investigation.
