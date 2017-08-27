from django.db import models

# Create your models here.
from django.forms import forms


class PlayerUI(models.Model):
    id = models.TextField(primary_key=True, null=False)

    human_choice = models.TextField(default='empty.png', null=False)
    ai_choice = models.TextField(default='empty.png', null=False)
    result_text = models.TextField(default=' ')
    score_text = models.TextField(default='0:0')

    human_story_choices = models.TextField(default='')
    ai_story_choices = models.TextField(default='')

    wins = models.IntegerField(default=0, null=False)
    loses = models.IntegerField(default=0, null=False)
    draws = models.IntegerField(default=0, null=False)
