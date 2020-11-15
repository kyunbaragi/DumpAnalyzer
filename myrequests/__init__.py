import requests
from .action import PostComment, AssignMainOwner, AssignSubOwners


class Url:
    LOGIN = 'https://foo.com/login'


class Session:
    HEADERS = {'Content-Type': 'application/json; charset=utf-8'}

    def __init__(self, user_id, user_password):
        self.session = self.login(user_id, user_password)

    def login(self, user_id, user_password):
        with requests.Session() as session:
            data = {'ID': user_id, 'PASSWORD': user_password}
            res = session.post(Url.LOGIN, data=data)
            res.raise_for_status()

            return session

    def post_comment(self, action):
        pass

    def assign_issue(self, action):
        current_owners = set(action.issue.assigned_list)
        current_main_owner = set(action.issue.assigned_list[0:1])

        main_owner = None
        sub_owners = None

        if isinstance(action, AssignMainOwner):
            if action.main_owner == current_main_owner:
                return
            main_owner = action.main_owner
            sub_owners = current_owners - main_owner

        if isinstance(action, AssignSubOwners):
            if action.sub_owners.issubset(current_owners):
                return
            main_owner = current_main_owner
            sub_owners = (current_owners | action.sub_owners) - main_owner

        if main_owner and sub_owners:
            assigned_list = list(main_owner) + list(sub_owners)
            pass

    def resolve_issue(self):
        pass
