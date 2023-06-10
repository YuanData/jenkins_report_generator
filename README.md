# Jenkins Report Generator
A Python project retrieves Jenkins job information and generates a report in Excel format.
可以獲取Jenkins任務資訊並生成Excel格式的報告的Python專案。

## Prerequisites
- Python 3.7 or higher
- Required Python packages:
  - pandas
  - requests

## Configuration
1. Open the `config.py` file.
2. Provide the following information:
   ```python
   JENKINS_URL = "https://your-jenkins-url"
   JENKINS_USER_ID = "your-user-id"
   JENKINS_USER_TOKEN = "your-user-token"
   JENKINS_PROJECT = "your-jenkins-project"
   ```   
3. Save and close the config.py file.

## Usage
1. Run the following commands to generate the Jenkins report:
   ```bash
   python generage_jenkins_report.py
   python parse_config_xml.py
   ```
2. The script will retrieve Jenkins job information and generate an Excel report named {JENKINS_PROJECT}.xlsx.
3. The generated report will contain the following columns:
- `class`: Job class (e.g., "FreeStyleProject", "Folder").
- `folder`: Name of the folder (if applicable).
- `project`: Name of the Jenkins project.
- `url:` Job URL.
- `name:` Job name.
- `triggers`: Job triggers (if available).
- `python_script`: Python script file associated with the job (if available).

## Note
- Make sure to configure the `config.py` file with the correct Jenkins URL, user ID, user token, and project name before running the script.  
 在運行之前，請確保使用正確的Jenkins URL、使用者ID、使用者Token和專案名稱配置`config.py`文件。
- The script may take some time to execute, depending on the number of jobs and the server load.  
 根據工作數量和伺服器負載情況，專案執行的時間可能會有所不同，可能需要一些時間。