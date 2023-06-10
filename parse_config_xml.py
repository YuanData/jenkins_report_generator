import re
import time

import pandas as pd
import requests

from config import JENKINS_USER_ID, JENKINS_USER_TOKEN, JENKINS_PROJECT

if __name__ == '__main__':
    df = pd.read_excel('jenkins_report.xlsx')
    data = df.to_dict('records')
    data = [d for d in data if d['project'] == JENKINS_PROJECT]

    for d in data:
        if d['class'] != 'FreeStyleProject':
            continue
        resp = requests.get(f"{d['url']}/config.xml", auth=(JENKINS_USER_ID, JENKINS_USER_TOKEN))
        resp_text = resp.text

        if '401 Unauthorized' in resp_text:
            raise Exception('HTTP ERROR 401 Unauthorized')

        d['python_script'] = re.findall(r'qa_project/.*\.py', resp_text) or ''
        d['triggers'] = re.findall(r'<spec>(.*?)</spec>', resp_text) or ''
        time.sleep(0.1)  # Slow down the access rate to mitigate server load.

    df = pd.DataFrame(data)
    columns = ['class', 'folder', 'project', 'url', 'name', 'triggers', 'python_script']
    df = df.reindex(columns=columns)
    df.to_excel(f'{JENKINS_PROJECT}.xlsx', index=False)
