from .models import League


def my_cp(request):
    
    ctx = {
        "leagues": League.objects.all()[:7],
    }

    return ctx