from __future__ import unicode_literals

from django.db import models

DEFAULT_GRADE_SCALE = '{"A":"93%", "A-":"90%", "B+":"87%", "B":"83%", "B-":"80%", "C+":"77%", "C":"73%", "C-":"70%", "D+":"67%", "D":"63%", "D-":"60%", "E":"0%"}'


# Create your models here.
class User(models.Model):
    netid = models.CharField(max_length=300, null=False, primary_key=True)
    password = models.CharField(max_length=64, null=False)

    def __unicode__(self):
        return self.netid

class Classes(models.Model):
    course_code = models.CharField(max_length=10, null=False)
    course_grade = models.CharField(max_length=7, null=False)
    course_title = models.CharField(max_length=255, null=False)
    grade_scale = models.TextField(default=DEFAULT_GRADE_SCALE, help_text='Contains a JSON-ified list of grades')
    cid = models.CharField(max_length=255, null=False)

    def __unicde__(self):
        return self.cid
