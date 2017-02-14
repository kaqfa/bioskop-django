from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField("Alamat", max_length=200, null=True, blank=True)
    phone = models.CharField("Nomor Telepon", max_length=20)
    prof_pic = models.ImageField("Foto Profil", upload_to='prof_pics/',
                                 null=True, blank=True)
    register_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def user_email(self):
        return  self.user.email

    def user_first_name(self):
        return self.user.first_name

    def user_full_name(self):
        return self.user.first_name+" "+self.user.last_name


class TopUp(models.Model):
    STATUS_CHOICES = (('p', 'pending'), ('v', 'valid'), ('i', 'invalid'))

    member = models.ForeignKey(Member)
    amount = models.IntegerField()
    receipt = models.ImageField("Bukti Bayar", upload_to='receipts/')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(auto_now=True)
    checked_by = models.ForeignKey(User, null=True, blank=True)
