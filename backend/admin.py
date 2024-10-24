from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class MyAdminSite(AdminSite):
    site_header = _('My Custom Admin Header')
    site_title = _('My Custom Admin Title')
    index_title = _('Welcome to My Admin Site')

admin_site = MyAdminSite(name='myadmin')
