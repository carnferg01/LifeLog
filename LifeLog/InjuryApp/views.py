from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

# Create your views here.
class InjuryListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = "InjuryApp.view_injury"
    #table_class = InjuryTable
    #queryset = Injury.objects.all()
    #filterset_class = InjuryFilter
    paginate_by = 15
    
    # def get_template_names(self):
    #     if "table_partial" in self.request.GET.keys():
    #         return "generic-list-partial.html"
    #     else:
    #         return "generic-list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'List injury'
        context["add_url"] = 'injury-create'
        context["detail_link"] = 'injury-detail'
        return context