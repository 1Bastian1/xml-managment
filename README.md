# xml-managment
Creación de data demo en xml  para Odoo en base a un excel
La carpeta correcta es data_demo con el archivo xml_generator.py

El codigo consiste en crear la data de demo de odoo, la cual es manejada a travez de archiosn xml.
Se toma un xlsx con ciertas columnas (con nombres especificos) y se transforma y ordena en un xml con los "id" y las caracterisiticas necesarias para el manejo de one2many, many2one y one2one.
Se genera tant para:
  -actor relevante
  
  -clase
  
  -departamentento
  
  -dicision
  
  -equipo 
  
  -familia de partes
  
  -marcas
  
  -materialidad (1-2-3-4): debido a la cantidad de registros se separan en 4 archivos distintos.
  
  -periodo
  
  -productos tag id
  
  -demo productos
  
  -proveedores
  
  -sub clase
  
  -sub departamento
  
  -trazabilidad levantada
  
  -unidadedes vendidas
  

Es importante destacar que para que los datos tengan coherencia entre sus relaciones es necesario ordenar el xlsx de forma correcta (ejemplo que en materialidad existan productos que no estan en el archivo de "productos.xlsx")

-input:  entrada de los xlsx correspondientes
-output:  salidad de archivos xlsx
