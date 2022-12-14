import pandas as pd
from Utils import Utils
import datetime

""" Este modulo se encarga de la limpieza de los Excels
"""



def organizations_excel(path):
    """
    Limpia el excel de organizations
    :param path: ruta del excel
    :return: DataFrame organizations
    """
    organizations_df = pd.read_excel(path)
    organizations_df = organizations_df.drop(
        columns=['Common', 'Kal Tire Region', 'Locale', 'Operating Pressure Hot: Max %',
                 'Operating Pressure Hot: Min %', 'Pressure Records - UOM ', 'Server Time Offset', 'Short Code'])

    organizations_df = organizations_df.rename(index=str, columns={
        'Organization': 'organization_name',
        'Out of Service': 'out_of_service'
    })

    organizations_df = organizations_df.rename(str.lower, axis='columns')

    return organizations_df


def ocurrences_inspection(path, connection):
    """
    Limpia el excel de inspecciones
    :param path: ruta del excel: str
    :param connection: conexion a la base de datos
    :return: DataFrame inspections
    """
    inspection_df_db = pd.read_sql_table('inspection', connection)
    inspection_df = pd.read_excel(path)
    inspection_df = inspection_df.drop(columns=['Department'])

    inspection_df = inspection_df.rename(index=str, columns={
        'Due Month': 'inspections_to_date',
        'Count': 'number_inspections',
        'Organization': 'organizationorganization_name',
        'PM Schedule': 'pm_schedule'
    })

    inspection_df = inspection_df.rename(str.lower, axis='columns')

    # if inspection_df_db.empty:

    """inspection_df['inspections_to_date'] = inspection_df['inspections_to_date'].apply(lambda x: str(x) + '-' +
                                                                                                    str(1))

    inspection_df['inspections_to_date'] = pd.to_datetime(inspection_df['inspections_to_date'])

    row_last_month = inspection_df.loc[(inspection_df['inspections_to_date'].dt.month) == (datetime.datetime.now().month)]

    inspection_df = inspection_df.drop(row_last_month.index)

    row_last_month['inspections_to_date'] = datetime.datetime.now()
    inspection_df = inspection_df.append(row_last_month)
    return inspection_df"""
    # else:

    inspection_df['inspections_to_date'] = inspection_df['inspections_to_date'].apply(lambda x: str(x) + '-' +
                                                                                                '01')
    inspection_df['inspections_to_date'] = pd.to_datetime(inspection_df['inspections_to_date'])

    row_last_month = inspection_df.loc[
        (inspection_df['inspections_to_date'].dt.month) == (datetime.datetime.now().month)]

    row_last_month['inspections_to_date'] = row_last_month['inspections_to_date'].apply(
        lambda x: x.replace(day=datetime.datetime.now().day))

    return row_last_month


def site_equipment_configurations(path):
    """
    Excel de los equipos de los sitios
    :param path: ruta del excel
    :return: DataFrame equipemts
    """
    site_equipment_configurations_df = pd.read_excel(path)
    site_equipment_configurations_df = site_equipment_configurations_df.drop(
        columns=['Axle 1 Rotation Alert', 'Axle 1 Tire Size', 'Axle 1 Site Recommended Cold Pressure',
                 'Axle 1 Rim Size', 'Axle 2 Rotation Alert', 'Axle 2 Tire Size',
                 'Axle 2 Site Recommended Cold Pressure', 'Axle 2 Rim Size',
                 'Axle 3 Rotation Alert', 'Axle 3 Tire Size',
                 'Axle 3 # Site Recommended Cold Pressure', 'Axle 3 Rim Size',
                 'Axle 4 Rotation Alert', 'Axle 4 Tire Size',
                 'Axle 4 Site Recommended Cold Pressure', 'Axle 4 Rim Size'])

    return site_equipment_configurations_df


