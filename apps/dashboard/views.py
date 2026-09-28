from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F, Q
from django.utils import timezone

from apps.academico.models import Exames, Frequencia, Notas
from apps.cadastros.models import Disciplinas, Estudantes, Professores, Turmas

@login_required
def dashboard(request):
    perfil = getattr(request.user, 'perfil', None)
    escola = perfil.escola if perfil else None
    estudantes = Estudantes.objects.filter(escola=escola) if escola else Estudantes.objects.none()
    professores = Professores.objects.filter(escola=escola) if escola else Professores.objects.none()
    turmas_escola = Turmas.objects.filter(escola=escola) if escola else Turmas.objects.none()
    disciplinas = Disciplinas.objects.filter(escola=escola) if escola else Disciplinas.objects.none()
    frequencias = Frequencia.objects.filter(escola=escola) if escola else Frequencia.objects.none()
    notas = Notas.objects.filter(escola=escola) if escola else Notas.objects.none()
    turmas_base = Turmas.objects.none()
    turnos = []
    turmas = Turmas.objects.none()
    busca = request.GET.get('q', '').strip()
    turno_selecionado = request.GET.get('turno', '').strip()

    if escola or request.user.is_superuser:
        if escola:
            turmas_base = Turmas.objects.filter(
                escola=escola,
                professor__escola=escola,
                professor__disciplina__escola=escola,
            )
            estudantes_da_turma = Q(estudantes__escola=escola)
            estudantes_na_busca = Q(estudantes__nome__icontains=busca, estudantes__escola=escola)
        else:
            turmas_base = Turmas.objects.all()
            turmas_escola = turmas_base
            estudantes_da_turma = Q(estudantes__escola=F('escola'))
            estudantes_na_busca = Q(estudantes__nome__icontains=busca, estudantes__escola=F('escola'))

        turnos = turmas_base.values('turno').annotate(
            total=Count('id_turmas')
        ).order_by('turno')
        turmas = turmas_base.annotate(
            estudantes_count=Count(
                'estudantes',
                filter=estudantes_da_turma,
                distinct=True,
            )
        ).select_related('professor', 'professor__disciplina')

        if turno_selecionado:
            turmas = turmas.filter(turno=turno_selecionado)
        if busca:
            turmas = turmas.filter(
                Q(serie__icontains=busca)
                | Q(turno__icontains=busca)
                | Q(sala__icontains=busca)
                | Q(professor__nome__icontains=busca)
                | Q(professor__disciplina__nome__icontains=busca)
                | estudantes_na_busca
            ).distinct()

        turmas = turmas.order_by('serie', 'turno', 'sala')

    total_frequencias = frequencias.count()
    presencas = frequencias.filter(presente=True).count()
    frequencia_media = (presencas / total_frequencias * 100) if total_frequencias else None

    contexto = {
        'escola': escola,
        'total_estudantes': estudantes.count(),
        'estudantes_ativos': estudantes.filter(status='Ativo').count(),
        'professores_ativos': professores.filter(status='Ativo').count(),
        'total_turmas': turmas_escola.count(),
        'disciplinas_ativas': disciplinas.filter(status='Ativa').count(),
        'frequencia_media': frequencia_media,
        'media_notas': notas.aggregate(media=Avg('media'))['media'],
        'proximos_exames': Exames.objects.filter(
            escola=escola,
            data__gte=timezone.localdate(),
        ).select_related('disciplina', 'turma', 'professor').order_by('data')[:5] if escola else Exames.objects.none(),
        'estudantes_recentes': estudantes.select_related('turma').order_by('-id_estudantes')[:5],
        'turmas': turmas,
        'turnos': turnos,
        'busca': busca,
        'turno_selecionado': turno_selecionado,
        'turmas_encontradas': turmas.count(),
        'total_turmas_escola': turmas_base.count(),
    }

    return render(request, 'dashboard/dashboard.html', contexto)