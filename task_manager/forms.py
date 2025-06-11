from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import (Task, TaskType,
                     Worker, Tag, Position)


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-multiselect block w-full mt-1 rounded-lg border-gray-300"
            }
        ),
        required=False,
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-multiselect block w-full mt-1 rounded-lg border-gray-300"
            }
        ),
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees",
            "tags",
        ]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настраиваем отображение имени сотрудника
        self.fields["assignees"].label_from_instance = lambda obj: f"{obj.username}: {obj.position.name}"

        # Если хочешь для тегов тоже форматировать отображение:
        self.fields["tags"].label_from_instance = lambda obj: obj.name

class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "email",
            "first_name",
            "last_name",
        )


class WorkerPositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["position"]


class PositionDeleteForm(forms.Form):
    positions = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class WorkerSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
            })
    )


class TaskSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
            })
    )

