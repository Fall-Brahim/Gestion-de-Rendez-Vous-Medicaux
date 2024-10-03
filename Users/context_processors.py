from .models import Notifications


def notifications_processor(request):
    if request.user.is_authenticated:
        unread_count = Notifications.objects.filter(user=request.user, envoyee=False, read=False).count()
    
        notifications = Notifications.objects.filter(user=request.user, envoyee=False, read=False).order_by('-date_created')
        return {'notifications': notifications,'unread_count':unread_count}
    return {}