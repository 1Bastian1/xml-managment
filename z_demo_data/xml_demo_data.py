import xml.etree.cElementTree as ET
import pandas as pd




#========DICCIONARIOS==================
# Diccionarios necesario para manejar los campos select y las entradas para alguno 
# many2one que ya estan registrados (eye, raee, pilas, etc...)
dic_origen ={
    "NACIONAL"  :"nacional",
    "IMPORTADO" :"importado"
}

dic_categoria_elemento= {
    "EYE Domiciliario"      : "eye_domiciliario",
    "EYE NO Domiciliario"   : "eye_no_domiciliario",
    "RAEE"                  : "raee",
    "PILAS"                 : "pilas",
    "Baterias"              : "baterias",
    "Aceites y Lubricantes" : "aceites_y_lubricantes",
    "Neumaticos"            : "neumaticos",
    "Textil"                : "textil"
}

dic_tipo_parte = {
    "PRIMARIO"      : "primario",
    "SECUNDARIO"    : "secundario",
    "TERCIARIO"     : "terciario",
    "NO APLICA"     : "no_aplica"
}

dic_caracteristica_reciclable = {
    "sin material reciclado"  : "sin_material_reciclado",
    ">10% material reciclado" : "porcentaje_10",
    ">25% material reciclado" : "porcentaje_25",
    ">50% material reciclado" : "porcentaje_50",
    ">80% material reciclado" : "porcentaje-80",
    "100% material reciclado" : "porcentaje_100"
}

dic_caracteristica_retornable = {
    "no retornable"         : "no_retornable",
    "retornable nuevo"      : "retornable_nuevo",
    "retornable recuperado" : "retornable_recuperado"
}

dic_peligrosidad = {
    "residuo NO peligroso" : "residuo_no_peligroso",
    "residuo peligroso" : "residuo_peligroso",
}

dic_materiales_eye = {
    "Otros envases PET (1)" : "data_tipo_eye_otros_envases_PET",
    "Envases de PP que NO contienen sustancias con grasa (5)" : "data_tipo_eye_pp_no_sustancias_grasas",
    "Envases de PP que contienen sustancias con grasa (5)" : "data_tipo_eye_pp_contiene_sustancias_grasa",
    "Envases de PEBD que NO contienen sustancias con grasa (4)" : "data_tipo_eye_pebd_no_sustancias_grasa",
    "(3)PVC" : "data_tipo_eye_pvc",
    "Envases de PEAD que NO contienen sustancias con grasa (2)" : "data_tipo_eye_pead_no_sustancias_grasa",
    "Otros envases plásticos (7)" : "data_tipo_eye_otro_envase_plastico",
    "Hojalata" : "data_tipo_eye_hojalata",
    "Botellas PET (1)" : "data_tipo_eye_botella_pet",
    "Envases de PS que NO contienen sustancias con grasa (6)" : "data_tipo_eye_ps_sustancias_grasa",
    "Otro papel compuesto" : "data_tipo_eye_otro_papel_compuesto",
    "Envases de PEBD que contienen sustancias con grasa (4)" : "data_tipo_eye_pebd_sustancias_grasa_4",
    "Envases de PEAD que contienen sustancias con grasa (2)" : "data_tipo_eye_pebd_sustancias_grasa_2",
    "Envases de PS que contienen sustancias con grasa (6) y envases de EPS" : "data_tipo_eye_ps_sustancias_grasa_y_envase_eps",
    "Madera" : "data_tipo_eye_madera",
    "Otro material" : "data_tipo_eye_otro_material",
    "Cartón" : "data_tipo_eye_carton",
    "Cartón para bebidas y alimentos" : "data_tipo_eye_carton_bebidas_alimentos",
    "Papel" : "data_tipo_eye_papel",
    "Vidrio" : "data_tipo_eye_vidrio",
    "Aluminio (latas)" : "data_tipo_eye_aluminios_latas",
    "Envases de aluminio" : "data_tipo_eye_envase_aluminio",
    "Metal con aire comprimido" : "data_tipo_eye_material_aire_comprimido",
    "Otros envases de metal" : "data_tipo_eye_motro_envase_metal",
    "Plástico compostable" : "data_tipo_eye_plastico_compostable"
}

