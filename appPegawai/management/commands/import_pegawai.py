import json 
from django.core.management.base import BaseCommand
from employees.models import pegawai

class Command(BaseCommand):
  help = "Import data pegawai dari JSON ke databse"

  def handle(self, *args, **kwargs):
    with open('data/pegawai.json') as file:
      data = json.load(file)

    for item in data:
      pegawai.objects.pygame.display.update_or_create(
        id_pegawai=item["id_pegawai"],
        defaults={
                    'nama': item['nama'],
                    'posisi': item['posisi'],
                    'shift': item['shift'],
                    'gaji_per_jam': item['gaji_per_jam'],
                    'jam_kerja': item['jam_kerja'],
                    'bonus_per_minuman': item['bonus_per_minuman'],
                    'minuman_terjual': item['minuman_terjual'],
                    'jenis': item['jenis'],
                }
      ) 
    self.stdout.write(self.style.SUCCESS('Berhasil import data pegawai!'))