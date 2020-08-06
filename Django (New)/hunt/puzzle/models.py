from django.db import models


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=False)
    level_completed = models.IntegerField()
    points = models.IntegerField()

    def __str__(self):
        return self.name


class Quiz(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='puzzle')
    answer = models.TextField(blank=False)

    def __str__(self):
        return str( self.id )


class Submission(models.Model):
    submitter = models.OneToOneField(Team, on_delete=models.CASCADE)
    quiz      = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    answer    = models.TextField()

    def __str__(self):
        return self.submitter.name + " to " + str(self.quiz)
