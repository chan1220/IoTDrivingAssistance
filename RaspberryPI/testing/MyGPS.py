from gps3 import gps3
import threading
import time


class MyGPS(threading.Thread):

    def run(self):
        self.lat = 0
        self.lon = 0
        sem = threading.Semaphore()
        gps_socket = gps3.GPSDSocket()
        data_stream = gps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()

        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                if data_stream.TPV['lat'] != 'n/a':
                    sem.acquire()
                    # print("수신성공!")
                    self.lat = data_stream.TPV['lat']
                    self.lon = data_stream.TPV['lon']
                    sem.release()


    def getPosition(self):
        return (self.lat, self.lon)


if __name__ == '__main__':
    import datetime
    zz = MyGPS()
    zz.start()
    
    def hehe():
        threading.Timer(1,hehe).start()
        s = datetime.datetime.now()
        with open('gpslog.txt', 'a') as f:
            f.write('{} : {}\n'.format(s,zz.getPosition()))
        print(s," : ",zz.getPosition())
        

    hehe()
    
        
        
