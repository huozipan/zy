from django.db import models

# Create your models here.
class Position(models.Model):
  name = models.CharField(max_length=100)

class Descript(models.Model):
  name = models.CharField(max_length=100)

class GroundFact(models.Model):
  name = models.CharField(max_length=100)
  position = models.ForeignKey('Position', on_delete=models.SET_NULL)
  descript = models.ForeignKey('Descript', on_delete=models.SET_NULL)
  level    = models.IntergerField(default=1)

class ZhengHou(models.Model):
  name      = models.CharField(max_length=100)
  zhenghous = models.ManyToManyField(ZhengHou)
  level     = models.IntergerField(default=1)
  gfs       = models.ManyToManyField(GroundFact)

class Synonym(models.Model):
  name      = models.CharField(max_length=100)
  syno      = models.CharField(max_length=100)


