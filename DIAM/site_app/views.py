from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from site_app.models import Jogo


# Create your views here.

def check_admin(user):
    return user.is_superuser;

def check_logged(request):
    return request.is_authenticated;

def login_site(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('paginaInicial'))
        else:
            return render(request, 'login.html', {'error_message': "Credenciais inválidas!!"})

    return render(request, 'login.html')

@user_passes_test(check_logged, login_url='/login')
def logout_view(request):
    logout(request)
    print("Logged out")
    return render(request, 'paginaInicial.html')
    ##return HttpResponseRedirect(reverse('paginaInicial'))


def registar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        data_nascimento = request.POST.get('dataNascimento')
        empresa = request.POST.get('empresa')
        is_cristico = request.POST.get('opcao')
        flag = False

        if is_cristico == "sim":
            flag = True

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email)
            utilizador = Utilizador.objects.create(user=user, nome=username, email=email,
                                                   data_nascimento=data_nascimento, empresa=empresa, is_cristico=flag)
            utilizador.save()

        else:
            return render(request, 'registar.html', {'error_message': "Nome do utilizador inválido!"})

        return HttpResponseRedirect(reverse('login_site'))

    return render(request, 'registar.html')

@user_passes_test(check_logged, login_url='/login')
def perfil(request):

    print("ola")
    if request.user.is_authenticated:
        likes_c = 0
        likes_u = 0
        reviews = 0
        lista_reviews = Review.objects.filter(user=request.user)
        for review in lista_reviews:
            likes_c = likes_c + review.like_c
            likes_u = likes_u + review.like_u
            reviews = reviews + 1

        utilizador = Utilizador.objects.get(user=request.user)

        return render(request, 'perfil.html',
                          {'utilizador': utilizador, 'likes_u': likes_u, 'likes_c': likes_c,
                           'reviews': reviews})


    return HttpResponseRedirect(reverse('login_site'))


@user_passes_test(check_admin, login_url='login')
def deletarJogo(request, jogoid):
    jogo = Jogo(id=jogoid)
    lista_reviews = Review.objects.filter(jogo=jogoid)
    lista_rating = Rating.objects.filter(jogo=jogoid)
    lista_plataformas = Plataforma.objects.filter(jogo=jogoid)

    for rating in lista_rating:
        rating.delete()
    for review in lista_reviews:
        review.delete()
    for plataforma in lista_plataformas:
        plataforma.delete()

    jogo.delete()
    return render(request, 'paginaInicial.html')


@user_passes_test(check_admin, login_url='/login')
def editarJogo(request, jogoid):
    jogo = Jogo.objects.get(id=jogoid)

    nome = request.POST.get('nome')
    empresa = request.POST.get('empresa')
    genero = request.POST.get('genero')
    descricao = request.POST.get('descricao')
    data_lancamento = request.POST.get('dataLancamento')
    plataforma = request.POST.getlist('opcao')
    video_trailler = request.POST.get('video')

    if data_lancamento:
        jogo.data_lancamento = data_lancamento
        jogo.save()

    if descricao:
        jogo.descricao = descricao
        jogo.save()

    jogo.nome = nome
    jogo.empresa = empresa
    jogo.genero = genero
    jogo.plataforma = plataforma
    jogo.video_trailler = video_trailler

    jogo.save()

    return redirect('jogo', jogoid)


def paginaInicial(request):
    lista_jogos = Jogo.objects.all()
    lista_reviews = Review.objects.all()
    lista_reviews = lista_reviews.order_by('-like_u')[:3]

    context = {'lista_reviews': lista_reviews, 'lista_jogos': lista_jogos}
    return render(request, 'paginaInicial.html', context)


def jogos(request):
    is_admin = False
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        is_admin = user.is_superuser
    list = []
    generos = Jogo.objects.all()
    for g in generos:
        if not list.__contains__(g.genero):
            list.append(g.genero)

    lista_jogos = Jogo.objects.all()
    return render(request, 'jogos.html', {'lista_jogos': lista_jogos, 'is_admin': is_admin, 'gens': list})


