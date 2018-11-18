from django.views.generic import ListView
from tasks.models import Tasks

class DesktopView(ListView):
    queryset = Tasks.objects.filter(is_published=True)
    context_object_name = 'created_task_list'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from tasks.forms import TaskReviewForm
from tasks.models import TaskReviews, Tasks


class TaskReviewView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'reviews.html'
    model = Tasks
    form_class = TaskReviewForm
    success_url = './'
    success_message = "Was changed successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = self.get_form()
        # print('id', kwargs['pk'])
        context['reviews'] = self.model.objects.get(id=self.kwargs['pk']).get_reviews(self.kwargs['pk'])
        # print('taskreviewwww', self.model.get_reviews(id=self.kwargs['pk']))
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        # return ""

    def form_valid(self, form):
        task = self.get_object()
        user = self.request.user
        review = form.cleaned_data.get("review")
        TaskReviews.objects.create(user=user, task=task, review=review)
        return super().form_valid(form)