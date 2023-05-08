from django.core.management.base import BaseCommand
from core.models import Person, Zone, Activity, Community, Sector

class HelperCommand(BaseCommand):
    people_names = {}
    zones_names = {}
    activities_names = {}
    community_names = {}
    sector_names = {}

    def __init__(self):
        people = Person.objects.all()
        for p in people:
            self.people_names[p.name] = p
        
        zones = Zone.objects.all()
        for z in zones:
            self.zones_names[z.name] = z
        
        activities = Activity.objects.all()
        for a in activities:
            self.activities_names[s.name] = a

    def add_arguments(self, parser):
        parser.add_argument(
            '--creates_if_none',
            default=False,
            help='it creates activites, diagnostics and sickness if doesnt exists',
        )

    def get_person(self, name, dni=None, sex=None):
        sex_data = None
        if sex == 'M':
            sex_data = Person.Sexs.MALE
        if sex == 'F':
            sex_data = Person.Sexs.FEMALE

        person = None
        if name in self.people_names:
            person = self.people_names[name]
        else:
            try:
                person = Person.objects.get(name=name)
            except Person.DoesNotExist:
                person = Person.objects.create(name=name, dni= dni, sex=sex_data)
                self.people_names[name] = person
        return person
    
    def get_zone(self, name, creates_if_none):        
        zone = None
        if name in self.zones_names:
            zone = self.zones_names[name]
        else:
            if creates_if_none:
                zone = Zone.objects.create(name=name)
                self.zones_names[name] = zone
            else:
                raise Zone.DoesNotExist()
        return zone

    def get_community(self, name, creates_if_none):        
        community = None
        if name in self.community_names:
            community = self.community_names[name]
        else:
            if creates_if_none:
                community = Community.objects.create(name=name)
                self.community_names[name] = community
            else:
                raise Community.DoesNotExist()
        return community

    def get_sector(self, name, creates_if_none):        
        sector = None
        if name in self.sector_names:
            sector = self.sector_names[name]
        else:
            if creates_if_none:
                sector = Sector.objects.create(name=name)
                self.sector_names[name] = sector
            else:
                raise Sector.DoesNotExist()
        return sector

    def get_activity(self, name, creates_if_none):
        activity = None
        if name in self.activities_names:
            activity = self.activities_names[name]
        else:
            if creates_if_none:
                activity = Activity.objects.create(name=name)
                self.activities_names[name] = activity
            else:
                raise Activity.DoesNotExist()
        return activity

        