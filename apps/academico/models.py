from django.db import models


class Horarios(models.Model):
    dia_semana = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    turma = models.ForeignKey(
        'cadastros.Turmas',
        on_delete=models.CASCADE
    )

    disciplina = models.ForeignKey(
        'cadastros.Disciplinas',
        on_delete=models.PROTECT
    )

    professor = models.ForeignKey(
        'cadastros.Professores',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return (
            f"{self.dia_semana} - "
            f"{self.hora_inicio} às {self.hora_fim} - "
            f"{self.turma} - "
            f"{self.disciplina} - "
            f"{self.professor}"
        )


class Frequencia(models.Model):
    estudante = models.ForeignKey(
        'cadastros.Estudantes',
        on_delete=models.CASCADE,
        related_name='frequencias'
    )

    data = models.DateField()

    presente = models.BooleanField(default=False)
    falta = models.BooleanField(default=False)
    atraso = models.BooleanField(default=False)

    def __str__(self):
        situacao = 'Presente' if self.presente else 'Ausente'
        return f"{self.estudante} - {self.data} - {situacao}"


class Exames(models.Model):
    data = models.DateField()

    disciplina = models.ForeignKey(
        'cadastros.Disciplinas',
        on_delete=models.PROTECT
    )

    turma = models.ForeignKey(
        'cadastros.Turmas',
        on_delete=models.CASCADE
    )

    professor = models.ForeignKey(
        'cadastros.Professores',
        on_delete=models.PROTECT
    )

    tipo = models.CharField(max_length=50)

    status = models.CharField(
        max_length=20,
        default='Agendado'
    )

    def __str__(self):
        return (
            f"{self.disciplina} - "
            f"{self.turma} - "
            f"{self.data} - "
            f"{self.tipo}"
        )


class Notas(models.Model):

    id_notas = models.AutoField(primary_key=True)

    estudante = models.ForeignKey(
        'cadastros.Estudantes',
        on_delete=models.PROTECT,
        related_name='notas'
    )

    disciplina = models.ForeignKey(
        'cadastros.Disciplinas',
        on_delete=models.PROTECT,
        related_name='notas'
    )

    bimestre = models.PositiveSmallIntegerField(
        choices=[
            (1, '1º Bimestre'),
            (2, '2º Bimestre'),
            (3, '3º Bimestre'),
            (4, '4º Bimestre'),
        ]
    )

    tipo_avaliacao = models.CharField(
        max_length=50
    )

    nota_1 = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )

    nota_2 = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )

    nota_3 = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )

    media = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )

    situacao = models.CharField(
        max_length=20,
        choices=[
            ('APROVADO', 'Aprovado'),
            ('RECUPERACAO', 'Recuperação'),
            ('REPROVADO', 'Reprovado'),
        ],
        default='RECUPERACAO'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'estudante',
                    'disciplina',
                    'bimestre',
                    'tipo_avaliacao'
                ],
                name='nota_unica_por_avaliacao'
            )
        ]

    def __str__(self):
        return (
            f"{self.estudante} - "
            f"{self.disciplina} - "
            f"{self.get_bimestre_display()} - "
            f"{self.tipo_avaliacao}"
        )