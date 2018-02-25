# punkweb-admin-templates

Django admin extension that allows admin users to edit templates from within the admin interface.

This package doesn't add any models, it simply creates two routes in the admin, `/admin/templates/` and `/admin/templates/<pk>`.  Templates are loaded when the server starts, and read when accessed.  CodeMirror is included.

I've seen other forum software have this feature.  Eventually I'd like to integrate this project with [punkweb-boards](https://github.com/Punkweb/punkweb-boards).


## Media

### Templates list view
![Sweet Shit](https://i.imgur.com/EgzVIFN.png)

### Me editing the page I'm currently viewing, from within the page I'm currently viewing.
![Badassery](https://i.imgur.com/pQH0V1H.gif)
