from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
import time
import logging
import os
import datetime
logging.basicConfig(level=logging.DEBUG,filename='log_'+str(datetime.datetime.now().date())+'_toms' + '.txt',
                    filemode='a', format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')



class TOMS:

    chrome_options = None
    driver = None
    prefs = None
    user = ""
    password = ""

    def __init__(self, user, password):

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--test-type')
        self.chrome_options.add_argument('start-maximized')
        #self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.prefs = {'download.default_directory': os.getcwd()}
        self.chrome_options.add_experimental_option('prefs', self.prefs)

        self.user = user
        self.password = password

    def __get_element_by_inside_text( self, text ):
        return self.driver.find_element_by_xpath("//span[text() = '"+text+"']")

    def __wait_to_load(self,msg,segs):
        try:
            WebDriverWait(self.driver,segs).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME,'busy-indicator'))
            )
            logging.info(msg)
            return True
        except TimeoutException:
            logging.exception('Se demoro demasiado en cargar',TimeoutException)
            return False


    def go_to_webpag_toms(self):
        self.driver.get('https://toms.kaltire.com/web/base/logindisp')
        try:
            WebDriverWait(self.driver, 36).until(
                expected_conditions.presence_of_element_located((By.ID, 'button-1036-btnInnerEl')))
            logging.info('Pagina TOMS Lista')
            return True
        except TimeoutException:
            logging.exception('Se ha demorado demasiado ingrasando a TOMS: ',TimeoutException)
            return False

    def login(self):
        button_signin = self.driver.find_element_by_id('button-1036-btnEl')
        text_box_user_name = self.driver.find_element_by_id('textfield-1034-inputEl')
        text_box_password = self.driver.find_element_by_id('textfield-1035-inputEl')

        text_box_user_name.send_keys(self.user)
        text_box_password.send_keys(self.password)

        button_signin.click()

        try:
            WebDriverWait(self.driver, 140).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.tab-panel-background.x-fit-item.tab-panel-background-default.x-box-layout-ct')))
            logging.info('Se ha ingresado con exito')
        except TimeoutException:
            logging.exception('Hubo un Error',TimeoutException)
            return False
        self.__wait_to_load('Log in',5)

    def organizations(self):
        self.__get_element_by_inside_text('Sites').click()
        self.__get_element_by_inside_text('Organization').click()
        self.__wait_to_load('Se ingreso a Organizations',5)


    def logout(self):
        button_down_array = self.driver.\
            find_element_by_css_selector('.x-btn-button.x-btn-button-mainmenuButton-toolbar-small.x-btn-no-text.x-btn-button-center')
        button_down_array.click()

        button_logout = self.__get_element_by_inside_text('Logout')
        button_logout.click()

        self.driver.close()

    def equipment(self):
        button_array_down_assets = self.__get_element_by_inside_text('Assets')

        button_array_down_assets.click()
        time.sleep(0.5)

        button_equipment = self.__get_element_by_inside_text('Equipment')
        button_equipment.click()

        self.__wait_to_load('Se ingreso a Equipment',4)






    def go_to_main_page(self):
        try:
            WebDriverWait(self.driver, 20).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se ha ingresado con exito')
        except TimeoutException:
            logging.error('Hubo un Error',TimeoutException)
            return False
        button_down_array = self.driver\
            .find_elements_by_css_selector('.x-btn.x-unselectable.x-box-item.x-toolbar-item.uft-id-session-menu_button.x-btn-mainmenuButton-toolbar-small')[0]
        time.sleep(1)
        button_down_array.click()

        button_start_center = self.driver.find_element_by_id('menu-1034').find_element_by_id('menuitem-1035-textEl')
        button_start_center.click()
        try:
            WebDriverWait(self.driver, 20).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME, 'busy-indicator')))
            logging.info('Se ha ingresado con exito')
            return True
        except TimeoutException:
            logging.error('Hubo un Error',TimeoutException)
            return False

    def change_department_default(self,department_prefix,organization_name):
        button_admin = self.driver.find_element_by_id('button-1043-btnEl')
        button_admin.click()

        button_user_default_site = self.driver.find_element_by_id('menuitem-1092-textEl')
        button_user_default_site.click()

        try:
            WebDriverWait(self.driver,10).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME,'busy-indicator'))
            )
            logging.info('Se Completo el request')
        except TimeoutException:
            logging.exception('Se demoro demasiado',TimeoutException)
            return False

        text_box_input_department = self.driver\
            .find_elements_by_css_selector('.x-form-field.x-form-text.x-form-text-default')[4]
        time.sleep(0.5)
        text_box_input_department.send_keys(department_prefix)
        time.sleep(0.5)
        button_save = self.driver\
            .find_element_by_css_selector('.x-btn-icon-el.x-btn-icon-el-default-toolbar-small.toolbarSave ')


        text_box_input_pbi_reporting = self.driver\
            .find_elements_by_css_selector('.x-form-field.x-form-text.x-form-text-default')[3]
        time.sleep(0.5)
        text_box_input_pbi_reporting.send_keys(organization_name)


        button_save.click()
        time.sleep(2)
        self.go_to_main_page()

        return True

    def go_to_fleet_inspections_kpi_departments(self):
        button_work_management = self.driver.find_element_by_id('button-1049-btnEl')
        button_work_management.click()
        time.sleep(1)

        button_fleet_inspections = self.driver.find_elements_by_css_selector\
            ('.x-menu-item-text.x-menu-item-text-default.x-menu-item-indent-right-arrow')[6]
        button_fleet_inspections.click()
        time.sleep(1)
        button_pm_kpi_supporting_data_deptos = self.driver\
            .find_element_by_css_selector('.x-menu-item.x-menu-item-default.x-box-item.uft-id-menuitem-menu-30120')
        button_pm_kpi_supporting_data_deptos.click()



        try:
            WebDriverWait(self.driver,7).until(expected_conditions.invisibility_of_element((By.CLASS_NAME,'busy-indicator')))
            logging.info('Se completo el request')
            return True
        except TimeoutException:
            logging.exception('No se completo el request',TimeoutException)
            return False


    def site_equipment_configurations(self):
        button_asssets=  self.__get_element_by_inside_text('Assets')

        button_asssets.click()

        time.sleep(0.5)

        dropdown_menu_configurations_masters = self.__get_element_by_inside_text('Configuration Masters')
        dropdown_menu_configurations_masters.click()

        time.sleep(0.5)

        button_site_equipments_configurations = self.__get_element_by_inside_text('Site Equipment Configurations')

        time.sleep(1)
        button_site_equipments_configurations.click()

        button_expand_right = self.driver.find_element_by_css_selector\
            ('.x-btn.rightButton.x-unselectable.uft-id-maintoolbar-collapseright.x-btn-default-toolbar-small')

        button_expand_right.click()


    def rotation_planning(self):
        button_work_management = self.driver.find_elements_by_css_selector\
            ('.x-btn-inner.x-btn-inner-mainmenuButton-toolbar-small')[4]
        button_work_management.click()

        button_rotation_planning = self.driver.find_element_by_css_selector\
            ('.x-menu-item.x-menu-item-default.x-box-item.uft-id-menuitem-menu-26009')

        button_rotation_planning.click()

        try:
            WebDriverWait(self.driver,7).until(
                expected_conditions.invisibility_of_element((By.CLASS_NAME,'busy-indicator'))
            )
            return True
        except TimeoutException:
            logging.exception(TimeoutException)
            return False

    def tire_dashboard(self):
        button_assets = self.__get_element_by_inside_text('Assets')
        button_assets.click()
        time.sleep(0.5)
        button_arrow_right_dashboards = self.__get_element_by_inside_text('Dashboards')

        button_arrow_right_dashboards.click()
        time.sleep(0.5)
        button_tire_dashboard = self.__get_element_by_inside_text('Tire Dashboard')
        time.sleep(0.5)
        button_tire_dashboard.click()
        self.__wait_to_load('Se ingreso a tire dashboard',5)


    def existing_session(self):
        try:
            button_ok = self.driver.find_element_by_css_selector\
                ('.x-btn.x-unselectable.x-box-item.x-toolbar-item.uft-id-ok.x-btn-popupfooter-small')

            button_ok.click()

            return True

        except Exception:
            logging.exception(Exception)
            return False

    def fleet_inspection_work_order(self):
        button_fiwo = self.__get_element_by_inside_text('Fleet Inspection Work Order')
        button_fiwo.click()
        self.__wait_to_load('Se ingreso a fleet inspection work order',5)

