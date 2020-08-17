# Project: Refresh Update Script for Hole Tracking App
# Create Date: 05/14/2020
# Last Updated: 
# Create by: Robert Domiano
# Updated by: 
# Purpose: To refresh the attribute rules on Spire's hole tracking point feature class
# ArcGIS Version:   Pro 2.3+
# Python Version:   3
# For a changelog of updates, visit the github at: https://github.com/SpireBadger/XXXXX
# Associated files: BAT file for task schedule, readme.md
# -----------------------------------------------------------------------

# Import modules
import arcpy, datetime, os, sys, shutil

try: 
    # Temporary sde path file. Delete upon script completion
    sdeTempPath = r"C:\tempConnect"
    # Create the folder if it doesn't exist
    if not os.path.exists(sdeTempPath):
        os.mkdir(sdeTempPath)
        print("Temporary directory not found. A new directory has been " + \
              "created at {0}.".format(sdeTempPath))
    # Enable overwriting so SDE can overwrite self
    arcpy.env.overwriteOutput=True 
    # hole tracking sde connection
    # Delete upon script completion
    sdeHole = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempHoleServ.sde', \
                                              'ORACLE', 'stl-dgisdb-20:1521/DGISPM',\
                                              'DATABASE_AUTH', 'LGC_GAS', \
                                              'c00rdin8r','SAVE_USERNAME')
    print("Database connection created at {0} to the Mo East Oracle Database."\
          .format(sdeTempPath))
    
    # Data variable
    holeFC = sdeHole.getOutput(0) + '/LGC_GAS.Hole_Tracking_Points'
    print(holeFC)
    # Field to be updated
    holeFields = ['HOLE_STATUS','LAST_SYNC_DATE']
    # current date variable
    d = datetime.datetime.now()
    
    # Start an edit session
    edit = arcpy.da.Editor(sdeHole)
    edit.startEditing(True,False)
    
    # insert cursor
    with arcpy.da.UpdateCursor(holeFC, holeFields) as cursor:
        # Initiate edit operation
        edit.startOperation()
        # For each row in the cursor, loop
        for row in cursor:
            # Only edit fields that do not have a Restored status
            if row[0] != 'NULL':
                print("Field is type {0} and {1} will be updated to {2}.".format(row[0], row[1], d))
                # Update sync date with current date
                row[1] = d
            else:
                print("The field type is {0} and it will NOT be updated.".format(row[0]))
            
            # Update row
            cursor.updateRow(row)
    # delete cursor
    del cursor
    # Stop the edit operation
    edit.stopOperation
    
    # stop the edit session and save changes
    edit.stopEditing(True)
    # Delete the SDE file
    os.remove(sdeHole.getOutput(0))
    # Delete the created folder
    shutil.rmtree(sdeTempPath)
    
except IOError as e:
    print(e)
except:
    #Stop edit on except
    edit.stopOperation
    # stop the edit session and save changes
    edit.stopEditing(True)
    print("Unexpected error:", sys.exc_info()[0])
    raise