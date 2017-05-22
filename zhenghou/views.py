from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from zhenghou.models import RawInfo,Wenxian

# Create your views here.
class WenxianCreate(CreateView):
  model = Wenxian
  fields = '__all__'
  success_url = reverse_lazy('wx_list')

class WenxianView(ListView):
  model = Wenxian
  
#import jieba
import jieba.posseg as pseg

#from .models import GroundFact
#
g_dicts = {}
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

class RawInfo(CreateView):
  model = RawInfo
  fields = '__all__'
  
  def get_form_kwargs(self):
    kwargs = super(RawInfo,self).get_form_kwargs()
    if 'data' in kwargs:
      myPost = kwargs['data'].copy()
      message = myPost['content']
      words = pseg.cut(message)
      tmp_str = []
      for word,flag in words:
        if flag == 'x':
          continue
        if word in g_dicts:
          tmp_str.append(":"+word)
        else:
          tmp_str.append(word)

      myPost['modified'] = "\n".join(tmp_str)
      myPost['level'] = 2
      kwargs['data'] = myPost

    return kwargs

  def form_valid(self, form):
#    kw1 = self.get_form_kwargs()
#    import pprint as pp
#    pp.pprint(kw1)
#    return super(RawInfo, self).form_valid(form)
    return self.render_to_response(self.get_context_data(form=form))
