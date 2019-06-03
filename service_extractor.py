import win32serviceutil
import win32event
import win32service
import servicemanager
import schedule
from sendmail import SendEmail
import sys
import socket
class ExtractorTOMSService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'extractor_TOMS'
    _svc_display_name_ = 'Service Extractor TOMS'
    _svc_description_ = 'This is the service that allow web scraping to web system TOMS'



    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        socket.setdefaulttimeout(60)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.stop_requested = False


    def SvcStop(self):

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True

    def SvcDoRun(self):

        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_,''))
        try:
            self.main()
        except Exception:
            print(Exception)


    def main(self):
        sch = schedule.every(2).minutes

        sch.do(SendEmail('toms.extractor.log@gmail.com', 'Kaltire.2019', 'smtp.gmail.com:587').send_email,'se.the.nowis@gmail.com', 'holaa', 'mensaje de prueba')
        while not self.stop_requested:
            schedule.run_pending()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ExtractorTOMSService)