from celery.task.schedules import crontab
from celery import Celery
import datetime
from django.utils import timezone
from tasks.models import Tasks
from celery.decorators import periodic_task
from django.core.mail import send_mail
from django.conf import settings

@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
	# user = User.objects.get(id=check_deadline_end(datetime.now))
	# print('dealine', datetime.timedelta(seconds=900))
	print('date', timezone.now())
	sharing_list = []
	tasks = Tasks.objects.filter(deadline__range=(timezone.now() + datetime.timedelta(seconds=600), timezone.now() + datetime.timedelta(seconds=660)))
	for task in tasks:
		print('task', task)
		for sharing in task.sharing_tasks.all():
			print('sharing', sharing)
			send_mail('To Do Application', 'Warning: ' + task.title + ' will be completed in 10 minutes.', settings.EMAIL_HOST_USER , [ sharing.user.email ], fail_silently=False,)