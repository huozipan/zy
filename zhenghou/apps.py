from django.apps import AppConfig
import jieba


class ZhenghouConfig(AppConfig):
    name = 'zhenghou'

    def ready(self):
      jieba.load_userdict('/etc/zy.conf')
      import shelve
      g = shelve.open('rawinput')
      gl = list(g.keys())
      for k in gl:
        jieba.add_word(k)
      g.close()
