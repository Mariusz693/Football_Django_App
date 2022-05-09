from .models import League


def my_cp(request):
    
    ctx = {
        "leagues": League.objects.all()[:10],
    }

    return ctx