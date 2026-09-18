import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='funcao',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='usuarios',
                to='usuarios.funcao',
            ),
        ),
    ]
