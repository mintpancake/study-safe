from django.db import models
from django.core.exceptions import ValidationError


class Venue(models.Model):
    TYPES = (
        ('LT', 'Lecture Theatre'),
        ('CR', 'Classroom'),
        ('TR', 'Tutorial Room'),
    )
    code = models.CharField(max_length=20, primary_key=True)
    location = models.CharField(max_length=150)
    type = models.CharField(max_length=2, choices=TYPES)
    capacity = models.IntegerField()

    def __str__(self):
        return self.code


class HkuMember(models.Model):
    hku_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=150)
    venues = models.ManyToManyField(Venue, through='Visit')

    def __str__(self):
        return f'{self.hku_id} {self.name}'


class Visit(models.Model):
    enter_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    hku_member = models.ForeignKey(HkuMember, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.exit_time:
            self.exit_time = None
        elif self.exit_time < self.enter_time:
            raise ValidationError("Exit time must be later than enter time!")
        super(Visit, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.enter_time} {self.exit_time} {self.hku_member.hku_id} {self.venue.code}'
