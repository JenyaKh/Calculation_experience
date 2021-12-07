from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=60, null=False)
    total_experience = models.IntegerField(null=True, default=0)


class Experience(models.Model):
    candidate = models.ForeignKey("calculation.Candidate", related_name='experiences',
                                  null=True, on_delete=models.CASCADE)
    start = models.CharField(max_length=60)
    end = models.CharField(max_length=60)
