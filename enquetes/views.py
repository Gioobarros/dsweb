from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Pergunta

# Create your views here.
def index (request):
     enquetes = Pergunta.objects.order_by('-data_pub')[:10]
     contexto = {'lista_enquetes': enquetes}
     return render(request, 'enquetes/index.html', contexto)

def detalhes (request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk = pergunta_id)
    contexto = {'enquete': pergunta}
    return render(request, 'enquetes/detalhes.html', contexto)

def votacao(request, pergunta_id):
    resultado = 'VOTAÇÃO da enquete de número %s'
    return HttpResponse (resultado % pergunta_id)

def resultado(request, pergunta_id):
    resultado = 'RESULTADO da enquete de número %s'
    return HttpResponse(resultado % pergunta_id)


