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
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
#import arcpy into python shell
import arcpy
#import oc into python shell
import os
def printFeatureClassNames(workspace):
    #set the arcpy workspace to be equal to the workspace in the function
    arcpy.env.workspace = workspace
    #set fcList to be equal to ListFeatureClasses to pull the list of
    #feature classes from the folder.
    fcList = arcpy.ListFeatureClasses('*')
    #for loop of fc in fcList
    for fc in fcList:
        #set desc to fc.Describe to get the properties of fc
        desc = arcpy.Describe(fc)
        #print the feature class (fc) and the feathure class shapeType(desc.shapeType)
        #in the format that is listed above.
        print(fc + ' is a ' + desc.shapeType + ' feature class')
###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    #set the arcpy workspace to be equal to the workspace in the function
    arcpy.env.workspace = workspace
    #get a list of all feature classes from workspace
    fcList = arcpy.ListFeatureClasses('*')
    #for loop of the list of feature classes
    for fc in fcList:
        #find the feature class that are equal to inputFc
        if fc == inputFc:
            #get the list of fields from the feature class
            fields = arcpy.ListFields(fc)
            #foor loop of the attributes from arcpy.ListFields
            for f in fields:
                #if f.type is float, int, or double it is a numerical type 
                if f.type == 'Float' or f.type=='Interger' or f.type == 'Double':
                    #print the numerical types
                    print(f)

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    #set the arcpy workspace to be the input_geodatabase
    arcpy.env.workspace = input_geodatabase
    #get list of the feature classes from the geodatabase
    fcList = arcpy.ListFeatureClasses('*')
    #do a for loop of the feature classes in the list of feature classes
    for fc in fcList:
        #use .Describe to get the properties of the feature class
        desc = arcpy.Describe(fc)
        #find the feature classes with a type of shapeType
        if desc.shapeType == shapeType:
            #create a new geodatabase in the output_geodatabase path
            arcpy.CreateFileGDB_management(output_geodatabase, 'name')
            #add the feature classes that match the shape type to the output geodatabase
            arcpy.FeatureClassToGeodatabase_conversion(desc,'name')

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    #set the workspace for the function to be equal to workspace provided
    arcpy.env.workspace = workspace
    #arcpy.management.AddJoin to join the table to the feature class using the idFieldInputFc and the idFieldTable
    newtable = arcpy.management.AddJoin(inputFC, idFieldInputFc, inputTable, idFieldTable)
    #used CopyFeatures to copy the table from newtable into a new feature class
    arcpy.CopyFeature_management(newtable, "newFC")


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
