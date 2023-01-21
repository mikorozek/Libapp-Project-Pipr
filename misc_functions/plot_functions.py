from matplotlib import pyplot as plt
from misc_functions.time_functions import plot_last_12_months


def generate_plot_for_member(member):
    """
    Function that generates plot where on x-axis are last 12 months and on
    y-axis are values of rentings done by client
    """
    keys = plot_last_12_months()
    keys.reverse()
    values = [
        member.month_amount_of_rentings_in_history(month)
        for month in keys
    ]
    plt.plot(keys, values, 'o-', label="Amount of rentings", markersize=6)
    plt.yticks(range(min(values), max(values) + 1))
    plt.xticks(rotation=30, fontsize='x-small', horizontalalignment='right')
    plt.legend()
    plt.title(label=str(member))
    plt.show()


def generate_plot_for_library(library):
    """
    Function that generates plot where on x-axis are last 12 months and on
    y-axis are values of rentings done by all library clients.
    """
    keys = plot_last_12_months()
    keys.reverse()
    values = [
        library.month_amount_of_rentings(month)
        for month in keys
    ]
    plt.plot(keys, values, 'o-', label="Amount of rentings", markersize=6)
    plt.yticks(range(min(values), max(values) + 1))
    plt.xticks(rotation=30, fontsize='x-small', horizontalalignment='right')
    plt.legend()
    plt.title(label="All rentings made in library last year")
    plt.show()
