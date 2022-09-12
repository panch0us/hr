
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Для веб сервера Apache (изаначально название было static_apache - но когда сделал staticcollection - удалил старую статику и переименовал,
# возможно не верно...)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_urls')

# Просто для проекта
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# Указывается откуда будем собирать статические файлы
STATICFILES_DIRS = [STATIC_DIR]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# После авторизации - перенаправляет не страницу приложения, а не профиля
LOGIN_REDIRECT_URL = '/candidate'
ADMIN_SITE_HEADER = 'Администрирование УРЛС'

# уникальное имя для куки необходимо для того, чтобы при переходе между проектами не требовало заново проходить ауентификацию
SESSION_COOKIE_NAME = 'urls__session_cookie'

