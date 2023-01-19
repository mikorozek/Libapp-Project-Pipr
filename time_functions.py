from datetime import date, datetime
from dateutil.relativedelta import relativedelta


date_format = "%d/%m/%Y"


def todays_date():
    return date.today().strftime(date_format)


def default_expiration_date():
    default_date = date.today() + relativedelta(months=3)
    return default_date.strftime(date_format)


def update_date(date, months):
    date_object = datetime.strptime(date, date_format)
    updated_date = date_object + relativedelta(months=months)
    return updated_date.strftime(date_format)


def prepare_date_from_Qt_Calendar(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    return date_object.strftime(date_format)
