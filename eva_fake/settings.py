# coding=utf-8
import rados
import configparser
import os


conf = configparser.SafeConfigParser()
conf.read('/etc/eva_fake/eva_fake.conf')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '=c!-f(jh$t_o5xa6^p*a31fid^nsx5@^$#u&%od(a+_i^r#1_7'

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = (
    'eva_fake.migrations',
)

MIDDLEWARE_CLASSES = (
)

ROOT_URLCONF = 'eva_fake.urls'

WSGI_APPLICATION = 'eva_fake.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': conf.get('db', 'name'),
        'USER': conf.get('db', 'user'),
        'PASSWORD': conf.get('db', 'password'),
        'HOST': conf.get('db', 'host'),
        'PORT': conf.get('db', 'port'),
    },
}


LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = False

USE_L10N = False

USE_TZ = False

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


TASKS_COUNT = conf.has_option('common', 'task_count') and conf.get('common', 'task_count') or 1
CEPH_CHUNK_SIZE = conf.has_option('common', 'ceph_chunk_size') and conf.getint('common', 'ceph_chunk_size') or 16777216
UPLOAD_IMAGE_TIMEOUT = conf.has_option('common', 'upload_image_timeout') and conf.getint('common', 'upload_image_timeout') or 600

if conf.has_option('common', 'default_timeout'):
    DEFAULT_TIME_OUT = conf.getint('common', 'default_timeout') or 10800
else:
    DEFAULT_TIME_OUT = 600

DEFAULT_DISK_FORMAT = conf.get('common', 'default_disk_format')
DEFAULT_CONTAINER_FORMAT = conf.get('common', 'default_container_fromat')

# 任务完成，是否删除导入镜像
COMPLETED_DEST_IMAGE_DELETE = conf.getboolean('common', 'completed_dest_image_delete')

CLUSTERS = {
    'src': {
        'ceph_conf_path': str(conf.get('src_cluster', 'ceph_conf_path')),
        'auth_url': conf.get('src_cluster', 'auth_url'),
        'default_auth_name': conf.get('src_cluster', 'default_auth_name'),
        'default_auth_password': conf.get('src_cluster', 'default_auth_password'),
    },
    'dest': {
        'ceph_conf_path': str(conf.get('dest_cluster', 'ceph_conf_path')),
        'auth_url': conf.get('dest_cluster', 'auth_url'),
        'default_auth_name': conf.get('dest_cluster', 'default_auth_name'),
        'default_auth_password': conf.get('dest_cluster', 'default_auth_password'),
        'network_id': conf.get('dest_cluster', 'network_id').split(','),
        'floating_network_id': conf.get('dest_cluster', 'floating_network_id'),
        'glance_host': conf.has_option('dest_cluster', 'glance_host') and conf.get('dest_cluster', 'glance_host') or None
    }
}


if CLUSTERS['src']['ceph_conf_path']:
    cluster = rados.Rados(conffile=CLUSTERS['src']['ceph_conf_path'])
    cluster.connect(timeout=5)
    cluster.shutdown()
if CLUSTERS['dest']['ceph_conf_path']:
    cluster = rados.Rados(conffile=CLUSTERS['dest']['ceph_conf_path'])
    cluster.connect(timeout=5)
    cluster.shutdown()


log_path = conf.get('common', 'log_path')
if not os.path.exists(log_path):
    dir_path, file_path = os.path.split(log_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s -- %(message)s'
        },
     },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': log_path,
            'formatter': 'verbose',
            'interval': 1,
            'backupCount': 365,
            'when': 'midnight',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}