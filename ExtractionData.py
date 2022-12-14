from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from Utils import Utils
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import PureWindowsPath
import logging
import pandas


class ExtractionData:
    def __init__(self, toms):
        self.toms = toms

    def __click_excel_button(self):

        button_export_excel = self.toms.driver.find_element_by_css_selector \
            ('.x-btn-icon-el.x-btn-icon-el-gridtoolbar-toolbar-small.exportExcel ')
        button_export_excel.click()

    def __diff_df_between_excels_downloaded(self, name_file, cmp_function):
        paths = WebDriverWait(self.toms.driver, 120, 1).until(Utils.every_downloads_chrome)
        downloaded_excel_path = paths[0]
        path_win = PureWindowsPath(downloaded_excel_path)
        path_win_dir = str(path_win).strip(path_win.name)

        if not os.path.exists(path_win_dir + name_file + '.xlsx'):
            os.rename(path_win, path_win_dir + name_file + '.xlsx')
            return pandas.read_excel(path_win_dir + name_file + '.xlsx')
        elif not cmp_function(path_win, path_win_dir + name_file + '.xlsx'):
            diff_df_excels = Utils.diff_between_excel_files(path_win, path_win_dir + name_file + '.xlsx')
            os.remove(path_win_dir + name_file + '.xlsx')
            os.rename(path_win, path_win_dir + name_file + '.xlsx')
            return diff_df_excels

        os.remove(path_win)
        return pandas.read_excel(path_win_dir + name_file + '.xlsx')

    def get_path_file_download(self, name_file, cmp_function):
        paths = WebDriverWait(self.toms.driver, 120, 1).until(Utils.every_downloads_chrome)
        downloaded_excel_path = paths[0]
        path_win = PureWindowsPath(downloaded_excel_path)
        path_win_dir = str(path_win).strip(path_win.name)

        if not os.path.exists(path_win_dir + name_file + '.xlsx'):
            os.rename(path_win, path_win_dir + name_file + '.xlsx')
            return path_win_dir + name_file + '.xlsx'
        elif not cmp_function(path_win, path_win_dir + name_file + '.xlsx'):
            os.remove(path_win_dir + name_file + '.xlsx')
            os.rename(path_win, path_win_dir + name_file + '.xlsx')
            return path_win_dir + name_file + '.xlsx'

        os.remove(path_win)
        return path_win_dir + name_file + '.xlsx'

    def get_organization(self):
        self.toms.organizations()

        time.sleep(1)

        button_expand_right = self.toms.driver.find_element_by_xpath("//a[@data-qtip='Expand Right (Alt+Right)']")

        button_expand_right.click()
        time.sleep(1)
        self.__click_excel_button()

        path = self.get_path_file_download('organizations', Utils.cmp_excel_files_by_rows_cols)

        self.toms.go_to_main_page()

        return path

    def get_ocurrencies_inspections(self, db):
        paths = []
        for depto, name in zip(db.get_all_prefix_departments(), db.get_all_organizations_names()):
            self.toms.change_department_default(depto, name)
            self.toms.go_to_fleet_inspections_kpi_departments()
            button_export_excel = self.toms.driver.find_element_by_css_selector \
                ('.x-btn-icon-el.x-btn-icon-el-gridtoolbar-toolbar-small.exportExcel ')
            button_export_excel.click()
            paths.append(self.get_path_file_download(depto, Utils.cmp_excel_files_by_count_cols))

        return paths

    def get_equipments(self):
        self.toms.equipment_dashboard()
        time.sleep(0.5)
        combo_box_input = self.toms.driver.find_element_by_xpath("//input[@type='text' and @name='dataspylist']")
        combo_box_input.clear()
        combo_box_input.send_keys('Installed Tires')
        combo_box_input.send_keys(Keys.ENTER)

        time.sleep(0.5)
        try:
            WebDriverWait(self.toms.driver, 6).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se cargo la tabla de Installed Tires')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None

        self.__click_excel_button()
        df_diff = self.__diff_df_between_excels_downloaded('equipments', Utils.cmp_excel_files_by_rows_cols)
        self.toms.go_to_main_page()
        return df_diff

    def get_site_equipment_configurations(self):
        self.toms.site_equipment_configurations()
        time.sleep(0.5)
        button_export_excel = self.toms.driver.find_element_by_css_selector \
            ('.x-btn.x-unselectable.x-box-item.x-toolbar-item.uft-id-gridexportexcel.x-btn-gridtoolbar-toolbar-small')

        button_export_excel.click()

        path = self.get_path_file_download('site_equioment_configurations', Utils.cmp_excel_files_by_rows_cols)

        self.toms.go_to_main_page()

        return path

    def get_rotation_planning_detailed(self):
        self.toms.rotation_planning()
        time.sleep(0.5)
        button_export_excel = self.toms.driver.find_element_by_css_selector \
            ('.x-btn-icon-el.x-btn-icon-el-gridtoolbar-toolbar-small.exportExcel ')

        button_export_excel.click()

        path = self.get_path_file_download('rotation_planning_detailed', Utils.cmp_excel_files_by_rows_cols)

        self.toms.go_to_main_page()

        return path

    def get_performance_from_tire_dashboard(self):
        self.toms.tire_dashboard()
        time.sleep(1)
        combo_box_input = self.toms.driver.find_element_by_xpath("//input[@type='text' and @name='dataspylist']")
        combo_box_input.clear()
        combo_box_input.send_keys('Performance')
        combo_box_input.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.toms.driver, 3).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se ingreso a Performance Dashboard')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None
        self.__click_excel_button()

        df_diff = self.__diff_df_between_excels_downloaded('performance', Utils.cmp_excel_files_by_rtd_col)
        self.toms.go_to_main_page()
        return df_diff

    def get_performance_smart(self):
        self.toms.tire_dashboard()
        time.sleep(1)

        input_box_fiwo = self.toms.driver.find_element_by_xpath("//input[@type='text' and @name='dataspylist']")
        input_box_fiwo.clear()
        input_box_fiwo.send_keys('Performance SMART')
        input_box_fiwo.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.toms.driver, 4).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se cargo la tabla de Performance SMART')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None

        self.__click_excel_button()



        path = self.get_path_file_download('performance_smart', Utils.cmp_excel_files_by_rows_cols)

        self.toms.go_to_main_page()

        return path

    def get_fleet_inspection_work_order(self):
        self.toms.fleet_inspection_work_order()

        try:
            WebDriverWait(self.toms.driver, 3).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se ingreso a Fleet Inspection Work Order')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None
        time.sleep(1)
        iframe = self.toms.driver.find_element_by_xpath("//iframe[@data-ref ='iframeEl']")
        time.sleep(2)
        self.toms.driver.switch_to.frame(iframe)
        time.sleep(5)
        input_box_fiwo = self.toms.driver.find_element_by_xpath("//input[@type='text' and @name='dataspylist']")
        input_box_fiwo.clear()
        input_box_fiwo.send_keys('Inspections')
        input_box_fiwo.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.toms.driver, 3).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se cargo la tabla de inspections')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None
        time.sleep(3)
        self.__click_excel_button()
        df_diff = self.__diff_df_between_excels_downloaded('fiwo', Utils.cmp_excel_files_by_rows_cols)
        self.toms.go_to_main_page()
        return df_diff

    def get_tires_installed_by_date(self):
        self.toms.tire_dashboard()

        input_box_tire_dashboard = self.toms.driver.find_element_by_xpath("//input[@type='text' and @name='dataspylist']")
        input_box_tire_dashboard.clear()
        input_box_tire_dashboard.send_keys('Installed by Date')
        input_box_tire_dashboard.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.toms.driver, 3).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se cargo la tabla de Installed by Date')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None

        self.__click_excel_button()

        df_diff = self.__diff_df_between_excels_downloaded('tires_installed', Utils.cmp_excel_files_by_rows_cols)
        self.toms.go_to_main_page()
        return df_diff
