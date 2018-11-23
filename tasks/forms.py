from django import forms
from django.http import request

from tasks.models import SharingTasks, TaskReviews, Tasks
from users.models import MyUser
import datetime

ccc = [
    ('v', 'View'),
    ('vr', 'View & Write Review')
]


class TaskShareForm(forms.ModelForm):
    sharing_type = forms.ChoiceField(choices=ccc, widget=forms.RadioSelect())

    class Meta:
        model = SharingTasks
        exclude = ['task']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskShareForm, self).__init__(*args, **kwargs)
        sss = MyUser.objects.all().exclude(id=self.user)
        self.fields["user"].queryset = sss



class TaskReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = TaskReviews
        exclude = ['task', 'user', 'ord', 'is_published']



class TaskForm(forms.ModelForm):
    title = forms.CharField(required=True,
                           widget=forms.TextInput(
                               attrs={'class': ' form-control '}),
                           max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    deadline = forms.DateTimeField(initial=datetime.datetime.now(), required=False, widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime'}))

    class Meta: 
        model = Tasks
        fields = ['title', 'description', 'deadline', ]
