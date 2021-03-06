from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
# Create your views here.

#def index(request):
#    return redirect('/agenda/')#um dos metodos para redirect



@login_required(login_url='/login/') # == se não estiver logado não acessa a agenda
def lista_eventos(request):
    usuario = request.user
    #usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   dataEvento__gt=data_atual)#filter usuario, aparece só os eventos da pessoa logada//se eu tirar filter e colocar all() mostra todos os eventos
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect(('/'))
        else:
            messages.error(request, 'Usuário ou senha inválido')
    return redirect('/')


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        dataEvento = request.POST.get('dataEvento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                       dataEvento=dataEvento,
                                                       descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,
                                  dataEvento=dataEvento,
                                  descricao=descricao,
                                  usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user#usa-se estas duas linhas para um usuario nao conseguir deletar o evento de outros usuarios
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404
    return redirect('/')


@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    # usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')  # filter usuario, aparece só os eventos da pessoa logada//se eu tirar filter e colocar all() mostra todos os eventos
    return JsonResponse(list(evento), safe=False)

