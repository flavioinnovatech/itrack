# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from equipments.models import Equipment
from vehicles.models import Vehicle
from system.models import System

import random

colors = ['Amarelo','Vermelho','Cinza','Preto','Branco','Azul', 'Verde','Rosa','Laranja']
models = [
            ['Carro','Volkswagen','Fusca'],
            ['Carro','Volkswagen','Corsa'],
            ['Carro','Volkswagen','Gol'],
            ['Carro','Ford','Fiesta'],
            ['Carro','Ford','Ka'],
            ['Carro','Ford','Fusion'],
            ['Caminhão','Scania','R470'],
            ['Caminhão','Scania','P380'],
            ['Caminhão','Scania','G400'],
          ]



class Command(BaseCommand):
    def handle(self, *args, **options):
        
        initial_plate = 1
        initial_chassi = 10003
        year = 2011
        
        equips = Equipment.objects.filter(vehicle=None)
        sys = System.objects.get(parent=None)
        
        for equip in equips:
            color = random.choice(colors)
            model = random.choice(models)
            v = Vehicle(
                equipment=equip,
                chassi=str(initial_chassi),
                license_plate='MXT'+str(initial_plate).zfill(4),
                color=color,
                year=year,
                manufacturer=model[1],
                model=model[2],
                type=model[0],
                threshold_time=0.5,
            )
            initial_plate  += 1
            initial_chassi += 1
            v.save()
            v.system.add(sys)
            v.save()

