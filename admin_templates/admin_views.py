import hashlib
import itertools
import os
from operator import itemgetter

from django import forms
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render
from django.template.loaders.app_directories import get_app_template_dirs

from codemirror import CodeMirrorTextarea

# Links I found useful when writing this:
# http://book.huihoo.com/django/en/1.0/chapter17/index.html
# https://stackoverflow.com/questions/17111822/get-all-templates-django-detects-from-template-loaders-and-template-dirs
# https://github.com/IlyaSemenov/django-templates-admin/blob/master/django_templates_admin/templates/models.py


class Template:
    def __init__(self, key, path, relative_path, filename):
        self.key = key
        self.path = path
        self.relative_path = relative_path
        self.filename = filename

    def relative_directory(self):
        substr = self.relative_path[0:self.relative_path.index(self.filename)]
        if len(substr) < 1:
            return '/'
        return substr

    def read(self):
        f = open(self.path, 'r')
        data = f.read()
        f.close()
        return data

    def fix_eols(self, data):
        """
        Convert to Unix EOLs unless the original file was Windows encoded.
        """
        rn_pos = data.find('\r\n')
        if rn_pos >= 0 and rn_pos < data.find('\n'):
            # Do not fix EOLs if the first EOL in the old data was \r\n
            return data

        return data.replace('\r\n', '\n')

    def write(self, data):
        f = open(self.path, 'w')
        f.write(data)
        f.close()


class TemplateStorage:
    def __init__(self):
        self.templates = []

        # Load all templates
        template_dir_list = []
        for template_dir in get_app_template_dirs('templates'):
            if settings.BASE_DIR in template_dir:
                template_dir_list.append(template_dir)

        for template_dir in (template_dir_list + settings.TEMPLATES[0]['DIRS']):
            for base_dir, subdir, filenames in os.walk(template_dir):
                for filename in filenames:
                    path = os.path.join(base_dir, filename)
                    relative_path = path[len(template_dir) + 1:]
                    key = hashlib.md5(path.encode()).hexdigest()
                    template = Template(
                        key=key, path=path, relative_path=relative_path, filename=filename)
                    self.add(template)

    def add(self, template):
        self.templates.append(template)

    def clear(self):
        self.templates = []

    def all(self):
        return self.templates

    def by_key(self, key):
        for template in self.all():
            if template.key == key:
                return template
        return None

    def grouped_by_directory(self):
        sorted_templates = sorted(self.templates, key=lambda x: x.relative_directory())
        groups = []
        for key, group in itertools.groupby(sorted_templates, key=lambda x: x.relative_directory()):
            groups.append(list(group))
        return groups

template_storage = TemplateStorage()


class TemplateForm(forms.Form):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].initial = content
        self.fields['content'].label = ''

    content = forms.CharField(
        widget=CodeMirrorTextarea(
            mode='htmlmixed',
            theme='base16-dark',
            config={
                'fixedGutter': True,
            },
            dependencies=('xml', 'javascript', 'css'),
        ),
    )

def templates_list(request):
    context = {
        'grouped_templates': template_storage.grouped_by_directory(),
        'has_permission': True,
    }
    return render(request, 'admin_templates/templates_list.html', context)

def template_view(request, key):
    template = template_storage.by_key(key)
    template_data = template.read()
    if request.method == 'POST':
        form = TemplateForm(template_data, request.POST)
        if form.is_valid():
            cleaned = template.fix_eols(form.cleaned_data['content'])
            template.write(cleaned)
    else:
        form = TemplateForm(template_data)
    context = {
        'form': form,
        'template': template,
        'template_data': template_data,
        'has_permission': True,
    }
    return render(request, 'admin_templates/template_view.html', context)

templates_list = staff_member_required(templates_list)
template_view = staff_member_required(template_view)
