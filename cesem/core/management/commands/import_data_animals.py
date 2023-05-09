import os
from django.conf import settings
from core.models import Activity, Community, Diagnostic, Drug, SicknessObservation, Zone, VisitAnimal, Sector
import pandas as pd

from .utils import HelperCommand

baset_path = os.path.join(settings.BASE_DIR,'core', 'management','commands','files')

class Command(HelperCommand):
    help = "import xls data"
    diagnostic_names = {}
    sickness_observation_names = {}

    def __init__(self):
        super().__init__()
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
            data_community = data['COMUNIDAD '][i]
            # data['PDE-2019'][i]
            data_sector =  data['SECTOR/IRRIGACION DE LA UP '][i]
            data_tipology = data['TIPOLOGIA DE UP'][i]
            data_is_pilot = data['UP ES PILOTO?'][i] == 'SI'
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
                
                production_unit = self.get_production_unit(
                            data_zone, 
                            data_community, 
                            data_sector, 
                            data_up_responsable_name, 
                            data_up_responsable_dni, 
                            data_up_responsable_sex,
                            data_up_member_name, 
                            data_up_member_dni, 
                            data_up_member_sex,
                            data_is_pilot=data_is_pilot,
                            data_tipology=data_tipology,
                            creates_if_none=creates_if_none,
                            )

                visits.append(VisitAnimal(
                    visited_at = data_visited_at,
                    production_unit = production_unit,
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
            except Community.DoesNotExist:
                print('row', str(i + 1) ,'not found community:', data_community)
                exit()
            except Sector.DoesNotExist:
                print('row', str(i + 1) ,'not found sector:', data_sector)
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
            
       
        VisitAnimal.objects.bulk_create(visits)
