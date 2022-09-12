from django.db import models


class PreviousPlaceWork(models.Model):
    """Предыдущее место работы"""
    ppw_id = models.AutoField(primary_key=True)
    ppw_title = models.CharField(unique=True, max_length=250, verbose_name='Название')
    ppw_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.ppw_title}"

    class Meta:
        verbose_name_plural = 'Предыдущие места работы'
        verbose_name = 'Предыдущее место работы'
        db_table = 'previous_place_work'
        ordering = ['ppw_title']


class DepartmentsRegionalLevel(models.Model):
    """ОВД на региональном уровне"""
    drl_id = models.AutoField(primary_key=True)
    drl_order_num = models.SmallIntegerField(blank=True, null=True, verbose_name='Порядок отображения')
    drl_title = models.CharField(unique=True, max_length=250, verbose_name='Название ОВД')
    drl_title_area = models.CharField(max_length=100, verbose_name='Название района',)
    fk_self_subordinate = models.ForeignKey('self', db_column='fk_self_subordinate', on_delete=models.SET_NULL, 
                                             blank=True, null=True, verbose_name='Входит в состав ОВД',
                                             help_text='Только для территориальных ОВД')
    drl_note = models.TextField(blank=True, verbose_name='Примечание')
    drl_url = models.SlugField(unique=True, verbose_name='Ссылка (url)', max_length=130, 
        help_text='Указать без пробелов и анг. буквами ссылку на службу (например: umvd_gorod)')

    def __str__(self):
        return f"{self.drl_title}"

    class Meta:
        verbose_name_plural = 'ОВД на региональном и районном уровне'
        verbose_name = 'ОВД на региональном и районном уровне'
        db_table = 'departments_regional_level'
        ordering = ['drl_order_num']


class Services(models.Model):
    """Службы ОВД"""
    s_id = models.AutoField(primary_key=True)
    s_title = models.CharField(unique=True, max_length=250, verbose_name='Служба ОВД')
    s_note = models.TextField(blank=True, verbose_name='Примечание')
    s_url = models.SlugField(unique=True, verbose_name='Ссылка (url)', max_length=130, 
        help_text='Указать без пробелов и анг. буквами ссылку на службу (например: ur)')

    def __str__(self):
        return f"{self.s_title}"

    class Meta:
        verbose_name_plural = 'Службы ОВД'
        verbose_name = 'Служба ОВД'
        db_table = 'services'


class Divisions(models.Model):
    """Подразделение"""
    d_id = models.AutoField(primary_key=True)
    d_title = models.CharField(unique=True, max_length=250, verbose_name='Подразделение ОВД')
    d_note = models.TextField(blank=True, verbose_name='Примечание')
    d_url = models.SlugField(unique=True, verbose_name='Ссылка (url)', max_length=130, 
        help_text='Указать без пробелов и анг. буквами ссылку на подразделение (например: obo_i_kpo)')

    def __str__(self):
        return f"{self.d_title}"

    class Meta:
        verbose_name_plural = 'Подразделения ОВД'
        verbose_name = 'Подразделение ОВД'
        db_table = 'divisions'


class DivisionsPersonnel(models.Model):
    """Подразделение Кадров, учитавющее кандидатов"""
    dp_id = models.AutoField(primary_key=True)
    dp_title = models.CharField(unique=True, max_length=250, verbose_name='Подразделение кадров')
    dp_note = models.TextField(blank=True, verbose_name='Примечание')
    dp_url = models.SlugField(unique=True, verbose_name='Ссылка (url)', max_length=130, 
        help_text='Указать без пробелов и анг. буквами ссылку на подразделение (например: kadri_obo_i_kpo)')

    def __str__(self):
        return f"{self.dp_title}"

    class Meta:
        verbose_name_plural = 'Подразделения кадров'
        verbose_name = 'Подразделение кадров'
        db_table = 'divisions_pesonnel'



class SourceOffer(models.Model):
    """Источник предложения по трудоустройства (комплектования)"""
    so_id = models.AutoField(primary_key=True)
    so_title = models.CharField(unique=True, max_length=250, verbose_name='Источник комплектования')
    so_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.so_title}"

    class Meta:
        verbose_name_plural = 'Источники комплектования'
        verbose_name = 'Источник комплектования'
        db_table = 'source_offer'


