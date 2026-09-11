from django.shortcuts import render


def financeiro(request):
    return render(request, 'financeiro/index.html')


def taxas(request):
    return render(request, 'financeiro/taxas.html')


def cobrancas(request):
    return render(request, 'financeiro/cobrancas.html')


def atrasos(request):
    return render(request, 'financeiro/atrasos.html')


def resumo(request):
    return render(request, 'financeiro/resumo.html')