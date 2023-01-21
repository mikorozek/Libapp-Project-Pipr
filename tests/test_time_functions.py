from misc_functions.time_functions import (
    plot_last_12_months,
    updated_date_format_for_renting,
    todays_date
)
from datetime import date


def test_plot_last_12_months():
    assert "01/2023" in plot_last_12_months()
    assert "12/2022" in plot_last_12_months()
    assert "03/2022" in plot_last_12_months()
    assert len(plot_last_12_months()) == 12


def test_updated_date_format_for_renting():
    assert updated_date_format_for_renting("19/09/1999") == "09/1999"


def test_todays_date():
    assert todays_date() == date.today().strftime("%d/%m/%Y")
