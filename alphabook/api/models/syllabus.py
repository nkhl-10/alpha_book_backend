from django.db import models
from django.db.models import JSONField


class SyllabusBook(models.Model):
    book = models.OneToOneField('Book', on_delete=models.CASCADE, related_name='syllabus')
    course_name = models.CharField(max_length=255)
    university_name = models.CharField(max_length=255)
    semester = models.CharField(max_length=100)
    subjects = JSONField(default=list)