from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from easy_pdf.views import PDFTemplateView
from django.shortcuts import render
from .models import *
from .forms import *
import datetime, json

def home(request):
	return render(request, 'home.html', {'title': 'Bienvenido'})

def find_product(request):
	if request.is_ajax:
		word = request.GET.get('term','')
		results = []
		products = Producto.objects.filter(name__icontains = word)
		if products:
			for product in products:
				response = {}
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

def product(request, product_pk = 0):
	try:
		producto = Producto.objects.get(pk = product_pk)
	except Producto.DoesNotExist:
		producto = product_pk
	if request.method == 'POST':
		response = {}
		form = ProductForm(request.POST, instance = producto)
		if form.is_valid():
			product_data = form.save()
			response['pk'] = product_data.pk
			response['name'] = product_data.name
			response['price'] = str(product_data.price)
		else:
			response['response'] = "Ha ocurrido un error"
		return HttpResponse(json.dumps(response), content_type = 'application/json')
	else:
		form = ProductForm(instance = producto)
	return render(request, 'form-producto.html', {'title': 'Nuevo Producto', 'product_val': producto, 'forms': form})

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

class FacturaPDFView(PDFTemplateView):
	template_name = "pdf_factura.html"

	def get_context_data(self, **kwargs):
		context = super(FacturaPDFView, self).get_context_data(**kwargs)
		factura = Factura.objects.get(pk = self.kwargs['factura_pk'])
		context['title'] = factura.code
		context['query'] = factura
		return context