def fleet_inspection_work_order(df_diff,connection):
    fleet_inspection_work_order_df = df_diff.sort_values('Date Completed', ascending=False) \
        .drop_duplicates(subset='Work Order', keep='first')


    fleet_inspection_work_order_df = fleet_inspection_work_order_df[['Organization','Work Order', 'Description', 'Lock On', 'Lock Off',
                                                                     'Status', 'Sched. End Date', 'Date Completed',
                                                                     'Date Created', 'Created By','WO Effective Date']]

    fleet_inspection_work_order_df = fleet_inspection_work_order_df.rename(index=str, columns={
        'Organization':'organization',
        'Work Order': 'id_work_order',
        'Description': 'description',
        'Lock On': 'lock_on',
        'Lock Off': 'lock_off',
        'Status': 'status',
        'Sched. End Date': 'schedule_end_time',
        'Date Completed': 'date_completed',
        'Date Created': 'date_created',
        'Created By': 'created_by',
        'WO Effective Date':'wo_effective_date'
    })

    return fleet_inspection_work_order_df



def equipments_organization_equipment(df_diff):
    """
    Limpia el excel de las organizations
    :param path: la ruta del excel
    :return: DataFrame
    """





    equipments_df = df_diff.rename(index=str, columns={
        'Equipment':'id',
        'Equipment Description':'description',
        'Equipment Status':'status',
        'Last Inspection Effective Date':'last_inspection_effective_date',
        'Organization':'organization',
        'Position RTD Average':'current_rtd_average',
        'Position RTD Inner':'current_rtd_inner',
        'Position RTD Outer':'current_rtd_outer',
        'Tire':'tire_id',
        'Tire Brand':'tire_brand_id',
        'Position Sort':'position_sort',
        'Position Key':'position_key',
        'Position':'position'
    })
    return equipments_df



def rotation_planning_detailed(path):
    rotation_planning_detailed_df = pd.read_excel(path)
    # todo elegir las columnas para extraer la informacion de


def performance_tire_dashboard(path, connection):
    """
    :param path:
    :param connection:
    :return:
    """
    performance_df = pd.read_excel(path)
    performance_db_df = pd.read_sql_table('Performance', connection, 'dbo')

    performance_exists = performance_df.loc[(performance_df['Casing Serial No'].isin(performance_db_df['Serie']) | \
                                             (performance_df['Tire ID'].isin(performance_db_df['Serie'])))]


    return performance_exists


def performance(df_diff, connection):
    #performance_df = pd.read_excel(path)
    #performance_df_db = pd.read_sql_table('tire', connection)
    #performance_organization_tire_df_db = pd.read_sql_table('organization_tire', connection)


    load_performance_tire_df = df_diff[['Organization','Tire ID','Status',
                                               'First Fitment Date','Size','Compound',
                                               'RTD Average','OTD','Hours','Distance',
                                               'Scrap Date', 'Scrap Reason Description','Pattern',
                                               'Manufacturer Code','RTD - Inner','RTD - Outer','RTD Average','Purchase Cost',
                                        'Min TD','Catalogue #','Casing Serial No']]


    load_performance_tire_df = load_performance_tire_df.rename(index=str, columns={
        'Organization':'organization',
        'Tire ID': 'id',
        'Status': 'status',
        'First Fitment Date': 'first_fitment_date',
        'Size': 'size',
        'Compound': 'compound',
        'RTD Average': 'rtd_average',
        'OTD': 'otd',
        'Hours': 'hours',
        'Distance': 'distance',
        'Scrap Date': 'scrap_date',
        'Pattern':'pattern',
        'Scrap Reason Description': 'scrap_reason_description',
        'Manufacturer Code': 'manufacture_code',
        'RTD - Inner':'rtd_inner',
        'RTD - Outer':'rtd_outer',
        'RTD Average':'rtd_average',
        'Purchase Cost':'purchase_cost',
        'Min TD':'min_td',
        'Catalogue #':'n_catalogue',
        'Casing Serial No':'casing_serial_no'
    })

    return load_performance_tire_df

def tires_installed_by_date(df_diff):
    #tires_installed_by_date_df = pd.read_excel(path)

    tires_installed_to_load_df = df_diff[['Organization','Location','Tire ID','Previous Status',
                                                             'Last Mounted Date','Hours']]

    tires_installed_to_load_df = tires_installed_to_load_df.rename(index=str, columns = {
        'Organization':'organization',
        'Location':'location',
        'Tire ID':'tire_id',
        'Previous Status':'previous_status',
        'Last Mounted Date':'last_mounted_date',
        'Hours':'hours'
    })
    return tires_installed_to_load_df