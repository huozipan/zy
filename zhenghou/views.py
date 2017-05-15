from django.shortcuts import render
from django.views.generic.edit import CreateView
from zhenghou.models import InfoInput

# Create your views here.
import jieba
import jieba.posseg as pseg

#from .models import GroundFact
#
#g_dicts = {}
#
#for e in GroundFact.objects.all():
#  jieba.add_word(e.name)
#  g_dicts[e.name] = ':'+e.name
#
#for e in ZhengHou.objects.all():
#  jieba.add_word(e.name)
#  g_dicts[e.name] = ':'+e.name


from .forms import ZhengHouForm
def zhenghou(request):
  if request.method == 'POST':
    form = ZhengHouForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['zh_name']
      message = form.cleaned_data['zh_message']
      result = form.cleaned_data['zh_result']
      i = form.cleaned_data['zh_is']

      words = pseg.cut(message)
      tmp_str = ''
      for word,flag in words:
        if flag == 'x':
          continue
        if word in g_dicts:
          tmp_str = ("%s:%s\n" %(tmp_str, word))
        else:
          tmp_str = ("%s%s\n" %(tmp_str, word))

      if i==False:
        newDict = {
            'zh_name':name,
            'zh_message': message,
            'zh_result': tmp_str
            }
        newForm = ZhengHouForm(newDict)
        print(newForm)
        return render(request, 'zhenghou.html', {'form': newForm})
    pass
  else:
    form = ZhengHouForm()

  return render(request, 'zhenghou.html', {'form': form})

class RawInput(CreateView):
  model = InputInfo
  
  def form_valid(self, form):
    return super(RawInput, self).form_valid(form)
