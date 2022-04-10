from django.db import models


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
    ACTIONS = (
        ('I', 'Entry'),
        ('O', 'Exit'),
    )
    time = models.DateTimeField()
    action = models.CharField(max_length=1, choices=ACTIONS)
    hku_member = models.ForeignKey(HkuMember, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.time} {self.action} {self.hku_member.hku_id} {self.venue.code}'
