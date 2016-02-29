import locale
from facturacion.apps.principal.models import *
from django import template
register = template.Library()

@register.simple_tag()
def multiply(cant, value):
	return "{0:,}".format(int(cant * value))

@register.simple_tag()
def height(cant):
	return (cant * 0.5) + 9

@register.simple_tag()
def multiply_tot(factura):
	sum_tot = 0
	factura = Factura.objects.get(code = factura)
	for query in factura.detallefactura_set.all():
		sum_tot += query.cantidad * query.producto.price
	return "{0:,}".format(int(sum_tot))