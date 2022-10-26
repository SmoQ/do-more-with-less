from django.shortcuts import render

from todo.models import ToDo


def todo_list(request):
    queryset = ToDo.objects.all()
    return render(request, "todo.html", {"queryset": queryset})
