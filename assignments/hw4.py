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
    return(["Aaron Sherman", "awsherman"])

###################################################################### 
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    #import arcpy and os
    import arcpy
    import os
    #set overwrite outputs to be true
    arcpy.env.overwriteOutput = True
    #set the workspace to the input_geodatabase
    arcpy.env.workspace = input_geodatabase
    #use near analysis to find the nearest polyline feature to a point and then append the distance to the points feature class
    arcpy.analysis.Near(fcPoint, fcPolyline)
    

######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    #import arcpy and os and then set overwrite output to true
    import arcypy
    import os
    arcpy.env.overwriteOutput = True
    #set the workspace to be the input geodatabase
    arcpy.env.workspace = input_geodatabase
    #set Nursing Homes to be equal to the results of using the SelectLayerByAttribute_management to select the points from the fcPoints
    #that have a field value that is equal to the pointFieldValue
    Nursing_Homes= arcpy.SelectLayerByAttribute_management(fcPoint, "NEW_SELECTION", "pointFieldName = pointFieldValue")
    #use the Summarize within tool to find the numbers of points within each polygon and append it to the polygon table
    arcpy.analysis.SummarizeWithin(fcPolygon, Nursing_Homes, "out_feature_class")

######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    import arcypy
    import os
    arcpy.env.overwriteOutput = True
    #set the workspace to be the input geodatabase
    arcpy.env.workspace = input_geodatabase
    #set an empty list to append the all the values of the select Field to
    listy=[]
    #run a search cursor that will find the values from a the field and then in they are not in the listy already will append them to the list
    with arcpy.da.SearchCursor(fcPoint, pointFieldName) as cursor:
        for row in cursor:
            if row not in listy:
                listy.append(row)
            else:
                pass
    #for each name in listy     
    for i in listy:
        #for character in the name from the listy
        for p in i:
            #if the character is a space it is replaced with no space to create a shortened version of the name
            t=p.replace(" ","")
            #add a field to the polygon with the shortened name
            arcpy.management.AddField(fcPolygon, t[0:12], "DOUBLE")
    #preform a spatial join of the two feature classes
    arcpy.analysis.SpatialJoin(fcPoint, fcPolygon, "Join_Output")
    #use summarize within to get the counts of the points to join into the polygon feature class
    arcpy.analysis.SummarizeWithin(fcPolygon, "Join_Output", "out_feature_class")
    #delete the Join_Output feature class now that it is no longer useful
    arcpy.management.Delete("Join_Output")
            

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
