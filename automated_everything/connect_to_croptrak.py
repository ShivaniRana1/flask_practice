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

def connect_croptrak():
    tables_show = '''
    SHOW TABLES;   
    '''
    df = pd.read_sql_query(tables_show,mydb)
    return df

def show_area_name():
    area_show =  '''
    SELECT AH.*,Var.value 'Variety' ,CPD.value 'Planted Date',EM.value 'Emergence Date', OEM.value 'Orginal Emergence data'
        FROM WaltherFarms_Reporting.Asset_Hierarchy as AH
        left join WaltherFarms_Reporting.sys_CROP_VARIETY as Var on Var.asset_guid = AH.guid and Var.end_date = '9999-12-31 23:59:59'
        left join WaltherFarms_Reporting.sys_CROP_PLANTED_DATE as CPD on CPD.asset_guid = AH.guid and CPD.end_date = '9999-12-31 23:59:59'
        left join WaltherFarms_Reporting.sys_50PERCENT_EMERGENCE as EM on EM.asset_guid =AH.guid and EM.end_date = '9999-12-31 23:59:59'
        left join WaltherFarms_Reporting.sys_EMERGENCE_DATE as OEM on OEM.asset_guid = AH.guid and OEM.end_date = '9999-12-31 23:59:59'
        where AH.Status = 'Active';
    '''
    df = pd.read_sql_query(area_show,mydb)
    df.drop(columns=['allowed_geometry','geom'],inplace=True)
    df['Emergence date'] = df['Emergence Date'].combine_first(df['Orginal Emergence data'])
    df_croptrak = df.drop(columns=['Emergence Date','Orginal Emergence data']).copy()
    
    return df_croptrak
