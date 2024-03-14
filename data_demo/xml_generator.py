import pandas as pd
import xml.etree.cElementTree as ET
from tqdm import tqdm
import random

class XML:
    def __init__(self):

        #=================================
        #=========DICCIONARIOS============
        #=================================
        #Seccion de diccionarios para hacer las conversiones correctas, tanto para los 
        # campos select o many2one que apuntan valores con id ya existentes
        self.dic_origen ={
            "NACIONAL"  :"nacional",
            "IMPORTADO" :"importado"
        }

        self.dic_stage_trazabilidad = {
            "Nuevo" : "data_trazabilidad_stage_nuevo",
            "Contacto inválido" : "data_trazabilidad_candidato_envalido",
            "Comunicación establecida" : "data_trazabilidad_comunicacion_establecida",
            "Información recibida" : "data_trazabilidad_informacion_recibida",
            "Proceso concluido" : "data_trazabilidad_proceso_concluido"
        }

        self.dic_stage_productos = {
            "No completado - Nuevo" : "data_productos_stage_no_completado_nuevo",
            "No completado - En revisión" : "data_productos_stage_no_completado_en_revision",
            "Proyectado" : "data_productos_stage_proyectado",
            "Completado parcial" : "data_productos_stage_completado_parcial",
            "Completado" : "data_productos_stage_completado"
        }

        self.dic_categoria_elemento= {
            "EYE Domiciliario"      : "eye_domiciliario",
            "EYE NO Domiciliario"   : "eye_no_domiciliario",
            "EYE No Domiciliario"   : "eye_no_domiciliario",
            "EYE No domiciliario"   : "eye_no_domiciliario",
            "RAEE"                  : "raee",
            "PILAS"                 : "pilas",
            "Baterias"              : "baterias",
            "Baterías"              : "baterias",
            "Aceites y Lubricantes" : "aceites_y_lubricantes",
            "Neumáticos"            : "neumaticos",
            "Neumaticos"            : "neumaticos",
            "Textil"                : "textil",
            "TEXTIL"                : "textil"
        }

        self.dic_tipo_parte = {
            "PRIMARIO"      : "primario",
            "SECUNDARIO"    : "secundario",
            "TERCIARIO"     : "terciario",
            "NO APLICA"     : "no_aplica"
        }

        self.dic_caracteristica_reciclable = {
            "sin material reciclado"  : "sin_material_reciclado",
            "Sin material reciclado"  : "sin_material_reciclado",
            ">10% material reciclado" : "porcentaje_10",
            ">25% material reciclado" : "porcentaje_25",
            ">50% material reciclado" : "porcentaje_50",
            ">80% material reciclado" : "porcentaje-80",
            "100% material reciclado" : "porcentaje_100"
        }

        self.dic_caracteristica_retornable = {
            "no retornable"         : "no_retornable",
            "No Retornable"         : "no_retornable",
            "retornable nuevo"      : "retornable_nuevo",
            "Retornable Nuevo"      : "retornable_nuevo",
            "retornable recuperado" : "retornable_recuperado"
        }

        self.dic_peligrosidad = {
            "residuo NO peligroso" : "residuo_no_peligroso",
            "Residuo NO Peligroso" : "residuo_no_peligroso",
            "residuo peligroso" : "residuo_peligroso",
            "Residuo Peligroso" : "residuo_peligroso",
        }

        self.dic_materiales_eye = {
            "Otros envases PET (1)" : "data_tipo_eye_otros_envases_PET",
            "Envases de PP que NO contienen sustancias con grasa (5)" : "data_tipo_eye_pp_no_sustancias_grasas",
            "Envases de PP que contienen sustancias con grasa (5)" : "data_tipo_eye_pp_contiene_sustancias_grasa",
            "Envases de PP que  contienen sustancias con grasa,  (5)" : "data_tipo_eye_pp_contiene_sustancias_grasa",
            "Envases de PEBD que NO contienen sustancias con grasa (4)" : "data_tipo_eye_pebd_no_sustancias_grasa",
            "Envases de PEBD que  contienen sustancias con grasa (4)" : "data_tipo_eye_pebd_no_sustancias_grasa",
            "(3)PVC" : "data_tipo_eye_pvc",
            "PVC (3)" : "data_tipo_eye_pvc",
            "Envases de PEAD que NO contienen sustancias con grasa (2)" : "data_tipo_eye_pead_no_sustancias_grasa",
            "Otros envases plásticos (7)" : "data_tipo_eye_otro_envase_plastico",
            "(7)Otros plásticos" : "data_tipo_eye_otro_envase_plastico",
            "Hojalata" : "data_tipo_eye_hojalata",
            "Botellas PET (1)" : "data_tipo_eye_botella_pet",
            "Envases de PS que NO contienen sustancias con grasa (6)" : "data_tipo_eye_ps_sustancias_grasa",
            "Otro papel compuesto" : "data_tipo_eye_otro_papel_compuesto",
            "Envases de PEBD que contienen sustancias con grasa (4)" : "data_tipo_eye_pebd_sustancias_grasa_4",
            "Envases de PEAD que contienen sustancias con grasa (2)" : "data_tipo_eye_pebd_sustancias_grasa_2",
            "Envases de PS que contienen sustancias con grasa (6) y envases de EPS" : "data_tipo_eye_ps_sustancias_grasa_y_envase_eps",
            "Madera" : "data_tipo_eye_madera",
            "MADERA" : "data_tipo_eye_madera",
            "Otro material" : "data_tipo_eye_otro_material",
            "OTRO MATERIAL" : "data_tipo_eye_otro_material",
            "Cartón" : "data_tipo_eye_carton",
            "CARTÓN" : "data_tipo_eye_carton",
            "Cartón para bebidas y alimentos" : "data_tipo_eye_carton_bebidas_alimentos",
            "Papel" : "data_tipo_eye_papel",
            "PAPEL" : "data_tipo_eye_papel",
            "Vidrio" : "data_tipo_eye_vidrio",
            "Aluminio (latas)" : "data_tipo_eye_aluminios_latas",
            "Envases de aluminio" : "data_tipo_eye_envase_aluminio",
            "Metal con aire comprimido" : "data_tipo_eye_material_aire_comprimido",
            "Otros envases de metal" : "data_tipo_eye_motro_envase_metal",
            "Otros envases de  metal" : "data_tipo_eye_motro_envase_metal",
            "Plástico compostable" : "data_tipo_eye_plastico_compostable"
        }

        self.dic_caracteristica_compostable = {
            "envase de servicio" : "envase_de_servicio",
            "envase general" : "envase_general",
            "no aplica" : "no_aplica",
            "No Aplica" : "no_aplica"
        }

        self.dic_caracteristica_material = {
            "rigido"        : "rigido",
            "flexible"      : "flexible",
            "expandido"     : "expandido",
            "corrugado"     : "corrugado",
            "cartulina"     : "cartulina",
            "transparente"  : "transparente",
            "color"         : "color",
            "compuesto"     : "compuesto",
            "polipapel"     : "polipapel",
            "encerado"      : "encerado",
            "engomado"      : "engomado",

            "Rígido"        : "rigido",
            "Flexible"      : "flexible",
            "Expandido"     : "expandido",
            "Corrugado"     : "corrugado",
            "Cartulina"     : "cartulina",
            "Transparente"  : "transparente",
            "Color"         : "color",
            "Compuesto"     : "compuesto",
            "Polipapel"     : "polipapel",
            "Encerado"      : "encerado",
            "Engomado"      : "engomado"
        }
        
        self.dic_tipo_raee = {
            "IT - Carburos con fluor o bromo"                       : "data_tipo_raee_carburo_fluor_o_bromo",
            "IT - De aire acondicionado"                            : "data_tipo_raee_aire_acondicionado",
            "IT - De aceite u otro líquido"                         : "data_tipo_raee_acceite_u_otro_liquido",
            "IT - Con gases"                                        : "data_tipo_raee_con_gases",
            "PP - Monitores y pantallas planas"                     : "data_tipo_raee_monitores_pantalla",
            "PP - Otros monitores y pantallas planas"               : "data_tipo_raee_otros_monitores_pantalla",
            "PP - Otros con pilas que no pueden extraerse"          : "data_tipo_raee_otros_pilas_no_extraerse",
            "LL - Lámparas de descarga con gas en su interior"      : "data_tipo_raee_lampara_descarga_gas_interior",
            "LL - Lámparas LED"                                     : "data_tipo_raee_lampara_led",
            "PF - Paneles fotovoltáicos con silicio"                : "data_tipo_raee_paneles_fotovoltaico_silicio",
            "PF - Paneles con telurio de cadmio"                    : "data_tipo_raee_paneles_telurio_cadmio",
            "AG - Equipos de informática y comunicaciones grandes"  : "data_tipo_raee_equipo_informatica_comunicacion_grande",
            "AG - Otros grandes aparatos"                           : "data_tipo_raee_otros_grandes_aparatos",
            "AP - Otros aparatos pequeños"                          : "data_tipo_raee_otros_aparatos_pequenios",
            "AP - Equipos de informática y comunicaciones pequeño"  : "data_tipo_raee_equipo_informatica_comunicacion_pequenio",
            "AP - Otros aparatos pequeños con pila o batería que no pueda extraerse" : "data_tipo_raee_otros_aparato_pequenio_pila_bateria_no_extraible"
        }

        self.dic_tipo_pila = {
            "Botón litio"                           : "data_tipo_pila_boton_litio",
            "Botón mercurio"                        : "data_tipo_pila_boton_mercurio",
            "Botón óxido de manganeso"              : "data_tipo_pila_boton_oxido_manganeso",
            "Botón óxido de plata"                  : "data_tipo_pila_boton_oxido_plata",
            "Botón zinc aire"                       : "data_tipo_pila_boton_zinc_aire",
            "Botón alcalinas"                       : "data_tipo_pila_boton_alcalinas",
            "Estándar alcalina"                     : "data_tipo_pila_estandar_alcalinas",
            "Estándar litio no recargable"          : "data_tipo_pila_estandar_litio_no_recargable",
            "Estándar zinc carbón"                  : "data_tipo_pila_estandarzinc_carbon",
            "Estándar zinc dióxido de manganeso"    : "data_tipo_pila_estandarzinc_zinc_dioxido_manganeso",
            "Acumulador niquel-cadmio"              : "data_tipo_pila_acumulador_niquel_cadmio",
            "Acumulador níquel hidruro metálico"    : "data_tipo_pila_acumulador_niquel__hidruro_metalico",
            "Acumulador ion litio"                  : "data_tipo_pila_acumulador_ion_litio",
            "Otras pilas"                           : "data_tipo_pila_otras_pilas"
        }

        self.dic_tipo_bateria = {
            "De plomo para vehiculos motorizados" : "data_tipo_bateria_plomo_vehiculo_motorizado",
            "De plomo industriales" : "data_tipo_bateria_plomo_industriales",
            "Otras baterias, pilas o acumuladores para vehiculos motorizados" : "data_tipo_bateria_otras_baterias"
        }

        self.dic_tipo_aceite_y_lubricante ={
            "Aceites Lubricantes No Recuperables" : "data_tipo_aceite_lubri_no_recuperable",
            "Aceites Lubricantes Recuperables" : "data_tipo_aceite_lubri_recuperable"
        }

        self.dic_neumaticos = {
            "CATEGORÍA A"   : "data_tipo_neumatico_categoria_A",
            "CATEGORÍA B"   : "data_tipo_neumatico_categoria_b",
            "MACIZOS"       : "data_tipo_neumatico_macizo",
            "Bicicletas, sillas de rueda y similares" : "data_tipo_neumatico_macizo_bicicleta_silla_de_rueda_similares"
        }



        #===================================
        #============DATA FRAMES============
        #===================================
        # Seccion destinada a guardar la data de los xlsx en dataframe para
        # mejor manipulacion de los datos.

        self.df_productos   = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="productos", na_values='')
        self.df_productos.replace('NaN', '')

        self.df_tag_id      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="tag_id", na_values='')
        self.df_tag_id .replace('NaN', '')

        self.df_periodos      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="periodos", na_values='')
        self.df_periodos .replace('NaN', '')

        self.df_marcas      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="marcas", na_values='')
        self.df_marcas .replace('NaN', '')

        self.df_proveedores      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="proveedor", na_values='')
        self.df_proveedores .replace('NaN', '')

        self.df_trazabilidad_levantamiento      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="trazabilidad_levantaiento", na_values='')
        self.df_trazabilidad_levantamiento .replace('NaN', '')

        self.df_actores_relevante      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="actor_relevante", na_values='')
        self.df_actores_relevante .replace('NaN', '')

        self.df_division      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="division", na_values='')
        self.df_division .replace('NaN', '')

        self.df_departamento      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="departamento", na_values='')
        self.df_departamento .replace('NaN', '')

        self.df_sub_departamento      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="sub_departamento", na_values='')
        self.df_sub_departamento .replace('NaN', '')

        self.df_clase      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="clases", na_values='')
        self.df_clase .replace('NaN', '')

        self.df_sub_clase      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="sub_clases", na_values='')
        self.df_sub_clase .replace('NaN', '')

        self.df_equipo      = pd.read_excel("./data_demo/input/Productos.xlsx", sheet_name="equipo", na_values='')
        self.df_equipo .replace('NaN', '')

        self.df_familia_partes     = pd.read_excel("./data_demo/input/materialidad/FAMILIA PARTES.xlsx", na_values='')
        self.df_familia_partes .replace('NaN', '')


        self.df_materialidad1      = pd.read_excel("./data_demo/input/materialidad/Materialidad1.xlsx", sheet_name="MATERIALIDAD_1", na_values='')
        self.df_materialidad1 .replace('NaN', '')

        self.df_materialidad2      = pd.read_excel("./data_demo/input/materialidad/Materialidad2.xlsx", sheet_name="MATERIALIDAD_2", na_values='')
        self.df_materialidad2 .replace('NaN', '')

        self.df_materialidad3      = pd.read_excel("./data_demo/input/materialidad/Materialidad3.xlsx", sheet_name="MATERIALIDAD_3", na_values='')
        self.df_materialidad3 .replace('NaN', '')

        self.df_materialidad4      = pd.read_excel("./data_demo/input/materialidad/Materialidad4.xlsx", sheet_name="MATERIALIDAD_4", na_values='')
        self.df_materialidad4 .replace('NaN', '')

        self.df_materialidades = [self.df_materialidad1, self.df_materialidad2, self.df_materialidad3, self.df_materialidad4]

    #====================================
    #=========UTILS======================
    #====================================
    #Funcionalidades utiles para converciones de datos por ejemplo:
    #   -lowerAndReplace: Estandarizar los nombre haciendo un lower y un replace a los espacios cambiando por un "_"
    #   -createStringMany2Many: Funciones que devuleven un arreglo de los valores separados por comas provenientes 
    #                           de los data frames usados.
    def createStringMany2ManyTagId(self, array):
        #   Prametros
        #   ---------
        #       array: lista con los periodos a los que se apuntan
        #
        #   Funcionalidad
        #   -------------
        #       Entrega un string con la forma necesaria para agregar a los campos xml 
        #       y asi apuntar a varios valores (many2many)
        #   
        
        len_array = len(array)
        ref = ''
        for i, data in enumerate(array) :
            ref = ref + "ref('demo_productos_tag_id_"+self.lowerAndReplace(data)+"')"
            if i < len_array - 1: ref = ref + ','
        return ref
    
    def createStringMany2ManyPeriodos(self, array):
        #   Prametros
        #   ---------
        #       array: lista con los periodos a los que se apuntan
        #
        #   Funcionalidad
        #   -------------
        #       Entrega un string con la forma necesaria para agregar a los campos xml 
        #       y asi apuntar a varios valores (many2many)
        #   
        
        len_array = len(array)
        ref = ''
        for i, data in enumerate(array) :
            ref = ref + "ref('demo_preriodo_"+self.lowerAndReplace(data)+"')"
            if i < len_array - 1: ref = ref + ','
        return ref
    
    def lowerAndReplace(self, string):
        #   Prametros
        #   ---------
        #       string: valor que se quiere modificar
        #
        #   Funcionalidad
        #   -------------
        #       Entrega un string donde se reemplazan los espacios y los puntso (.) 
        #       por guienes bajos (_)
        #   
        aux = string.lower()
        aux = aux.replace(" ","_")
        aux = aux.replace(".","_") 
        return aux

    #====================================
    #=========XML FUNCTIONS==============
    #====================================
    # Funciones encargadas de crear los archivos xml con las etiquetas y referencias correspondientes.
    #
    # OBS 
    # ---------------
    # (etiquetas)
    # Ref : es usado para los Many2One
    # Eval: es usado para los Many2Many
    #
    # (xlsx)
    # todos los xls deben tener como obligacion los mismos encabezados, tal vez no el mismo orden pero si la misma
    # cantidad de columas y con los mismos nombres (el df se usa con el string del nombre)
    #
    #
    # FUNCIONAMIENTO
    # --------------
    # El codigo crea los registros que aprecen en el xlsx con un identificador unico, en general el nombre del mismo registro,
    # a excepcion de materialidad que es el nombre del producto mas el nombre del material.
    # 
    # COPY PASTE PLATAFORMA
    # ---------------------
    # Al pasar la materialidad a la plataforma aprovechar de separar los xml debido a que son muy extensos. HAy disponible 6
    # archivos xml destinados a la data de demo de la materialdiad para repartir todos los registros.
    def createTagId(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_tag_id.iterrows():
            id_name = self.lowerAndReplace(str(row['tag_id']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.producto_tag', id='demo_productos_tag_id_'+str(id_name))
            
            ET.SubElement(record, 'field', name='name').text=  str(row['tag_id'])


        file_producto_tag_id = ET.ElementTree(odoo)
        file_producto_tag_id.write('data_demo/output/demo_productos_tag_id.xml', encoding="utf-8", xml_declaration=True)

    def createPeriodos(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_periodos.iterrows():
            id_name = self.lowerAndReplace(str(row['periodo']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.periodo', id='demo_preriodo_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['periodo'])
        
        file_periodo = ET.ElementTree(odoo)
        file_periodo.write('data_demo/output/demo_periodo.xml', encoding="utf-8", xml_declaration=True)

    def createMarcas(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_marcas.iterrows():
            id_name = self.lowerAndReplace(str(row['marca']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.marca', id='demo_marca_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['marca'])

        file_marca = ET.ElementTree(odoo)
        file_marca.write('data_demo/output/demo_marcas.xml', encoding="utf-8", xml_declaration=True)

    def createProveedor(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_proveedores.iterrows():
            id_name = self.lowerAndReplace(str(row['proveedor']))

            record = ET.SubElement(odoo, 'record', model='res.partner', id='demo_proveedor_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['proveedor'])

        file_proveedor = ET.ElementTree(odoo)
        file_proveedor.write('data_demo/output/demo_proveedor.xml', encoding="utf-8", xml_declaration=True)

    def createTrazabilidadLevantada(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_trazabilidad_levantamiento.iterrows():
            id_name = self.lowerAndReplace(str(row['trazabilidad_levantamiento']))
            id_periodos = self.createStringMany2ManyPeriodos(str(row['periodo']).split(','))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.traz_lev', id='demo_traz_lev_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['trazabilidad_levantamiento'])
            ET.SubElement(record, 'field', name='etapa_trazabilidad', ref = self.dic_stage_trazabilidad[str(row['etapa_trazabilidad'])])
            ET.SubElement(record, 'field', name='periodo',  eval=f"[(6, 0, [{id_periodos}])]")

        file_trazabilidad_levantada = ET.ElementTree(odoo)
        file_trazabilidad_levantada.write('data_demo/output/demo_trazabilidad_levantada.xml', encoding="utf-8", xml_declaration=True)

    def createActoresRelevantes(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_actores_relevante.iterrows():
            id_name     = self.lowerAndReplace(str(row['actor_relevante']))
            id_equipo   = self.lowerAndReplace(str(row['equipo']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.act_relev', id='demo_actor_relevante_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['actor_relevante'])
            if id_equipo != '' and id_equipo != 'nan': ET.SubElement(record, 'field', name='equipo', ref='demo_equipo_'+id_equipo)
            
        
        file_actor_relevante = ET.ElementTree(odoo)
        file_actor_relevante.write('data_demo/output/demo_actor_relevante.xml', encoding="utf-8", xml_declaration=True)

    def createDivision(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_division.iterrows():
            id_name = self.lowerAndReplace(str(row['division']))
            
            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.division', id='demo_division_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['division'])

        file_division = ET.ElementTree(odoo)
        file_division.write('data_demo/output/demo_division.xml', encoding="utf-8", xml_declaration=True)

    def createDepartamento(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_departamento.iterrows():
            id_name = self.lowerAndReplace(str(row['departamento']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.departamento', id='demo_departamento_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['departamento'])
        
        file_departemento = ET.ElementTree(odoo)
        file_departemento.write('data_demo/output/demo_departemento.xml', encoding="utf-8", xml_declaration=True)

    def createSubDepartamento(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_sub_departamento.iterrows():
            id_name = self.lowerAndReplace(str(row['sub_departamento']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.sub_depart', id='demo_sub_departamento_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['sub_departamento'])
        
        file_sub_departemento = ET.ElementTree(odoo)
        file_sub_departemento.write('data_demo/output/demo_sub_departemento.xml', encoding="utf-8", xml_declaration=True)

    def createClase(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_clase.iterrows():
            id_name = self.lowerAndReplace(str(row['clases']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.clase', id='demo_clase_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['clases'])
        
        file_clase = ET.ElementTree(odoo)
        file_clase.write('data_demo/output/demo_clase.xml', encoding="utf-8", xml_declaration=True)

    def createSubClase(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_sub_clase.iterrows():
            id_name = self.lowerAndReplace(str(row['sub_clase']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.sub_clase', id='demo_sub_clase_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['sub_clase'])
        
        file_sub_clase = ET.ElementTree(odoo)
        file_sub_clase.write('data_demo/output/demo_sub_clase.xml', encoding="utf-8", xml_declaration=True)

    def createEquipo(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_equipo.iterrows():
            id_name = self.lowerAndReplace(str(row['equipos']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.equipo', id='demo_equipo_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['equipos'])

        file_equipo = ET.ElementTree(odoo)
        file_equipo.write('data_demo/output/demo_equipo.xml', encoding="utf-8", xml_declaration=True)

    def createProductos(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in tqdm(self.df_productos.iterrows()):
            id_name     = self.lowerAndReplace(str(row['name']))
            id_tag_id   = self.createStringMany2ManyTagId(str(row['tag_id']).split(','))
            id_periodos = self.createStringMany2ManyPeriodos(str(row['periodo']).split(','))
            id_marca    = self.lowerAndReplace(str(row["marca"]))
            id_proveedor= self.lowerAndReplace(str(row["proveedor"]))
            id_traz_lev = self.lowerAndReplace(str(row["trazabilidad_levantamiento"]))
            id_act_relev= self.lowerAndReplace(str(row["actor_relevante"]))
            id_division = self.lowerAndReplace(str(row["division"]))
            id_depa     = self.lowerAndReplace(str(row["departamento"]))
            id_sub_depa = self.lowerAndReplace(str(row["sub_departamento"]))
            id_clase    = self.lowerAndReplace(str(row["clases"]))
            id_sub_clase= self.lowerAndReplace(str(row["sub_clase"]))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.producto', id='demo_productos_'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['name'])
            ET.SubElement(record, 'field', name='tag_id',  eval=f"[(6, 0, [{id_tag_id}])]")
            ET.SubElement(record, 'field', name='periodo',  eval=f"[(6, 0, [{id_periodos}])]")
            ET.SubElement(record, 'field', name='descripcion').text=  str(row['descripcion'])
            ET.SubElement(record, 'field', name='marca', ref='demo_marca_'+id_marca)
            ET.SubElement(record, 'field', name='ean').text=  str(row['ean'])
            ET.SubElement(record, 'field', name='codigo_ref_proveedor').text=  str(row['codigo_ref_proveedor'])
            ET.SubElement(record, 'field', name='proveedor', ref='demo_proveedor_'+id_proveedor)
            ET.SubElement(record, 'field', name='trazabilidad_levantamiento', ref='demo_traz_lev_'+id_traz_lev)
            ET.SubElement(record, 'field', name='actor_relevante', ref='demo_actor_relevante_'+id_act_relev)
            ET.SubElement(record, 'field', name='origen').text=  self.dic_origen[str(row['origen'])]
            ET.SubElement(record, 'field', name='division', ref='demo_division_'+id_division)
            ET.SubElement(record, 'field', name='departamento', ref='demo_departamento_'+id_depa)
            if id_sub_depa != '' and id_sub_depa != 'nan': ET.SubElement(record, 'field', name='sub_departamento', ref='demo_sub_departamento_'+id_sub_depa)
            if id_clase != '' and id_clase != 'nan': ET.SubElement(record, 'field', name='clases', ref='demo_clase_'+id_clase)
            if id_sub_clase != '' and id_sub_clase != 'nan': ET.SubElement(record, 'field', name='sub_clase', ref='demo_sub_clase_'+id_sub_clase)
            ET.SubElement(record, 'field', name='stage_id', ref=self.dic_stage_productos[str(row['stage_id'])])

            if str(row['eye']) != '' and str(row['eye']) != 'nan': ET.SubElement(record, 'field', name='eye').text=  str(row['eye'])
            if str(row['raee']) != '' and str(row['raee']) != 'nan': ET.SubElement(record, 'field', name='raee').text=  str(row['raee'])
            if str(row['pilas']) != '' and str(row['pilas']) != 'nan': ET.SubElement(record, 'field', name='pilas').text=  str(row['pilas'])
            if str(row['neumaticos']) != '' and str(row['neumaticos']) != 'nan': ET.SubElement(record, 'field', name='neumaticos').text=  str(row['neumaticos'])
            if str(row['baterias']) != '' and str(row['baterias']) != 'nan': ET.SubElement(record, 'field', name='baterias').text=  str(row['baterias'])
            if str(row['aceite_y_lubrcante']) != '' and str(row['aceite_y_lubrcante']) != 'nan': ET.SubElement(record, 'field', name='aceite_y_lubrcante').text=  str(row['aceite_y_lubrcante'])
            if str(row['textil']) != '' and str(row['textil']) != 'nan': ET.SubElement(record, 'field', name='textil').text=  str(row['textil'])
            



        file_periodo = ET.ElementTree(odoo)
        file_periodo.write('data_demo/output/demo_productos.xml', encoding="utf-8", xml_declaration=True)




    #==============================MATERIALIDAD==============================================000
    def createFamiliaPartes(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in self.df_familia_partes.iterrows():
            id_name = self.lowerAndReplace(str(row['x_studio_familia_de_parte']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.familia_de_partes', id='demo_familia_partes'+str(id_name))

            ET.SubElement(record, 'field', name='name').text=  str(row['x_studio_familia_de_parte'])

        file_familia_partes = ET.ElementTree(odoo)
        file_familia_partes.write('data_demo/output/demo_familia_partes.xml', encoding="utf-8", xml_declaration=True)

    def createUnidadesVendidas(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for index, row in tqdm(self.df_productos.iterrows()):
            id_name     = self.lowerAndReplace(str(row['name']))
            id_producto = self.lowerAndReplace(str(row['name']))
            n_unidades_vendidas = random.randint(0,3000)


            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.unidades_vendidas', id='demo_unidades_vendidas'+str(id_name))

            if str(row['name']) != '' and str(row['name']) != 'nan': ET.SubElement(record, 'field', name='name').text=  "Unid. Vendida " + str(row['name'])
            if id_producto != '' and id_producto != 'nan': ET.SubElement(record, 'field', name='producto', ref='demo_productos_'+id_producto)
            ET.SubElement(record, 'field', name='periodo', ref='demo_preriodo_2023')
            ET.SubElement(record, 'field', name='unidades_vendidas').text= str(n_unidades_vendidas)

        file_unidades_vendidas = ET.ElementTree(odoo)
        file_unidades_vendidas.write('data_demo/output/demo_unidades_vendidas.xml', encoding="utf-8", xml_declaration=True)

    def createMaterialidad(self):
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        
        odoo =  ET.Element('odoo')

        for i ,materialidad in tqdm(enumerate(self.df_materialidades)):

            for index, row in materialidad.iterrows():
                id_name = self.lowerAndReplace(str(row['producto_real'])) + "_" + self.lowerAndReplace(str(row['x_name']))
                id_producto = self.lowerAndReplace(str(row['producto_real']))
                id_familia_partes = self.lowerAndReplace(str(row['x_studio_familia_de_parte']))
                id_raee = self.lowerAndReplace(str(row['x_studio_raee']))

                record = ET.SubElement(odoo, 'record', model='levantamiento_rep.materialidad', id='demo_materialidad_'+str(id_name))

                if str(row['x_name']) != '' and str(row['x_name']) != 'nan': ET.SubElement(record, 'field', name='name').text=  str(row['x_name'])
                if id_producto != '' and id_producto != 'nan': ET.SubElement(record, 'field', name='producto', ref='demo_productos_'+id_producto)
                if id_familia_partes != '' and id_familia_partes != 'nan': ET.SubElement(record, 'field', name='familia_de_partes', ref='demo_familia_partes'+id_familia_partes)
                if str(row['x_studio_descripcion']) != '' and str(row['x_studio_descripcion']) != 'nan': ET.SubElement(record, 'field', name='descripcion').text=  str(row['x_studio_descripcion'])
                if str(row['x_studio_indice_de_reciclabilidad']) != '' and str(row['x_studio_indice_de_reciclabilidad']) != 'nan': ET.SubElement(record, 'field', name='indice_reciclabilidad').text=  str(row['x_studio_indice_de_reciclabilidad'])
                if str(row['x_studio_peso_informado']) != '' and str(row['x_studio_peso_informado']) != 'nan': ET.SubElement(record, 'field', name='peso_informado').text=  str(row['x_studio_peso_informado'])
                if str(row['x_studio_categoria_elemento']) != '' and str(row['x_studio_categoria_elemento']) != 'nan': ET.SubElement(record, 'field', name='categoria_elemento').text=  self.dic_categoria_elemento[str(row['x_studio_categoria_elemento'])]
                if str(row['x_studio_tipo_de_parte']) != '' and str(row['x_studio_tipo_de_parte']) != 'nan': ET.SubElement(record, 'field', name='tipo_de_parte').text=  self.dic_tipo_parte[str(row['x_studio_tipo_de_parte'])]
                if str(row['x_studio_caracterstica_reciclable']) != '' and str(row['x_studio_caracterstica_reciclable']) != 'nan': ET.SubElement(record, 'field', name='caracteristicas_reciclable').text=  self.dic_caracteristica_reciclable[str(row['x_studio_caracterstica_reciclable'])]
                if str(row['x_studio_caracterstica_retornable']) != '' and str(row['x_studio_caracterstica_retornable']) != 'nan': ET.SubElement(record, 'field', name='caracteristicas_retornable').text=  self.dic_caracteristica_retornable[str(row['x_studio_caracterstica_retornable'])]
                if str(row['x_studio_peligrosidad']) != '' and str(row['x_studio_peligrosidad']) != 'nan': ET.SubElement(record, 'field', name='peligrosidad').text=  self.dic_peligrosidad[str(row['x_studio_peligrosidad'])]
                if str(row['x_studio_material']) != '' and str(row['x_studio_material']) != 'nan':   ET.SubElement(record, 'field', name='maetrial', ref=self.dic_materiales_eye[str(row['x_studio_material'])])
                if str(row['x_studio_definir_otro_opcional']) != '' and str(row['x_studio_definir_otro_opcional']) != 'nan': ET.SubElement(record, 'field', name='composicion_material').text=  str(row['x_studio_definir_otro_opcional'])
                if str(row['x_studio_caracterstica_compostable_opcional']) != '' and str(row['x_studio_caracterstica_compostable_opcional']) != 'nan': ET.SubElement(record, 'field', name='caracteristicas_compostable').text=  self.dic_caracteristica_compostable[str(row['x_studio_caracterstica_compostable_opcional'])]
                if str(row['x_studio_caracteristica_material']) != '' and str(row['x_studio_caracteristica_material']) != 'nan': ET.SubElement(record, 'field', name='caracteristicas_material').text=  self.dic_caracteristica_material[str(row['x_studio_caracteristica_material'])]
                if str(row['x_studio_productos_por_envase']) != '' and str(row['x_studio_productos_por_envase']) != 'nan': ET.SubElement(record, 'field', name='producto_por_envase').text=  str(row['x_studio_productos_por_envase'])
                if str(row['x_studio_proporcion_envase_m']) != '' and str(row['x_studio_proporcion_envase_m']) != 'nan': ET.SubElement(record, 'field', name='proporcion_por_envase').text=  str(row['x_studio_proporcion_envase_m'])

                #=========RAEE============
                if str(row['x_studio_raee']) != '' and str(row['x_studio_raee']) != 'nan': ET.SubElement(record, 'field', name='tipo_raee', ref=self.dic_tipo_raee[str(row['x_studio_raee'])])

                ##=========PILAS==========
                if str(row['x_studio_pilas']) != '' and str(row['x_studio_pilas']) != 'nan': ET.SubElement(record, 'field', name='tipo_de_pila', ref=self.dic_tipo_pila[str(row['x_studio_pilas'])])
                if str(row['x_studio_cantidad_pilas']) != '' and str(row['x_studio_cantidad_pilas']) != 'nan': ET.SubElement(record, 'field', name='cantidad_pilas').text=  str(row['x_studio_cantidad_pilas'])

                #========BATERIAS=========
                if str(row['x_studio_tipo_bateria']) != '' and str(row['x_studio_tipo_bateria']) != 'nan': ET.SubElement(record, 'field', name='tipo_bateria', ref=self.dic_tipo_bateria[str(row['x_studio_tipo_bateria'])])

                #==========ACEITES Y LUBRICANTES===========
                if str(row['x_studio_tipo_aceite_lubricante']) != '' and str(row['x_studio_tipo_aceite_lubricante']) != 'nan': ET.SubElement(record, 'field', name='tipo_aceite_lubricante', ref=self.dic_tipo_aceite_y_lubricante[str(row['x_studio_tipo_aceite_lubricante'])])
                if str(row['x_studio_volumen_m3']) != '' and str(row['x_studio_volumen_m3']) != 'nan': ET.SubElement(record, 'field', name='volumen').text=  str(row['x_studio_volumen_m3'])



                #===========NEUMATICOS=================
                if str(row['x_studio_tipo_neumatico']) != '' and str(row['x_studio_tipo_neumatico']) != 'nan': ET.SubElement(record, 'field', name='tipo_neumatico', ref=self.dic_neumaticos[str(row['x_studio_tipo_neumatico'])])
                if str(row['x_studio_cantidad_de_neumticos']) != '' and str(row['x_studio_cantidad_de_neumticos']) != 'nan': ET.SubElement(record, 'field', name='cantidad_neumatico').text=  str(row['x_studio_cantidad_de_neumticos'])

                #============TEXTIL==================
                if str(row['x_studio_material_textil']) != '' and str(row['x_studio_material_textil']) != 'nan': ET.SubElement(record, 'field', name='material_textil').text=  str(row['x_studio_material_textil'])
                if str(row['x_studio_ratio_textil']) != '' and str(row['x_studio_ratio_textil']) != 'nan': ET.SubElement(record, 'field', name='ratio_textil').text=  str(row['x_studio_ratio_textil'])


            file_materialidad = ET.ElementTree(odoo)
            file_materialidad.write('data_demo/output/demo_materialidad'+str(i+1)+'.xml', encoding="utf-8", xml_declaration=True)


#=========================
#==========MAIN===========
#=========================            
xml = XML()
xml.createTagId()
xml.createProductos()
xml.createPeriodos()
xml.createMarcas()
xml.createProveedor()
xml.createTrazabilidadLevantada()
xml.createActoresRelevantes()
xml.createDivision()
xml.createDepartamento()
xml.createSubDepartamento()
xml.createClase()
xml.createSubClase()
xml.createEquipo()
xml.createFamiliaPartes()
xml.createUnidadesVendidas()
xml.createMaterialidad()