try:
    import config_local  # noqa: F401
except ImportError:
    pass
import django_setup  # noqa: F401
from todo.models import ToDo


def handler(*args, **kwargs):
    print("It works")
    print(ToDo.objects.all())
