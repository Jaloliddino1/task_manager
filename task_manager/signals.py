from notifications.consumers import notify_user
from notifications.models import Notification
from task_manager.models import Task
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Task)
def create_task_and_send_notification(sender, instance, created, **kwargs):
    if created and instance.user:
        n = Notification.objects.create(
            title=f'Task created {instance.id}',
            message=f'You have created a new task: {instance.title}',
            user=instance.user
        )
        notify_user(instance.user.id, n.title)
