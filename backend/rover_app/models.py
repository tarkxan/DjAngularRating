from django.db import models
from phone_field import PhoneField
from .import utils
from time import time


class Owner(models.Model):

    owner_name = models.CharField(max_length=50)
    owner_image = models.CharField(max_length=200)
    owner_phone_number = PhoneField()
    owner_email = models.CharField(max_length=100)

    def __str__(self):
        return 'Owner: {}'.format(self.owner_name)

    def __unicode__(self):
        return self.owner_name


class Pet(models.Model):

    pet_name = models.CharField(max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return 'Pet: {} of {}'.format(self.pet_name, self.owner.owner_name)

    def __unicode__(self):
        return self.pet_name


class Sitter(models.Model):

    sitter_name = models.CharField(max_length=50)
    sitter_image = models.CharField(max_length=200)
    sitter_phone_number = PhoneField()
    sitter_email = models.CharField(max_length=100)
    sitter_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avg_rating_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overall_sitter_rank = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return 'Sitter: {}'.format(self.sitter_name)

    def __unicode__(self):
        return self.sitter_name

    def get_absolute_url(self):

        return '/sitters/{}/'.format(self.id)


class Stay(models.Model):
    RATING_CHIOICES = [(1, 1),(2, 2),(3, 3),(4, 4),(5, 5)]

    rating = models.IntegerField(choices=RATING_CHIOICES)
    text = models.TextField(max_length=1000)
    start_date = models.DateField(max_length=50)
    end_date = models.DateField(max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)
    pets = models.ManyToManyField(Pet, verbose_name='List of Pets')

    def __str__(self):
        # return str(self.rating)
        return 'Review of {} for {} on {}'.format(self.owner.owner_name, self.sitter.sitter_name, self.start_date)

    # override to update Sitter's scores when sitter's stay updated (saved)
    def save(self,
             *args,
             **kwargs):

        super().save(*args, **kwargs)  # Call the "real" save()
        utils.calculate_sitter_scores(sitters_lst = None,
                                      sitter = self.sitter)