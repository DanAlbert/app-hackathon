from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Vote(models.Model):
    project = models.ForeignKey(Project)
    count = models.IntegerField()
    
    def increment(self):
        self.count += 1