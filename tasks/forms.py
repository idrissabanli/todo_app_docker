from django import forms
from django.http import request

from tasks.models import SharingTasks, TaskReviews
from users.models import MyUser

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
    review = forms.CharField()

    class Meta:
        model = TaskReviews
        exclude = ['task', 'user', 'ord', 'is_published']