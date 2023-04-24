from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Activity, Community, Diagnostic, Drug, SicknessObservation, Zone, Visit, Person
#import excel2json
#from python_excel2json import parse_excel_to_json
import pandas as pd
import math
import os

baset_path = os.path.join(settings.BASE_DIR,'core', 'management','commands','files')

class Command(BaseCommand):
    help = "import xls data"
    people_names = {}
    diagnostic_names = {}
    sickness_observation_names = {}
    activities_names = {}
    zones_names = {}

    def __init__(self):
        people = Person.objects.all()
        for p in people:
            self.people_names[p.name] = p

        diagnostics = Diagnostic.objects.all()
        for d in diagnostics:
            self.diagnostic_names[d.name] = d
        
        zones = Zone.objects.all()
        for z in zones:
            self.zones_names[z.name] = z

        sickness_observations = SicknessObservation.objects.all()
        for s in sickness_observations:
            self.sickness_observation_names[s.name] = s

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

    def get_diagnostic(self, name, creates_if_none):
        diagnostic = None
        if name in self.diagnostic_names:
            diagnostic = self.diagnostic_names[name]
        else:
            if creates_if_none:
                diagnostic = Diagnostic.objects.create(name=name)
                self.diagnostic_names[name] = diagnostic
            else:
                raise Diagnostic.DoesNotExist()
        return diagnostic
    
    def get_sickness_observation(self, name, creates_if_none):
        sickness_observation = None
        if name in self.sickness_observation_names:
            sickness_observation = self.sickness_observation_names[name]
        else:
            if creates_if_none:
                sickness_observation = SicknessObservation.objects.create(name=name)
                self.sickness_observation_names[name] = sickness_observation
            else:
                raise SicknessObservation.DoesNotExist()
        return sickness_observation

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

    def zero_if_nan(self, val):
        try:
            if str(float(val)).lower() == 'nan':
                return 0
        except:
            return 0
        #if math.isnan(val):
        return val


    def handle(self, *args, **kwargs):
        creates_if_none = kwargs['creates_if_none']

        path = os.path.join(baset_path,'bd_xyz.xls')
        # columns format ['Nº', 'MES', 'FECHA', 'ZONA', 'COMUNIDAD ', 'PDE-2019', 'SECTOR/IRRIGACION DE LA UP ', 'TIPOLOGIA DE UP', 'UP  ES PILOTO?', 'NOMBRE RESPONSABLE UP', 'Nº DNI', 'SEXO RUP', 'NOMBRE DEL INTEGRANTE DE LA UP', 'Nº DNI.1', 'SEXO IUP', 'SECTOR/IRRIGACION DEL BENEFICIARIO', 'NOMBRE DE ESPECIALISTA', 'RESPONSABLE DE ACTIVIDAD', 'ACTIVIDAD REALIZADA', 'SECCION 1', 'ENFERMEDAD/TRANSTORNO/OBSERVACION', 'DIAGNOSTICO', 'VACA', 'VAQUILLONA', 'VAQUILLA', 'TERNERO', 'TORETE', 'TORO', 'VACUNOS', 'OVINOS', 'ALPACAS', 'LLAMAS', 'CANES', '1 FARMACOS /SALES', 'CANTIDAD', 'U.M.', '2 FARMACOS /SALES', 'CANTIDAD.1', 'U.M..1', '3 FARMACOS /SALES', 'CANTIDAD.2', 'U.M..2', '4 FARMACOS /SALES', 'CANTIDAD.3', 'U.M..3']
        # the order and names should be the same in xls file
        df = pd.read_excel(path)
        data = df.to_dict()
        rows_count = len(data['Nº'].keys())
        visits = []

        for i in range (rows_count):
            
            # data['Nº'][i]
            # data['MES'][i]
            data_visited_at = data['FECHA'][i]
            data_zone = data['ZONA'][i]
            # data['COMUNIDAD '][i]
            # data['PDE-2019'][i]
            # data['SECTOR/IRRIGACION DE LA UP '][i]
            # data['TIPOLOGIA DE UP'][i]
            # data['UP  ES PILOTO?'][i]
            data_up_responsable_name = data['NOMBRE RESPONSABLE UP'][i]
            data_up_responsable_dni = data['Nº DNI'][i]
            data_up_responsable_sex = data['SEXO RUP'][i]
            data_up_member_name = data['NOMBRE DEL INTEGRANTE DE LA UP'][i]
            data_up_member_dni = data['Nº DNI.1'][i]
            data_up_member_sex = data['SEXO IUP'][i]
            # data['SECTOR/IRRIGACION DEL BENEFICIARIO'][i]
            data_employ_specialist = data['NOMBRE DE ESPECIALISTA'][i]
            data_employ_responsable = data['RESPONSABLE DE ACTIVIDAD'][i]
            data_activity = data['ACTIVIDAD REALIZADA'][i]
            # data['SECCION 1'][i]
            data_sickness_observation = data['ENFERMEDAD/TRANSTORNO/OBSERVACION'][i]
            data_diagnostic = data['DIAGNOSTICO'][i]
            # data['VACA'][i]
            # data['VAQUILLONA'][i]
            # data['VAQUILLA'][i]
            # data['TERNERO'][i]
            # data['TORETE'][i]
            # data['TORO'][i]
            data_cattle = self.zero_if_nan(data['VACUNOS'][i])
            data_sheep = self.zero_if_nan(data['OVINOS'][i])
            data_alpacas = self.zero_if_nan(data['ALPACAS'][i])
            data_llamas = self.zero_if_nan(data['LLAMAS'][i])
            data_canes = self.zero_if_nan(data['CANES'][i])
            # data['1 FARMACOS /SALES'][i]
            # data['CANTIDAD'][i]
            # data['U.M.'][i]
            # data['2 FARMACOS /SALES'][i]
            # data['CANTIDAD.1'][i]
            # data['U.M..1'][i]
            # data['3 FARMACOS /SALES'][i]
            # data['CANTIDAD.2'][i]
            # data['U.M..2'][i]
            # data['4 FARMACOS /SALES'][i]
            # data['CANTIDAD.3'][i]
            # data['U.M..3'][i]

            try:
                visited_at = data_visited_at
                zone = self.get_zone(data_zone, creates_if_none)
                up_responsable = self.get_person(data_up_responsable_name, data_up_responsable_dni, data_up_responsable_sex)
                up_member = self.get_person(data_up_member_name, data_up_member_dni, data_up_member_sex)                
                employ_specialist = self.get_person(data_employ_specialist)
                employ_responsable = self.get_person(data_employ_responsable)
                activity = self.get_activity(data_activity, creates_if_none)
                sickness_observation = self.get_sickness_observation(data_sickness_observation, creates_if_none)
                diagnostic = self.get_diagnostic(data_diagnostic, creates_if_none)
                cattle =  data_cattle
                sheep = data_sheep
                alpacas = data_alpacas
                llamas = data_llamas
                canes = data_canes
                
                visits.append(Visit(
                    visited_at = visited_at,
                    zone = zone,
                    up_responsable = up_responsable,
                    up_member = up_member,
                    employ_specialist = employ_specialist,
                    employ_responsable = employ_responsable,
                    activity = activity,
                    sickness_observation = sickness_observation,
                    diagnostic = diagnostic,
                    cattle = cattle,
                    sheep = sheep,
                    alpacas = alpacas,
                    llamas = llamas,
                    canes = canes,
                ))

            except Zone.DoesNotExist:
                print('row', str(i + 1) ,'not found zone:', data_zone)
                exit()
            except Activity.DoesNotExist:
                print('row', str(i + 1) ,'not found activity:', data_activity)
                exit()
            except Diagnostic.DoesNotExist:
                print('row', str(i + 1) ,'not found diagnostic:', data_diagnostic)
                exit()
            except SicknessObservation.DoesNotExist:
                print('row', str(i + 1) ,'not found sickness/observation:', data_sickness_observation)
                exit()
            
       
        Visit.objects.bulk_create(visits)
