from django.db import models
from django.contrib.postgres.fields import JSONField
import requests
import os
import structlog
from json.decoder import JSONDecodeError
from django.conf import settings
log = structlog.get_logger()


class TopicTree(models.Model):
    local_modified = models.DateTimeField(auto_now=True)
    tree = JSONField(blank=True, null=True)

    def get(self):
        rep = requests.get("http://www.khanacademy.org/api/v1/topictree")
        self.tree = rep.json()
        self.save()

    def propigate(self):
        for kid in self.tree['children']:
            topic, _ = Topic.objects.get_or_create(ka_slug=kid['slug'])
            topic.tree_slug = kid["slug"]
            topic.get()
            topic.propigate()


class Topic(models.Model):
    local_modified = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    data = JSONField(blank=True, null=True)
    tree_slug = models.CharField(max_length=256, db_index=True)
    ka_slug = models.CharField(max_length=256, db_index=True)

    def get(self):
        log.msg("getting_topic", saved_slug=self.ka_slug)
        rep = requests.get("http://www.khanacademy.org/api/v1/topic/%s" % self.ka_slug)
        try:
            self.data = rep.json()
            self.save()
        except JSONDecodeError:
            log.error("JSON Error", ka_slug=self.ka_slug, status=rep.status_code, body=rep.content)


    def propigate(self):
        log.msg("propigating", saved_slug=self.ka_slug)
        if self.data and self.data['kind']:
            for kid in self.data['children']:
                if kid['kind'] == 'Topic':
                    try:
                        ka_slug = kid['slug']
                    except KeyError:
                        ka_slug = kid['id']


                    topic, _ = Topic.objects.get_or_create(ka_slug=ka_slug, parent=self)
                    topic.tree_slug = self.tree_slug + '/' + ka_slug
                    topic.get()
                    topic.propigate()

                if kid['kind'] == 'Video':
                    ka_id = kid['id']
                    video, _ = Video.objects.get_or_create(ka_id=ka_id, parent=self)
                    video.tree_slug = self.tree_slug + '/' + ka_id
                    video.get()


class Video(models.Model):
    data = JSONField(blank=True, null=True)
    ka_id = models.CharField(max_length=256, db_index=True)
    parent = models.ForeignKey(Topic, blank=True, null=True)
    tree_slug = models.CharField(max_length=256, db_index=True)

    big_file = models.FileField(blank=True, null=True, max_length=2048)
    small_file = models.FileField(blank=True, null=True, max_length=2048)

    def get(self):
        log.msg("getting_video_data", id=self.id, ka_id=self.ka_id)
        rep = requests.get("http://www.khanacademy.org/api/v1/videos/%s" % self.ka_id)
        try:
            self.data = rep.json()
            self.save()
        except JSONDecodeError:
            log.error("JSON Error", ka_slug=self.ka_slug, status=rep.status_code, body=rep.content)


    def propigate(self):
        return

    def download_file(url, filename):
        local_filename = url.split('/')[-1]


    def download_big(self):
        if self.tree_slug[0] == "/":
            self.tree_slug = self.tree_slug[1:]

        filename = "%s.big.mp4" % self.data['title']
        path = os.path.join(settings.MEDIA_ROOT, self.tree_slug)
        if not os.path.exists(path):
            print("making dir %s" % path)
            os.makedirs(path)
        media_path = os.path.join(self.tree_slug, filename)
        local_filename = os.path.join(path, filename)

        log.msg("download_big", id=self.id, ka_id=self.ka_id, path=local_filename)
        r = requests.get(self.data["download_urls"]["mp4"], stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        self.big_file = media_path
        self.save()
        return local_filename

    def download_small(self):
        if self.tree_slug[0] == "/":
            self.tree_slug = self.tree_slug[1:]

        filename = "%s.small.mp4" % self.data['title']
        path = os.path.join(settings.MEDIA_ROOT, self.tree_slug)
        if not os.path.exists(path):
            print("making dir %s" % path)
            os.makedirs(path)
        media_path = os.path.join(self.tree_slug, filename)
        local_filename = os.path.join(path, filename)

        log.msg("download_small", id=self.id, ka_id=self.ka_id, path=local_filename)
        r = requests.get(self.data["download_urls"]["mp4-low"], stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        self.small_file = media_path
        self.save()
