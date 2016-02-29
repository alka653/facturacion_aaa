from django.db import models

class Producto(models.Model):
	name = models.CharField(max_length = 50)
	price = models. DecimalField(max_digits = 11, decimal_places = 2)

	def __str__(self):
		return self.name

class Factura(models.Model):
	code = models.CharField(max_length = 10, blank = True, null = True)
	date = models.DateField(auto_now = False)

	def __str__(self):
		return self.code

class DetalleFactura(models.Model):
	producto = models.ForeignKey(Producto)
	factura = models.ForeignKey(Factura)
	cantidad = models.IntegerField()