from django.db import models

# Create your models here.
class Position(models.Model):
  name = models.CharField(max_length=100, unique=True)

class Descript(models.Model):
  name = models.CharField(max_length=100, unique=True)

class GroundFact(models.Model):
  name = models.CharField(max_length=100, unique=True)
  position = models.ForeignKey('Position', on_delete=models.PROTECT)
  descript = models.ForeignKey('Descript', on_delete=models.PROTECT)
  level    = models.IntegerField(default=1)

class ZhengHou(models.Model):
  name      = models.CharField(max_length=100, unique=True)
  zhenghous = models.ManyToManyField('self')
  level     = models.IntegerField(default=1)
  gfs       = models.ManyToManyField(GroundFact)

class Synonym(models.Model):
  name      = models.CharField(max_length=100, unique=True)
  syno      = models.CharField(max_length=100)

class InfoInput(models.Model):
  Stage   = (
    (1, "raw"),
    (2, "jiebad"),
  )
  name      = models.CharField(max_length=100, unique=True)
  content   = models.TextField()
  modified  = models.TextField()
  comefrom  = models.CharField(max_length=100)
  level     = models.CharField(choices=Stage, default=1)