dic_caracteristica_compostable = {
    "envase de servicio" : "envase_de_servicio",
    "envase general" : "envase_general",
    "no aplica" : "no_aplica"
}

dic_caracteristica_material = {
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
    "engomado"      : "engomado"
}

dic_tipo_raee = {
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

dic_tipo_pila = {
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

dic_tipo_bateria = {
    "De plomo para vehiculos motorizados" : "data_tipo_bateria_plomo_vehiculo_motorizado",
    "De plomo industriales" : "data_tipo_bateria_plomo_industriales",
    "Otras baterias, pilas o acumuladores para vehiculos motorizados" : "data_tipo_bateria_otras_baterias"
}

dic_tipo_aceite_y_lubricante ={
    "Aceites Lubricantes No Recuperables" : "data_tipo_aceite_lubri_no_recuperable",
    "Aceites Lubricantes Recuperables" : "data_tipo_aceite_lubri_recuperable"
}

dic_neumaticos = {
    "CATEGORÍA A"   : "data_tipo_neumatico_categoria_A",
    "CATEGORÍA B"   : "data_tipo_neumatico_categoria_b",
    "MACIZOS"       : "data_tipo_neumatico_macizo",
    "Bicicletas, sillas de rueda y similares" : "data_tipo_neumatico_macizo_bicicleta_silla_de_rueda_similares"
}

dic_produstos_stage = {
    "No completado - Nuevo"         : "data_productos_stage_no_completado_nuevo",
    "No completado - En revisión"   : "data_productos_stage_no_completado_en_revision",
    "Proyectado"                    : "data_productos_stage_proyectado",
    "Completado parcial"            : "data_productos_stage_completado_parcial",
    "Completado"                    : "data_productos_stage_completado"
}

dic_trazabilidad_stage = {
    "Nuevo" : "data_trazabilidad_stage_nuevo",
    "Contacto inválido" : "data_trazabilidad_candidato_envalido",
    "Comunicación establecida" : "data_trazabilidad_comunicacion_establecida",
    "Información recibida" : "data_trazabilidad_informacion_recibida",
    "Proceso concluido" : "data_trazabilidad_proceso_concluido"
}


#=======CLASE XML======================
class XML:

    #======FUNCIONES ADICIONALES=========
    # Funcionalidades extras para manejo y convercion de datos
    def createStringMany2ManyPeriodo(self, array):
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
            ref = ref + "ref('demo_periodo_"+data+"')"
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

    #======FUNCIONES XML=============
    # Funciones encargadas de crear los xml por cada uno de los modelos
    # de la plataforma

    def createPeriodo(self):
        df_periodo = pd.read_csv('z_demo_data/demo_periodo.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo')
        for index, row in df_periodo.iterrows():
            id_name = str(row['name']).lower()
            id_name = id_name.replace(" ","_")
            id_name = id_name.replace(".","_")
            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.periodo', id='demo_periodo_'+id_name)
            
            ET.SubElement(record, 'field', name='name').text=  str(row['name'])


        file_periodo = ET.ElementTree(odoo)
        file_periodo.write('z_demo_data/demo_periodo.xml', encoding="utf-8", xml_declaration=True)

    def createMarca(self):
        df_marca = pd.read_csv('z_demo_data/demo_marca.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo')
        for index, row in df_marca.iterrows():
            id_name  = self.lowerAndReplace(str(row['name']))   
            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.marca', id='demo_marca_'+id_name)
            
            ET.SubElement(record, 'field', name='name').text=  str(row['name'])

        file_marca = ET.ElementTree(odoo)
        file_marca.write('z_demo_data/demo_marca.xml', encoding="utf-8", xml_declaration=True)

    def createProveedor(self):
        df_proveedor = pd.read_csv('z_demo_data/demo_proveedores.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo')
        for index, row in df_proveedor.iterrows():
            id_name  = self.lowerAndReplace(str(row['name']))
            record = ET.SubElement(odoo, 'record', model='res.partner', id='demo_proveedor_'+id_name)

            ET.SubElement(record, 'field', name='name').text=  str(row['name'])

        file_proveedor = ET.ElementTree(odoo)
        file_proveedor.write('z_demo_data/demo_proveedores.xml', encoding="utf-8", xml_declaration=True)
    
    def createActorRelevantes(self):
        df_actores_relevantes = pd.read_csv('z_demo_data/demo_actores_relevantes.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo')
        for index, row in df_actores_relevantes.iterrows():
            id_name  = self.lowerAndReplace(str(row['name']))
            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.act_relev', id='demo_actores_relevantes_'+id_name)

            ET.SubElement(record, 'field', name='name').text=  str(row['name'])
        
        file_actores_relevantes = ET.ElementTree(odoo)
        file_actores_relevantes.write('z_demo_data/demo_actores_relevantes.xml', encoding="utf-8", xml_declaration=True)

    def createTrazabilidadLevantamiento(self):
        df_trazabilidad_levantamiento = pd.read_csv('z_demo_data/demo_trazabilidad_levantada.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo')
        for index, row in df_trazabilidad_levantamiento.iterrows():
            id_name  = self.lowerAndReplace(str(row['name'])) 
            periodos = self.createStringMany2ManyPeriodo(str(row['periodo']).split(','))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.traz_lev', id='demo_trazabilidad_levantada_'+id_name)

            ET.SubElement(record, 'field', name='name').text=  str(row['name'])
            ET.SubElement(record, 'field', name='periodo', eval=f"[(6, 0, [{periodos}])]")
            if str(row['etapa_trazabilidad']) != '' : ET.SubElement(record, 'field', name='etapa_trazabilidad', ref=dic_trazabilidad_stage[str(row['etapa_trazabilidad'])])
        
        file_trazabilidad_levantada = ET.ElementTree(odoo)
        file_trazabilidad_levantada.write('z_demo_data/demo_trazabilidad_levantada.xml', encoding="utf-8", xml_declaration=True)

    def createProductos(self):
        df_productos = pd.read_csv('z_demo_data/demo_productos.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo')
        for index, row in df_productos.iterrows():
            id_name  = self.lowerAndReplace(str(row['name']))
            periodos = self.createStringMany2ManyPeriodo(row['periodo'].split(','))
            id_marca = self.lowerAndReplace(str(row['marca']))
            id_proveedor = self.lowerAndReplace(str(row['proveedor']))
            id_trazabilidad = self.lowerAndReplace(str(row['trazabilidad_levantamiento'])) 
            id_actor_relev  = self.lowerAndReplace(str(row['actor_relevante']))


            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.producto', id='demo_productos_'+id_name) 

            

            ET.SubElement(record, 'field', name='name').text=  str(row['name'])
            # ET.SubElement(record, 'field', name='tag_id').text=  str(row['tag_id'])   many2many
            ET.SubElement(record, 'field', name='periodo', eval=f"[(6, 0, [{periodos}])]")
            ET.SubElement(record, 'field', name='descripcion').text=  str(row['descripcion'])
            ET.SubElement(record, 'field', name='marca', ref='demo_marca_'+id_marca)
            ET.SubElement(record, 'field', name='ean').text=  str(row['ean'])
            ET.SubElement(record, 'field', name='codigo_ref_proveedor').text=  str(row['codigo_ref_proveedor'])
            ET.SubElement(record, 'field', name='proveedor', ref='demo_proveedor_'+id_proveedor)
            ET.SubElement(record, 'field', name='trazabilidad_levantamiento', ref='demo_trazabilidad_levantada_'+id_trazabilidad)
            ET.SubElement(record, 'field', name='actor_relevante', ref='demo_actores_relevantes_'+id_actor_relev)
            ET.SubElement(record, 'field', name='origen').text=  dic_origen[str(row['origen'])]
            if str(row['eye']) != '' : ET.SubElement(record, 'field', name='eye').text=  str(row['eye'])
            if str(row['raee']) != '' : ET.SubElement(record, 'field', name='raee').text=  str(row['raee'])
            if str(row['pilas']) != '' : ET.SubElement(record, 'field', name='pilas').text=  str(row['pilas'])
            if str(row['neumaticos']) != '' : ET.SubElement(record, 'field', name='neumaticos').text=  str(row['neumaticos'])
            if str(row['baterias']) != '' : ET.SubElement(record, 'field', name='baterias').text=  str(row['baterias'])
            if str(row['aceite_y_lubrcante']) != '' : ET.SubElement(record, 'field', name='aceite_y_lubrcante').text=  str(row['aceite_y_lubrcante'])
            if str(row['textil']) != '' : ET.SubElement(record, 'field', name='textil').text=  str(row['textil'])

            if str(row['stage_id']) != '' : ET.SubElement(record, 'field', name='stage_id', ref=dic_produstos_stage[str(row['stage_id'])])



        file_productos = ET.ElementTree(odoo)
        file_productos.write('z_demo_data/demo_productos.xml', encoding="utf-8", xml_declaration=True)

    def createFamiliaPartes(self):
        df_familiapartes = pd.read_csv('z_demo_data/demo_familia_de_partes.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo') 
        for index, row in df_familiapartes.iterrows():
            id_name  = self.lowerAndReplace(str(row['name']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.familia_de_partes', id='demo_familia_de_partes_'+id_name) 
            
            ET.SubElement(record, 'field', name='name').text=  str(row['name'])


        file_familia_partes = ET.ElementTree(odoo)
        file_familia_partes.write('z_demo_data/demo_familia_de_partes.xml', encoding="utf-8", xml_declaration=True)

    def createMaterialidad(self):
        df_materialidad = pd.read_csv('z_demo_data/demo_materialidad.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo') 
        for index, row in df_materialidad.iterrows():
            id_name  = self.lowerAndReplace(str(row['name']))+'_'+str(row['producto'])
            id_familia_partes =  self.lowerAndReplace(str(row['familia_de_partes']))

            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.materialidad', id='demo_materialidad_'+id_name) 

            #=== DATA INCIAL ===
            ET.SubElement(record, 'field', name='name').text=  str(row['name'])
            if id_familia_partes != '' : ET.SubElement(record, 'field', name='familia_de_partes', ref='demo_familia_de_partes_'+id_familia_partes)
            ET.SubElement(record, 'field', name='producto', ref='demo_productos_'+str(row['producto']))
            ET.SubElement(record, 'field', name='descripcion').text=  str(row['descripcion'])
            ET.SubElement(record, 'field', name='peso_informado').text=  str(row['peso_informado'])
            ET.SubElement(record, 'field', name='categoria_elemento').text=  dic_categoria_elemento[str(row['categoria_elemento'])]

            #=== EYE ===
            if str(row['tipo_de_parte']) != '' :ET.SubElement(record, 'field', name='tipo_de_parte').text=  dic_tipo_parte[str(row['tipo_de_parte'])]
            if str(row['caracteristicas_reciclable']) != '' :  ET.SubElement(record, 'field', name='caracteristicas_reciclable').text=  dic_caracteristica_reciclable[str(row['caracteristicas_reciclable'])]
            if str(row['caracteristicas_retornable']) != '' :  ET.SubElement(record, 'field', name='caracteristicas_retornable').text=  dic_caracteristica_retornable[str(row['caracteristicas_retornable'])]
            if str(row['peligrosidad']) != '' :  ET.SubElement(record, 'field', name='peligrosidad').text=  dic_peligrosidad[str(row['peligrosidad'])]
            if str(row['maetrial']) != '' :  ET.SubElement(record, 'field', name='maetrial', ref=dic_materiales_eye[str(row['maetrial'])])
            ET.SubElement(record, 'field', name='composicion_material').text=  str(row['composicion_material'])
            if str(row['caracteristicas_compostable']) != '' :ET.SubElement(record, 'field', name='caracteristicas_compostable').text=  dic_caracteristica_compostable[str(row['caracteristicas_compostable'])]
            if str(row['caracteristicas_material']) != '' :ET.SubElement(record, 'field', name='caracteristicas_material').text=  dic_caracteristica_material[str(row['caracteristicas_material'])]
            ET.SubElement(record, 'field', name='producto_por_envase').text=  str(row['producto_por_envase'])
            ET.SubElement(record, 'field', name='proporcion_por_envase').text=  str(row['proporcion_por_envase'])

            #=== RAEE ===
            if str(row['tipo_raee']) != '' :ET.SubElement(record, 'field', name='tipo_raee', ref=dic_tipo_raee[str(row['tipo_raee'])])

            #=== PILAS ===
            if str(row['tipo_de_pila']) != '' :ET.SubElement(record, 'field', name='tipo_de_pila', ref=dic_tipo_pila[str(row['tipo_de_pila'])])
            ET.SubElement(record, 'field', name='cantidad_pilas').text=  str(row['cantidad_pilas'])

            #=== BATERIAS ===
            if str(row['tipo_bateria']) != '' :ET.SubElement(record, 'field', name='tipo_bateria', ref=dic_tipo_bateria[str(row['tipo_bateria'])])
            ET.SubElement(record, 'field', name='name_bateria').text=  str(row['name_bateria'])

            #=== ACEITE Y LUBRICANTE ===
            if str(row['tipo_aceite_lubricante']) != '' :ET.SubElement(record, 'field', name='tipo_aceite_lubricante', ref=dic_tipo_aceite_y_lubricante[str(row['tipo_aceite_lubricante'])])
            if str(row['volumen']) != '' :ET.SubElement(record, 'field', name='volumen').text=  str(row['volumen'])

            #=== NEUMATICOS ===
            if str(row['tipo_neumatico']) != '' :ET.SubElement(record, 'field', name='tipo_neumatico', ref=dic_neumaticos[str(row['tipo_neumatico'])])
            if str(row['cantidad_neumatico']) != '' :ET.SubElement(record, 'field', name='cantidad_neumatico').text=  str(row['cantidad_neumatico'])

            #=== TEXTIL ===
            if str(row['material_textil']) != '' :ET.SubElement(record, 'field', name='material_textil').text=  str(row['material_textil'])
            if str(row['ratio_textil']) != '' :ET.SubElement(record, 'field', name='ratio_textil').text=  str(row['ratio_textil'])


        file_productos = ET.ElementTree(odoo)
        file_productos.write('z_demo_data/demo_materialidad.xml', encoding="utf-8", xml_declaration=True)

    def createUnidadesVendidas(self):
        df_unidades_vendidas = pd.read_csv('z_demo_data/demo_unidades_vendidas.csv', keep_default_na=False)
        declaration = ET.Element("<?xml", version="1.0", encoding="utf-8")
        odoo =  ET.Element('odoo') 
        for index, row in df_unidades_vendidas.iterrows():
            id_name  = self.lowerAndReplace(str(row['name']))
            record = ET.SubElement(odoo, 'record', model='levantamiento_rep.unidades_vendidas', id='demo_unidades_vendidas_'+str(index)) 

            ET.SubElement(record, 'field', name='name').text= id_name
            if str(row['periodo']) != '' :  ET.SubElement(record, 'field', name='periodo', ref="demo_periodo_"+str(row['periodo']))
            if str(row['producto']) != '' :  ET.SubElement(record, 'field', name='producto', ref="demo_productos_"+str(row['producto']))
            if str(row['unidades_vendidas']) != '' :  ET.SubElement(record, 'field', name='unidades_vendidas').text=  str(row['unidades_vendidas'])
            

        
        file_unidades_vendidas = ET.ElementTree(odoo)
        file_unidades_vendidas.write('z_demo_data/demo_unidades_vendidas.xml', encoding="utf-8", xml_declaration=True)



#=====================
#========MAIN=========
#=====================

xml = XML()
xml.createPeriodo()
xml.createMarca()
xml.createProveedor()
xml.createActorRelevantes()
xml.createTrazabilidadLevantamiento()
xml.createProductos()
xml.createFamiliaPartes()
xml.createMaterialidad()
xml.createUnidadesVendidas()
