from django.db import models

class Professores(models.Model):
    id_professores = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    formacao = models.CharField(max_length=100)
    disciplina = models.CharField(max_length=100)
    carga_horaria = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Ativo')

    def __str__(self):
        return self.nome

class Turmas(models.Model):
    id_turmas = models.AutoField(primary_key=True)
    serie = models.CharField(max_length=15)
    turno = models.CharField(max_length=15)
    sala = models.CharField(max_length=15)
    professor = models.ForeignKey(Professores, on_delete=models.PROTECT, related_name='turmas')

    def __str__(self):
        return f"{self.serie} - {self.turno}"

class Estudantes(models.Model):
    id_estudantes = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turmas, on_delete=models.CASCADE, related_name='estudantes')
    data_nascimento = models.DateField()
    responsavel = models.ForeignKey('Responsaveis', on_delete=models.PROTECT, related_name='estudantes')
    telefone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='Ativo')

    def __str__(self):
        return self.nome

class Responsaveis(models.Model):
    id_responsaveis = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nome