from django.apps import AppConfig
import jieba


class ZhenghouConfig(AppConfig):
    name = 'zhenghou'

    def ready(self):
      jieba.load_userdict('/etc/zy.conf')
