import os
from django.conf import settings
from core.models import Activity, Community, Diagnostic, Drug, SicknessObservation, Zone, VisitGrass, Sector
import pandas as pd

from .utils import HelperCommand

baset_path = os.path.join(settings.BASE_DIR,'core', 'management','commands','files')

class Command(HelperCommand):
    help = "import xls data"
    diagnostic_names = {}
    sickness_observation_names = {}

    def __init__(self):
        diagnostics = Diagnostic.objects.all()
        for d in diagnostics:
            self.diagnostic_names[d.name] = d

        sickness_observations = SicknessObservation.objects.all()
        for s in sickness_observations:
            self.sickness_observation_names[s.name] = s

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

        path = os.path.join(baset_path,'bd_pastos_test.xlsx')
        # columns format ['Nº', 'MES', 'FECHA', 'ZONA', 'COMUNIDAD ', 'PDE-2019', 'SECTOR/IRRIGACION DE LA UP ', 'TIPOLOGIA DE UP', 'UP  ES PILOTO?', 'NOMBRE RESPONSABLE UP', 'Nº DNI', 'SEXO RUP', 'NOMBRE DEL INTEGRANTE DE LA UP', 'Nº DNI.1', 'SEXO IUP', 'SECTOR/IRRIGACION DEL BENEFICIARIO', 'NOMBRE DE ESPECIALISTA', 'RESPONSABLE DE ACTIVIDAD', 'ACTIVIDAD REALIZADA', 'SECCION 1', 'ENFERMEDAD/TRANSTORNO/OBSERVACION', 'DIAGNOSTICO', 'VACA', 'VAQUILLONA', 'VAQUILLA', 'TERNERO', 'TORETE', 'TORO', 'VACUNOS', 'OVINOS', 'ALPACAS', 'LLAMAS', 'CANES', '1 FARMACOS /SALES', 'CANTIDAD', 'U.M.', '2 FARMACOS /SALES', 'CANTIDAD.1', 'U.M..1', '3 FARMACOS /SALES', 'CANTIDAD.2', 'U.M..2', '4 FARMACOS /SALES', 'CANTIDAD.3', 'U.M..3']
        # the order and names should be the same in xls file
        df = pd.read_excel(path)
        data = df.to_dict()
        rows_count = len(data['N°'].keys())
        visits = []
        
        for i in range (rows_count):
            
            # data['Nº'][i]
            # data['MES'][i]
            data_visited_at = data['FECHA'][i]
            # data['DATOS GENERALES'][i]
            data_zone = data['ZONA'][i]
            data_community = data['COMUNIDAD '][i]
            data_sector =  data['SECTOR/IRRIGACION'][i]
            data_up_responsable_name = data['NOMBRE RESPONSABLE UP'][i]
            data_up_responsable_dni = data['Nº DNI'][i]
            data_up_responsable_sex = data['SEXO RUP'][i]
            data_up_member_name = data['NOMBRE DEL INTEGRANTE DE LA UP'][i]
            data_up_member_dni = data['Nº DNI.1'][i]
            data_up_member_sex = data['SEXO IUP'][i]
            data_coordenate = data['COORDENADAS UTM Anuales'][i]
            data_employ_responsable = data['NOMBRE RESPONSABLE'][i]
            data_employ_specialist = data['RESPONSABLE DE ACTIVIDAD'][i]
            data_activity = data['ACTIVIDAD REALIZADA'][i]
            # data['SECCION 3'][i]
            # data['SECCION 3'][i]
            # TODO: work on activity quantities 

            try:
                visited_at = data_visited_at
                zone = self.get_zone(data_zone, creates_if_none)
                community = self.get_community(data_community, creates_if_none)
                sector = self.get_sector(data_sector, creates_if_none)
                up_responsable = self.get_person(data_up_responsable_name, data_up_responsable_dni, data_up_responsable_sex)
                up_member = self.get_person(data_up_member_name, data_up_member_dni, data_up_member_sex)                
                coordenate = data_coordenate
                employ_responsable = self.get_person(data_employ_responsable)
                employ_specialist = self.get_person(data_employ_specialist)
                activity = self.get_activity(data_activity, creates_if_none)
                
                visits.append(VisitGrass(
                    visited_at = visited_at,
                    zone = zone,
                    community = community,
                    sector = sector,
                    up_responsable = up_responsable,
                    up_member = up_member,
                    utm_coordenate = coordenate,
                    employ_specialist = employ_specialist,
                    employ_responsable = employ_responsable,
                    activity = activity,
                ))

            except Zone.DoesNotExist:
                print('row', str(i + 1) ,'not found zone:', data_zone)
                exit()
            except Community.DoesNotExist:
                print('row', str(i + 1) ,'not found community:', data_community)
                exit()
            except Sector.DoesNotExist:
                print('row', str(i + 1) ,'not found sector:', data_sector)
                exit()
            except Activity.DoesNotExist:
                print('row', str(i + 1) ,'not found activity:', data_activity)
                exit()
            
       
        VisitGrass.objects.bulk_create(visits)
