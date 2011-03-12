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
from django.core.urlresolvers import reverse

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
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
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


# ------------------------- #
# templates.py file section #
# ------------------------- #



TEMPLATES_CREATE = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Create {%% endblock %%}

{%% block heading %%}<h1>  %(modelClass)s - Create </h1>  {%% endblock %%}
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

{%% block title %%} <h1> %(modelClass)s </h1><h2> List </h2> {%% endblock %%}

{%% block heading %%} 
<h1> %(modelClass)s</h1>
<h2> List Records</h2>
{%% endblock %%}
{%% block content %%} 

<table>
<thead>
<tr><th>Record</th><th colspan="3">Actions</th></tr>
{%% for item in list_items.object_list %%}
  <tr><td>  {{item}}</td> <td><a href="{%% url %(app)s.views.view_%(model)s item.id %%}">Show</a> </td> <td><a href="{%% url %(app)s.views.edit_%(model)s item.id %%}">Edit</a></tr>
{%% endfor %%}
<tr><td colspan="3"> <a href="{%% url %(app)s.views.create_%(model)s %%}">Add New</a></td></tr>
</table>

<div align="center">
{%% if list_items.has_previous %%}
    <a href="?page={{ list_items.previous_page_number }}">Previous</a>
{%% endif %%}

<span class="current">
    Page {{ list_items.number }} of {{ list_items.paginator.num_pages }}.
</span>

{%% if list_items.has_next %%}
        <a href="?page={{ list_items.next_page_number }}">Next</a>
{%% endif %%}

</div>
{%% endblock %%}
"""


TEMPLATES_EDIT = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Edit {%% endblock %%}

{%% block heading %%} <h1> %(modelClass)s</h1><h2> Edit </h2> {%% endblock %%}
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

{%% block heading %%} <h1> %(modelClass)s</h1><h2>View</h2>  {%% endblock %%}
{%% block content %%} 
<table>
{{ %(model)s_instance }}
</table>
{%% endblock %%}
"""

TEMPLATES_BASE = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr">

<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	<meta name="description" content=""/>
	<meta name="keywords" content="" />
	<meta name="author" content="" />
    <title>
        {% block title %} {% endblock %}
    </title>
      <style type="text/css"> 
        html * { padding:0; margin:0; }
        body * { padding:10px 20px; }
        body * * { padding:0; }
        body { font:small sans-serif; }
        body>div { border-bottom:1px solid #ddd; }
        h1 { font-weight:normal; }
        h2 { margin-bottom:.8em; }
        h2 span { font-size:80% ; color:#666; font-weight:normal; }
        h3 { margin:1em 0 .5em 0; }
        h4 { margin:0 0 .5em 0; font-weight: normal; }
        td {font-size:1em;  padding:3px 17px 2px 17px;}
        ul { margin-left: 2em; margin-top: 1em; }
        #summary { background: #e0ebff; }
        #summary h2 { font-weight: normal; color: #666; }
        #explanation { background:#eee; }
        #content { background:#f6f6f6; }
        #summary table { border:none; background:transparent; }
      </style> 
</head>
<body>


<div id="summary">
{% block heading %}  
{% endblock %}
</div>

<div id="content">
{% block content %} 


{% endblock %}
</div>

<div id="explanation" align="center">
django-groundwork
</div>

</body>
</html>
"""

