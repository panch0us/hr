from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Candidates, Services, DepartmentsRegionalLevel, DivisionsPersonnel
import datetime


class MainView(LoginRequiredMixin, ListView):
    template_name = 'candidate/main.html'
    queryset = Candidates.objects.all()
    context_object_name = 'candidates'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/accounts/login/'


class AnalyticsView(LoginRequiredMixin, ListView):
    """Аналитическая справка по кандидатам"""
    model = Candidates
    template_name = 'candidate/analytics.html'
    queryset = Candidates.objects.all()
    context_object_name = 'candidates'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/accounts/login/'
    # Вспомогательные переменные
    current_year = int(datetime.datetime.now().year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # -- БЛОК КАНДИДАТОВ
        # ---- кандидаты
        context['can_all'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)
        # ---- принятые на службу
        context['can_hire_all'] = Candidates.objects.filter(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)
        # ---- непринятые на службу
        context['can_refusal_all'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)
        # -- БЛОК "ПЛАНИРУЕМЫЕ СЛУЖБЫ КАНДИДАТОВ
        # ---- кандидаты
        context['can_in_ser'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True).values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(cnt=Count('c_id')).order_by('fk_services_planed__s_title')
        # ---- принятые на службу
        context['can_in_ser_hire'] = Candidates.objects.filter(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True).values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(cnt=Count('c_id')).order_by('fk_services_planed__s_title')
        # ---- непринятые на службу
        context['can_in_ser_refusal'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False).values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(cnt=Count('c_id')).order_by('fk_services_planed__s_title')
        # ---- КАНДИДАТЫ С ГРУППИРОВКОЙ
        # ---- ОВД
        context['can_group_ovd'] = Candidates.objects.all().order_by('fk_dep_reg_lvl_planed__drl_order_num').values('fk_dep_reg_lvl_planed__drl_title', 'fk_dep_reg_lvl_planed__drl_url').annotate(can=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)), can_hire=Count('c_id', filter=Q(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)), can_refusal=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)))
        # ---- службы
        context['can_group_ser'] = Candidates.objects.all().order_by('fk_services_planed__s_title').values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(can=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)), can_hire=Count('c_id', filter=Q(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)), can_refusal=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)))
        # ---- подразделения
        context['can_group_div'] = Candidates.objects.all().order_by('fk_divisions_planed__d_title').values('fk_divisions_planed__d_title', 'fk_divisions_planed__d_url').annotate(can=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)), can_hire=Count('c_id', filter=Q(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)), can_refusal=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)))
        # ---- подразделения с отдельными кадрами
        context['can_group_div_kadri'] = Candidates.objects.all().order_by('fk_divisions_personnel').values('fk_divisions_personnel__dp_title', 'fk_divisions_personnel__dp_url').annotate(can=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)), can_hire=Count('c_id', filter=Q(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)), can_refusal=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)))
        return context


