import odoolib
import pandas as pd


def transformar(item):
    return [
        item["x_studio_producto"][1] if type(item["x_studio_producto"]) == list else "",
        item["x_name"],
        item["x_studio_familia_partes"][1] if type(item["x_studio_familia_partes"]) == list else "",
        item["x_active"],
        item["x_studio_indice_de_reciclabilidad"],
        item["x_studio_peso_informado"],
        item["x_studio_categoria_elemento"],
        item["x_studio_tipo_de_parte"],
        item["x_studio_caracteristica_reciclable"],
        item["x_studio_caracteristica_reciclable"],
        item["x_studio_peligrosidad"],
        item["x_studio_material"][1] if type(item["x_studio_material"]) == list else "",
        item["x_studio_definir_otro_opcional"],
        item["x_active"],
        item["x_studio_caracteristica_material"],
        item["x_studio_productos_por_envase"],
        item["x_studio_proporcion_envase_m"],
        item["x_studio_raee"],
        item["x_studio_pilas"],
        item["x_studio_cantidad_pilas"],
        item["x_studio_tipo_bateria"],
        item["x_studio_tipo_aceite_lubricante"],
        item["x_studio_volumen_m3"],
        item["x_studio_tipo_neumatico"],
        item["x_studio_cantidad_de_neumticos"],
        item["x_studio_material_textil"],
        item["x_studio_ratio_textil"]
    ]

df = pd.read_excel("./data_demo/data.xlsx")

conexion = odoolib.get_connection(
            hostname    = "rep-ripley-test.odoo.com",
            database    = "rep-ripley-test",
            login       = "bastian.olivares@sinergiaindustrias.cl",
            password    = "1234",
            port        = 443,
            protocol    ='jsonrpcs'
        )


productos = conexion.get_model('x_materialidad')


product = df['nombre_real'].to_list()
product = [str(item) for item in product]

print(product)

aux = productos.search_read(
    [("x_studio_producto", "in", product)],
    ["x_studio_producto","x_name","x_studio_familia_partes","x_active","x_studio_indice_de_reciclabilidad","x_studio_peso_informado","x_studio_categoria_elemento","x_studio_tipo_de_parte","x_studio_caracteristica_reciclable","x_studio_caracteristica_retornable","x_studio_peligrosidad","x_studio_material","x_studio_definir_otro_opcional","x_active","x_studio_caracteristica_material","x_studio_productos_por_envase","x_studio_proporcion_envase_m","x_studio_raee","x_studio_pilas","x_studio_cantidad_pilas","x_studio_tipo_bateria","x_studio_tipo_aceite_lubricante","x_studio_volumen_m3","x_studio_tipo_neumatico","x_studio_cantidad_de_neumticos","x_studio_material_textil","x_studio_ratio_textil"],
    offset=0 ,
    limit=100000
)

product = [transformar(out) for out in aux]

pd.DataFrame(product).to_excel("./data_demo/materialidad_ripey.xlsx")

print("2")


