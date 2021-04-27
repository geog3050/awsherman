###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["name", "hawkid"])

###################################################################### 
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
    #import arcpy and os and set overwriteOutput to true
    import arcpy
    import os
    arcpy.env.overwriteOutput = True
    #set the workspace to be the geodatabase that is provided
    arcpy.env.workspace = geodatabase
    #use the AddFieldDelimiters function to remove the IA0000 column from the data
    expression = arcpy.AddFieldDelimiters(arcpy.env.workspace, "stationID") + " <> 'IA0000'"
    #use table to table conversion to convert the table into the geodatabase
    arcpy.conversion.TableToTable(intable, arcpy.env.workspace, "CSVtable", expression)

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 
def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
    #import arcpy and os and set overwriteOutput to true
    import arcpy
    import os
    arcpy.env.overwriteOutput = True
    #set the workspace to be the geodatabase that is provided
    arcpy.env.workspace = geodatabase
    #map out the X and Y points from a table
    arcpy.management.XYTableToPoint(inTable, "year", xField, yField)
    #.Describe to find the features of the year dataset
    desc= arcpy.Describe("year")
    #set variable cellsize to 0
    CellSize= 0
    #set the width and the height to the .extent width and height
    width = desc.extent.width
    height= desc.extent.height
    #if the width is smaller it divded by 1000 is the cellsize, else the height divided by 1000 is the cell size
    if width < height:
        CellSize = width / 1000
    else:
        CellSize = height / 1000
    #set a variable for the output name
    field = "F2018_PREC"
    #preform the Kriging on the dataset and save it as F2018k
    outKriging = Kriging("year, field, '#', CellSize)
    outKriging.save("F2018k")
    #.Describe the clip feature class to find it's extent then set variable rectangle to be equal to it's extent information
    descClip = arcpy.Describe(inClipFc)
    rectangle = str(descClip.extent.XMin) + " " + str(descClip.extent.YMin) + " " + str(descClip.extent.XMax) + " " + str(descClip.extent.YMax)
    #clip the raster
    arcpy.Clip_management(outKriging, rectangle, "F2018KC", inClipFc, "#", "ClippingGeometry", "MAINTAIN_EXTENT" )
    #change to an integer from a floating point raster
    outInt = Int("F2018KC")
    outInt.save("F2018KCI")
    #find the min and max values of the outInt
    min_F2018 = arcpy.management.GetRasterProperties(outInt, "MINIMUM")
    max_F2018 = arcpy.management.GetRasterProperties(outInt, "MAXIMUM")
    #set a variable with the number of classes
    numofclasses = 5
    #find the class range for equal interval breaks
    eq_interval = (int(max_F2018.getOutput(0)) - int(min_F2018.getOutput(0))) / numofclasses
    print(eq_interval)
    #set an empty list
    remapRangeList = []
    mybreak = int(min_F2018.getOutput(0))
    #the following for loop populates the list with the lower bound, upper bound, and the class number for each of the 5 classes                    
    for t in range(0, numofclasses):
        newClassCode = t + 1
        lowerBound = mybreak
        upperbound = mybreak + eq_interval
        remap = [lowerBound, upperbound, newClassCode]
        remapRangeList.append(remap)
        mybreak += eq_interval
    #reclassify the raster into an isarithmic map based on the remapRangeList
    outReclassRR = Reclassify("F2018KCI", "Value", RemapRange(remapRangeList), "NODATA")
    outReclassRR.save("F2018_CL")
    #convert to polygon
    arcpy.RasterToPolygon_conversion("F2018_CL", "F2018_ismc")
        

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
