from django.db import models


class Professores(models.Model):
    id_professores = models.AutoField(primary_key=True)
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.PROTECT, related_name='professores')
    matricula = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    formacao = models.CharField(max_length=100)
    disciplina = models.ForeignKey('Disciplinas', on_delete=models.PROTECT, related_name='professores')
    carga_horaria = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Ativo')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['escola', 'matricula'], name='unique_matricula_por_escola')
        ]

    def __str__(self):
        return self.nome


class Disciplinas(models.Model):
    id_disciplinas = models.AutoField(primary_key=True)
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.PROTECT, related_name='disciplinas')
    codigo = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    carga_horaria = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Ativa')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['escola', 'codigo'], name='unique_codigo_por_escola')
        ]

    def __str__(self):
        return self.nome


class Turmas(models.Model):
    id_turmas = models.AutoField(primary_key=True)
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.PROTECT, related_name='turmas')
    serie = models.CharField(max_length=15)
    turno = models.CharField(max_length=15)
    sala = models.CharField(max_length=15)
    professor = models.ForeignKey(Professores, on_delete=models.PROTECT, related_name='turmas')

    def __str__(self):
        return f"{self.serie} - {self.turno}"


class Estudantes(models.Model):
    id_estudantes = models.AutoField(primary_key=True)
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.PROTECT, related_name='estudantes')
    matricula = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turmas, on_delete=models.CASCADE, related_name='estudantes')
    data_nascimento = models.DateField()
    responsavel = models.ForeignKey('Responsaveis', on_delete=models.PROTECT, related_name='estudantes')
    telefone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='Ativo')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['escola', 'matricula'], name='unique_matricula_estudante_por_escola')
        ]

    def __str__(self):
        return self.nome


class Responsaveis(models.Model):
    id_responsaveis = models.AutoField(primary_key=True)
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.PROTECT, related_name='responsaveis')
    cpf = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['escola', 'cpf'], name='unique_cpf_por_escola')
        ]

    def __str__(self):
        return self.nome