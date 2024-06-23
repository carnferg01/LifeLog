
from django.urls import path
from django.views.generic import RedirectView
from .views import InjuryListView, InjuryDetailView, InjuryCreateView, InjuryUpdateView, InjuryDeleteView
from .views import IllnessListView, IllnessDetailView, IllnessCreateView, IllnessUpdateView, IllnessDeleteView
from .views import InjurySummary_view, InjurySummary_data

urlpatterns = [    
    # exercise/injury
    path('injury/', InjuryListView.as_view(), name='injury-list'),
    path('injury/<int:pk>/', InjuryDetailView.as_view(), name='injury-detail'),
    path('injury/new/', InjuryCreateView.as_view(), name='injury-create'),
    path('injury/<int:pk>/edit/', InjuryUpdateView.as_view(), name='injury-update'),
    path('injury/<int:pk>/delete/', InjuryDeleteView.as_view(), name='injury-delete'),
    path('injury/summary/', InjurySummary_view, name='injury-summary'),
    path('api/injurysummary/', InjurySummary_data, name='injury-summary-fetch-data'),

    # exercise/illness
    path('illness/', IllnessListView.as_view(), name='illness-list'),
    path('illness/<int:pk>/', IllnessDetailView.as_view(), name='illness-detail'),
    path('illness/new/', IllnessCreateView.as_view(), name='illness-create'),
    path('illness/<int:pk>/edit/', IllnessUpdateView.as_view(), name='illness-update'),
    path('illness/<int:pk>/delete/', IllnessDeleteView.as_view(), name='illness-delete'),
]