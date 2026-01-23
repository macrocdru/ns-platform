from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import GoalsBacklog, GoalType, GoalResultType

class GoalListView(LoginRequiredMixin, ListView):
    model = GoalsBacklog
    template_name = 'goals/goal_list.html'
    context_object_name = 'goals'
    
    def get_queryset(self):
        return GoalsBacklog.objects.filter(nsuser=self.request.user)

class GoalDetailView(LoginRequiredMixin, DetailView):
    model = GoalsBacklog
    template_name = 'goals/goal_detail.html'
    context_object_name = 'goal'
    
    def get_queryset(self):
        return GoalsBacklog.objects.filter(nsuser=self.request.user)

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = GoalsBacklog
    template_name = 'goals/goal_form.html'
    fields = ['goal_type', 'goal_result_type', 'goal_name', 'goal_reason', 'visibleforothers', 'priority_weight']
    success_url = reverse_lazy('goal_list')
    
    def form_valid(self, form):
        form.instance.nsuser = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal_types'] = GoalType.objects.all()
        context['result_types'] = GoalResultType.objects.all()
        return context
