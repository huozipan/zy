from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from zhenghou.models import RawInfo,Wenxian,Position,Descript,GroundFact,OrigZZ
import shelve

# Create your views here.
# {{{ Wenxian 
class WenxianCreate(CreateView):
  model = Wenxian
  fields = '__all__'
  success_url = reverse_lazy('wx_list')

class WenxianView(ListView):
  model = Wenxian
  
# }}}
import jieba
import jieba.posseg as pseg

#from .models import GroundFact
#
g_dicts = shelve.open('rawinput')
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
  g_error = 0
  g_errstr = ''
  
  def get_form_kwargs(self):
    kwargs = super(RawInfo,self).get_form_kwargs()
    if 'data' in kwargs:
      if kwargs['data']['level'] == '1':
        myPost = kwargs['data'].copy()
        message = myPost['content']
        words = pseg.cut(message)
        tmp_str = []
        for word,flag in words:
          if flag == 'x':
            continue
          if word in g_dicts:
            tmp_str.append("#"+word)
          else:
            tmp_str.append(word)

        myPost['modified'] = "\n".join(tmp_str)
        myPost['level'] = '2'
        kwargs['data'] = myPost
      else:
#        b1 = Position(id=1,name='test1')
#        b1.save()
#        import pprint as pp
#        pp.pprint(b1.id)

        myDetail = kwargs['data']['modified']
        myList = myDetail.split("\n")
        for item in myList:
#          if item == '' or item[:1] == '#':
          item = item.strip()
          inJieba = 1
          v = item
          vJieba = ''
          vOrder = 0
          if item == '':
            continue
          elif item[:1] == '#':
            k = item[1:]
            v = g_dicts[k]
            inJieba = 0
            # if key in g_dict, then only continue, because already in db
            continue
          elif item[:1] == ';':
            v = item[1:]
            inJieba = 0
          elif item[:1] == '*':
            k = item[1:].split('*')
            v = k[1]
            vJieba = k[0]
          elif item[:1] == '^':
            v = item[1:]
            vOrder = 1
          else:
            pass

          ll = v.split('|')
          for l in ll:
            d = l.split(':')
            kl=[]
            vl=[]
            if len(d) == 1:
              kl = [d[0][:1]]
              vl = [d[0][1:]]
            elif len(d) != 2:
              self.g_error = 1
              self.g_errstr = "[%s] is a wrong format, should x:y|w,z:k,c..." %(v)
              break
            else:
              if vOrder == 1:
                vJieba = d[0]+d[1]
                kl = d[1].split(',')
                vl = d[0].split(',')
              else:
                kl = d[0].split(',')
                vl = d[1].split(',')
            for k1 in kl:
              for v1 in vl:
                tmp1 = k1+v1
                if vJieba != '':
                  tmp1 = vJieba
                if tmp1 in g_dicts:
                  continue
                else:
                  b = OrigZZ(name=tmp1, position=k1, descript=v1)
                  b.save()

                  tmp2 = {}
                  tmp2['pos'] = k1
                  tmp2['desc'] = v1
                  g_dicts[tmp1] = tmp2

                  jieba.add_word(tmp1,freq=1000,tag='n')


          if self.g_error == 1:
            break

          if inJieba == 1:
            pass



    return kwargs

  def form_valid(self, form):
    if form.cleaned_data.get('level') == 1:
      form.cleaned_data['level'] = 2
    else:
      pass

    if self.g_error == 1:
      form.add_error(None, self.g_errstr)
#    kw1 = self.get_form_kwargs()
#    import pprint as pp
#    pp.pprint(kw1)
#    return super(RawInfo, self).form_valid(form)
    return self.render_to_response(self.get_context_data(form=form))
