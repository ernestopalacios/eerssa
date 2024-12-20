
from eerssa import gestionOT

from dask.distributed import LocalCluster


def isOT( pdf_path ):
  
  pdf = None

  try: 
    with pymupdf.open( pdf_path ) as pdf:

      if pdf.metadata['producer'] not in ['FPDF 1.7']:  # TODO: Agregar PDF24
        return False
      else:
        return True
  except:
    return False # TODO: Log error, not a valid "Orden de Trabajo PDF"


print("Hola Mundo!")