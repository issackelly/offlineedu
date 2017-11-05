from django.core.management.base import BaseCommand, CommandError
from get_khan.models import Topic, TopicTree, Video
import numpy as np

def print_topic(t, tab_depth=1):
    if t.data:
        vid_count = Video.objects.filter(parent=t).count()
        if vid_count:
            count_str = "[%s Video%s] " % (vid_count, "s" if vid_count > 1 else " ")
        else:
            count_str = ""
        print("%sT: %s%s :: %s" % (
            "  " * tab_depth,
            count_str,
            t.data['title'],
            t.tree_slug
        ))
        for v in t.video_set.all():
            print("%sV: %s :: %s" % (
                "  " * (tab_depth + 1),
                v.data['title'] if v.data else "",
                v.tree_slug
            ))
        for kid in Topic.objects.filter(parent=t):
            print_topic(kid, tab_depth + 1)

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

class Command(BaseCommand):

    def handle(self, *args, **options):
        top = TopicTree.objects.get()

        print("%s Topics: ", Topic.objects.all().count())

        for t in Topic.objects.filter(parent__isnull=True):
            print_topic(t)

        print("%s Total Videos" % Video.objects.count())


        b_bytes = []
        s_bytes = []
        for v in Video.objects.all():
            if v.data and v.data.get('download_sizes'):
                if v.data['download_sizes'].get('mp4'):
                    b_bytes.append(v.data["download_sizes"]["mp4"])
                #else:
                #    print("No High video")
                if v.data['download_sizes'].get('mp4-low'):
                    s_bytes.append(v.data["download_sizes"]["mp4-low"])
                #else:
                #    print("No low video")
            #else:
            #    print("no download sizes")

        print("%s Full Res Downloaded [%s]" % (
            Video.objects.exclude(big_file="").count(),
            sizeof_fmt(np.sum(b_bytes))
        ))
        print("%s Low Res Downloaded [%s]" % (
            Video.objects.exclude(small_file="").count(),
            sizeof_fmt(np.sum(s_bytes))
        ))
