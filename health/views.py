#from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse

from health.forms import InjurySummaryFilterForm
from .models import Injury, Illness
#from .forms import InjuryForm

# exercise/injury
class InjuryListView(ListView):
    model = Injury
    template_name = 'health/injury_list.html'
    def get_queryset(self):
        return Injury.objects.select_related('calculated_injury').all()

class InjuryDetailView(DetailView):
    model = Injury
    template_name = 'health/injury_detail.html'
    def get_queryset(self):
        return Injury.objects.select_related('calculated_injury').all()

class InjuryCreateView(CreateView):
    model = Injury
    fields = ['issue', 'area', 'side', 'start_datetime', 'severity', 'description']
    template_name = 'health/injury_form.html'
    success_url = reverse_lazy('injury-list')

class InjuryUpdateView(UpdateView):
    model = Injury
    #form_class = InjuryForm
    fields = ['issue', 'area', 'side', 'start_datetime', 'severity', 'description']
    template_name = 'health/injury_form.html'
    success_url = reverse_lazy('injury-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url'] = reverse_lazy('injury-delete', kwargs={'pk': self.object.pk})
        return context

class InjuryDeleteView(DeleteView):
    model = Injury
    template_name = 'health/injury_confirm_delete.html'
    success_url = reverse_lazy('injury-list')
    
def InjurySummary_view(request):
    form = InjurySummaryFilterForm(request.GET)
    return render(request, 'health/injury_summary.html', {'form': form})

def InjurySummary_data(request):
    if request.method == 'GET':
        form = InjurySummaryFilterForm(request.GET)
        if form.is_valid():
            queryset = Injury.objects.all()
            if form.cleaned_data['date_from']:
                queryset = queryset.filter(start_datetime__gte=form.cleaned_data['date_from'])
            else:
                queryset = Injury.objects.all()
            queryset = "".join(list(queryset.values_list('issue', flat=True)))
            return JsonResponse({'data': queryset})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# exercise/illness
class IllnessListView(ListView):
    model = Illness
    template_name = 'health/illness_list.html'
    def get_queryset(self):
        return Illness.objects.select_related('calculated_illness').all()

class IllnessDetailView(DetailView):
    model = Illness
    template_name = 'health/illness_detail.html'
    def get_queryset(self):
        return Illness.objects.select_related('calculated_illness').all()

class IllnessCreateView(CreateView):
    model = Illness
    fields = ['issue', 'start_datetime', 'severity', 'description']
    template_name = 'health/illness_form.html'
    success_url = reverse_lazy('illness-list')

class IllnessUpdateView(UpdateView):
    model = Illness
    fields = ['issue', 'start_datetime', 'severity', 'description']
    template_name = 'health/illness_form.html'
    success_url = reverse_lazy('illness-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url'] = reverse_lazy('illness-delete', kwargs={'pk': self.object.pk})
        return context

class IllnessDeleteView(DeleteView):
    model = Illness
    template_name = 'health/illness_confirm_delete.html'
    success_url = reverse_lazy('illness-list')    
    
