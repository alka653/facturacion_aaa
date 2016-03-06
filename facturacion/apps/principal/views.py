# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from easy_pdf.views import PDFTemplateView
from django.shortcuts import render
from .models import *
import datetime, json
from .forms import *

def home(request):
	return render(request, 'home.html', {'title': 'Bienvenido'})

def list_product(request):
	products = Producto.objects.all()
	return render(request, 'list_product.html', {'title': 'Lista de Productos', 'products': products})

def find_product(request):
	results = []
	response = {}
	if request.is_ajax:
		word = request.GET.get('term','')
		products = Producto.objects.filter(name__icontains = word)
		if products:
			for product in products:
				response['pk'] = product.pk
				response['name'] = product.name
				response['label'] = product.name
				response['price'] = str(int(product.price))
				results.append(response)
		else:
			response['label'] = "No hay resultados"
			results.append(response)
		data_json = json.dumps(results)
	else:
		data_json = 'fail'
	mimetype = "application/json"
	return HttpResponse(data_json, mimetype)

def add_product(request, product_pk):
	response = {}
	response['edit'] = request.GET.get('new')
	try:
		producto = Producto.objects.get(pk = product_pk)
		product = producto.pk
		response['edit'] = 'true'
	except Producto.DoesNotExist:
		producto = product_pk
		product = producto
	if request.method == 'POST':
		form = ProductForm(request.POST, instance = producto)
		if form.is_valid():
			product_data = form.save()
			response['pk'] = product_data.pk
			response['name'] = product_data.name
			response['price'] = str(product_data.price)
			response['type'] = "success"
			response['response'] = "Operacion realizada con exito"
		else:
			response['response'] = "Ha ocurrido un error"
			response['type'] = "error"
		return HttpResponse(json.dumps(response), content_type = 'application/json')
	else:
		form = ProductForm(instance = producto)
	return render(request, 'form-producto.html', {'title': 'Nuevo Producto', 'product_val': product, 'new': request.GET.get('new'),'forms': form})

def delete_product(request, product_pk):
	response = {}
	try:
		producto = Producto.objects.get(pk = product_pk)
		producto.delete()
		response['type'] = 'success'
		response['msg'] = 'Producto eliminado'
	except Producto.DoesNotExist:
		response['type'] = 'error'
		response['msg'] = 'Producto no encontrado'
	return HttpResponse(json.dumps(response), "application/json")

@csrf_exempt
def factura(request):
	response = {}
	if request.method == 'POST':
		data = request.POST
		date_now = datetime.datetime.now()
		code = 'AAA'+date_now.strftime("%y")+str(date_now.day)+str(date_now.minute)+str(date_now.second)
		factura = Factura(code = code, date = date_now)
		factura.save()
		for key, value in data.iteritems():
			product = Producto.objects.get(pk = key)
			detalle_factura = DetalleFactura(producto = product, factura = factura, cantidad = value)
			detalle_factura.save()
		print code
		response['response'] = True
		response['message'] = factura.pk
	else:
		response['response'] = False
		response['message'] = 'Ha ocurrido un error'
	return HttpResponse(json.dumps(response), "application/json")

def list_factura(request):
	facturas = Factura.objects.all()
	return render(request, 'list_factura.html', {'title': 'Lista de Facturas', 'facturas': facturas})

def detail_factura(request, factura_pk):
	factura = Factura.objects.get(pk = factura_pk)
	return render(request, 'detail-factura.html', {'title': 'Detalle de '+factura.code, 'factura': factura})

def delete_factura(request, factura_pk):
	response = {}
	try:
		factura = Factura.objects.get(pk = factura_pk)
		factura.delete()
		response['type'] = 'success'
		response['msg'] = 'Factura eliminada'
	except Factura.DoesNotExist:
		response['type'] = 'error'
		response['msg'] = 'Factura no encontrada'
	return HttpResponse(json.dumps(response), "application/json")

class FacturaPDFView(PDFTemplateView):
	template_name = "pdf_factura.html"

	def get_context_data(self, **kwargs):
		context = super(FacturaPDFView, self).get_context_data(**kwargs)
		factura = Factura.objects.get(pk = self.kwargs['factura_pk'])
		context['title'] = factura.code
		context['query'] = factura
		return context