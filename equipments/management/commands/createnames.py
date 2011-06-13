from equipments.models import CustomField,CustomFieldName
from system.models import System
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q


class Command(BaseCommand):
    args = 'no args'
    help = 'Insert one tracking to the database tables'
    
    
    def handle(self, *args, **options):
        sys = System.objects.get(pk=2)
        cf_set = CustomField.objects.all()
        
        for cf in cf_set:
            cfd = CustomFieldName(name = cf.name, custom_field = cf, system = sys)
            cfd.save()
        
        
