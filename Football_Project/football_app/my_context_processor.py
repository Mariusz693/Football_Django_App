from .models import League


def my_cp(request):
    
    ctx = {
        "leagues": League.objects.all().order_by('name'), 
    }

    return ctx