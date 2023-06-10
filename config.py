import configparser

config = configparser.ConfigParser()
config.read('config.env')

JENKINS_URL = config.get('JENKINS', 'JENKINS_URL')
JENKINS_PROJECT = config.get('JENKINS', 'JENKINS_PROJECT')

DASHBOARD_JOBS_JSON_FILE = config.get('FILE', 'DASHBOARD_JOBS_JSON_FILE')
PROJECT_JOBS_JSON_FILE = config.get('FILE', 'PROJECT_JOBS_JSON_FILE')

JENKINS_USER_ID = config.get('AUTH', 'JENKINS_USER_ID')
JENKINS_USER_TOKEN = config.get('AUTH', 'JENKINS_USER_ID')
