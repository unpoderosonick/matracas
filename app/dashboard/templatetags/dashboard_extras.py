from datetime import datetime, timedelta
from django import template

register = template.Library()


def get_columns_labels(view_model, colums):
    columns = []
    for column in colums:
        columns.append(view_model.get_serializer().fields[column].label)
    return columns


def get_column_label(view_model, column_name):
    if column_name in view_model.get_serializer().fields:
        return view_model.get_serializer().fields[column_name].label
    return column_name


def get_home_path(value):
    return value.get_serializer().get_home_path()


def get_model_name_plural(value):
    return value.get_serializer().Meta.model._meta.verbose_name_plural.title()


def get_model_name(value):
    return value.get_serializer().Meta.model._meta.verbose_name.title()


def active_if_path_match(keyword, request):
    if request.path.__contains__(keyword):
        return "active"
    return ""


register.filter("get_columns_labels", get_columns_labels)
register.filter("get_column_label", get_column_label)
register.filter("get_model_name_plural", get_model_name_plural)
register.filter("get_model_name", get_model_name)
register.filter("get_home_path", get_home_path)
register.filter("active_if_path_match", active_if_path_match)
