import pandas as pd
import time

class Utils:

    @staticmethod
    def diff_between_excel_files(excel_file_path_new,excel_file_path_old):
        df_new = pd.read_excel(excel_file_path_new)
        df_old = pd.read_excel(excel_file_path_old)

        df_diff = pd.concat([df_new,df_old]).drop_duplicates(keep=False)

        return df_diff

    @staticmethod
    def diff_between_df(df_new,df_old,columns=None):
        return pd.concat([df_new,df_old]).drop_duplicates(subset = columns,keep=False)

    @staticmethod
    def difference_between_df(df_new,df_old,columns):
        create_df = pd.DataFrame( columns = df_new.columns)
        for i in columns:
            df_diff = pd.concat([df_new,df_old]).drop_duplicates(subset = [i],keep=False)
            create_df = create_df.append(df_diff)

        return create_df



    @staticmethod
    def cmp_excel_files_by_count_cols(excel_file_path,excel_file2_path):
        df_excel = pd.read_excel(excel_file_path)
        df_excel2 = pd.read_excel(excel_file2_path)

        return df_excel['Count'].equals(df_excel2['Count'])


    @staticmethod
    def cmp_excel_files_by_rows_cols(excel_file_path, excel_file2_path):
        df_excel = pd.read_excel(excel_file_path)
        df_excel2 = pd.read_excel(excel_file2_path)

        if df_excel.shape == df_excel2.shape:
            return True
        else:
            return False

    @staticmethod
    def cmp_excel_files_by_rtd_col(excel_file_path,excel_file2_path):
        df_excel = pd.read_excel(excel_file_path)
        df_excel2 = pd.read_excel(excel_file2_path)

        return df_excel['RTD Average'].equals(df_excel2['RTD Average'])

    @staticmethod
    def every_downloads_chrome(driver):
        if not driver.current_url.startswith('chrome://downloads'):
            window_before = driver.window_handles[0]
            time.sleep(1)
            driver.execute_script('window.open("/get")')
            time.sleep(0.5)
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            driver.get('chrome://downloads/')
            time.sleep(0.5)


        paths = driver.execute_script("""
            var items = downloads.Manager.get().items_;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.filePath);
            """)

        driver.close()
        driver.switch_to.window(window_before)

        return paths
