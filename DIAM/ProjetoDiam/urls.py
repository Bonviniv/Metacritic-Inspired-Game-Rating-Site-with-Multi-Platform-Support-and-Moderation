"""
URL configuration for ProjetoDiam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from site_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.paginaInicial, name='paginaInicial'),
    path('jogos', views.jogos, name="jogos"),
    path('site_app/reviews', views.reviews, name="reviews"),
    path('site_app/criticos/', views.criticos, name="criticos"),
    path('login', views.login_site, name='login_site'),
    path('registar', views.registar, name='registar'),
    path('jogo/<int:id>/', views.jogo, name='jogo'),
    path('paginaInicial', views.logout_view, name='logout_view'),
    path('<int:id>/', views.AdicionarReview, name='teste'),
    path('gravarJogo', views.gravarJogo, name='gravarJogo'),
    path('<int:review_id>/<int:id>/', views.avaliarReview, name='avaliarReview'),
    path('jogos/', views.jogos_view_filtrado, name="jogos_view_filtrado"),
    path('jogos/pesquisa', views.jogos_view_filtrado_pesquisar, name="jogos_view_filtrado_pesquisar"),
    path('reviews/pesquisa', views.review_view_filtrado, name="review_view_filtrado"),
    path('reviews/', views.review_view_filtrado_pesquisar, name="review_view_filtrado_pesquisar"),
    path('perfil', views.perfil, name='perfil'),
    path('perfil/', views.upload_profilepic, name='upload_profilepic'),
    path('reviews/perfil', views.review_view_filtrado_perfil, name="review_view_filtrado_perfil"),
    path('jogo/apagado/<int:idreview>', views.apagar_review, name="apagar_review"),
    path('paginaInicial/<int:jogoid>', views.deletarJogo, name='deletarJogo'),
    path('editarJogo/<int:jogoid>', views.editarJogo, name='editarJogo'),

]
