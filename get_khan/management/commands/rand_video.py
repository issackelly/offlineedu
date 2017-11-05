from django.core.management.base import BaseCommand, CommandError
from get_khan.models import Video

class Command(BaseCommand):

    def handle(self, *args, **options):
        v = Video.objects.filter(big_file="").order_by('?')[0]
        #try:
        #    v.download_small()
        #except KeyError:
        #    print("KE, small", v.id, v.data)
        v.download_big()
        v.save()
