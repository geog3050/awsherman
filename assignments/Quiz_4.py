#import arcpy
import arcpy
#set the arcpy.env.workspace to the workspace where airports.shp is saved
arcpy.env.workspace = "C:/Users/awshe/Desktop/Geospatial_Programming/Quiz_4"
#set a variable to be equal to the airports.shp file
airports = "C:/Users/awshe/Desktop/Geospatial_Programming/Quiz_4/airports.shp"
#set a path for the output data
buffer_airports = "C:/Users/awshe/Desktop/Geospatial_Programming/Quiz_4/buffer_airports.shp"
#use a UpdateCursor to look through the FEAUTRE field from the airports.shp
with arcpy.da.UpdateCursor(airports, ["FEATURE"]) as cursor:
    #for loop to get the contents of the FEATURE field
    for row in cursor:
        #if the contents are equal to ["Seaplane Base"], preform buffer analysis of 7500 meters
        #with the output feature classes being the buffer_airports
        if row == ['Seaplane Base']:
            arcpy.Buffer_analysis(row, buffer_airports, '7500 meters')
            #if the contents are equal to ["Airport"], preform buffer analysis of 15000 meters
        #with the output feature classes being the buffer_airports
        elif row == ['Airport']:
            arcpy.Buffer_analysis(row, buffer_airports, '15000 meters')
