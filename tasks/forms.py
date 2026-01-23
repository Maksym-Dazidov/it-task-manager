from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from tasks.models import Position, Tag, TaskType, Task

Worker = get_user_model()


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = '__all__'


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ('position', 'first_name', 'last_name', 'email')


class WorkerUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Worker
        fields = ('username', 'first_name', 'last_name', 'email', 'position', 'is_active', 'is_staff')

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
    )
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'deadline',
            'is_completed',
            'priority',
            'task_type',
            'assignees',
            'tags',
        ]
