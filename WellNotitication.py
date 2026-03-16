import arcpy
import os
from arcpy import env

env.workspace = r"RUTA DE LA PC\GISTPython\GISTPython\Data\City of Oleander.gdb"
env.overwriteOutput = True

fcName = "BC_Assoc_3H_Path"

gdbtemp = r"RUTA DE LA PC\GISTPython\GISTPython\MyExercises\Scratch\Temporary Storage.gdb"
fcbuffer = "SelectionBuffer"

output_buffer = os.path.join(gdbtemp, fcbuffer)

with arcpy.da.SearchCursor(fcName, ["Shape_Length"]) as cursor:
    for row in cursor:
        drillLength = row[0]

if drillLength < 300:
    wellBuffDist = 75
elif drillLength < 4000:
    wellBuffDist = 175
else:
    wellBuffDist = 300

arcpy.analysis.PairwiseBuffer(fcName, output_buffer, f"{wellBuffDist} Meters")

# crear layer temporal
arcpy.management.MakeFeatureLayer("Parcels", "ParcelsLayer")

# seleccionar parcelas que intersectan el buffer
arcpy.management.SelectLayerByLocation(
    "ParcelsLayer",
    "INTERSECT",
    output_buffer
)

arcpy.management.CopyRows("ParcelsLayer", r"G:\Mi unidad\PC\UCR\Modelado Espacial\2026-1\Semana 2\GISTPython\GISTPython\Data\\"+ fcName +"MailList.dbf")
