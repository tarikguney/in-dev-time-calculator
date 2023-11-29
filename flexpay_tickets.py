from jira import JIRA
from datetime import datetime
from dotenv import load_dotenv
import os
from calculate_hours import working_hours_per_week

load_dotenv()

# Jira setup - replace these with your details
jira_server = 'https://vivint.atlassian.net'
project_key = 'VTCORE'
board_id = 657

# Connect to Jira
jira = JIRA(jira_server, basic_auth=(os.getenv("JIRA_USER"), os.getenv("JIRA_PASSWORD")))

max_results = 50  # Maximum results per page (adjust as needed)
start_at = 0  # Starting index
all_sprints = []

print('\033[93m' + 'Please wait...' + '\033[0m')

while True:
    sprints = jira.sprints(board_id, startAt=start_at, maxResults=max_results, state='closed, active')
    all_sprints.extend(sprints)

    if len(sprints) < max_results:
        # Break the loop if the number of sprints is less than the max, indicating the last page
        break

    start_at += max_results

last_5_sprints = all_sprints[-5:]

for sprint in last_5_sprints:
    jql_query = f'project = {project_key} AND Sprint = {sprint.id} and labels in (Flexpay, Flex-pay) and labels = "Discovery-team"'
    sprint_issues = jira.search_issues(jql_query, expand='changelog')

    for issue in sprint_issues:
        print('\033[94m' + issue.key + ' - ' + issue.raw["fields"]["summary"] + '\033[0m')
        if issue.fields.assignee is not None:
            print(f' - Assigned To: {issue.fields.assignee}')
        print(f' - Link: {jira_server}/browse/{issue.key}')
        to_development_date = None
        from_development_date = None
        for history in issue.changelog.histories:
            for item in history.items:
                if item.field == 'status' and item.toString == 'Development':
                    to_development_date = datetime.strptime(history.created, '%Y-%m-%dT%H:%M:%S.%f%z')
                elif item.field == 'status' and item.fromString == 'Development':
                    from_development_date = datetime.strptime(history.created, '%Y-%m-%dT%H:%M:%S.%f%z')

        if to_development_date is not None and from_development_date is not None:
            for (key,value) in working_hours_per_week(to_development_date, from_development_date).items():
                print(f' - {key} - {value} hour(s) in development')
