import json
import requests
from scheduler.lib.config_manager import get_config_value


def create_fd_ticket(subject, company_id, group_id, task_body, task_type):

    base_url = get_config_value('freshdesk', 'url')
    full_url = f'{base_url}/api/v2/tickets'

    logger_email = 'dev-team@three6five.com'
    params = {
        'email': logger_email,
        'subject': subject,
        'description': task_body,
        'status': 2,  # 2 is open
        'priorty': 1,  # 1 is low
        'group_id': int(group_id),
        'company_id': int(company_id),
        'type': task_type
    }

    result = requests.post(full_url, json=json.loads(params))

    return True # returns true or False for success or fail..