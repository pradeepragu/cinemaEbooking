from django.utils import timezone

try:
    from .models import Tickets
except AppRegistryNotReady:
    Tickets = apps.get_model('cinema_Ebooking', 'Tickets')

def expire_old_tickets():
    ten_minutes_ago = timezone.now() - timezone.timedelta(minutes=10)
    tickets_to_expire = Tickets.objects.filter(isBooked=False, time_created__lt=ten_minutes_ago, status='Active')
    for ticket in tickets_to_expire:
        ticket.status = 'Expired'
        ticket.save()