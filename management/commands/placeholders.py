# -------------------- #
# urls.py file section #
# -------------------- #


URL_IMPORTS = """
from django.conf.urls.defaults import *
from models import *
from views import *

urlpatterns = patterns('',
"""

URL_CRUD_CONFIG = """
    (r'%(model)s/create/$', create_%(model)s),
    (r'%(model)s/list/$', list_%(model)s ),
    (r'%(model)s/edit/(?P<id>[^/]+)/$', edit_%(model)s),
    (r'%(model)s/view/(?P<id>[^/]+)/$', view_%(model)s),
    """ 

URL_END = """
)
"""



# --------------------- #
# forms.py file section #
# --------------------- #

FORMS_IMPORTS = """
from django import forms
from models import *

"""

FORMS_MODELFORM_CONFIG = """

class %(modelClass)sForm(forms.ModelForm):
	
    class Meta:
        model = %(modelClass)s	
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(%(modelClass)sForm, self).__init__(*args, **kwargs)

"""		





# --------------------- #
# views.py file section #
# --------------------- #

VIEWS_IMPORTS = """
# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator

# app specific files

from models import *
from forms import *
"""

VIEWS_CREATE = """

def create_%(model)s(request):
    form = %(modelClass)sForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = %(modelClass)sForm()

    t = get_template('%(app)s/create_%(model)s.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

"""

VIEWS_LIST = """

def list_%(model)s(request):
  
    list_items = %(modelClass)s.objects.all()
    paginator = Paginator(list_items ,20)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list_items = paginator.page(paginator.num_pages)

    t = get_template('%(app)s/list_%(model)s.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

"""


VIEWS_UPDATE = """
def edit_%(model)s(request, id):

    %(model)s_instance = %(modelClass)s.objects.get(id=id)

    form = %(modelClass)sForm(request.POST or None, instance = %(model)s_instance)

    if form.is_valid():
        form.save()

    t=get_template('%(app)s/edit_%(model)s.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""

VIEWS_VIEW = """

def view_%(model)s(request, id):
    %(model)s_instance = %(modelClass)s.objects.get(id = id)

    t=get_template('%(app)s/view_%(model)s.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""


TEMPLATES_CREATE = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Create {%% endblock %%}

{%% block heading %%}  %(modelClass)s - Create  {%% endblock %%}
{%% block content %%} 
<table>
<form action="" method="POST"> {%% csrf_token %%}
  {{form}}
  <tr>
    <td colspan="2" align="right"><input type="submit" value="Create"/></td>
  </tr>
</form>
</table>
{%% endblock %%}
"""

TEMPLATES_LIST = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - List {%% endblock %%}

{%% block heading %%}  %(modelClass)s - List  {%% endblock %%}
{%% block content %%} 
<table>
{%% for item in list_items.object_list %%}
  <tr><td>{{forloop.counter}}</td><td> {{item}} </td></tr>
{%% endfor %%}
</table>

{%% if list_items.has_previous %%}
    <a href="?page={{ list_items.previous_page_number }}">Previous</a>
{%% endif %%}

<span class="current">
    Page {{ list_items.number }} of {{ list_items.paginator.num_pages }}.
</span>

{%% if list_items.has_next %%}
        <a href="?page={{ list_items.next_page_number }}">Previous</a>
{%% endif %%}

{%% endblock %%}
"""


TEMPLATES_EDIT = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Edit {%% endblock %%}

{%% block heading %%}  %(modelClass)s - Edit  {%% endblock %%}
{%% block content %%} 
<table>
<form action="" method="POST"> {%% csrf_token %%}
  {{form}}
  <tr>
    <td colspan="2" align="right"><input type="submit" value="Save"/></td>
  </tr>
</form>
</table>
{%% endblock %%}
"""

TEMPLATES_VIEW = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - View {%% endblock %%}

{%% block heading %%}  %(modelClass)s - View  {%% endblock %%}
{%% block content %%} 
<table>
{{ %(model)s_instance }}
</table>
{%% endblock %%}
"""

TEMPLATES_BASE = """
{%% block title %%} 
{%% endblock %%}

{%% block heading %%}  
{%% endblock %%}

{%% block content %%} 


{%% endblock %%}
"""

