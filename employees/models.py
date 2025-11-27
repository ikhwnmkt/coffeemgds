from django.db import models

class pegawai(models.Model):
  id_pegawai = models.CharField(max_length=10, unique=True)
  nama = models.CharField(max_length=100)
  posisi = models.CharField(max_length=50)
  shift = models.CharField(max_length=100)
  gaji_per_jam = models.IntegerField()
  jam_kerja = models.IntegerField(default=0) 
  bonus_per_minuman = models.IntegerField(default=0) 
  miuman_terjual = models.IntegerField(default=0) 
  jenis = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.nama} - {self.posisi}"