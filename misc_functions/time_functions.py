from datetime import date, datetime
from dateutil.relativedelta import relativedelta


date_format = "%d/%m/%Y"


def plot_last_12_months():
    """
    Function used to create list of last 12 months strings in month/year
    format. It is used for plot printing purposes.
    :return: List[str]
    """
    list_of_months = []
    for number in range(12):
        month = (date.today() - relativedelta(months=number)).strftime("%m/%Y")
        list_of_months.append(month)
    return list_of_months


def updated_date_format_for_renting(date):
    """
    Function that updates date format from day/month/year into month/year.
    :return: str
    """
    date_object = datetime.strptime(date, date_format)
    return date_object.strftime("%m/%Y")


def todays_date():
    """
    This method returns todays date in day/month/year format.
    :return: str
    """
    return date.today().strftime(date_format)


def default_expiration_date():
    """
    This method returns default expiration date in day/month/year format
    when client borrows a book. It is 3 months after today.
    :return: str
    """
    default_date = date.today() + relativedelta(months=3)
    return default_date.strftime(date_format)


def update_date(date, months):
    """
    This method is used to update the date with amount of months.
    :param date: str, date in day/month/year format
    :param months: int, amount of months that will be added to  date
    :return: str, date in day/month/year format
    """
    date_object = datetime.strptime(date, date_format)
    updated_date = date_object + relativedelta(months=months)
    return updated_date.strftime(date_format)
