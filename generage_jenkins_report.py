import json
import os
import time

import pandas as pd
import requests

from config import JENKINS_URL, DASHBOARD_JOBS_JSON_FILE, PROJECT_JOBS_JSON_FILE


def save_jenkins_dashboard_jobs():
    """
    Save Jenkins dashboard jobs to a JSON file.
    """
    resp = requests.get(JENKINS_URL)
    assert resp.status_code == 200

    resp_json = resp.json()
    jobs = resp_json.get('jobs')

    result = [{'name': job.get('name'), 'url': job.get('url')} for job in jobs]

    with open(DASHBOARD_JOBS_JSON_FILE, "w") as outfile:
        json.dump(result, outfile)


def read_jenkins_dashboard_jobs() -> list:
    """
    Read Jenkins dashboard jobs from a JSON file.

    If the file doesn't exist, it saves the jobs first.

    :return: A list of jobs.
    """
    if not os.path.exists(DASHBOARD_JOBS_JSON_FILE):
        save_jenkins_dashboard_jobs()

    with open(DASHBOARD_JOBS_JSON_FILE, "r") as infile:
        return json.load(infile)


def save_project_jobs(project_name: str, project_url: str):
    """
    Save project jobs for a specific project to a JSON file.

    :param project_name: The name of the project.
    :param project_url: The URL of the project.
    """
    resp_json = requests.get(f'{project_url}api/json').json()
    jobs = resp_json.get('jobs')

    result = []
    for job in jobs:
        class_name = job.get('_class').split('.')[-1]
        job_parsed = {'class': class_name, 'name': job.get('name'), 'url': job.get('url')}
        result.append(job_parsed)

    json_file = PROJECT_JOBS_JSON_FILE.format(project_name)

    with open(json_file, "w") as outfile:
        json.dump(result, outfile)


def read_project_jobs(project_name: str, project_url: str) -> list:
    """
    Read project jobs for a specific project from a JSON file.

    If the file doesn't exist, it saves the jobs first.

    :param project_name: The name of the project.
    :param project_url: The URL of the project.
    :return: A list of project jobs.
    """
    json_file = PROJECT_JOBS_JSON_FILE.format(project_name)
    if not os.path.exists(json_file):
        save_project_jobs(project_name, project_url)

    with open(json_file, "r") as infile:
        return json.load(infile)


def parse_project_jobs(project_name: str, jobs: list) -> list:
    """
    Parse project jobs, including folders, normal jobs, and pipeline jobs.

    :param project_name: The name of the project.
    :param jobs: A list of project jobs.
    :return: Parsed project jobs.
    """
    folders = [d for d in jobs if d['class'] == 'Folder']
    projects = [d for d in jobs if d['class'] == 'FreeStyleProject']  # normal jobs
    workflows = [d for d in jobs if d['class'] == 'WorkflowJob']  # pipeline jobs

    for folder in folders:
        resp_json = requests.get(f'{folder["url"]}api/json').json()
        jobs = resp_json.get('jobs')
        jobs_lst = []
        for job in jobs:
            class_name = job.get('_class').split('.')[-1]
            job_parsed = {'class': class_name, 'name': job.get('name'), 'url': job.get('url'), 'folder': folder['name']}
            jobs_lst.append(job_parsed)
        projects.extend(jobs_lst)

    output = []
    output.extend(projects)
    output.extend(workflows)
    output = [{**d, 'project': project_name} for d in output]
    return output


if __name__ == '__main__':
    dashboard_jobs = read_jenkins_dashboard_jobs()

    data = []
    for djob in dashboard_jobs:
        project_jobs = read_project_jobs(djob['name'], djob['url'])
        jobs_parsed = parse_project_jobs(djob['name'], project_jobs)
        data.extend(jobs_parsed)

        print(djob['name'])
        time.sleep(0.1)  # Slow down the access rate to mitigate server load.

    df = pd.DataFrame(data)
    columns = ['class', 'project', 'folder', 'name', 'url', ]
    df = df.reindex(columns=columns)
    df.to_excel('jenkins_report.xlsx', index=False)
