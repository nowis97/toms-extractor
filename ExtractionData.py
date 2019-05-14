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


class ExtractionData:
    def __init__(self, toms):
        self.toms = toms

    def __click_excel_button(self):

        button_export_excel = self.toms.driver.find_element_by_css_selector \
            ('.x-btn-icon-el.x-btn-icon-el-gridtoolbar-toolbar-small.exportExcel ')
        button_export_excel.click()

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
        self.toms.equipment()
        time.sleep(0.5)
        iframe = self.toms.driver.find_element_by_tag_name('iframe')

        self.toms.driver.switch_to.frame(iframe)
        time.sleep(0.5)
        button_export_excel = self.toms.driver.find_element_by_css_selector \
            ('.x-btn-icon-el.x-btn-icon-el-gridtoolbar-toolbar-small.exportExcel ')
        time.sleep(0.5)
        button_export_excel.click()
        path = self.get_path_file_download('equipments', Utils.cmp_excel_files_by_rows_cols)

        return path

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
        combo_box_arrow_down = self.toms.driver \
            .find_element_by_css_selector(
            '.x-form-trigger.x-form-trigger-default.x-form-arrow-trigger.x-form-arrow-trigger-default ')
        time.sleep(1)
        combo_box_arrow_down.click()

        elements_list_combo_box = self.toms.driver.find_elements_by_css_selector('.x-boundlist-item')
        time.sleep(1)

        for element in elements_list_combo_box:
            if element.text == 'Performance':
                element.click()
                break

        try:
            WebDriverWait(self.toms.driver, 3).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se ingreso a Performance Dashboard')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None

        time.sleep(0.5)
        button_export_excel = self.toms.driver.find_element_by_css_selector \
            ('.x-btn-icon-el.x-btn-icon-el-gridtoolbar-toolbar-small.exportExcel ')
        button_export_excel.click()

        path = self.get_path_file_download('performance', Utils.cmp_excel_files_by_rtd_col)

        self.toms.go_to_main_page()

        return path

    def get_performance_smart(self):
        self.toms.tire_dashboard()
        time.sleep(1)

        combo_box_arrow_down = self.toms.driver \
            .find_element_by_css_selector(
            '.x-form-trigger.x-form-trigger-default.x-form-arrow-trigger.x-form-arrow-trigger-default ')

        time.sleep(1)
        combo_box_arrow_down.click()

        elements_list_combo_box = self.toms.driver.find_elements_by_css_selector('.x-boundlist-item')
        time.sleep(1)

        for element in elements_list_combo_box:
            if element.text == 'Performance SMART':
                element.click()
                break

        try:
            WebDriverWait(self.toms.driver, 5).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se ingreso a Performance SMART')
        except TimeoutException:
            logging.exception('Se demoro demasiado', TimeoutException)
            return None

        time.sleep(0.5)
        button_export_excel = self.toms.driver.find_element_by_css_selector \
            ('.x-btn-icon-el.x-btn-icon-el-gridtoolbar-toolbar-small.exportExcel ')
        button_export_excel.click()

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
        iframe = self.toms.driver.find_element_by_tag_name('iframe')
        time.sleep(2)
        self.toms.driver.switch_to.frame(iframe)
        time.sleep(5)
        input_box_fiwo= self.toms.driver.find_element_by_xpath("//input[@value='Planned']")
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
        path = self.get_path_file_download('fiwo', Utils.cmp_excel_files_by_rows_cols)
        self.toms.go_to_main_page()
        return path

    def get_tires_installed_by_date(self):
        self.toms.tire_dashboard()


        input_box_tire_dashboard = self.toms.driver.find_element_by_xpath("//input[@value = 'All Records']")
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

        path = self.get_path_file_download('tires_installed',Utils.cmp_excel_files_by_rows_cols)
        self.toms.go_to_main_page()
        return path
