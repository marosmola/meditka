from django.db import models


class Day(models.Model):
    date = models.DateField(unique=True)
    dayofweek = models.CharField(max_length=10)
    nameday = models.CharField(max_length=100)
    saintsday = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

    class Meta:
        verbose_name = 'Deň'
        verbose_name_plural = 'Dni'


class Gospel(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='gospels')
    chapter = models.CharField(max_length=100)
    chapter_title = models.CharField(blank=True, null=True, max_length=100)
    verse = models.TextField()
    text = models.TextField()
    gospel_from = models.CharField(max_length=100)

    class Meta:
        unique_together = ['day', 'chapter']

    def __str__(self):
        return "gospel_{}".format(self.day)


class Psalm(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "psalm_{}".format(self.day)


class Reading(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "reading_{}".format(self.day)
