# CONNECT TO CROPTRAK DATABASE
import mysql.connector
import warnings
import os 
import pandas as pd
warnings.filterwarnings("ignore")

mydb = mysql.connector.connect(
    host= 'waltherfarms.croptrak.us',
    user = 'waltherfarms_ext',
    password = os.environ.get('croptrak_pass'),
    port = '3306',
    database ='WaltherFarms_Reporting'
)
def croptrak_data(Farm_Name,year,data):
    year = str(year)+'%'
    if data:
        test_query= f'''
        SELECT AH.*,Var.value 'Variety' ,CPD.value 'Planted Date',coalesce(OEM.value,EM.value) 'Emergence Date'
        FROM WaltherFarms_Reporting.Asset_Hierarchy as AH
        left join WaltherFarms_Reporting.sys_CROP_VARIETY as Var on Var.asset_guid = AH.guid and Var.end_date = '9999-12-31 23:59:59'
        left join WaltherFarms_Reporting.sys_CROP_PLANTED_DATE as CPD on CPD.asset_guid = AH.guid and CPD.end_date = '9999-12-31 23:59:59'
        left join WaltherFarms_Reporting.sys_50PERCENT_EMERGENCE as EM on EM.asset_guid =AH.guid and EM.end_date = '9999-12-31 23:59:59'
        left join WaltherFarms_Reporting.sys_EMERGENCE_DATE as OEM on OEM.asset_guid = AH.guid and OEM.end_date = '9999-12-31 23:59:59'
        where AH.Status = 'Active' and AH.Farm_Name = '{Farm_Name}' and CPD.value like '{year}'
        order by AH.Area_Name, AH.Farm_name,Asset_Name;
        '''
    df = pd.read_sql_query(test_query,mydb)
    return df