def jogo(request, id):
    reviewss = []
    reviews_u = []
    reviews_c = []
    game = Jogo.objects.get(id=id)
    for review in Review.objects.all():
        if id == review.jogo.id:
            reviewss.append(review)

    for review in reviewss:
        if review.user.utilizador.is_cristico:
            reviews_c.append(review)
        else:
            reviews_u.append(review)

    lista_plataformas = Plataforma.objects.filter(jogo_id=id)
    if User.objects.filter(pk=request.user.id).exists():
        user = User.objects.get(pk=request.user.id)
        is_admin = user.is_superuser
        print("Funcionaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    else:
        is_admin = False

    return render(request, 'jogo.html', {'game': game, 'reviews_u': reviews_u, 'reviews_c': reviews_c,
                                         'lista_plataformas': lista_plataformas, 'is_admin': is_admin})


def reviews(request):
    revs = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': revs})


def criticos(request):
    return render(request, 'critico.html')




@user_passes_test(check_admin, login_url='login')
def gravarJogo(request):
    print("acontece!!!!")
    if request.method == 'POST':
        print("acontece!!!!")
        nome = request.POST.get('nome')
        empresa = request.POST.get('empresa')
        genero = request.POST.get('genero')
        descricao = request.POST.get('descricao')
        data_lancamento = request.POST.get('dataLancamento')
        plataforma = request.POST.getlist('opcao')
        video_trailler = request.POST.get('video')
        myfile = request.FILES['imagem']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        print("Acontece isso -> ", descricao)

        jogo = Jogo(nome=nome, empresa=empresa, genero=genero, descricao=descricao, data_lancamento=data_lancamento,
                    rating_c=0, rating_u=0, video_trailler=video_trailler, imagem_jogo=uploaded_file_url)
        jogo.save()

        for plat in plataforma:
            Plataforma(jogo_id=jogo.id, nome=plat).save()
            print(plat)

    return redirect('jogos')

@user_passes_test(check_logged, login_url='/login')
def AdicionarReview(request, id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        selec_plataorma = request.POST.get('plataforma')
        review_text = request.POST.get('review')
        # print("Rating:", rating)
        # print("plataforma:", selec_plataorma)
        utilizador = Utilizador.objects.get(user=request.user)
        plataforma = Plataforma.objects.get(jogo_id=id, nome=selec_plataorma)
        rating_list = Rating.objects.filter(jogo_id=id, plataforma_id=plataforma.id)

        count = 0
        for r in rating_list:
            if Review.objects.filter(user_id=request.user.id, rating_id=r.id).exists():
                count += 1

        if count > 0:
            return redirect('jogo', id=id)

        if utilizador.is_cristico:
            new_rating = Rating.objects.create(rating_c=rating, rating_u=0.0, jogo_id=id, plataforma_id=plataforma.id)
            new_rating.save()
        else:
            new_rating = Rating.objects.create(rating_c=0.0, rating_u=rating, jogo_id=id, plataforma_id=plataforma.id)
            new_rating.save()

        new_review = Review.objects.create(review=review_text, like_c=0, like_u=0,
                                           jogo=Jogo.objects.get(id=id), rating=new_rating, user=request.user)
        new_review.save()
        recalcular_ratings(id)

    return redirect('jogo', id=id)


def recalcular_ratings(id):
    jogo = Jogo.objects.get(pk=id)
    lista_ratings = Rating.objects.filter(jogo=jogo)
    contador_u = 0
    contador_c = 0
    rating_u = 0
    rating_c = 0
    for r in lista_ratings:
        if r.rating_u == 0:
            rating_c += r.rating_c
            contador_c += 1
        if r.rating_c == 0:
            rating_u += r.rating_u
            contador_u += 1

    if contador_u != 0:
        jogo.rating_u = rating_u / contador_u
    else:
        jogo.rating_u = 0

    if contador_c != 0:
        jogo.rating_c = rating_c / contador_c
    else:
        jogo.rating_c = 0

    jogo.save()

@user_passes_test(check_logged, login_url='/login')
def avaliarReview(request, review_id, id):
    review = Review.objects.get(pk=review_id)
    utilizador = Utilizador.objects.get(pk=request.user.utilizador.id)
    has_existing_evaluation = AvaliacaoReview.objects.filter(user=request.user.id, review=review_id).exists()
    if not has_existing_evaluation:
        if utilizador.is_cristico:
            review.like_c += 1
        else:
            review.like_u += 1
        AvaliacaoReview.objects.create(user=request.user, review=review, is_like=True).save()
        review.save()
    else:
        if utilizador.is_cristico:
            review.like_c -= 1
        else:
            review.like_u -= 1
        avaliacao_review = AvaliacaoReview.objects.get(user=request.user.id, review=review_id)
        avaliacao_review.delete()
        review.save()

    return redirect('jogo', id=id)


def jogos_view_filtrado(request):
    min_year = request.POST.get('min_year')
    max_year = request.POST.get('max_year')
    plataformas = request.POST.getlist('opcao')
    generos = request.POST.getlist('opcaoG')
    lista_plataforma = Plataforma.objects.all()
    lista_jogos = Jogo.objects.all()
    lista_resultados = Jogo.objects.all()

    if (plataformas):
        for p in lista_plataforma:
            lista_resultados = lista_resultados.exclude(pk=p.jogo_id)
        for p in lista_plataforma:
            if p.nome in plataformas:
                lista_resultados = lista_jogos.filter(
                    pk__in=[p.jogo_id for p in lista_plataforma if p.nome in plataformas])

    if (min_year and max_year):
        for jogo in lista_resultados:
            if int(jogo.data_lancamento.year) < int(min_year):
                lista_resultados = lista_resultados.exclude(pk=jogo.pk)
            else:
                if int(jogo.data_lancamento.year) > int(max_year):
                    lista_resultados = lista_resultados.exclude(pk=jogo.pk)

    if (generos):
        for jogo in lista_resultados:
            print(jogo.genero)
            if jogo.genero not in generos:
                lista_resultados = lista_resultados.exclude(pk=jogo.pk)

    context = {'lista_jogos': lista_resultados}

    return render(request, 'jogos.html', context)


def jogos_view_filtrado_pesquisar(request):
    pesquisar = request.POST.get('pesquisar')
    for jogo in Jogo.objects.all():
        print(jogo.nome)
    if pesquisar:
        print(pesquisar)
        print("ola")
        lista_jogos = Jogo.objects.filter(nome__icontains=pesquisar)
    else:
        lista_jogos = Jogo.objects.all()

    context = {'lista_jogos': lista_jogos}

    return render(request, 'jogos.html', context)

@user_passes_test(check_logged, login_url='/login')
def review_view_filtrado_perfil(request):
    pesquisar = request.user.utilizador.nome

    if pesquisar:
            lista_review = Review.objects.filter(user__utilizador__nome=pesquisar)
            if not lista_review:
                lista_review = Review.objects.all()

    else:
        lista_review = Review.objects.all()

    context = {'reviews': lista_review}

    return render(request, 'reviews.html', context)

def review_view_filtrado_pesquisar(request):
    pesquisar = request.POST.get('pesquisar')

    if pesquisar:
        print(pesquisar)
        print("ola")
        lista_review = Review.objects.filter(jogo__nome__icontains=pesquisar)
        if not lista_review:
            lista_review = Review.objects.filter(user__utilizador__nome__icontains=pesquisar)
            if not lista_review:
                lista_review = Review.objects.all()

    else:
        lista_review = Review.objects.all()

    context = {'reviews': lista_review}

    return render(request, 'reviews.html', context)


def review_view_filtrado(request):
    min_year = request.POST.get('min_year')
    max_year = request.POST.get('max_year')
    plataformas = request.POST.getlist('opcao')
    generos = request.POST.getlist('opcaoG')
    tipoUser = request.POST.getlist('opcaoU')
    lista_plataforma = Plataforma.objects.all()
    lista_reviews = Review.objects.all()
    lista_resultados = Review.objects.all()
    ratingu = request.POST.get('ratingU')
    ratingc = request.POST.get('ratingC')

    if plataformas:
        for plataforma in lista_plataforma:
            if plataforma.nome not in plataformas:
                lista_plataforma = lista_plataforma.exclude(pk=plataforma.pk)

        for review in lista_resultados:
            if review.rating.plataforma not in lista_plataforma:
                lista_resultados = lista_resultados.exclude(pk=review.pk)

    if min_year and max_year:
        for review in lista_resultados:
            print(review.pub_data.year)
            if int(review.pub_data.year) < int(min_year):
                lista_resultados = lista_resultados.exclude(pk=review.pk)
            else:
                if int(review.pub_data.year) > int(max_year):
                    lista_resultados = lista_resultados.exclude(pk=review.pk)

    if generos:
        for review in lista_resultados:
            print(review.jogo.genero)
            if review.jogo.genero not in generos:
                lista_resultados = lista_resultados.exclude(pk=review.pk)

    if tipoUser:
        for review in lista_resultados:
            print(review.user.utilizador.is_cristico)
            if "user" not in tipoUser and not review.user.utilizador.is_cristico:
                lista_resultados = lista_resultados.exclude(pk=review.pk)
            if "critico" not in tipoUser and review.user.utilizador.is_cristico:
                lista_resultados = lista_resultados.exclude(pk=review.pk)

    ratingc_decimal = float(ratingc)
    ratingu_decimal = float(ratingu)

    if ratingu_decimal == 5.0 and ratingc_decimal == 5.0:
        pass
    else:
        for review in lista_resultados:
            if ratingu_decimal > review.jogo.rating_u:
                lista_resultados = lista_resultados.exclude(pk=review.pk)
            else:
                if ratingc_decimal > review.jogo.rating_c:
                    lista_resultados = lista_resultados.exclude(pk=review.pk)

    context = {'reviews': lista_resultados}

    return render(request, 'reviews.html', context)

@user_passes_test(check_logged, login_url='/login')
def upload_profilepic(request):

    utilizador = Utilizador.objects.get(user=request.user)

    myfile = request.FILES['user-image']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    print("Acontece isso -> ", uploaded_file_url)

    utilizador.imageurl = uploaded_file_url
    utilizador.save()

    imgurl = uploaded_file_url

    return render(request, 'perfil.html', {'utilizador': utilizador, 'imgurl': imgurl})

@user_passes_test(check_logged, login_url='/login')
def apagar_review(request, idreview):
    review = Review.objects.get(id=idreview)
    reting =Rating.objects.get(id=review.rating.id)
    idJogo=review.jogo_id
    review.delete()
    reting.delete()
    recalcular_ratings(idJogo)

    return redirect('jogo', id=idJogo)