
import os
import cvb
import cvb.ui
from gevserver import Stream
import numpy as np
from PySide2.QtCore import Property, QObject, QUrl, Signal
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication


FRAME_RATE = 30
WIDTH = 2064
HEIGHT = 1544


def configure_device(device: cvb.Device) -> None:
    dnode = device.node_maps['Device']
    dnode['Cust::autoBrightnessMode'].value = 'Off'
    dnode['Std::BalanceWhiteAuto'].value = 'OnDemand'
    dnode['Std::AcquisitionFrameRate'].value = FRAME_RATE
    dnode['Std::Width'].value = WIDTH
    dnode['Std::Height'].value = HEIGHT
    dnode['Std::TriggerMode'].value = 'Off'
    #dnode['Std::GevSCPSPacketSize'].value = 8192


discover = cvb.DeviceFactory.discover_from_root(cvb.DiscoverFlags.IgnoreVins)
dev_info = discover[0]
dev = cvb.DeviceFactory.open(dev_info.access_token)
print(dev)
#handler = cvb.SingleStreamHandler(dev.stream)
print(discover)

# with cvb.DeviceFactory.open(os.path.join(cvb.install_path(), "drivers", "CVMock.vin")) as device:
#     stream = device.stream
# dev_info = discover[0]
# dev = cvb.DeviceFactory.open(dev_info.access_token)
# handler = cvb.SingleStreamHandler(dev.stream)
# print(discover)


# app = QApplication([])
# app.setOrganizationName('University of Nottingham')
# # app.setOrganizationDomain('https://www.horizon.ac.uk/')
# app.setApplicationName('VHQ2 Camera Recorder')

# #qmlBridge = QmlBridge()

# driver = os.path.join(cvb.install_path(), 'drivers', 'GenICam.vin')
# device = cvb.DeviceFactory.open("GenICam.vin", port=1)
# print(device)
# # with cvb.DeviceFactory.open(driver, port=0) as device:
# #     configure_device(device)
