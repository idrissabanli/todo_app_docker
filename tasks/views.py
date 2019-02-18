from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormMixin
from tasks.forms import TaskShareForm
from tasks.models import TaskReviews, Tasks, SharingTasks
from django.contrib.auth.decorators import login_required
from tasks.forms import TaskReviewForm, TaskForm
from users.models import MyUser
from django.core.mail import send_mail
from django.conf import settings


@method_decorator(login_required, name='dispatch')
class CreatedTaskList(LoginRequiredMixin, ListView):
    model = Tasks
    context_object_name = 'task_list'
    template_name = 'task_list.html'

    # def get_queryset(self):
    #     return self.model.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['created_tasks'] = self.model.objects.filter(created_by=self.request.user)
        context['shared_tasks'] = SharingTasks.objects.filter(user=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class TaskList(ListView):
    model = SharingTasks
    context_object_name = 'task_list'
    template_name = 'task_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class Change_Review(FormView):
    model = TaskReviews
    form_class = TaskReviewForm
    template_name = 'edit_review.html'
    
    def get(self, request, *args, **kwargs):
        task = self.model.objects.get(id=self.request.GET['id'])
        form = self.form_class(request.POST or None, instance=task)
        return self.render_to_response(self.get_context_data(form=form))
            
    def get_context_data(self, **kwargs):
        return kwargs


@method_decorator(login_required, name='dispatch')
class CreatedTaskDetail(FormMixin, DetailView):
    model = Tasks
    template_name = 'task_detail.html'
    form_class = TaskReviewForm
    success_url = './'
    success_message = "Was changed successfully"

    # share olunan task oldugu kimi bazada varsa hec ne etmir, ferqli varianti varsa deyisdirilir, yoxdursa elave edilir.
    def check_user_have_status_on_shared_task(self, **kwargs):
        if self.request.POST:
            print('self.request.POST', self.request.POST['sharing_type'])
            task = Tasks.objects.get(slug=self.kwargs['slug'])
            sharing_type = self.request.POST['sharing_type']
            user = MyUser.objects.get(id=self.request.POST['user'])
            sharing_task, created = SharingTasks.objects.update_or_create(task=task, user=user,
                                                                          defaults={'sharing_type': sharing_type})

            if created:
                # send_mail('Todo Application', self.request.user.first_name + self.request.user.last_name + ' shared ' + task.title + ' task with you - Todo Application', settings.EMAIL_HOST_USER, [user.email], fail_silently=False,)
                return HttpResponse('Sharing created')
            else:
                # send_mail('Todo Application', 'Shared Task' + task.title + 'changed - Todo Application', settings.EMAIL_HOST_USER, [user.email], fail_silently=False,)
                return HttpResponse('Sharing updated')

    def post(self, request, *args, **kwargs):
        task = self.model.objects.get(slug=self.kwargs['slug'])
        if check_user_can_share(task, request.user):
            self.check_user_have_status_on_shared_task(**kwargs)
            form = self.form_class()
            reviews = task.get_reviews(self.kwargs['slug'])
            share_form = TaskShareForm(user=self.request.user.id)
            message = self.success_message
            return render(request, self.template_name, {'form': form, 'task': task, 'message': message, 'reviews': reviews, 'share_form': share_form})
        else:
            raise PermissionError


    def get_context_data(self, **kwargs):
        task = self.model.objects.get(slug=self.kwargs['slug'])
        if user_have_permission_on_task(task, self.request.user):
            context = super().get_context_data(**kwargs)
            context['task'] = task
            context['reviews'] = task.get_reviews(self.kwargs['slug'])
            # if task creator == user olmalıdı!
            context['share_form'] = TaskShareForm(user=self.request.user.id)
            return context
        else:
            raise PermissionError


@method_decorator(login_required, name='dispatch')
class TaskCreate(CreateView):
    model = Tasks
    template_name = 'task_form.html'
    form_class = TaskForm

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

def user_have_permission_on_task(task, user):
    if task.created_by == user or SharingTasks.objects.filter(task=task, user=user):
        return True
    else:
        return False


def check_user_can_share(task, user):
    if task.created_by == user:
        return True
    else:
        return False
