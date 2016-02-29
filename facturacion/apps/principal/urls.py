from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('facturacion.apps.principal.views',
	url(r'^$', 'home', name = 'home'),
	url(r'^find-product/$', 'find_product', name = 'find_product'),
	url(r'^save-factura/$', 'factura', name = 'factura'),
	url(r'^add-product/(?:/(?P<product_pk>\d+))?', 'product', name = 'product'),
	url(r'^factura-print/(?P<factura_pk>\d+)/$', FacturaPDFView.as_view(), name = 'pdf_factura'),
)