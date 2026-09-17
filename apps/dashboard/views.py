from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.utils import timezone

from apps.academico.models import Exames, Frequencia, Notas
from apps.cadastros.models import Disciplinas, Estudantes, Professores, Turmas

@login_required
def dashboard(request):
    perfil = getattr(request.user, 'perfil', None)
    escola = perfil.escola if perfil else None
    estudantes = Estudantes.objects.filter(escola=escola) if escola else Estudantes.objects.none()
    professores = Professores.objects.filter(escola=escola) if escola else Professores.objects.none()
    turmas = Turmas.objects.filter(escola=escola) if escola else Turmas.objects.none()
    disciplinas = Disciplinas.objects.filter(escola=escola) if escola else Disciplinas.objects.none()
    frequencias = Frequencia.objects.filter(escola=escola) if escola else Frequencia.objects.none()
    notas = Notas.objects.filter(escola=escola) if escola else Notas.objects.none()

    total_frequencias = frequencias.count()
    presencas = frequencias.filter(presente=True).count()
    frequencia_media = (presencas / total_frequencias * 100) if total_frequencias else None

    contexto = {
        'escola': escola,
        'total_estudantes': estudantes.count(),
        'estudantes_ativos': estudantes.filter(status='Ativo').count(),
        'professores_ativos': professores.filter(status='Ativo').count(),
        'total_turmas': turmas.count(),
        'disciplinas_ativas': disciplinas.filter(status='Ativa').count(),
        'frequencia_media': frequencia_media,
        'media_notas': notas.aggregate(media=Avg('media'))['media'],
        'proximos_exames': Exames.objects.filter(
            escola=escola,
            data__gte=timezone.localdate(),
        ).select_related('disciplina', 'turma', 'professor').order_by('data')[:5] if escola else Exames.objects.none(),
        'estudantes_recentes': estudantes.select_related('turma').order_by('-id_estudantes')[:5],
    }

    return render(request, 'dashboard/dashboard.html', contexto)