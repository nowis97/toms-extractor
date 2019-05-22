from sqlalchemy import create_engine
import Cleaner
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import pyodbc
import pandas as pd


class DataBasePopulate:
    connection = None
    database_name = ""
    password = ""
    user = ""
    host = ""
    string_connection_pyodb = ""

    def __init__(self, user, password, database_name, host):
        self.user = user
        self.password = password
        self.database_name = database_name
        self.host = host
        self.connection = create_engine(
            'mssql+pyodbc://' + self.user + ':' + self.password + '@' + self.host + '/' + self.database_name +
            '?driver=SQL+Server+Native+Client+11.0')
        self.string_connection_pyodb = 'DRIVER={SQL Server Native Client 11.0};SERVER=' + self.host + ';DATABASE=' + self.database_name + ';UID=' \
                                       + self.user + ';PWD=' + self.password

    def insert_organizations(self, path):
        organizations_df = Cleaner.organizations_excel(path)

        self.insert_or_ignore_rows(organizations_df, 'organization', 'append')

    def get_all_prefix_departments(self):
        prefix_rows = self.connection.engine.execute(text('select prefix from organization')).fetchall()
        list_prefix_departments = []
        for i in prefix_rows:
            if i[0] is not None:
                list_prefix_departments.append(i[0].strip())

        return list_prefix_departments

    def get_all_organizations_names(self):
        names_rows = self.connection.engine.execute(text('select organization_name from organization')).fetchall()
        list_names_organizations = []
        for i in names_rows:
            if i[0] != 'TRANSIT':
                list_names_organizations.append(i[0].strip())

        return list_names_organizations

    def insert_inspections_ocurrencies(self, paths):
        for path in paths:
            inspections_organization = Cleaner.ocurrences_inspection(path, self.connection)
            self.insert_or_ignore_rows(inspections_organization, 'inspection', 'append')

    def insert_inspections(self, df_diff):

        inspection_df = Cleaner.fleet_inspection_work_order(df_diff, self.connection)

        self.connection.connect().execution_options(autocommit=True).execute(text('delete from inspection'))
        inspection_df.to_sql('inspection', con=self.connection, if_exists='append', index=False)


        #organization_inspection_df.to_sql('organization_inspection', con=self.connection, if_exists='append',
        #                                     index=False)

        """upsert_query = 'exec UpsertInspection :id,:desc,:lon,:loff,:status,:set,:dcompleted,:dcreated,:cb'

        for i in inspection_df.itertuples(index=False, name='Inspection'):

            self.connection.connect().execution_options(autocommit=True).execute(text(upsert_query), {
                'id': i[0],
                'desc': i[1],
                'lon': i[2] if i[2] is not pd.NaT else None,
                'loff': i[3] if i[3] is not pd.NaT else None,
                'status': i[4],
                'set': i[5] if i[5] is not pd.NaT else None,
                'dcompleted': i[6] if i[6] is not pd.NaT else None,
                'dcreated': i[7] if i[7] is not pd.NaT else None,
                'cb': i[8]
            })"""


    def insert_or_ignore_rows(self, df, ne, ie):
        j = 0
        for i in range(len(df)):
            try:
                df.iloc[i:i + 1].to_sql(name=ne, if_exists=ie, con=self.connection, index=False)
            except IntegrityError:
                j += 1
                pass
        print('Se han omitido ', j, ' columnas de ', ne)

    def insert_or_return_update_rows(self, df, ne):
        j = 0
        df_rows_update = pd.DataFrame(columns=df.columns)
        for i in range(len(df)):
            try:
                df.iloc[i:i + 1].to_sql(name=ne, if_exists='append', con=self.connection, index=False)
            except IntegrityError:
                j += 1
                df_rows_update = df_rows_update.append(df.iloc[i])

        print('Se han omitido ', j, ' columnas de ', ne)

    def insert_equipments(self, path):
        equipments_df, relationship_organization_equipment = Cleaner.equipments_organization_equipment(path)

        self.insert_or_ignore_rows(equipments_df, 'equipment', 'append')
        self.insert_or_ignore_rows(relationship_organization_equipment, 'organization_equipment', 'append')

    def update_performance_from_dashboard_tire(self, path):
        performance_df, last_rows_performance_db = Cleaner.performance_tire_dashboard(path, self.connection)
        conn = pyodbc.connect(self.string_connection_pyodb, autocommit=True)
        cursor = conn.cursor()

        list_insert = []

        for i in performance_df.itertuples():
            j = tuple(i)
            list_insert.append((None if j[3] is pd.NaT else str(j[3]),
                                j[4], j[5], j[2], j[-1], j[6], j[6]))

        cursor.executemany(
            'UPDATE Performance SET [Fecha De ultima inspeccion] = ?, [RTD Actual] = ?, [Km Actual] = ?, [horas actuales] = ?,'
            '[estado actual] = ? where [Serie] = ? and  #Envios = (SELECT max(#Envios) from Performance where [Serie] = ?) ',
            list_insert)

        cursor.close()
        conn.close()

    def insert_tires_installed_by_date(self,df_diff):
        tires_installed_by_date_df = Cleaner.tires_installed_by_date(df_diff)

        self.connection.connect().execution_options(autocommit=True).execute(text('delete from tires_installed'))
        tires_installed_by_date_df.to_sql(name='tires_installed', con=self.connection, if_exists='append',index=False)

    def insert_or_update_performance(self, df_diff):
        self.connection.connect().execution_options(autocommit=True).execute(text('delete from tire'))
        update_tire_df = Cleaner.performance(df_diff, self.connection)
        update_tire_df.to_sql(name='tire', con=self.connection, if_exists='append', index=False)


    """
        list_insert = []

        for i in update_tire_df.itertuples():
            list_insert.append((i[5],
                                i[-1],
                                None if i[3] is pd.NaT or pd.isna(i[3]) else (i[3]),
                                i[-2],
                                i[1],
                                int(i[-5]) if not pd.isna(i[-5]) else 0,
                                int(i[-6]) if not pd.isna(i[-6]) else 0,
                                int(i[4]) if not pd.isna(i[4]) else 0,
                                int(i[2]) if not pd.isna(i[2]) else 0,
                                None if i[-4] is pd.NaT or pd.isna(i[-4]) else (i[-4]),
                                i[-3] if not pd.isnull(i[-3]) else None,
                                i[6]))

        # update_query = 'Update tire set status =?,first_fitment_date =? ,size = ? ,compound = ?,rtd_average = ? ,otd=?,hours= ?,distance=?,scrap_date=?,scrap_reason_description=?,manufacturer_code=? where id = ?'

        upsert_query = text('exec UpsertTire :id,:status,:ffd,:size,:comp,:rtd,:otd,:hours,:dist,:sd,:sr,:man')
        # for i in list_insert:
        #   cursor.execute(upsert_query,i)

        for i in list_insert:
            try:
                self.connection.connect().execution_options(autocommit=True).execute(upsert_query, {
                'id': i[0],
                'status': i[1],
                'ffd': i[2],
                'size': i[3],
                'comp': i[4],
                'rtd': i[5],
                'otd': i[6],
                'hours': i[7],
                'dist': i[8],
                'sd': i[9],
                'sr': i[10],
                'man': i[11]
                })
            except Exception as e:
                print(e)
                pass

        self.insert_or_ignore_rows(update_organization_tire, 'organization_tire', 'append')
        """
