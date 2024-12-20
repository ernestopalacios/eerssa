from .constants import BoxesValues
from .constants import Current
from datetime import datetime
from pytz import timezone
from pprint import pprint

import os

import pymupdf
from   pymupdf import Rect

import pickle
import json

import pandas as pd
pd.set_option("future.no_silent_downcasting", True)
import numpy as np

from icecream import ic
ic.configureOutput( prefix = '\not_pdf| ', includeContext=True)

# this function defines if the directory is a PDF and from a valid producer:
# as of v0.10.2 there is support for FPFD 1.7 and pdf24
def isOT( pdf_path ):
  
  pdf = None

  try: 
    with pymupdf.open( pdf_path ) as pdf:

      if pdf.metadata['producer'] not in ['FPDF 1.7','PDF24']:  # TODO: Agregar PDF24
        return False
      else:
        return True
  except:
    return False # TODO: Log error, not a valid "Orden de Trabajo PDF"


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
    self.link     = link_to_pdf
    self.valido   = isOT(link_to_pdf)



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