from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import PositionForm, TaskTypeForm, TagForm, WorkerCreationForm, WorkerUpdateForm, TaskForm
from .mixins import SafeDeleteMixin
from .models import Position, TaskType, Tag, Worker, Task


@login_required
def index(request):
    num_task_types = TaskType.objects.count()
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_task_types': num_task_types,
        'num_workers': num_workers,
        'num_tasks': num_tasks,
        'num_visits': num_visits + 1
    }

    return render(request, 'tasks/index.html', context=context)


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = 'tasks/position_list.html'
    context_object_name = 'position_list'


class PositionDetailView(LoginRequiredMixin, DetailView):
    model = Position
    template_name = 'tasks/position_detail.html'
    context_object_name = 'position'


class PositionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:position-list')
    success_message = 'Position successfully created!'
    extra_context = {
        'page_title': 'Create position'
    }


class PositionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:position-list')
    success_message = 'Position successfully updated!'
    extra_context = {
        'page_title': 'Edit position'
    }


class PositionDeleteView(LoginRequiredMixin, SafeDeleteMixin, DeleteView):
    model = Position
    template_name = 'tasks/_generic_confirm_delete.html'
    success_url = reverse_lazy('tasks:position-list')
    protected_error_message = 'Cannot delete position because it is assigned to workers.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_url"] = self.success_url
        return context


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = 'tasks/task_type_list.html'
    context_object_name = 'task_type_list'


class TaskTypeDetailView(LoginRequiredMixin, DetailView):
    model = TaskType
    template_name = 'tasks/task_type_detail.html'
    context_object_name = 'task_type'


class TaskTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:task-type-list')
    success_message = 'Task type successfully created!'
    extra_context = {
        'page_title': 'Create task type'
    }


class TaskTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:task-type-list')
    success_message = 'Task type successfully updated!'
    extra_context = {
        'page_title': 'Edit task type'
    }


class TaskTypeDeleteView(LoginRequiredMixin, SafeDeleteMixin, DeleteView):
    model = TaskType
    template_name = 'tasks/_generic_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-type-list')
    protected_error_message = 'Cannot delete position because it is assigned to workers.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_url"] = self.success_url
        return context


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'tasks/tag_list.html'
    context_object_name = 'tag_list'


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'tasks/tag_detail.html'
    context_object_name = 'tag'


class TagCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:tag-list')
    success_message = 'Tag successfully created!'
    extra_context = {
        'page_title': 'Create tag'
    }


class TagUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:tag-list')
    success_message = 'Tag successfully updated!'
    extra_context = {
        'page_title': 'Edit tag'
    }


class TagDeleteView(LoginRequiredMixin, SafeDeleteMixin, DeleteView):
    model = Tag
    template_name = 'tasks/_generic_confirm_delete.html'
    success_url = reverse_lazy('tasks:tag-list')
    protected_error_message = 'Cannot delete tag because it is used in tasks.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_url"] = self.success_url
        return context


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = 'tasks/worker_list.html'
    context_object_name = 'worker_list'
    queryset = Worker.objects.select_related('position').annotate(
        num_tasks=Count('tasks')
    )


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = 'tasks/worker_detail.html'
    context_object_name = 'worker'
    queryset = Worker.objects.select_related('position').prefetch_related('tasks__task_type')


class WorkerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:worker-list')
    success_message = 'Worker successfully created!'
    extra_context = {
        'page_title': 'Create worker'
    }


class WorkerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:worker-list')
    success_message = 'Worker successfully updated!'
    extra_context = {
        'page_title': 'Edit worker'
    }


class WorkerDeleteView(LoginRequiredMixin, SafeDeleteMixin, DeleteView):
    model = Worker
    template_name = 'tasks/_generic_confirm_delete.html'
    success_url = reverse_lazy('tasks:worker-list')
    success_message = 'Deleted successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_url"] = self.success_url
        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'task_list'
    queryset = Task.objects.select_related('task_type').prefetch_related('assignees', 'tags')
    paginate_by = 10


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    queryset = Task.objects.select_related('task_type').prefetch_related('assignees__position', 'tags')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:task-list')
    success_message = 'Task successfully created!'
    extra_context = {
        'page_title': 'Create task'
    }


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/_generic_form.html'
    success_url = reverse_lazy('tasks:task-list')
    success_message = 'Task successfully updated!'
    extra_context = {
        'page_title': 'Edit task'
    }


class TaskDeleteView(LoginRequiredMixin, SafeDeleteMixin, DeleteView):
    model = Task
    template_name = 'tasks/_generic_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')
    success_message = 'Deleted successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_url"] = self.success_url
        return context


@login_required
def toggle_assign_to_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    if task.assignees.filter(pk=user.pk).exists():
        task.assignees.remove(user)
        messages.info(request, 'You have left this task')
    else:
        task.assignees.add(user)
        messages.success(request, 'You have joined this task')

    return redirect('tasks:task-detail', pk=pk)
