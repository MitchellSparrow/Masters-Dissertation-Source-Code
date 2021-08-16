import os
import sys
import cvb
import cvb.ui


from PySide2.QtCore import QObject, QUrl
from PySide2.QtQml import qmlRegisterType
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtQuick import QQuickView, QQuickPaintedItem
from PySide2.QtGui import QIcon


if __name__ == "__main__":

    app = QApplication([])
    #app.setOrganizationName('STEMMER IMAGING')
    # app.setOrganizationDomain('https://www.stemmer-imaging.com/')
    app.setApplicationName('Display Python tutorial')

    # tell Windows the correct AppUserModelID for this process (shows icon in the taskbar)
    if sys.platform == 'win32':
        import ctypes
        myappid = u'stemmerimaging.commonvisionblox.pystreamdisplay.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        app.setWindowIcon(QIcon('Tutorial-Python_32x32.png'))

    # load the device
    driver = os.path.join(cvb.install_path(), 'Drivers', 'GenICam.vin')
    print(cvb.install_path())
    device = cvb.DeviceFactory.open(driver, port=0)

    # device = cvb.DeviceFactory.open(
    #     os.path.join(cvb.install_path(), "drivers", "CVMock.vin"),
    #     cvb.AcquisitionStack.Vin)

    # use a single stream handler to setup an acquisition thread and acquire images

    handler = cvb.SingleStreamHandler(device.stream())
    # create an image controller to interact with the UI
    image_controller = cvb.ui.ImageController()

    # register the display component with QML
    cvb.ui.ImageViewItem.register()

    # setup the QML UI
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    context = view.rootContext()
    context.setContextProperty("mainImage", image_controller)
    filepath = os.path.dirname(os.path.realpath(__file__))
    view.setSource(QUrl.fromLocalFile(os.path.join(filepath, "main.qml")))
    view.resize(640, 480)
    view.show()

    # register the device image with UI controller to trigger automatic refreshes
    image_controller.refresh(device.device_image, cvb.ui.AutoRefresh.On)

    # start the aquisition thread
    handler.run()

    # start the UI event handler
    app.exec_()

    # stop the aquisition after UI exits
    handler.try_finish()
