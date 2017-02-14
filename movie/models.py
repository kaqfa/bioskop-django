from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Genre(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="judul")
    cover = models.ImageField(upload_to="movie_covers/", blank=True,
                              default="no-image.png")
    description = models.TextField("deskripsi", null=True, blank=True)
    show_from = models.DateField("tayang dari")
    show_until = models.DateField("tayang hingga")
    genres = models.ManyToManyField(Genre)
    posted_by = models.ForeignKey(User, verbose_name="yang posting")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def show_genres(self):
        genre = self.genres.all()
        text = ''
        for data in genre:
            text += data.title+", "
        return text

    def in_show(self):
        now = datetime.now().date()
        if now >= self.show_from and now <= self.show_until:
            return 1 # sedang tayang
        elif now > self.show_until:
            return -1 # selesai tayang
        else:
            return 0 # segera tayang

    def show_status(self):
        if self.in_show() == 1:
            return "sedang tayang"
        elif self.in_show() == -1:
            return "selesai tayang"
        else:
            return "segera tayang"
