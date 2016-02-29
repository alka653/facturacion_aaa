from django.contrib import admin
from .models import *

admin.site.register(Producto)
admin.site.register(Factura)
admin.site.register(DetalleFactura)