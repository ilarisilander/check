""" Logic to handle the configuration """
from src.file_handler import JsonFile
from src.constants import JIRA_CONFIG_PATH


class Jira:
    def __init__(self) -> None:
        self.jira_settings = JsonFile.read(JIRA_CONFIG_PATH)

    def get_base_url(self) -> str:
        return self.jira_settings['credentials']['base_url']

    def get_user_token(self) -> str:
        return self.jira_settings['credentials']['user_token']

    def get_api_token(self) -> str:
        return self.jira_settings['credentials']['api_token']

    def get_leading_work_group(self) -> dict:
        return self.jira_settings['leading_work_group']['id']

    def get_project(self) -> str:
        return self.jira_settings['project']['id']

    def get_assignee(self) -> str:
        return self.jira_settings['assignee']

    def get_issue_type_story(self) -> str:
        return self.jira_settings['issuetype']['story']['id']

    def get_transition_todo(self) -> str:
        return self.jira_settings['transitions']['todo']

    def get_transition_in_progress(self) -> str:
        return self.jira_settings['transitions']['in_progress']

    def get_transition_done(self) -> str:
        return self.jira_settings['transitions']['done']


if __name__ == '__main__':
    pass
