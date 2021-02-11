import win32com.client 


def surfer_interpolation(file_csv, level):
    """
    ! Surfer должен быть запущен
    Делает интерполяцию в Surfer метод Kriging
    Выходной файл в dat формате
    """
    x_min, x_max = 134.5, 164.5
    y_min, y_max = 49.5, 61.5
    spacing = 0.5
    # DataFile = r'C:\Users\malyg\Desktop\kag_64\dat\0.csv'
    DataFile = file_csv
    
    col_1 = 8
    col_2 = 9
    # col_3 = 12-19
    
    # for col_3 in (range(12,20) if level < 1000 else range(12,19)):
    for col_3 in range(12,20):
        OutFile = f"C:/Users/malyg/Desktop/kag_64/csv/grd/{level}_{col_3}"
        app = win32com.client.gencache.EnsureDispatch('Surfer.Application')

        app.GridData(DataFile=DataFile,
                    # Номера колонок
                    xCol = col_1, yCol = col_2, zCol = col_3,
                    Algorithm = win32com.client.constants.srfKriging,
                    # Spacing 
                    NumCols = ((x_max-x_min)/spacing) + 1,
                    NumRows = ((y_max-y_min)/spacing) + 1,
                    xMin = x_min, xMax = x_max, yMin = y_min, yMax = y_max, ShowReport=False,
                    # OutFmt = win32com.client.constants.srfGridFmtXYZ,
                    OutFmt = win32com.client.constants.srfGridFmtBinary,
                    OutGrid = OutFile,
                    
        )


# Границы уровней
dct_1 = {i: i + 9 for i in range(0, 31, 10)}
dct_2 = {i: i + 19 for i in range(30, 31)}
dct_3 = {i: i + 24 for i in range(50, 99, 25)}
dct_4 = {i: i + 49 for i in range(100, 251, 50)}
dct_5 = {i: i + 99 for i in range(300, 600, 100)}
dct_6 = {i: i + 99 for i in range(600, 1001, 200)}
# dct_7 = {i: i + 199 for i in range(1000, 1200, 200)}
dct_std_lvl = {**dct_1, **dct_2, **dct_3, **dct_4, **dct_5, **dct_6 }
std_lvl = [*dct_std_lvl.keys()]


for lvl in std_lvl:
    file_csv = f'C:/Users/malyg/Desktop/kag_64/csv/{lvl}m.csv'
    surfer_interpolation(file_csv, lvl)

# def main(): 
#     app = win32com.client.Dispatch("Surfer.Application") 
#     plot = app.Documents.Add(1) 
#     app.Visible = True 
# main()

# def main():
#     app = win32com.client.gencache.EnsureDispatch('Surfer.Application')
#     # app = win32com.client.Dispatch("Surfer.Application") 
#     Plot = app.Documents.Add(1)
#     app.Visible = True
#     # DataFile = "C:\Program Files\Golden Software\Surfer 12\Samples\demogrid.dat"
#     DataFile = r'C:\Users\malyg\Desktop\kag_64\dat\0.csv'
#     # OutFile = r'C:\Users\malyg\Desktop\kag_64\dat\0_NEW_Krigin_3.grd'
#     # app.GridData(DataFile=DataFile, xCol = 1, yCol = 2, zCol = 3, Algorithm = win32com.client.constants.srfMinCurvature, NumRows=150, NumCols=150, ShowReport=False, OutGrid= OutFile)
#     app.GridData(DataFile=DataFile, xCol = 1, yCol = 2, zCol = 3, 
   
#     # DupMethod=win32com.client.constants.srfDupMedZ,
#     # xDupTol=0.5,
#     # yDupTol=0.5,
    

#     Algorithm = win32com.client.constants.srfKriging, 
#     NumCols = 61,  
#     NumRows = 41, 
#     xMin = 139, xMax = 169, yMin = 40, yMax = 60, ShowReport=False,
#     OutFmt = win32com.client.constants.srfGridFmtXYZ,
#     OutGrid = r'C:\Users\malyg\Desktop\kag_64\dat\00_NEW_Krigin_3',
#     )
   
        
#     # #Creates a contour map and assigns the map frame to the variable "MapFrame"
#     # MapFrame = Plot.Shapes.AddContourMap(GridFileName=OutFile)
#     # #Changes the limits and scale of the map
#     # MapFrame.SetLimits (xMin=0.5, xMax=4.5, yMin=0.5, yMax=3.5)
#     # MapFrame.xLength=6
#     # MapFrame.yLength=4
#     # #Declares ContourMap as an Object and assigns the contour map to variable "ContourMap"
#     # ContourMap = MapFrame.Overlays(1)
    
# main()


# def main_work():
#     app = win32com.client.gencache.EnsureDispatch('Surfer.Application')
#     # app = win32com.client.Dispatch("Surfer.Application") 
#     # Plot = app.Documents.Add(1)
#     # app.Visible = True
#     # DataFile = "C:\Program Files\Golden Software\Surfer 12\Samples\demogrid.dat"
#     DataFile = r'C:\Users\malyg\Desktop\kag_64\dat\0.csv'
#     OutFile = r'C:\Users\malyg\Desktop\kag_64\dat\TEST_main_work2'
#     # app.GridData(DataFile=DataFile, xCol = 1, yCol = 2, zCol = 3, Algorithm = win32com.client.constants.srfMinCurvature, NumRows=150, NumCols=150, ShowReport=False, OutGrid= OutFile)
#     app.GridData(DataFile=DataFile, xCol = 1, yCol = 2, zCol = 3, 
   
#     # DupMethod=win32com.client.constants.srfDupMedZ,
#     # xDupTol=0.5,
#     # yDupTol=0.5,
    

#     Algorithm = win32com.client.constants.srfKriging, 
#     NumCols = 61,  
#     NumRows = 41, 
#     xMin = 139, xMax = 169, yMin = 40, yMax = 60, ShowReport=False,
#     OutFmt = win32com.client.constants.srfGridFmtXYZ,
#     OutGrid = OutFile,
#     )
   
        
    # #Creates a contour map and assigns the map frame to the variable "MapFrame"
    # MapFrame = Plot.Shapes.AddContourMap(GridFileName=OutFile)
    # #Changes the limits and scale of the map
    # MapFrame.SetLimits (xMin=0.5, xMax=4.5, yMin=0.5, yMax=3.5)
    # MapFrame.xLength=6
    # MapFrame.yLength=4
    # #Declares ContourMap as an Object and assigns the contour map to variable "ContourMap"
    # ContourMap = MapFrame.Overlays(1)
    
# main_work()




# import glob 
# import datetime 
# #call this script like this: 
# #\programs\python25\python.exe krig_data.py 
# #get an instance of the Surfer application  
# #Surfer = win32com.client.Dispatch('Surfer.Application') 
# lFile = glob.glob('wl*.csv') 
# for i in range(len(lFile)): 
# #the min and max listed below are center coordinates while gdal_grid uses edge 
# #coordinates 
# sFilePrefix = lFile[i][:lFile[i].index('.')] 
# Surfer.GridData(DataFile = lFile[i], xCol = 1, yCol = 2, zCol = 3, NumCols = 4133,  NumRows = 3017, xMin = 455355, xMax = 579315, yMin = 1954585, yMax = 2045065,  ShowReport = False, DupMethod = win32com.client.constants.srfDupAvg, OutFmt = win32com.client.constants.srfGridFmtBinary, OutGrid = '%s.grd' %sFilePrefix) 
# print ('finished kriging %s at %s' % (lFile[i], datetime{source}))