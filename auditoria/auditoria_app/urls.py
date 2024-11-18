from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
import random
import string
compremento = ''.join(random.choices(((string.ascii_letters + string.digits + string.punctuation).replace('(', '').replace(')', '').replace('/', '').replace("'", "").replace('"', '')), k=(random.randint(1, 15))))

app_name='auditoria_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cads/', views.cads, name='cads'),
    path(f'{compremento}/', views.acessar, name='entra'),  
    path('entra/', views.acessar, name='entra'),  
    path('home/<int:valida>', views.home, name='home'),
    path('prontinho/', views.cadastrar, name='prontu'),
    path('problemas/<int:valida>', views.prob, name='problema_entra'),
    path('configuracao/<int:valida>', views.conf, name='conf_entra'),
    path('configuracao_img/<int:valida>', views.img, name='atu_img'),
    path('home_f/<int:valida>/<str:filtro>', views.home_filtro, name='home_filter'),
    path('info/<int:valida>/<str:pj>', views.info, name='info_usu'),
    path('auditoria/<int:valida>/<str:empresa>', views.auditoria_api, name='auditoria'),
    path('<int:valida>/<str:fim_data>/<str:ini_dada>/graf', views.exibir_graficos, name='graf'),
    path('<str:ini_data>/<str:fim_data>/donload', views.dowload_audi, name='download_pdf'),
    path('<int:valida>/<str:argumento>', views.contra, name='contra'),
    path('preview/', views.pre, name='pre'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)