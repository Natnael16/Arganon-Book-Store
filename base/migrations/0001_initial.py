
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('oldprice', models.FloatField()),
                ('pages', models.IntegerField()),
                ('description', models.TextField()),
                ('about_author', models.TextField(blank=True, null=True)),
                ('image_front', models.ImageField(default='yebrhan_enat.jpg', null=True, upload_to='')),
                ('image_back', models.ImageField(default='yebrhan_enat.jpg', null=True, upload_to='')),
                ('new_book', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('popularity', models.IntegerField(blank=True, default=0, null=True)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Equb',
            fields=[
                ('type', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('amount', models.FloatField(default=220)),
                ('currentRound', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Equbtegna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unpaid_month', models.IntegerField(default=0)),
                ('equb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.equb')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(error_messages={'unique': 'በዚህ ስልክቁጥር የተመዘገበ ደንበኛ አለ!'}, max_length=13, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('is_equbtegna', models.BooleanField(default=False)),
                ('chat_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('author', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014)], default=2014)),
                ('month', models.CharField(choices=[('መስከረም', 'መስከረም'), ('ጥቅምት', 'ጥቅምት'), ('ህዳር', 'ህዳር'), ('ታህሳስ', 'ታህሳስ'), ('ጥር', 'ጥር'), ('የካቲት', 'የካቲት'), ('መጋቢት', 'መጋቢት'), ('ሚያዚያ', 'ሚያዚያ'), ('ግንቦት', 'ግንቦት'), ('ሰኔ', 'ሰኔ'), ('ሐምሌ', 'ሐምሌ'), ('ነሐሴ', 'ነሐሴ')], default='መስከረም', max_length=200)),
                ('round', models.IntegerField(default=0)),
                ('equbtegna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.equbtegna')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('አስተያየት', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', to='base.book')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.member')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('discount', models.FloatField()),
                ('price', models.FloatField()),
                ('amount', models.IntegerField(default=0)),
                ('description', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),

            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.member')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.packages')),
            ],
        ),
        migrations.CreateModel(
            name='OrderBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.member')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('delivery', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('sold', models.BooleanField(default=False)),
    ],
        ),
        migrations.CreateModel(
            name='EqubtegnaDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.FloatField()),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014)], default=2014)),
                ('month', models.CharField(choices=[('መስከረም', 'መስከረም'), ('ጥቅምት', 'ጥቅምት'), ('ህዳር', 'ህዳር'), ('ታህሳስ', 'ታህሳስ'), ('ጥር', 'ጥር'), ('የካቲት', 'የካቲት'), ('መጋቢት', 'መጋቢት'), ('ሚያዚያ', 'ሚያዚያ'), ('ግንቦት', 'ግንቦት'), ('ሰኔ', 'ሰኔ'), ('ሐምሌ', 'ሐምሌ'), ('ነሐሴ', 'ነሐሴ')], default='መስከረም', max_length=200)),
                ('equbtegna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.equbtegna')),
            ],
        ),
        migrations.AddField(
            model_name='equbtegna',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.member'),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
 ),
    ]
