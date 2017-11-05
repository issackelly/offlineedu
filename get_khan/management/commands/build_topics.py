from django.core.management.base import BaseCommand, CommandError
from get_khan.models import Topic, TopicTree, Video

class Command(BaseCommand):

    def handle(self, *args, **options):
        #try:
        #    top = TopicTree.objects.get()
        #except:
        #TopicTree.objects.all().delete()
        #Topic.objects.all().delete()
        #Video.objects.all().delete()
        #top = TopicTree()

        #top.get()
        #top.propigate()
