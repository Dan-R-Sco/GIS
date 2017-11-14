#
#  author:  XXXX
#  CLIENTE: XXX
#
__doc__ = """ """  
import os, sys  
import arcpy  
from arcpy import env  
import argparse


#mxd = arcpy.mapping.MapDocument("CURRENT")

#

a = 1 == 2
ingreso = r"e:\ora\smurfit\a1"
salida =  r"e:\ora\smurfit\a2"


  
if __name__ == '__main__':  
  parser = argparse.ArgumentParser(description="Cambio de fuente tipo .SDE", usage='%(prog)s [options]' )
  
  parser.add_argument('--inicio', action='store', dest='inicio', default='C:\\', help='Directorio con los MXD')  
  parser.add_argument('--salida', action='store', dest='salida', default=None, help='Directorio de Salida') 
  parser.add_argument('--fuentes', action='store', dest='osource', default='c:\\gis\\conexion\\Pconsulta.sde',  help='more than one Sources ? Modificar separadas por coma,\n\t por ej: "C:\\x\\a.sde,C:\\Documents and Settings\\user\\Datos de programa\\ESRI\ArcCatalog\\Pconsulta.sde"') 
  parser.add_argument('--fuenteNueva', action='store', dest='nsource', default=None, help='Nuevo source, por ej: X:\\gis\\Productivo.sde') 
  parser.add_argument('--filtro',action='store', dest='filtro', default='mxd', choices=('mxd','lyr'), help='Seleccionar tipo: mxd o lyr')
  #boolean  
  parser.add_argument('--listar', action='store_true', dest='listonly', default=False,help='Solo Lista las fuentes actuales.')  
  
  
  #(options, args) = parser.parse_args() 
  options = parser.parse_args() 

def get_all_files(options, startpath, filter, norecursivo):  
  files = []  
  for filename in os.listdir(startpath):  
    f = os.path.join(startpath,filename)  
    if os.path.isdir(f) and not norecursivo:
      print " "  
      print "Directorio ====> %s" % (f) 
      try: 
       result = get_all_files(options, f, filter, norecursivo) 
      except:
       result = None 
      if result is not None:  
        files += result  
    if f.upper().endswith(filter.upper()):  
      files.append(f.upper())  
  if files is not None and len(files) > 0:  
    files.sort()  
  return files  
  
filtro = "."+options.filtro

if options.listonly:
   lista =[]
   i =0
   print "Listando archivos ===> "+filtro
   print "------------------------------------------------"
   filelist = get_all_files(options, options.inicio,filtro, False)
   if filelist is not None:  
    for file in filelist:
      xfile = file  
      i=i+1
      print " [%s] - %s" % (i,file)  
      changed = False  
      if (filtro==".mxd"):
          mxd = arcpy.mapping.MapDocument(file)  
      else:
          mxd = arcpy.mapping.Layer(file)
      layerList = arcpy.mapping.ListLayers(mxd)  
      #print layerList
      for layer in layerList:  
        #print layer.supports("DATASOURCE")
        if layer.supports("DATASOURCE"):  
             #if options.listonly:
             b = layer.workspacePath
             #b = b.replace(layer.longName,"")
             a = [ x for x in lista if b == x]
             if (len(a) == 0):
                 lista.append(b)  
             #print "\tLayer %s se conecta a: %s" % (layer.name, layer.dataSource)
   print ""
   print "CONEXIONES DIFERENTES"
   print "---------------------"
   for a in lista:
       print a
   print "---------------------"
  
else:  
 osource=options.osource
 lista = osource.split(",")
 Nomalo = True
 w2 = options.nsource
 ingreso = options.inicio
 salida = options.salida
 if ingreso is not None:
  print "Path Inicial= "+ ingreso
 else:
  Nomalo = False
  print "Falta --inicio"
 if salida is not None:
  print "Path Salida = "+salida
 else:
  Nomalo = False
  print "Falta --salida"
 if osource is not None:
  print "Conexiones a Modificar="+osource
 else:
  Nomalo = False
  print "Falta --fuentes"
 if w2 is not None:
  print "Conexion Nueva      ="+w2
 else:
  Nomalo = False
  print "Falta --fuenteNueva"
 i = 0
 if Nomalo:
  print "Procesando ======> "+ filtro
  for raiz, dirs, files in os.walk(ingreso):
    for nombre in files:
       if nombre.endswith(filtro):
               a= os.path.join(raiz, nombre)
               i=i+1
               print "[%s] - %s" % (i,a)
               if (filtro == ".mxd"):
                 mxd = arcpy.mapping.MapDocument(a)
                 for par in lista:
                   ww1 = par
                   #print "procesando "+ww1
                   mxd.findAndReplaceWorkspacePaths(ww1, w2, False)
               else:
                 mxd = arcpy.mapping.Layer(a)
                 if (mxd.supports("DATASOURCE")):
                  for par in lista:
                   ww1 = par
                   #print "procesando "+ww1
                   mxd.findAndReplaceWorkspacePath(ww1, w2, False)
   

               b = a
               

               b = b.replace( raiz, salida)
               mxd.saveACopy(b)
 print ""
 print "=================="
 print "Proceso finalizado"
