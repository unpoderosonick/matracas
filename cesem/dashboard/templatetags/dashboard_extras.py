from django import template

register = template.Library()

def get_columns_names(value, arg):

    columns = []
    for column in arg:
        columns.append(value.get_serializer().fields[column].label)
    return columns

def get_home_path(value):    
    return value.get_serializer().get_home_path()

def get_model_name_plural(value):    
    return value.get_serializer().Meta.model._meta.verbose_name_plural.title()

def get_model_name(value):
    return value.get_serializer().Meta.model._meta.verbose_name.title()

register.filter("get_columns_names", get_columns_names)
register.filter("get_model_name_plural", get_model_name_plural)
register.filter("get_model_name", get_model_name)
register.filter("get_home_path", get_home_path)
