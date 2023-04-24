from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Activity, Community, Diagnostic, Drug, SicknessObservation, Zone
import os

baset_path = os.path.join(settings.BASE_DIR,'core', 'management','commands','files')

class Command(BaseCommand):
    help = "initialize db"

    def sync_model(self, model, file_path):
        path = os.path.join(baset_path,file_path)
        lines = []
        res = []

        with open(path, encoding="utf8") as f:
            lines = f.readlines()        
        for sub in lines:
            res.append(sub.replace("\n", ""))        
        existings = model.objects.filter(name__in= res)
        to_add = []
        for r in res:
            found = False
            for e in existings:
                if e.name == r:
                    found = True
            if not found:
                to_add.append(model(name=r))
        model.objects.bulk_create(to_add)

    def handle(self, *args, **options):
        self.sync_model(Activity, 'activities.txt')
        self.sync_model(Community, 'comunities.txt')
        self.sync_model(Diagnostic, 'diagnostics.txt')
        self.sync_model(Drug, 'drugs.txt')
        self.sync_model(SicknessObservation, 'sickness.txt')
        self.sync_model(Zone, 'zones.txt')
        
        