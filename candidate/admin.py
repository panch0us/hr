from django.contrib import admin
from django.db.models import Q

from .models import DepartmentsRegionalLevel, Services, SourceOffer, Positions, ReasonsRefusalHire, Candidates, PreviousPlaceWork, Divisions, DivisionsPersonnel

admin.site.site_url = '/candidate'

class PreviousPlaceWorkAdmin(admin.ModelAdmin):
    """Предыдущее место работы"""
    list_display = ('ppw_title', 'ppw_note',)
    list_display_links = ('ppw_title', 'ppw_note',)
    search_fields = ('ppw_title', 'ppw_note',)


class DepartmentsRegionalLevelAdmin(admin.ModelAdmin):
    """Территориальный ОВД на районном уровне"""
    list_display = ('drl_title', 'drl_title_area', 'fk_self_subordinate', 'drl_note',)
    list_display_links = ('drl_title', 'drl_title_area', 'fk_self_subordinate', 'drl_note',)
    search_fields = ('drl_title', 'drl_title_area',)


class ServicesAdmin(admin.ModelAdmin):
    """Службы ОВД"""
    list_display = ('s_title', 's_note')
    list_display_links = ('s_title', 's_note',)
    search_fields = ('s_title',)


class DivisionsAdmin(admin.ModelAdmin):
    """Подразделения ОВД"""
    list_display = ('d_title', 'd_note')
    list_display_links = ('d_title', 'd_note',)
    search_fields = ('d_title',)


class DivisionsPersonnelAdmin(admin.ModelAdmin):
    """Подразделения Кадров"""
    list_display = ('dp_title', 'dp_note')
    list_display_links = ('dp_title', 'dp_note',)
    search_fields = ('dp_title',)


class SourceOfferAdmin(admin.ModelAdmin):
    """Источник предложения по трудоустройства (комплектования)"""
    list_display = ('so_title','so_note',)
    list_display_links = ('so_title', 'so_note',)
    search_fields = ('so_title', 'so_note',)


class PositionsAdmin(admin.ModelAdmin):
    """Должности"""
    list_display = ('pos_title', 'pos_note',)
    list_display_links = ('pos_title', 'pos_note',)
    search_fields = ('pos_title', 'pos_note',)


class ReasonsRefusalHireAdmin(admin.ModelAdmin):
    """Основания отказа в приеме на службу"""
    list_display = ('rrh_title', 'rrh_details',)
    list_display_links = ('rrh_title', 'rrh_details',)
    search_fields = ('rrh_title', 'rrh_details',)


class CandidatesAdmin(admin.ModelAdmin):
    """Кандидаты"""
    list_display = ('fk_dep_reg_lvl_planed', 'fk_services_planed', 'c_surname', 'c_date_hire', 'fk_reason_refusal_hire', 'fk_divisions_personnel')
    list_display_links = ('fk_dep_reg_lvl_planed', 'fk_services_planed', 'c_surname', 'c_date_hire', 'fk_reason_refusal_hire')
    search_fields = ('c_surname', 'c_name',)
    #fieldsets = ("Сведения о кандидате", {"fields": (("c_surname", "c_name"),)}),


    def get_queryset(self, request):
        qs = super(CandidatesAdmin, self).get_queryset(request)
        # Если текущий пользователь суперюзер возвращаем всё:
        if request.user.is_superuser:
            return qs
        # Если текущий пользователь принадлежит к определенной группе:
        if request.user.groups.filter(name='УМВД России по г.Брянску').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='УМВД России по г.Брянску') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП-1') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП-2') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП-3'))
        if request.user.groups.filter(name='МО МВД России "Брянский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Брянский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Сельцо"'))
        if request.user.groups.filter(name='МО МВД России "Дятьковский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Дятьковский"'))
        if request.user.groups.filter(name='МО МВД России "Жуковский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Жуковский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Клетнянское"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Дубровское"') |
                Q(fk_dep_reg_lvl_planed__drl_title='ПП "Рогнединский"'))
        if request.user.groups.filter(name='ОМВД России по Карачевскому району').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='ОМВД России по Карачевскому району'))
        if request.user.groups.filter(name='МО МВД России "Клинцовский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Клинцовский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Гордеевское"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Красногорское"'))
        if request.user.groups.filter(name='МО МВД России "Навлинский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Навлинский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП "Брасовский"'))
        if request.user.groups.filter(name='МО МВД России "Новозыбковский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Новозыбковский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП "Климовский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Злынковское"'))
        if request.user.groups.filter(name='МО МВД России "Почепский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Почепский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП "Выгоничский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ПП "Жирятинский"'))
        if request.user.groups.filter(name='МО МВД России "Севский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Севский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Комаричское"'))
        if request.user.groups.filter(name='МО МВД России "Стародубский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Стародубский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП "Погарский"'))
        if request.user.groups.filter(name='МО МВД России "Трубчевский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Трубчевский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Суземское"'))
        if request.user.groups.filter(name='МО МВД России "Унечский"').exists():
            return qs.filter(
                Q(fk_dep_reg_lvl_planed__drl_title='МО МВД России "Унечский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='ОП "Суражский"') | 
                Q(fk_dep_reg_lvl_planed__drl_title='Отд.П "Мглинское"'))
        if request.user.groups.filter(name='ОБ ППСП УМВД России по г.Брянску').exists():
            return qs.filter(
                Q(fk_services_planed__s_title='ППСП') & 
                Q(fk_dep_reg_lvl_planed__drl_title='УМВД России по г.Брянску'))
        if request.user.groups.filter(name='МСЧ МВД России по Брянской области').exists():
            return qs.filter(
                Q(fk_services_planed__s_title='МСЧ'))
        if request.user.groups.filter(name='ОБ ДПС УМВД России по Брянской области').exists():
            return qs.filter(
                Q(fk_services_planed__s_title='ДПС') & 
                Q(fk_dep_reg_lvl_planed__drl_title='УМВД России по Брянской области'))
        if request.user.groups.filter(name='ОБ ДПС УМВД России по г.Брянску').exists():
            return qs.filter(
                Q(fk_services_planed__s_title='ДПС') & 
                Q(fk_dep_reg_lvl_planed__drl_title='УМВД России по г.Брянску'))
        if request.user.groups.filter(name='ОБО и КПО УМВД России по Брянской области').exists():
            return qs.filter(
                Q(fk_services_planed__s_title='ОБО и КПО'))
        if request.user.groups.filter(name='СУ УМВД России по Брянской области').exists():
            return qs.filter(
                Q(fk_services_planed__s_title='Следствие'))
        if request.user.groups.filter(name='ФКУ "ЦХ и СО УМВД России по Брянской области"').exists():
            return qs.filter(
                Q(fk_divisions_planed__d_title='ФКУ "ЦХ и СО УМВД"'))
        return qs


admin.site.register(PreviousPlaceWork, PreviousPlaceWorkAdmin)
admin.site.register(DepartmentsRegionalLevel, DepartmentsRegionalLevelAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(SourceOffer, SourceOfferAdmin)
admin.site.register(Positions, PositionsAdmin)
admin.site.register(ReasonsRefusalHire, ReasonsRefusalHireAdmin)
admin.site.register(Candidates, CandidatesAdmin)
admin.site.register(Divisions, DivisionsAdmin)
admin.site.register(DivisionsPersonnel, DivisionsPersonnelAdmin)