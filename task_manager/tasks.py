import pandas as pd
from celery import shared_task

from accounts.models import User
from notifications.models import Notification
from task_manager.models import Task


@shared_task
def export_model_to_exel():
    task = Task.objects.all().values()
    df = pd.DataFrame(list(task))
    file_path = 'media/exports/task_export.xlsx'
    df.to_excel(file_path, index=True)
    for user in User.objects.filter(is_superuser=True):
        Notification.objects.create(
            title='Task export',
            message='30 kunlik Tasklar export qilindi excelga quydagi linkni orqali yuklab oling'
                    f'http://127.0.0.1:8000/{file_path}',
            user=user
        )

    return file_path
