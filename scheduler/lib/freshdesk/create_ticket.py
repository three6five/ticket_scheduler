import json
import requests
from env import fd_api_key
from scheduler.lib.config_manager import get_config_value


def create_fd_ticket(subject, company_id, group_id, task_body, task_type_name, agent_id=None):
    base_url = get_config_value('freshdesk', 'url')
    full_url = f'{base_url}/api/v2/tickets'

    logger_email = 'dev-team@three6five.com'
    params = {
        'email': logger_email,
        'subject': subject,
        'description': task_body,
        'status': 2,  # 2 is open
        'priority': 1,  # 1 is low
        'group_id': int(group_id),
        'company_id': int(company_id),
        'type': task_type_name
    }

    if agent_id:
        params[agent_id] = agent_id

    headers = {
        'Content-Type': 'application/json'
    }

    result = requests.post(full_url, data=json.dumps(params), auth=(fd_api_key, 'X'), headers=headers)

    if result.status_code == 201:
        return True

    print(result.text)
    return False
