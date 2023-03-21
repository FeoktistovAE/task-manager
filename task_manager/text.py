from django.utils.translation import gettext_lazy as _


class UserFlashMessages:
    create_user = _('User has created')
    update_user = _('User succesfully updated')
    no_rights_to_update_user = _('You do not have rights to edit another user')
    not_authorhorized_user = _('You are not authorized! Please sign in.')
    delete_user = _('User successfully deleted')
    delete_protected_user = _("Unable to delete user. He's in use")
    no_rights_to_delete_user = _('You do not have rights to delete another user')
    login_user = _('You are logged in')
    logout_user = _('You are logged out')


class TaskFlashMessages:
    create_task = _('Task succesfully created')
    update_task = _('Task successfully updated')
    delete_task = _('Task successfully deleted')
    no_rights_to_delete_task = _('A task can only be deleted by its author.')


class LabelFlashMessages:
    create_label = _('Label succesfully created')
    update_label = _('Label successfully updated')
    delete_label = _('Label successfully deleted')
    delete_protected_label = _("Unable to delete label. It's in use")


class StatusFlashMessages:
    create_status = _('Status succesfully created')
    update_status = _('Status successfully updated')
    delete_status = _('Status successfully deleted')
    delete_protected_status = _("Unable to delete status. It's in use")


class TitleNames:
    labels = _('Labels')
    label_create = _('Create a label')
    label_update = _('Update the label')
    label_delete = _('Delete the label')

    statuses = _('Statuses')
    status_create = _('Create a status')
    status_update = _('Update the status')
    status_delete = _('Delete the status')

    tasks = _('Tasks')
    task_detail = _('Task view')
    task_create = _('Create a task')
    task_update = _('Update the task')
    task_delete = _('Delete the task')

    users = _('Users')
    user_create = _('Sign up')
    user_update = _('Update the user')
    user_delete = _('Delete the user')
    user_login = _('Sign in')


class FieldNames:
    name = _('Name')
    desctiption = _('Description')
    author = _('Author')
    status = _('Status')
    date_created = _('Date created')
    executor = _('Executor')
    labels = _('Labels')
    label = _('Label')
    own_tasks = _('Only your own tasks')
