from TOMS import TOMS
from ExtractionData import ExtractionData
from DataBasePopulate import DataBasePopulate
import time
import argparse
import win32api
import logging
import sys
from LoggerWriter import LoggerWriter



parser = argparse.ArgumentParser(description='Extrae datos a partir de TOMS')
parser.add_argument('-uw','--user_web',type=str, help='El usuario de la pagina web')
parser.add_argument('-udb','--user_db',type=str, help='El usuario de la base de datos')
parser.add_argument('-pw','--pass_web',type=str,help='La contraseña de la pagina web')
parser.add_argument('-pdb','--pass_db',type=str,help='La contraseña de la base de datos')
parser.add_argument('-ndb','--name_db',type=str,help='Nombre de la base de datos')
parser.add_argument('-ip','--ip_db',type=str,help='Direccion ip de la base de datos')
parser.add_argument('-w','--where_put',type=bool, help= 'depende de esta opcion hara un web scraping entregandole info a SMART')
args = parser.parse_args()

gettrace = getattr(sys, 'gettrace', None)

if gettrace() is None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
        filename="out_toms.log",
        filemode='a'
    )
    log = logging.getLogger(__name__)
    sys.stderr = LoggerWriter(log.debug)
    sys.stdout = LoggerWriter(log.info)


def fill_smart(user_db,pass_db,name_db,ip_db,user_web,pass_web):
    try:
        win32api.SetCursorPos((1, 1)) #esta linea mueve el cursor
    except Exception as e:
        pass

    try:
        db = DataBasePopulate(user_db,pass_db,name_db,ip_db)
        toms = TOMS(user_web,pass_web)
        ext = ExtractionData(toms)
        toms.go_to_webpag_toms()
        time.sleep(3)
        toms.login()
        toms.existing_session()
        db.update_performance_from_dashboard_tire(ext.get_performance_smart())

        toms.logout()
        toms.driver.close()
    except Exception as e:
        print(e)
        print('Ha terminado con errores')
        exit(-1)



def main(user_db,pass_db,name_db,ip_db,user_web,pass_web):
    try:
        win32api.SetCursorPos((1, 1))  # esta linea mueve el cursor
    except Exception:
        pass
    
    #try:

    db = DataBasePopulate(user_db, pass_db, name_db, ip_db)
    toms = TOMS(user_web, pass_web)
    ext = ExtractionData(toms)
    toms.go_to_webpag_toms()

    toms.login()
    time.sleep(1)

    toms.existing_session()
    time.sleep(5)


    db.insert_inspections(ext.get_fleet_inspection_work_order())
    db.insert_tires_installed_by_date(ext.get_tires_installed_by_date())
    db.insert_equipments(ext.get_equipments())
    db.insert_or_update_performance(ext.get_performance_from_tire_dashboard())
    toms.driver.close()

    print('Ha terminado')
    #except Exception as e:
     #   print(e)
     #   print('Termino con errores')
     #   exit(-1)


if __name__ == '__main__':
    if args.where_put is None:
        main(args.user_db,args.pass_db,args.name_db,args.ip_db,args.user_web,args.pass_web)
    else:
        fill_smart(args.user_db,args.pass_db,args.name_db,args.ip_db,args.user_web,args.pass_web)

