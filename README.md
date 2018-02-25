# punkweb-admin-templates

Django admin extension that allows admin users to edit templates from within the admin interface.

This package doesn't add any models, it simply creates two routes in the admin, `/admin/templates/` and `/admin/templates/<pk>`.  Templates are loaded when the server starts, and read when accessed.  CodeMirror is used by default.

I've seen other forum software have this feature.  Eventually I'd like to integrate this project with [punkweb-boards](https://github.com/Punkweb/punkweb-boards).


Run example project:

Download [CodeMirror](https://codemirror.net/) and extract it at `example_project/static/example_project/codemirror` (this directory can be configured in settings)
```
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Open up to `localhost:8000/admin/templates/`


## Media

### Templates list view
![Sweet Shit](https://i.imgur.com/EgzVIFN.png)

### Me editing the page I'm currently viewing, from within the page I'm currently viewing.
![Badassery](https://i.imgur.com/pQH0V1H.gif)
