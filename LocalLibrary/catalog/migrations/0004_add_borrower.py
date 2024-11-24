from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_bookinstance_id_alter_bookinstance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name=''
                 'borrower',
            field=models.ForeignKey(null=True, blank=True, on_delete=models.SET_NULL, to='auth.User'),
        ),
    ]
