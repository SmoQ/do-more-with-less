try:
    import config_local  # noqa: F401
except ImportError:
    pass
import django_setup  # noqa: F401
from todo.models import ToDo


def handler(event, *args, **kwargs):
    title = event.get("title")
    obj = ToDo.objects.create(title=title)
    print(f"Successfully created todo list {obj}.")