class FilterAnalyticsView(LoginRequiredMixin, ListView):
    """Кандидаты после фильтра, выбранного пользователем по дате"""
    model = Candidates
    template_name = 'candidate/analytics.html'
    queryset = Candidates.objects.all()
    context_object_name = 'candidates'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        # Получаем даты от запроса пользователя

        date_begin = self.request.GET.get("begin")
        date_end = self.request.GET.get("end")

        context = super().get_context_data(**kwargs)
        # -- БЛОК КАНДИДАТОВ
        # -- кандидаты
        context['can_all'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True, c_date_statement__gte=date_begin, c_date_statement__lte=date_end)
        # -- принятые на службу
        context['can_hire_all'] = Candidates.objects.filter(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True, c_date_statement__gte=date_begin, c_date_statement__lte=date_end)
        # -- непринятые на службу
        context['can_refusal_all'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False, c_date_statement__gte=date_begin, c_date_statement__lte=date_end)
        # -- БЛОК Планируемые службы кандидатов 
        # -- кандидаты
        context['can_in_ser'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True, c_date_statement__gte=date_begin, c_date_statement__lte=date_end).values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(cnt=Count('c_id'))
        # -- принятые на службу
        context['can_in_ser_hire'] = Candidates.objects.filter(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True, c_date_statement__gte=date_begin, c_date_statement__lte=date_end).values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(cnt=Count('c_id'))
        # -- непринятые на службу
        context['can_in_ser_refusal'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False, c_date_statement__gte=date_begin, c_date_statement__lte=date_end).values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(cnt=Count('c_id'))
        # -- КАНДИДАТЫ С ГРУППИРОВКОЙ
        # -- ОВД
        context['can_group_ovd'] = Candidates.objects.filter(c_date_statement__gte=date_begin, c_date_statement__lte=date_end).order_by('fk_dep_reg_lvl_planed__drl_order_num').values('fk_dep_reg_lvl_planed__drl_title', 'fk_dep_reg_lvl_planed__drl_url', ).annotate(can=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)), can_hire=Count('c_id', filter=Q(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)), can_refusal=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)))
        # -- Службы
        context['can_group_ser'] = Candidates.objects.filter(c_date_statement__gte=date_begin, c_date_statement__lte=date_end).order_by('fk_services_planed__s_title').values('fk_services_planed__s_title', 'fk_services_planed__s_url').annotate(can=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)), can_hire=Count('c_id', filter=Q(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)), can_refusal=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)))
        # ---- подразделения с отдельными кадрами
        context['can_group_div_kadri'] = Candidates.objects.filter(c_date_statement__gte=date_begin, c_date_statement__lte=date_end).order_by('fk_divisions_personnel').values('fk_divisions_personnel__dp_title', 'fk_divisions_personnel__dp_url').annotate(can=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True)), can_hire=Count('c_id', filter=Q(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True)), can_refusal=Count('c_id', filter=Q(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False)))
        return context


class CandidatesDetailView(LoginRequiredMixin, DetailView):
    """Ссылка на Кандидата"""
    model = Candidates
    slug_field = "c_url"
    login_url = '/accounts/login/'


class DepartmentsDetailView(LoginRequiredMixin, DetailView):
    """Ссылка на ОВД на региональном уровне"""
    model = DepartmentsRegionalLevel
    slug_field = "drl_url"
    template_name = 'candidate/departments_detail.html'
    login_url = '/accounts/login/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущий ОВД (object берется из контекста модели DepartmentsRegionalLevel)
        context['my_obj'] = self.object
        # -- кандидаты
        context['candidates'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True, fk_dep_reg_lvl_planed__drl_title=context['my_obj'])
        # -- принятые на службу
        context['can_in_dep_hire'] = Candidates.objects.filter(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True, fk_dep_reg_lvl_planed__drl_title=context['my_obj'])
        # -- непринятые на службу
        context['can_in_dep_refusal'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False, fk_dep_reg_lvl_planed__drl_title=context['my_obj'])
        return context


class DivisionsPersonnelDetailView(LoginRequiredMixin, DetailView):
    """Ссылка на подразделение с отдельными кадрами"""
    model = DivisionsPersonnel
    slug_field = "dp_url"
    template_name = 'candidate/divisions_personnel_detail.html'
    login_url = '/accounts/login/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущее подразделение с отдельными картами (object берется из контекста модели DivisionsPersonnel)
        context['my_obj'] = self.object
        # -- кандидаты
        context['candidates'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True, fk_divisions_personnel__dp_title=context['my_obj'])
        # -- принятые на службу
        context['can_in_dep_hire'] = Candidates.objects.filter(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True, fk_divisions_personnel__dp_title=context['my_obj'])
        # -- непринятые на службу
        context['can_in_dep_refusal'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False, fk_divisions_personnel__dp_title=context['my_obj'])
        return context


class ServicesDetailView(LoginRequiredMixin, DetailView):
    """Ссылка на Службу"""
    model = Services
    slug_field = "s_url"
    login_url = '/accounts/login/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущую службу (object берется из контекста модели Services)
        context['my_obj'] = self.object
        # -- кандидаты
        context['candidates'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=True, fk_services_planed__s_title=context['my_obj'])
                # -- кандидаты
        context['can_in_ser_hire'] = Candidates.objects.filter(c_date_hire__isnull=False, fk_reason_refusal_hire__isnull=True, fk_services_planed__s_title=context['my_obj'])
                # -- кандидаты
        context['can_in_ser_refusal'] = Candidates.objects.filter(c_date_hire__isnull=True, fk_reason_refusal_hire__isnull=False, fk_services_planed__s_title=context['my_obj'])
        return context