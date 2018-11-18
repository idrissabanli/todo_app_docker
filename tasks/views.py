from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormMixin
from tasks.forms import TaskShareForm
from tasks.models import TaskReviews, Tasks, SharingTasks
from django.contrib.auth.decorators import login_required
from tasks.forms import TaskReviewForm

from users.models import MyUser


class CreatedTaskList(LoginRequiredMixin, ListView):
    model = Tasks
    context_object_name = 'task_list'
    template_name = 'task_list.html'

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)


class TaskList(ListView, LoginRequiredMixin):
    model = SharingTasks
    context_object_name = 'task_list'
    template_name = 'task_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


# @method_decorator(login_required, name='dispatch')
class CreatedTaskDetail(FormMixin, DetailView, LoginRequiredMixin):
    model = Tasks
    template_name = 'task_detail.html'
    form_class = TaskReviewForm
    success_url = './'
    success_message = "Was changed successfully"

    # share olunan task oldugu kimi bazada varsa hec ne etmir, ferqli varianti varsa deyisdirilir, yoxdursa elave edilir.
    # def check_user_have_status_on_shared_task(self, **kwargs):
    #     if self.request.POST:
    #         task = Tasks.objects.get(slug=self.kwargs['slug'])
    #         sharing_type = self.request.POST['sharing_type']
    #         user = MyUser.objects.get(id=self.request.POST['user'])
    #         sharing_task, created = SharingTasks.objects.update_or_create(task=task, user=user,
    #                                                                       defaults={'sharing_type': sharing_type})
    #         if created:
    #             return HttpResponse('Sharing created')
    #         else:
    #             return HttpResponse('Sharing updated')

    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseForbidden()
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #         # return ""
    #
    # def form_valid(self, form):
    #     task = self.get_object()
    #     user = self.request.user
    #     review = form.cleaned_data.get("review")
    #     TaskReviews.objects.create(user=user, task=task, review=review)
    #     return super().form_valid(form)

    # share olunan task oldugu kimi bazada varsa hec ne etmir, ferqli varianti varsa deyisdirilir, yoxdursa elave edilir.
    def check_user_have_status_on_shared_task(self, **kwargs):
        if self.request.POST:
            task = Tasks.objects.get(slug=self.kwargs['slug'])
            sharing_type = self.request.POST['sharing_type']
            user = MyUser.objects.get(id=self.request.POST['user'])
            sharing_task, created = SharingTasks.objects.update_or_create(task=task, user=user,
                                                                          defaults={'sharing_type': sharing_type})
            if created:
                return HttpResponse('Sharing created')
            else:
                return HttpResponse('Sharing updated')

    def post(self, request, *args, **kwargs):
        self.check_user_have_status_on_shared_task(**kwargs)
        task = self.model.objects.get(slug=self.kwargs['slug'])
        share_form = TaskShareForm(user=self.request.user.id)
        message = self.success_message
        reviews = task.get_reviews(self.kwargs['slug'])
        return render(request, self.template_name, {'form': self.form_class, 'share_form': share_form, 'task': task, 'message': message, 'reviews': reviews})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.model.objects.get(slug=self.kwargs['slug'])
        context['task'] = task
        context['reviews'] = task.get_reviews(self.kwargs['slug'])
        # if task creator == user olmalıdı!
        context['share_form'] = TaskShareForm(user=self.request.user.id)
        return context


class ShareTask(FormView, LoginRequiredMixin):
    model = Tasks
    context_object_name = 'task'
    template_name = 'share_task.html'
    success_message = "Was changed successfully"
    form_class = TaskShareForm
    success_url = './'

    # share olunan task oldugu kimi bazada varsa hec ne etmir, ferqli varianti varsa deyisdirilir, yoxdursa elave edilir.
    def check_user_have_status_on_shared_task(self, **kwargs):
        if self.request.POST:
            task = Tasks.objects.get(slug=self.kwargs['slug'])
            sharing_type = self.request.POST['sharing_type']
            user = MyUser.objects.get(id=self.request.POST['user'])
            sharing_task, created = SharingTasks.objects.update_or_create(task=task, user=user,
                                                                          defaults={'sharing_type': sharing_type})
            if created:
                return HttpResponse('Sharing created')
            else:
                return HttpResponse('Sharing updated')

    def post(self, request, *args, **kwargs):
        self.check_user_have_status_on_shared_task(**kwargs)
        task = self.model.objects.get(slug=self.kwargs['slug'])
        form = self.form_class(user=self.request.user.id)
        message = self.success_message
        return render(request, self.template_name, {'form': form, 'task': task, 'message': message})

    def get_context_data(self, **kwargs):
        context = super(ShareTask, self).get_context_data(**kwargs)
        context['task'] = self.model.objects.get(slug=self.kwargs['slug'])
        context['form'] = self.form_class(user=self.request.user.id)
        self.check_user_have_status_on_shared_task(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class TaskCreate(CreateView):
    model = Tasks
    template_name = 'task_form.html'
    fields = ['title', 'description', 'deadline', ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def check_write_comment(task, user):
    if task.created_by == user:
        return True
    elif SharingTasks.objects.get(task=task, user=user).sharing_type == 'vr':
        return True
    else:
        return False
