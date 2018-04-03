from gps3 import gps3
import threading
import time
import datetime
import uuid
import pymysql
class MyGPS(threading.Thread):

    def run(self):
        self.lat = 0.0
        self.lon = 0.0
        self.pos_list = []
        self.mac_addr = self.get_mac()
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
                    print("수신성공!")
                    self.lat = data_stream.TPV['lat']
                    self.lon = data_stream.TPV['lon']
                    self.insertPosList(self.lat,self.lon) # insert list
                    sem.release()

    def get_mac(self):
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac

    def insertPosList(self,lat,lon):
        self.pos_list.append((datetime.datetime.now().strftime('%Y-%m-%d %H:%H:%S'),lat,lon))


    def getPosition(self):
        self.insertPosList(self.lat, self.lon)
        return (self.lat, self.lon)

    def insertDB(self):
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='pidb',charset='utf8',autocommit=True) # DB 개방
        cursor = db.cursor()
        query = 'INSERT INTO POSITION VALUES(%s,%s,%s,%s)'
        for pos in self.pos_list:
            cursor.execute(query, (self.mac_addr, pos[0], pos[1], pos[2]))
        db.close()
        print("Position insert SUCCESS!")
        


if __name__ == '__main__':
    import datetime
    zz = MyGPS()
    zz.start()
    
    """
    def hehe():
        threading.Timer(1,hehe).start()
        s = datetime.datetime.now()
        with open('gpslog.txt', 'a') as f:
            f.write('{} : {}\n'.format(s,zz.getPosition()))
        print(s," : ",zz.getPosition())
        

    hehe()
    """

    for i in range(30):
        print(zz.getPosition())
        time.sleep(1)

    zz.insertDB()
        
        
