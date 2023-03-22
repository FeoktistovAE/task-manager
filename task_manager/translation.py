from django.utils.translation import gettext_lazy as _


USER_CREATE = _('User has created')
USER_UPDATE = _('User succesfully updated')
NO_RIGHTS_TO_UPDATE_USER = _('You do not have rights to edit another user')
NOT_AUTHORIZED_USER = _('You are not authorized! Please sign in.')
USER_DELETE = _('User successfully deleted')
DELETE_PROTECTED_USER = _("Unable to delete user. It's in use")
NO_RIGHTS_TO_DELETE_USER = _('You do not have rights to delete another user')
USER_LOGIN = _('You are logged in')
USER_LOGOUT = _('You are logged out')

TASK_CREATE = _('Task succesfully created')
TASK_UPDATE = _('Task successfully updated')
TASK_DELETE = _('Task successfully deleted')
NO_RIGHTS_TO_DELETE_TASK = _('A task can only be deleted by its author.')

LABEL_CREATE = _('Label succesfully created')
LABEL_UPDATE = _('Label successfully updated')
LABEL_DELETE = _('Label successfully deleted')
DELETE_PROTECTED_LABEL = _("Unable to delete label. It's in use")

STATUS_CREATE = _('Status succesfully created')
STATUS_UPDATE = _('Status successfully updated')
STATUS_DELETE = _('Status successfully deleted')
DELETE_PROTECTED_STATUS = _("Unable to delete status. It's in use")

LABELS_TITLE = _('Labels')
LABEL_CREATE_TITLE = _('Create a label')
LABEL_UPDATE_TITLE = _('Update the label')
LABEL_DELETE_TITLE = _('Delete the label')

STATUSES_TITLE = _('Statuses')
STATUS_CREATE_TITLE = _('Create a status')
STATUS_UPDATE_TITLE = _('Update the status')
STATUS_DELETE_TITLE = _('Delete the status')

TASKS_TITLE = _('Tasks')
TASK_DETAIL_TITLE = _('Task view')
TASK_CREATE_TITLE = _('Create a task')
TASK_UPDATE_TITLE = _('Update the task')
TASK_DELETE_TITLE = _('Delete the task')

USERS_TITLE = _('Users')
USER_CREATE_TITLE = _('Sign up')
USER_UPDATE_TITLE = _('Update the user')
USER_DELETE_TITLE = _('Delete the user')
USER_LOGIN_TITLE = _('Sign in')

NAME_FIELD = _('Name')
DESCRIPTION_FIELD = _('Description')
AUTHOR_FIELD = _('Author')
STATUS_FIELD = _('Status')
DATE_CREATED_FIELD = _('Date created')
EXECUTOR_FIELD = _('Executor')
LABELS_FIELD = _('Labels')
LABEL_FIELD = _('Label')
OWN_TASKS_FIELD = _('Only your own tasks')
