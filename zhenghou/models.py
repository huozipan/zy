from django.db import models

# Create your models here.
class synonym(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name

class dimention(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name

class Position(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name

class Descript(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name

class GroundFact(models.Model):
  name = models.CharField(max_length=100, unique=True)
  position = models.ForeignKey('Position', on_delete=models.PROTECT)
  descript = models.ForeignKey('Descript', on_delete=models.PROTECT)
  level    = models.IntegerField(default=1)

  def __str__(self):
    return self.name

class ZhengHou(models.Model):
  name      = models.CharField(max_length=100, unique=True)
  zhenghous = models.ManyToManyField('self')
  level     = models.IntegerField(default=1)
  gfs       = models.ManyToManyField(GroundFact)

  def __str__(self):
    return self.name

class Synonym(models.Model):
  name      = models.CharField(max_length=100, unique=True)
  syno      = models.CharField(max_length=100)

class Wenxian(models.Model):
  name      = models.CharField(max_length=100, unique=True)
  detail    = models.TextField(blank=True)
  totable   = models.CharField(max_length=100, default='ZhengHou')

  def __str__(self):
    return self.name

class RawInfo(models.Model):
  Stage   = (
    (1, "raw"),
    (2, "jieba"),
  )
  name      = models.CharField(max_length=100, unique=True)
  content   = models.TextField()
  modified  = models.TextField(blank=True)
  comefrom  = models.ForeignKey('Wenxian', on_delete=models.PROTECT,
      to_field='name')
  level     = models.IntegerField(choices=Stage, default=1)
