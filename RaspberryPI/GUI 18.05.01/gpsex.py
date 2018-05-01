from PyQt5 import QtCore
from gps3 import gps3


class gpsex(QtCore.QThread):
    on_changed_gps = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.enabled = False

    def stop(self):
        self.enabled = False

    def run(self):
        self.enabled = True
        gps_socket = gps3.GPSDSocket()
        data_stream = gps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()

        for new_data in gps_socket:
            if self.enabled is False:
                break

            if new_data is None:
                continue

            data_stream.unpack(new_data)
            if data_stream.TPV['lat'] == 'n/a':
                continue

            position = (data_stream.TPV['lat'], data_stream.TPV['lon'])
            self.on_changed_gps.emit(position)
