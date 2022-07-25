from scheduler.lib.data_management.sql import get_df_from_table
from scheduler.models import Group, Company, Engineer


# todo - refactor 3 functions below into a single one
def update_groups():
    group_df = get_df_from_table('freshdesk_groups')

    for row in group_df.to_dict('records'):
        if Group.objects.filter(name=row['name']):
            continue

        new_group = Group(name=row['name'], freshdesk_id=row['id'])
        new_group.save()


def update_companies():
    companies_df = get_df_from_table('freshdesk_companies')

    for row in companies_df.to_dict('records'):
        if Company.objects.filter(name=row['name']):
            continue

        new_company = Company(name=row['name'], freshdesk_id=row['id'])
        new_company.save()


def update_engineers():
    agents_df = get_df_from_table('freshdesk_agents')

    for row in agents_df.to_dict('records'):
        if Engineer.objects.filter(name=row['name']):
            continue

        new_engineer = Engineer(name=row['name'], freshdesk_id=row['id'])
        new_engineer.save()


def update_fd_data():
    update_engineers()
    update_companies()
    update_groups()
