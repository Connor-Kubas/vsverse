from django.db import models
import uuid
from authentication.models import User

class Affiliations(models.Model):
    id = models.IntegerField(primary_key=True)
    affiliation = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'affiliations'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)



class Data(models.Model):
    uuid = models.CharField(primary_key=True, max_length=36, blank=True, null=False)
    title = models.CharField(max_length=40, blank=True, null=True)
    version = models.CharField(max_length=60, blank=True, null=True)
    card_number = models.CharField(max_length=10, blank=True, null=True)
    rarity = models.CharField(max_length=1, blank=True, null=True)
    rules = models.CharField(max_length=570, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    attack = models.IntegerField(blank=True, null=True)
    defense = models.IntegerField(blank=True, null=True)
    affiliation = models.CharField(max_length=40, blank=True, null=True)
    mutant = models.CharField(max_length=30, blank=True, null=True)
    flight = models.IntegerField(blank=True, null=True)
    range = models.IntegerField(blank=True, null=True)
    visible = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data'


class Cards(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    power = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    attack = models.IntegerField(blank=True, null=True)
    defense = models.IntegerField(blank=True, null=True)
    affiliation = models.CharField(max_length=40, blank=True, null=True)
    mutant = models.CharField(max_length=30, blank=True, null=True)
    flight = models.CharField(max_length=10, blank=True, null=True)
    range = models.CharField(max_length=10, blank=True, null=True)
    visible = models.CharField(max_length=20, blank=True, null=True)

    # card_image = models.ForeignKey(CardImages, on_delete=models.CASCADE)
    def image_url(self):
        data = Data.objects.filter(title=self.title, version=self.version).first()

        return '/static/images/cards_low_res/'+data.uuid+'.jpg'

    class Meta:
        managed = False
        db_table = 'cards'

class CardImages(models.Model):
    # card_id = models.ForeignKey(Cards, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50, blank=True, null=True)
    image_type = models.CharField(max_length=4, blank=True, null=True)

    card = models.OneToOneField(Cards, on_delete=models.CASCADE, related_name='card_image')

    class Meta:
        managed = False
        db_table = 'card_images'

class Decks(models.Model):
    id = models.AutoField(primary_key=True)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=36)
    title = models.CharField(max_length=30, blank=True, null=True)
    main_card = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'decks'        

class DeckCards(models.Model):
    deck = models.ForeignKey(Decks, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    id = models.AutoField(primary_key=True)

    card = models.ForeignKey(Cards, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'deck_cards'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Expansions(models.Model):
    id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=3, blank=True, null=True)
    expansion = models.CharField(max_length=50, blank=True, null=True)
    year_date = models.CharField(max_length=25, blank=True, null=True)
    number_of_cards = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expansions'

