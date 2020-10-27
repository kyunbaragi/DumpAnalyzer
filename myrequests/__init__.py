from .action import PostComment, AssignMainOwner, AssignSubOwner


class Session:
    def __init__(self):
        pass

    def post_comment(self, action):
        if not isinstance(action, PostComment):
            return
        pass

    def assign_issue(self, action):
        if not isinstance(action, AssignMainOwner) \
                or not isinstance(action, AssignSubOwner):
            return

        current_owners = set(action.issue.assigned_list)
        current_main_owner = set(action.issue.assigned_list[0:1])
        current_sub_owners = set(action.issue.assigned_list[1:])

        main_owner = None
        sub_owners = None
        if isinstance(action, AssignMainOwner):
            # Already the main owner in charge.
            if action.main_owner == current_main_owner:
                return
            main_owner = action.main_owner
            sub_owners = current_owners - main_owner
        elif isinstance(action, AssignSubOwner):
            # Already included in the current assigned list.
            if action.sub_owners.issubset(current_owners):
                return
            main_owner = current_main_owner
            sub_owners = (current_sub_owners | action.sub_owners) - main_owner

        if main_owner and sub_owners:
            assigned_list = list(main_owner) + list(sub_owners)
            comment = action.comment
