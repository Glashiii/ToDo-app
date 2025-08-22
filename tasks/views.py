from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormMixin

from .forms import TaskForm
from .models import Task

class TaskListCreateView(LoginRequiredMixin, FormMixin, ListView):
    model               = Task
    template_name       = 'tasks/list.html'
    context_object_name = 'tasks'

    form_class  = TaskForm
    success_url = reverse_lazy('tasks_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs['form'] = kwargs.get('form') or self.get_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)

def toggle_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.task_active = not task.task_active
    task.save()
    return redirect('tasks_list')

@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # или task_user
    task.delete()
    return redirect('tasks_list')
