from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import NSSession, SessionType, SessionStatus

class SessionListView(LoginRequiredMixin, ListView):
    model = NSSession
    template_name = 'goal_sessions/session_list.html'
    context_object_name = 'sessions'
    
    def get_queryset(self):
        return NSSession.objects.all()

class SessionDetailView(LoginRequiredMixin, DetailView):
    model = NSSession
    template_name = 'goal_sessions/session_detail.html'
    context_object_name = 'session'

class SessionCreateView(LoginRequiredMixin, CreateView):
    model = NSSession
    template_name = 'goal_sessions/session_form.html'
    fields = ['session_status', 'session_type', 'start_date', 'stop_date']
    success_url = reverse_lazy('session_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['session_types'] = SessionType.objects.all()
        context['session_statuses'] = SessionStatus.objects.all()
        return context
