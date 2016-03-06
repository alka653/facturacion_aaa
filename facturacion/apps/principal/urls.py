from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('facturacion.apps.principal.views',
	url(r'^$', 'home', name = 'home'),
	url(r'^list-product/$', 'list_product', name = 'list_product'),
	url(r'^find-product/$', 'find_product', name = 'find_product'),
	url(r'^save-factura/$', 'factura', name = 'factura'),
	url(r'^list-factura/$', 'list_factura', name = 'list_factura'),
	url(r'^delete-factura/(?P<factura_pk>\d+)/$', 'delete_factura', name = 'delete_factura'),
	url(r'^detail-factura/(?P<factura_pk>\d+)/$', 'detail_factura', name = 'detail_factura'),
	url(r'^add-product/(?:/(?P<product_pk>\d+))?', 'add_product', name = 'add_product'),
	url(r'^delete-product/(?P<product_pk>\d+)/$', 'delete_product', name = 'delete_product'),
	url(r'^factura-print/(?P<factura_pk>\d+)/$', FacturaPDFView.as_view(), name = 'pdf_factura'),
)