from django.db import models


class Person(models.Model):
    class Sexs(models.IntegerChoices):
        FEMALE = 0, ("femenino")
        MALE = 1, ("masculino")

    class Titles(models.IntegerChoices):
        tec = 0, ("tec.")
        mvz = 1, ("mvz.")

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "personas"
        ordering = ("name",)

    dni = models.CharField("dni", max_length=8, null=True, blank=True)
    name = models.CharField("nombres", max_length=50)
    last_name = models.CharField("apellidos", max_length=50, null=True, blank=True)
    sex = models.IntegerField("sexo", choices=Sexs.choices, blank=True, null=True)
    title = models.IntegerField("titulo", choices=Titles.choices, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
