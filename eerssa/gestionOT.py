from .constants import BoxesValues
from .constants import Current
from datetime import datetime
from pytz import timezone
from pprint import pprint

import os
import traceback

import pymupdf
from   pymupdf import Rect

import pickle
import json

import pandas as pd
pd.set_option("future.no_silent_downcasting", True)
import numpy as np



# this function defines if the directory is a PDF and from a valid producer:
# as of v0.10.2 there is support for FPFD 1.7 and pdf24
def isOT( pdf_path ):
  
  pdf = None

  try: 
    with pymupdf.open( pdf_path ) as pdf:

      if pdf.metadata['producer'] not in ['FPDF 1.7','PDF24']:
        return pdf.metadata['producer']
      
      if ( pdf.page_count < 4 ):       
        return True
      else:
        return pdf.page_count # Log error, too many pages.
  
  except Exception as e:
    return e  # Log error, not a valid "Orden de Trabajo PDF"


# CLASS DEFINITION

class GestionOt:
  
  VERSION = Current.VERSION.value


  # Areas where the information is to be extracted using PyMuPDF
  # boxes hoja 1 : primera cara

  bx_id_ot                  = Rect( BoxesValues.ID_OT.value )
  bx_numero_ot              = Rect( BoxesValues.NUMERO_OT.value )
  bx_gerencia               = Rect( BoxesValues.GERENCIA.value )
  bx_sitio                  = Rect( BoxesValues.SITIO.value )
  bx_fechaInicial_1         = Rect( BoxesValues.FECHA_INICIAL_UNO.value )

  bx_responsable            = Rect( BoxesValues.RESPONSABLE.value )
  bx_nombresColaboradores   = Rect( BoxesValues.COLABORADORES_NOMBRES.value)
  bx_cargosColaboradores    = Rect( BoxesValues.COLABORADORES_CARGOS.value)

  bx_vehiculoHoja1          = Rect( BoxesValues.DATOS_VEHICULO_HOJA_1.value )
  bx_tipos_trabajo          = Rect( BoxesValues.TIPOS_TRABAJO.value )
  bx_descripcion            = Rect( BoxesValues.DESCRIPCION.value)
  bx_fechaInicio_Testimado  = Rect( BoxesValues.FECHA_INICIO_TESTIMADO.value)
  bx_riesgos_epps           = Rect( BoxesValues.RIESGOS_EPPS.value)
  bx_medidas_seg            = Rect( BoxesValues.MEDIDAS_SEGURIDAD.value)
  bx_precauciones           = Rect( BoxesValues.PRECAUCIONES.value)
  bx_carencias              = Rect( BoxesValues.CARENCIAS.value)
  bx_firmas                 = Rect( BoxesValues.FIRMAS.value)

  # boxes hoja 2: reverso

  bx_cuadrilla              = Rect( BoxesValues.CUADRILLA_NOMBRE.value )
  bx_vehiculo               = Rect( BoxesValues.VEHICULO.value )
  bx_kilometraje            = Rect( BoxesValues.KILOMETRAJE.value )
  bx_actividades            = Rect( BoxesValues.ACTIVIDADES.value )
  bx_observaciones          = Rect( BoxesValues.OBSERVACIONES.value )
  bx_terminado              = Rect( BoxesValues.ESTADO_OT.value)
  bx_fechaFin               = Rect( BoxesValues.FECHA_FINAL.value)
  bx_accidentes             = Rect( BoxesValues.ACCIDENTES.value)


  # init method or constructor
  def __init__(self, link_to_pdf):
    self.link       = link_to_pdf
    self.version    = self.VERSION 
    self.createdAt  = None
    self.modifiedAt = []
    self.id_ot      = 0
    self.log        = []
    self.n_fallas   = 0
    self.n_errores  = 0
    self.n_revisar  = 0
    self.n_info     = 0
    self.data       = {}

    analisis_pdf    = isOT(link_to_pdf)

    if analisis_pdf == True:
      self.valido = True
      return

    if isinstance(analisis_pdf, str):
      producer_entry = {
                  "t": datetime.now().isoformat(),
                  "level"  : "FATAL",
                  "message": "El archivo PDF se encuentra en un formato no reconocido",
                  "detail" : f"Formato PDF: {analisis_pdf}"
      }
      self.log.append( producer_entry )
      self.n_fallas = 1
      self.valido = False
      return

    if isinstance(analisis_pdf, int):
      pages_entry = {
                  "t": datetime.now().isoformat(),
                  "level"  : "FATAL",
                  "message": "El archivo PDF tiene un numero no soportado de hojas",
                  "detail" : f"Hojas PDF: {analisis_pdf}"
      }
      self.log.append( pages_entry )
      self.n_fallas = 1
      self.valido = False
      return

    if isinstance( analisis_pdf, Exception ):
        falla_entry = {
                  "t": datetime.now().isoformat(),
                  "level"  : "FATAL",
                  "message": "El archivo indicado no es una Orden de Trabajo",
                  "detail" : traceback.format_exc( analisis_pdf )
        }
        self.log.append(falla_entry)
        self.n_fallas = 1
        return

  def DrawBoxesOt( self ):
    """ 
    Draw the fields with information to be extracted.

    :param str inputPDF_path: Path to the PDF File to be drawn uppon
    :return: The path to the created file, same directory as input or FALSE
    """
    try:
      doc = pymupdf.open( self.link )

      page_one = doc[0].new_shape()

      page_one.draw_rect( self.bx_id_ot          )
      page_one.draw_rect( self.bx_numero_ot      )
      page_one.draw_rect( self.bx_gerencia       )
      page_one.draw_rect( self.bx_sitio          )
      page_one.draw_rect( self.bx_fechaInicial_1 )
      page_one.draw_rect( self.bx_responsable       )
      page_one.draw_rect( self.bx_nombresColaboradores )
      page_one.draw_rect( self.bx_cargosColaboradores )
      page_one.draw_rect( self.bx_vehiculoHoja1  )
      page_one.draw_rect( self.bx_tipos_trabajo  )
      page_one.draw_rect( self.bx_descripcion )
      page_one.draw_rect( self.bx_fechaInicio_Testimado )
      page_one.draw_rect( self.bx_riesgos_epps )
      page_one.draw_rect( self.bx_medidas_seg )
      page_one.draw_rect( self.bx_precauciones )
      page_one.draw_rect( self.bx_carencias )
      page_one.draw_rect( self.bx_firmas )

      page_two = doc[1].new_shape()

      page_two.draw_rect( self.bx_cuadrilla )
      page_two.draw_rect( self.bx_vehiculo  )
      page_two.draw_rect( self.bx_kilometraje )
      page_two.draw_rect( self.bx_actividades )
      page_two.draw_rect( self.bx_observaciones )
      page_two.draw_rect( self.bx_terminado )
      page_two.draw_rect( self.bx_fechaFin )
      page_two.draw_rect( self.bx_accidentes )

      page_one.finish( color=(1, 0, 0), fill=None )
      page_two.finish( color=(1, 0, 0), fill=None )
      page_one.commit()
      page_two.commit()

      result = os.path.dirname(self.link)+ "/CAMPOS_version_"+ self.VERSION + ".pdf"

      doc.save(result)

      return result
    
    except:

      return False

  def Log2Ot( self, level, message, detail ):
    entry = {
      "t": datetime.now().isoformat(),
      "level"  : level,
      "message": message,
      "detail" : detail
    }
    self.log.append(entry)

    match level:
      case "FATAL":
        self.n_fallas += 1      
      case "ERROR":
        self.n_errores += 1
      case "REVISAR":
        self.n_revisar += 1
      case "INFO":
        self.n_info += 1
      case _:
        pass

  def load_ot( self ):
    try:
      with pymupdf.open( self.link ) as pdf:

        # Is it a Valid OT ?
        if self.valido == False:

          # Cannot create on an invalid OT
          self.Log2Ot("INFO", "No es posible la creacion de la OT", "No se puede crear una OT que no es valida")
          self.createdAt = datetime.now().isoformat(),
          return         # EXIT no more processing needed
        
        else: 
          # Log the creation of the OT
          self.Log2Ot("INFO", "Creacion de la OT", "Ninguno")
          self.createdAt = datetime.now().isoformat(),

        # 1. getId_Ot
        id_ot = self.getId_Ot( pdf[0], self.bx_id_ot )         
        
        if isinstance(id_ot, Exception):
          self.Log2Ot( "ERROR", "El archivo no tiene un ID automatico del sistema Intranet", traceback.format_exc( id_ot ) )
          return
        
        self.id_ot = id_ot
        self.data.update(
              {"version"    : self.version, 
               "link"       : self.link, 
               "id_ot"      : id_ot,
               "valido_ot"  : self.valido,
               "n_fallas"   : 0, ##  AQUI: Debería inicializarlas ?????
               "n_errores"  : 0, # no, mejor al final de todo.
               "n_revisar"  : 0,
              })
        

        

        


    except Exception as e:
      self.Log2Ot( "FATAL", "Error desde la funcion load_Ot()", traceback.format_exception(e) )
    

  def getId_Ot( self, hoja, box ):
    try:
      texto = hoja.get_text( clip = box )
      id_ot = texto
      id_ot = id_ot.split('\n')[1].replace(',',"")
      id_ot = int(id_ot)
      return id_ot
    
    except Exception as e:
      return e
    

  def getNumeracion( self, hoja, box ):
    try:
      texto = hoja.get_text( clip = box )
      numeracion = texto
      numeracion = numeracion.replace('NM:', "").replace(',', "").strip()
      numeracion = int(numeracion)
    except:
      ic({"archivo: ": hoja, "variable: ":texto})
      numeracion = 0
    return numeracion


  def getGerencia( self, hoja, box ):
    try:
      texto = hoja.get_text( clip = box ).strip()
      gerencia = texto
    except:
      ic({"archivo: ": hoja, "variable: ":texto})
      gerencia = "·"
    return gerencia


  def getSitio( self, hoja, box ):
    try:
      sitio = hoja.get_text( clip = box ).strip()
    except:
      ic({"archivo: ": hoja, "variable: ":sitio})
      sitio = "·"
    return sitio


  def getFechaInicio( self, hoja, box ):
    try:
      fechaInicio = hoja.get_text( clip = box ).strip()
    except:
      ic({"archivo: ": hoja, "variable: ":fechaInicio})
      fechaInicio = "·"
    return fechaInicio


  def toDateEcuador( fecha ):
      try:
          meses_a_numero = {
              'enero' : '01',
              'febrero' : '02',
              'marzo' : '03',
              'abril' : '04',
              'mayo' : '05',
              'junio' : '06',
              'julio' : '07',
              'agosto' : '08',
              'septiembre' : '09',
              'octubre' : '10',
              'noviembre' : '11',
              'diciembre' : '12'
          }

          fechaString = fecha.lower()

          fechaString = (
              fechaString
              .split(',')[1]
              .strip()
              .replace('del ', '')
              .replace('de ', '')
              )

          for mes, numero in meses_a_numero.items():
              fechaString = fechaString.replace(mes, numero)

          respuesta = fechaString.split(' ')
          respuesta = '/'.join(respuesta)
          date_object = datetime.strptime(respuesta, '%d/%m/%Y')
          ecuador = timezone("America/Guayaquil")
          local_datetime = ecuador.localize(date_object)


      except:
          ic({"archivo: ": fecha, "variable: ": fechaString})
          local_datetime = fecha

      return local_datetime
  

  def getDiaSemana( fechaInicio ):
    try:
      diaSemana = fechaInicio.split(',')[0]
    except:
      ic({"archivo: ": fechaInicio, "variable: ":diaSemana})
      diaSemana = "·"
    return diaSemana


  def getResponsable( self, hoja, box ):
      try:
          texto = hoja.get_text( clip = box)
          df_personal = texto
          df_personal = df_personal.strip().split('\n')
          responsable = [df_personal[0],df_personal[1]]
      except:
          ic({"archivo: ": hoja, "variable: ":texto})
          responsable = "·"
      return responsable


  def getColaboradores( self, hoja, box_colab, box_cargos ):
      try:
          texto = hoja.get_text( clip = box_colab )
          df_personal = texto
          df_personal = df_personal.strip().split('\n')
          df_personal = [ item for item in df_personal if item != '' ]

          data = hoja.get_text( clip = box_cargos )
          df_cargos = data
          df_cargos = df_cargos.strip().split('\n')
          df_cargos = [ item for item in df_cargos if item != '' ]

          totalColaboradores = len(df_personal)

          colaboradores = []
          for i in range(totalColaboradores):
              colaboradores.append([df_personal[i],df_cargos[i]])
      except:
          ic({"archivo: ": hoja, "Nombres: ":texto, "Cargo: ":data})
          totalColaboradores = 0
          colaboradores = []

      respuesta = {}
      respuesta['total'] = totalColaboradores
      respuesta['nombres'] = colaboradores
      return respuesta


  def getVehiculo( self, hoja, box ):
    try:
      texto = hoja.get_text( clip = box ).strip().split('\n')
      df_vehiculo = texto

      if df_vehiculo[3] == 'Placa:':  # Hay un vehículo

        data_vehiculo={}
        data_vehiculo['numero'] = df_vehiculo[2]
        data_vehiculo['placa'] = df_vehiculo[4]
        data_vehiculo['marca'] = df_vehiculo[6]
        data_vehiculo['rentado'] = df_vehiculo[8]
        data_vehiculo['propietario'] = df_vehiculo[10]

        if len(df_vehiculo) == 13:
          data_vehiculo['chofer'] = df_vehiculo[12]
        else:
          data_vehiculo['chofer'] = "·"

      else:
        data_vehiculo={}
        data_vehiculo['numero'] = "·"
        data_vehiculo['placa'] = "·"
        data_vehiculo['marca'] = "·"
        data_vehiculo['rentado'] = "·"
        data_vehiculo['propietario'] = "·"
        data_vehiculo['chofer'] = "·"

    except:
      ic({"archivo: ": hoja, "variable: ":texto})
      data_vehiculo = "·"

    return data_vehiculo


  def getTiposTrabajo( self, hoja, box ):
    try:
      df_tipos_trabajo = hoja.find_tables( clip = box )
      df_tipos_trabajo = df_tipos_trabajo.tables[0].to_pandas()
      df_tipos_trabajo = df_tipos_trabajo.to_numpy().flatten()
      df_tipos_trabajo = [ item for item in df_tipos_trabajo if item != '' ]
    except:
      ic(hoja)
      df_tipos_trabajo = "·"
    return df_tipos_trabajo


  def getDescripcion( self, hoja, box ):
    try:
      descripcion = hoja.get_text( clip = box ).strip()
    except:
      ic({"archivo: ": hoja, "variable: ":descripcion})
      descripcion = "·"
    return descripcion


  def getFechaInicio2( self, hoja, box ):

    find_word_index = lambda word_list, target_word: word_list.index(target_word) if target_word in word_list else -1

    try:
      texto = hoja.get_text( clip = box ).strip().split('\n')
      fechaInicio2 = texto
      index = find_word_index(fechaInicio2, 'TIEMPO ESTIMADO DE DURACIÓN (HORAS):')

      if index != -1:
        fechaInicio2 = fechaInicio2[index - 1]
      else:
        ic(fechaInicio2)
        fechaInicio2 = "·"
    except:
      ic({"archivo: ": hoja, "variable: ":texto})
      fechaInicio2 = "·"
    return fechaInicio2


  def getTiempoEstimado( self, hoja, box ):

    find_word_index = lambda word_list, target_word: word_list.index(target_word) if target_word in word_list else -1

    try:
      texto = hoja.get_text( clip = box ).strip().split('\n')
      Testimado = texto
      index = find_word_index(Testimado, 'TIEMPO ESTIMADO DE DURACIÓN (HORAS):')

      if index != -1:
        Testimado = Testimado[index + 1]
      else:
        ic(Testimado)
        Testimado = "·"
    except:
      ic({"archivo: ": hoja, "variable: ":texto})
      Testimado = "·"
    return Testimado


  def getRiesgos(self, hoja, box ):
      riesgos_dict = {}
      try:
          df_riesgos = hoja.find_tables( clip = box )
          df_riesgos = df_riesgos.tables[0].to_pandas().replace('', np.nan).dropna(how = 'all')
          for _, row in df_riesgos.iterrows():
              key = row['RIESGOS EXISTENTES:']
              value = [row[col] for col in df_riesgos.columns if col != 'RIESGOS EXISTENTES:']
              riesgos_dict[key] = value
      except:
          ic(hoja)
          riesgos_dict = "·"
      return riesgos_dict


  def getMedidasSeguridad( self, hoja, box ):
      try:
          df_medidas_seg = hoja.find_tables( clip = box )
          df_medidas_seg = df_medidas_seg.tables[0].to_pandas()
          df_medidas_seg = df_medidas_seg[['0-MEDIDAS','1-ESTADO']].replace('', np.nan).dropna(how = 'all')
          df_medidas_seg = dict(zip(df_medidas_seg['0-MEDIDAS'],df_medidas_seg['1-ESTADO']))

      except:
          ic(hoja)
          df_medidas_seg = "·"
      return df_medidas_seg


  def getEPPs( self, hoja, box ):
      try:
          df_epps = hoja.find_tables( clip = box )
          df_epps = df_epps.tables[0].to_pandas()
          df_epps = df_epps[['2-EQUIPOS DE PROTECCIÓN','3-ESTADO']].replace('', np.nan).dropna(how = 'all')
          df_epps = dict(zip(df_epps['2-EQUIPOS DE PROTECCIÓN'],df_epps['3-ESTADO']))

      except:
          ic(hoja)
          df_epps = "·"
      return df_epps


  def getPrecauciones( self, hoja, box ):
      try:
          precauciones = hoja.get_text( clip = box ).strip()
          precauciones = precauciones.replace('PRECAUCIONES:', "").strip()
      except:
          ic({"archivo: ": hoja, "variable: ":precauciones})
          precauciones = "·"
      return precauciones


  def getCarencias( self, hoja, box ):
      try:
          carencias = hoja.get_text( clip = box ).strip()
          carencias = carencias.replace('CARENCIAS:', "").strip()
      except:
          ic({"archivo: ": hoja, "variable: ":carencias})
          carencias = "·"
      return carencias


  def getFechaInicioHoja1( self, hoja, box ):
      try:
          df_fecha_final = hoja.find_tables( clip = box )
          df_fecha_final = df_fecha_final.tables[0].to_pandas()
          df_fecha_final = df_fecha_final.iloc[1,0].strip().split(':')
          df_fecha_final = df_fecha_final[1].strip()
      except:
          ic(hoja)
          df_fecha_final = "·"
      return df_fecha_final


  def getFirmas( self, hoja, box ):
      try:
          df_firmas = hoja.find_tables( clip = box )
          df_firmas = df_firmas.tables[0].to_pandas()
          df_firmas = df_firmas.iloc[0,:].to_list()
          df_firmas = [ item for item in df_firmas if item != '' ]
          df_firmas = df_firmas[1:]
      except:
          ic(hoja)
          df_firmas = "·"
      return df_firmas


  def getCuadrilla( self, hoja, box ):
      try:
          cuadrilla = hoja.get_text( clip = box ).strip()
      except:
          ic({"archivo: ": hoja, "variable: ":cuadrilla})
          cuadrilla = "·"
      return cuadrilla


  def getKilometraje( self, hoja, box ):
      try:
          df_kilometraje = hoja.find_tables( clip = box )
          df_kilometraje = df_kilometraje.tables[0].header.names
          kmInicio = int(df_kilometraje[2].replace(',',""))
          kmFinal = int(df_kilometraje[4].replace(',',""))
          kmRecorrido = int(df_kilometraje[6].replace(',',""))
      except:
          ic(hoja)
          kmInicio = "·"
          kmFinal = "·"
          kmRecorrido = "·"
      return kmInicio, kmFinal, kmRecorrido


  def getActividades( self, hoja, box ):
      try:
          df_actividades = hoja.find_tables( clip = box, strategy = 'lines_strict' )
          df_actividades = df_actividades.tables[0].to_pandas()
          df_actividades.columns = ['Item','Actividad','Descipcion','Ali','Alimentador','Tipo','FechaInicial','FechaFinal']

          while len(df_actividades.iloc[0,0]) > 2:
              df_actividades = df_actividades.drop(0)
              df_actividades = df_actividades.reset_index(drop=True)

          df_actividades['FechaInicial'] = df_actividades['FechaInicial'].str.replace('\n', ' ')
          df_actividades['FechaFinal']   = df_actividades['FechaFinal'].str.replace('\n', ' ')
          df_actividades = df_actividades.replace('', np.nan).dropna(how='all')
          df_actividades = df_actividades.replace(np.nan, "·" )
          df_actividades = df_actividades.to_dict('records')
      except:
          ic(hoja)
          df_actividades = "·"
      return df_actividades


  def getObservaciones( self, hoja, box ):
      try:
          observaciones = hoja.get_text( clip = box ).strip()
      except:
          ic({"archivo: ": hoja, "variable: ":observaciones})
          observaciones = "·"
      return observaciones


  def getTerminado( self, hoja, box ):
      try:
          terminado = hoja.get_text( clip = box ).strip()
      except:
          ic({"archivo: ": hoja, "variable: ":terminado})
          terminado = "·"
      return terminado


  def getFechaFinal2( self, hoja, box ):
      try:
          fechaFinal2 = hoja.get_text( clip = box ).strip()
      except:
          ic({"archivo: ": hoja, "variable: ":fechaFinal2})
          fechaFinal2 = "·"
      return fechaFinal2


  def getAccidentes( self, hoja, box ):
      try:
          accidentes = hoja.get_text( clip = box ).strip()
      except:
          ic({"archivo: ": hoja, "variable: ":accidentes})
          accidentes = "·"
      return accidentes







