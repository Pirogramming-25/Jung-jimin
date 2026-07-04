from django.db import models

class DevTool(models.Model):
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.name


class Idea(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='idea_images/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE)
    is_star = models.BooleanField(default=False)

    def __str__(self):
        return self.title
