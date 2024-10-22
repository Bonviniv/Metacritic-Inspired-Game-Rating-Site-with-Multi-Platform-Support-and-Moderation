from django.db import models

# Create your models here.


import django
from django.db import models
from django.utils import timezone
from six import string_types
import datetime
from django.contrib.auth.models import User


class Utilizador(models.Model):
    # Atributos

    # user - user do django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # nome - primeiro e ultimo nome
    nome = models.CharField(max_length=100)
    # email - email do utilizador
    email = models.CharField(max_length=50)
    # data de nascimento
    data_nascimento = models.DateField(blank=True)
    # empresa - só para critico
    empresa = models.CharField(max_length=50)
    # numero de reviews - para os dois
    numero_reviews = models.IntegerField(default=0)
    # flag - critico ou não
    is_cristico = models.BooleanField(default=False)
    # imageurl - imagem do utilizador
    imageurl = models.URLField(null=True)



class Jogo(models.Model):
    # Atributos

    # Nome - nome do jogo
    nome = models.CharField(max_length=100)
    # empresa - empresa que fez
    empresa = models.CharField(max_length=50)
    # genero - genero do jogo
    genero = models.CharField(max_length=20)
    # plataformas - lista das plataformas disponiveis; Não acham que seria melhor uma class
    # descrição
    descricao = models.CharField(max_length=500)
    # data de lançamento - data de lançamento
    data_lancamento = models.DateField(blank=True)
    # data de inserção - data em que o jogo foi postado no site
    pub_data = models.DateTimeField(default=django.utils.timezone.now)
    # rating_c - critico
    rating_c = models.DecimalField(max_digits=5, decimal_places=1)
    # rating_u - utilizadores
    rating_u = models.DecimalField(max_digits=5, decimal_places=1)

    video_trailler = models.URLField()

    imagem_jogo = models.URLField()


class Plataforma(models.Model):
    nome = models.CharField(max_length=50)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)


class Rating(models.Model):
    # Atributos
    # plataforma
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    # Jogos - jogo associado ao rating
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    # rating_c - critico
    rating_c = models.DecimalField(max_digits=5, decimal_places=1)
    # rating_u - utilizadores
    rating_u = models.DecimalField(max_digits=5, decimal_places=1)


class Review(models.Model):
    # Atributo

    # user - django
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Jogo
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    # Rating
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE)
    # review - texto
    review = models.CharField(max_length=500)
    # data da review
    pub_data = models.DateTimeField(default=django.utils.timezone.now)
    # Like_c - critico
    like_c = models.IntegerField(default=0)
    # Like_u - utilizador
    like_u = models.IntegerField(default=0)


#fiz pra que cada like ou deslike tenha um user e uma review associada
#pra q um user só de um like por review
#e pra que a pessoa não possa dar like e deslike

class AvaliacaoReview(models.Model):
    # user - django
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # review
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # flag - like ou deslike
    is_like = models.BooleanField(default=True)