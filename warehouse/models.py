# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DevcieInfo(models.Model):
    device_name = models.CharField(max_length=40, blank=True, null=True)
    device_ip = models.CharField(max_length=30, blank=True, null=True)
    device_port = models.CharField(max_length=20, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True)
    commu_type = models.CharField(max_length=30, blank=True, null=True)
    commu_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devcie_info'


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


class OpcAddressTb(models.Model):
    serial_nbr = models.AutoField(primary_key=True)
    plc_no = models.CharField(max_length=10, blank=True, null=True)
    plc_node = models.CharField(max_length=20, blank=True, null=True)
    route_addr = models.CharField(db_column='route_Addr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    readflag_addr = models.CharField(db_column='readflag_Addr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    device_zone = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opc_address_tb'


class Rizhibiao(models.Model):
    id = models.IntegerField(primary_key=True)
    rizhileixing = models.CharField(max_length=20, blank=True, null=True)
    rizhiguanjianzi = models.CharField(max_length=20, blank=True, null=True)
    rizhibianhao = models.CharField(max_length=20, blank=True, null=True)
    rizhimingxi = models.CharField(max_length=20, blank=True, null=True)
    datatime = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rizhibiao'


class RouteNode(models.Model):
    serialno = models.CharField(db_column='serialNo', primary_key=True, max_length=20)  # Field name made lowercase.
    sourcenode = models.CharField(db_column='sourceNode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    destinnode = models.CharField(db_column='destinNode', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'route_node'


class SortScanNode(models.Model):
    serial_nbr = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=50, blank=True, null=True)
    device_zone = models.CharField(max_length=50, blank=True, null=True)
    scan_node = models.CharField(max_length=40, blank=True, null=True)
    scan_ip = models.CharField(max_length=40, blank=True, null=True)
    scan_port = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sortscannode'


class Ssx(models.Model):
    sbid = models.CharField(max_length=255, blank=True, null=True)
    sbmc = models.CharField(max_length=255, blank=True, null=True)
    zt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssx'


class Users(models.Model):
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    usersex = models.CharField(max_length=255, blank=True, null=True)
    userage = models.CharField(max_length=255, blank=True, null=True)
    authority = models.CharField(max_length=20, blank=True, null=True)
    creationtimes = models.CharField(max_length=20, blank=True, null=True)
    updatetimes = models.CharField(max_length=20, blank=True, null=True)
    states = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'users'
