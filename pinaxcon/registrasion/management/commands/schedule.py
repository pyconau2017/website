from symposion.schedule.models import Slot


class Command(BaseCommand):
    help = 'Resaves all the slots so that their names are updated with all their rooms.'

    def handle(self, *args, **options):

        for slot in Slot.objects.all():
            slot.save()
