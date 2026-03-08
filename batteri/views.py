from django.http import HttpResponse
from django.shortcuts import render
from .data_dk2 import get_plots_for_prices,  get_plots_for_purchasedvolumne, get_plots_for_energy_prod, get_plot_for_dayahead, get_plot_for_daily_variation, correlation_matrix_outliers_removoed, logistic_regression_model, FCR_AI_AGENT, investerings_case
# Create your views here.


def batteri_view(request):
    context = {
        "plot_price": get_plots_for_prices(),
        "plot_daily_variation": get_plot_for_daily_variation(),
        "plot_purchasedvolumne_local": get_plots_for_purchasedvolumne(),
        "plot_energy_prod": get_plots_for_energy_prod(),
        "plot_dayahead": get_plot_for_dayahead(),
        "correlation_outliers_removed": correlation_matrix_outliers_removoed(),
        "logistic_model": logistic_regression_model(),
        "investerings_case": investerings_case(),

    }

    if request.GET.get("run_ai") == "1":
        context["ai_agent_dk1"] = FCR_AI_AGENT()

    return render(request, "batteri/batteri.html", context)
