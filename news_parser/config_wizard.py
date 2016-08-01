"""
Module for creating default configuration and accessing already created.

Methods:
    create_default(filename): creates default configuration with name = filename
    load_config(filename): loads configuration and returns it as a dict

"""



from configparser import ConfigParser

default_config = {
    'database_settings': {
        'DATABASE_ENGINE': 'django.db.backends.postgresql',
        'DATABASE_NAME': 'mydatabasename',
        'DATABASE_USER': 'myuser',
        'DATABASE_PASSWORD': 'mysecretpass',
        'DATABASE_HOST': '127.0.0.1',
        'DATABASE_PORT': '5432'
    },
    'debug_settings': {
        'DEBUG': 'True'
    },
    'lentaru_settings': {
        'RSS_URL': 'https://lenta.ru/rss/news'
    },
    'celery_settings': {
        'CELERY_BROKER_URL': 'amqp://',
        'CELERY_RESULT_BACKEND': 'rpc://',
        'CELERY_ACCEPT_CONTENT': "['json']",
        'CELERY_TASK_SERIALIZER': 'json',
        'CELERY_RESULT_SERIALIZER': 'json',
        'CELERY_TIMEZONE': 'Europe/Moscow'
    },
    'smtp_server_settings': {
        'SMTP_SERVER_URL': 'smtp.yandex.com',
        'SMTP_SERVER_USERNAME': 'myusername',
        'SMTP_SERVER_PASSWORD': 'mysecretpass',
        'SMTP_SERVER_PORT': '465',
        'SMTP_SENT_FROM': 'myusername@yandex.ru'
    }


}


def create_default(file_name='settings.ini'):

    config_generator = ConfigParser()

    for section, settings in default_config.items():
        config_generator.add_section(section)
        for option, value in settings.items():
            config_generator.set(section, option, value)

    with open(file_name, 'w') as config_file:
        config_generator.write(config_file)


def load_config(file_name='settings.ini'):
    config = ConfigParser()
    config.read(file_name)

    options = {}

    for section in config.sections():
        for option, value in config.items(section):
            options[option] = value
    return options
