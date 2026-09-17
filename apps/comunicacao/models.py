from django.db import models

class Avisos(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(null=True, blank=True)
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Eventos(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_evento = models.DateTimeField()
    local = models.CharField(max_length=255)
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Reunioes(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_reuniao = models.DateTimeField()
    local = models.CharField(max_length=255)
    participantes = models.IntegerField()
    status = models.CharField(max_length=50, choices=[('Agendada', 'Agendada'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')])
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Reclamacoes(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_reclamacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Aberta', 'Aberta'), ('Em andamento', 'Em andamento'), ('Resolvida', 'Resolvida')])
    escola = models.ForeignKey('usuarios.Escola', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo