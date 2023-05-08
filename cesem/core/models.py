from django.db import models

class Person(models.Model):
    class Sexs(models.IntegerChoices):
        FEMALE = 0, ('femenino')
        MALE = 1, ('masculino')

    class Titles(models.IntegerChoices):
        tec = 0, ('tec.')
        mvz = 1, ('mvz.')

    class Meta:
        verbose_name = 'persona'
        verbose_name_plural = 'personas'

    dni = models.CharField('dni', max_length=8, null=True, blank=True)
    name = models.CharField('nombres', max_length=20)
    last_name = models.CharField('apellidos', max_length=20, null=True, blank=True)
    sex = models.IntegerField('sexo', choices=Sexs.choices, blank=True, null=True)
    title = models.IntegerField('titulo', choices=Titles.choices, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name

        
class Zone(models.Model):
    name = models.CharField('zona', max_length=20)
    
    class Meta:
        verbose_name = 'zona'
        verbose_name_plural = 'zonas'

    def __str__(self) -> str:
        return self.name


class Sector(models.Model):
    name = models.CharField('Sector', max_length=20)

    def __str__(self) -> str:
        return self.name


class Community(models.Model):
    name = models.CharField('comunidad', max_length=20)

    class Meta:
        verbose_name = 'comunidad'
        verbose_name_plural = 'comunidades'

    def __str__(self) -> str:
        return self.name


class ProductyUnit(models.Model):
    tipology = models.IntegerField()
    is_pilot = models.BooleanField()

class Activity(models.Model):
    class Meta:
        verbose_name = 'actividad'
        verbose_name_plural = 'actividades'

    name = models.CharField('actividad', max_length=50)

    def __str__(self) -> str:
        return self.name


class SicknessObservation(models.Model):
    name = models.CharField('actividad', max_length=50)

    class Meta:
        verbose_name = 'enfermedad/observación'
        verbose_name_plural = 'enfermedades/observaciones'
    
    def __str__(self) -> str:
        return self.name


class Diagnostic(models.Model):
    name = models.CharField('observación', max_length=50) # the name 'name' allow us an easy sync in sync_masters func
    
    class Meta:
        verbose_name = 'diagnostico'
        verbose_name_plural = 'diagnosticos'
    
    def __str__(self) -> str:
        return self.name


class Drug(models.Model):
    class UnitMeasurement(models.IntegerChoices):
        ml = 0, ('ml.')
        gr = 1, ('gr.')

    name = models.CharField('nombre', max_length= 50)
    um = models.IntegerField('unidad de medida', choices=UnitMeasurement.choices, default=0)

    class Meta:
        verbose_name = 'farmaco'
        verbose_name_plural = 'farmacos'

    def __str__(self) -> str:
        return self.name


class VisitAnimal(models.Model):
    visited_at = models.DateField('fecha de creacion')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name='zona')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name='comunidad')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name='sector')
    up_responsable = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='up_responsable_animal', verbose_name='up. responsable')
    up_member = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='up_member_animal', verbose_name='up. integrante')
    employ_specialist = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='employ_specialist_animal', verbose_name='personal especialista')
    employ_responsable = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='employ_responsable_animal', verbose_name='personal responsable')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='actividad')    
    sickness_observation = models.ForeignKey(SicknessObservation, on_delete=models.CASCADE, verbose_name='enfermedad/observación')
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, verbose_name='diagnostico')
    cattle = models.IntegerField('vacunos', default=0)
    sheep = models.IntegerField('ovinos', default=0)
    alpacas = models.IntegerField('alpacas', default=0)
    llamas = models.IntegerField('llamas', default=0)
    canes = models.IntegerField('canes', default=0)

    class Meta:
        verbose_name = 'visita animal'
        verbose_name_plural = 'visitas animales'

class VisitAnimalDetails(models.Model):
    visit = models.ForeignKey(VisitAnimal, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name='farmacos')
    quantity = models.IntegerField('cantidad', default=0)
    
    class Meta:
        verbose_name = 'visita animal - detalle'
        verbose_name_plural = 'visitas animales - detalles'

class VisitGrass(models.Model):
    visited_at = models.DateField('fecha de creacion')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name='zona')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name='comunidad')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name='sector')
    up_responsable = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='up_responsable_grass', verbose_name='up. responsable')
    up_member = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='up_member_grass', verbose_name='up. integrante')
    utm_coordenate = models.CharField('coordenadas UTM anuales', max_length=30, null=True, blank=True)
    employ_specialist = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='employ_specialist_grass', verbose_name='personal especialista')
    employ_responsable = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='employ_responsable_grass', verbose_name='personal responsable')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='actividad')
    quantity = models.IntegerField('cantidad', default=0)

    class Meta:
        verbose_name = 'visita pastos'
        verbose_name_plural = 'visitas pastos'