class Positions(models.Model):
    """Должности"""
    pos_id = models.AutoField(primary_key=True)
    pos_title = models.CharField(unique=True, max_length=100, verbose_name='Название должности')
    pos_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.pos_title}"

    class Meta:
        verbose_name_plural = 'Должности'
        verbose_name = 'Должность'
        db_table = 'positions'
        ordering = ['pos_title']


class ReasonsRefusalHire(models.Model):
    """Основания отказа в приеме на службу"""
    rrh_id = models.AutoField(primary_key=True)
    rrh_title = models.CharField(max_length=250, verbose_name='Основание отказа')
    rrh_details = models.CharField(blank=True, max_length=250, verbose_name='Подробное описание отказа')

    def __str__(self):
        return f"{self.rrh_title} ({self.rrh_details})"

    class Meta:
        verbose_name_plural = 'Основания отказа в приеме на службу'
        verbose_name = 'Основание отказа в приеме на службу'
        db_table = 'reasons_refusal_hire'
        ordering = ['rrh_title']


class Candidates(models.Model):
    """Кандидаты на трудоустройство"""
    C_CHOICES_GENDER = (('М', 'М'),
                        ('Ж', 'Ж'))
    C_CHOICES_TYPE_WORK = (('Аттестованный', 'Аттестованный'),
                            ('ФГГС', 'ФГГС'),
                            ('Вольный найм', 'Вольный найм'))
    C_CHOICES_AGE_GROUP = (('До 20 лет', 'До 20 лет'),
                            ('От 21 до 30 лет', 'От 21 до 30 лет'),
                            ('От 31 до 40 лет', 'От 31 до 40 лет'),
                            ('От 41 до 55 лет', 'От 41 до 55 лет'),
                            ('Старше 55 лет', 'Старше 55 лет'))
    C_CHOICES_TYPE_TITLE = (('Полиция', 'Полиция'),
                            ('Юстиция', 'Юстиция'),
                            ('Внутренняя служба', 'Внутренняя служба'))
    C_CHOICES_CATEGORIES_TITLE = (('Рядовой состав', 'Рядовой состав'),
                                  ('Младший начальствующий состав', 'Младший начальствующий состав'),
                                  ('Средний начальствующий состав', 'Средний начальствующий состав'),
                                  ('Cтарший начальствующий состав', 'Cтарший начальствующий состав'),
                                  ('Высший начальствующий состав', 'Высший начальствующий состав'))

    fk_divisions_personnel = models.ForeignKey('DivisionsPersonnel', db_column='fk_divisions_personnel', on_delete=models.SET_NULL,
                                     null=True, verbose_name='Подразделение кадров',
                                     related_name='fk_divisions_personnel_divisions_personnel_dp_title',
                                     help_text='Подразделение кадров, ответсвенное за учет кандидатов')
    c_id = models.AutoField(primary_key=True)
    c_surname = models.CharField(max_length=50, verbose_name='Фамилия')
    c_name = models.CharField(max_length=50, verbose_name='Имя')
    c_middle_name = models.CharField(blank=True, max_length=50, verbose_name='Отчество')
    c_birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    с_age_group = models.CharField(blank=True, max_length=50, choices=C_CHOICES_AGE_GROUP, verbose_name='Возрастная группа')
    с_gender = models.CharField(max_length=50, choices=C_CHOICES_GENDER, verbose_name='Пол')
    c_education = models.CharField(blank=True, max_length=250, verbose_name='Образование')
    fk_previous_place_work = models.ForeignKey('PreviousPlaceWork', db_column='fk_previous_place_work', on_delete=models.SET_NULL,
                                         blank=True, null=True, verbose_name='Предыдущее место работы')
    fk_source_offer = models.ForeignKey('SourceOffer', db_column='fk_source_offer', on_delete=models.SET_NULL,
                                         blank=True, null=True, verbose_name='Источник комплектования',
                                         help_text='Кто пригласил кандидата на службу')
    fk_dep_reg_lvl = models.ForeignKey(
        'DepartmentsRegionalLevel', db_column='fk_dep_reg_lvl', on_delete=models.SET_NULL, 
        blank=True, null=True, verbose_name='ОВД на рег. или рай. уровне',
        help_text='Из какого ОВД приглашен кандидат (поле заполняется, если "Источник комлектования" из системы МВД')
    fk_services = models.ForeignKey(
        'Services', db_column='fk_services', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Служба ОВД',
        help_text='Из какой службы приглашен кандидат (поле заполняется, если "Источник комлектования" из системы МВД')
    c_date_statement = models.DateField(verbose_name='Дата заявления')
    с_type_work = models.CharField(max_length=50, choices=C_CHOICES_TYPE_WORK, verbose_name='Планируемый вид работы')
    с_type_title = models.CharField(blank=True, max_length=50, choices=C_CHOICES_TYPE_TITLE, verbose_name='Планируемый вид спец. звания')
    с_categories_title = models.CharField(blank=True, max_length=50, choices=C_CHOICES_CATEGORIES_TITLE, 
                                          verbose_name='Планируемая категория должности')
    fk_position_planned = models.ForeignKey('Positions', db_column='fk_position_planned', on_delete=models.SET_NULL,
                                    blank=True, null=True, verbose_name='Планируемая должность',
                                    related_name='fk_position_planned_positions_pos_title',
                                    help_text='На какую должность кандидатом написано заявление (без указания отделов и отделений)')
    fk_services_planed = models.ForeignKey('Services', db_column='fk_services_planed', on_delete=models.SET_NULL,
                                     null=True, verbose_name='Планируемая служба ОВД',
                                     related_name='fk_services_planed_services_s_title',
                                     help_text='Какая службы выбрана кандидатом')
    fk_divisions_planed = models.ForeignKey('Divisions', db_column='fk_divisions_planed', on_delete=models.SET_NULL,
                                     blank=True, null=True, verbose_name='Планируемое подразделение ОВД',
                                     related_name='fk_divisions_planed_divisions_d_title',
                                     help_text='Какое подразделение выбрано кандидатом')
    fk_dep_reg_lvl_planed = models.ForeignKey('DepartmentsRegionalLevel', db_column='fk_dep_reg_lvl_planed', 
                                               on_delete=models.SET_NULL, null=True, 
                                               verbose_name='Планируемый ОВД на рег. или рай. уровне',
                                               related_name='fk_dep_reg_lvl_planed_departments_regional_level_drl_title',
                                               help_text='Какое ОВД выбрано кандидатом')
    c_date_medical_examination = models.DateField(blank=True, null=True, verbose_name='Дата назначения ВВК')
    c_date_psychological_test = models.DateField(blank=True, null=True, verbose_name='Дата назначения ЦПД',
                                                 help_text='Центр психологической диагностики')
    c_date_psychological_selection = models.DateField(blank=True, null=True, verbose_name='Дата назначения ППО',
                                                      help_text='Профессиональный психологический отбор')
    c_date_polygraph = models.DateField(blank=True, null=True, verbose_name='Дата назначения полиграфа')
    c_date_hire = models.DateField(blank=True, null=True, verbose_name='Дата приема на службу')
    fk_reason_refusal_hire = models.ForeignKey('ReasonsRefusalHire', db_column='fk_reason_refusal_hire', 
                                                on_delete=models.SET_NULL, blank=True, null=True, 
                                                verbose_name='Основание отказа')
    c_note = models.TextField(blank=True, verbose_name='Примечание')
    c_url = models.SlugField(unique=True, verbose_name='Ссылка (url)', max_length=130, 
        help_text='Указать без пробелов и анг. буквами ссылку на кандидата (например: ivanov).')

    def __str__(self):
        return f"{self.c_surname} {self.c_name} {self.c_middle_name}"

    class Meta:
        verbose_name_plural = 'Кандидаты'
        verbose_name = 'Кандидат'
        db_table = 'candidates'
        ordering = ['fk_dep_reg_lvl_planed', 'fk_services_planed']