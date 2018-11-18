from django.db import models
try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    from datetime import datetime
    datetime_now = datetime.now
from core.utils import utf_slugify
from django.utils.translation import ugettext_lazy as _
from users.models import MyUser
from django.urls import reverse
# Create your models here.


class Tasks(models.Model):
    title = models.CharField(_(u'Title'), max_length=100, help_text='You must write here task title')
    slug = models.SlugField(_(u'Slug'), max_length=100, editable=False, null=True)
    description = models.TextField(_(u'Description'), help_text='You must write here task description')
    deadline = models.DateTimeField('Deadline', default=datetime_now)
    created_by = models.ForeignKey(MyUser, related_name='creator_tasks', on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, default=datetime_now)
    updated = models.DateTimeField(editable=False, auto_now=True)
    ord = models.PositiveIntegerField('Ord', default=1)
    is_published = models.BooleanField('Is Published', default=True)
    status = models.CharField('Status', choices=(('s', 'Starting'), ('r', 'Running'), ('c', 'Complated'),),  max_length=1, default='s')

    class Meta:
        verbose_name = _(u'Task')
        verbose_name_plural = _(u'Tasks')
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('tasks:created-task-detail', kwargs={'slug': self.slug})

    def get_reviews(self, slug):
        return TaskReviews.objects.filter(task__slug=slug)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_unique_slug(self):
        slug = utf_slugify(self.title)
        unique_slug = slug
        counter = 1
        while Tasks.objects.filter(slug=unique_slug):
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        return super(Tasks, self).save(*args, **kwargs)

class SharingTasks(models.Model):
    user = models.ForeignKey(MyUser, related_name='sharing_tasks', on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, related_name='sharing_tasks', on_delete=models.CASCADE)
    sharing_type = models.CharField('Sharing Type', choices=(('v', 'View'), ('vr', 'View & Write Review'),),  max_length=2)

    class Meta:
        verbose_name = _(u'Sharing Task')
        verbose_name_plural = _(u'Sharing Tasks')

    def get_absolute_url(self):
        return reverse('tasks:created-task-detail', kwargs={'slug': self.task.slug})

    def __unicode__(self):
        return self.task.title

    def __str__(self):
        return self.task.title


class TaskReviews(models.Model):
    review = models.TextField(_(u'Review'), help_text='You must write here task your review')
    task = models.ForeignKey(Tasks, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, related_name='reviews', on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, default=datetime_now)
    updated = models.DateTimeField(editable=False, auto_now=True)
    ord = models.PositiveIntegerField('Ord', default=1)
    is_published = models.BooleanField('Is Published', default=True)

    class Meta:
        verbose_name = _(u'Task Review')
        verbose_name_plural = _(u'Task Reviews')
        ordering = ('-created',)

    def __unicode__(self):
        return self.task.title

    def __str__(self):
        return self.task.title
