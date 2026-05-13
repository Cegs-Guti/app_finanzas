from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.PositiveSmallIntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')])),
                ('anio', models.PositiveIntegerField(verbose_name='Año')),
                ('saldo_inicial', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='auth.user')),
            ],
            options={
                'verbose_name': 'Balance',
                'verbose_name_plural': 'Balances',
                'ordering': ['-anio', '-mes'],
                'unique_together': {('usuario', 'mes', 'anio')},
            },
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')], max_length=10)),
                ('categoria', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=300)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacciones', to='finanzas_app.balance')),
            ],
            options={
                'ordering': ['-creado'],
            },
        ),
    ]
