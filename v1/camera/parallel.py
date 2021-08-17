import time
import os
import cvb
import cvb.ui
from PySide2.QtCore import QUrl
from PySide2.QtQml import qmlRegisterType
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtGui import QIcon


class MyStreamHandler(cvb.SingleStreamHandler):

    def __init__(self, stream):
        super().__init__(stream)
        self.rate_counter = cvb.RateCounter()

    # called in the interpreter thread to setup additionla stuff.
    def setup(self, stream):
        super().setup(stream)
        print("setup")

    # called in the interpreter thread to tear down stuff from setup.
    def tear_down(self, stream):
        super().tear_down(stream)
        print("tear_down")

    # called from the aqusition thread
    def handle_async_stream(self, stream):
        super().handle_async_stream(stream)
        print("handle_async_stream")

    # called from the aqusition thread
    def handle_async_wait_result(self, image, status):
        super().handle_async_wait_result(image, status)
        self.rate_counter.step()
        print("New image: " + image.__class__.__name__ + " " + str(image) +
              " | Status: " + str(status) + " | Buffer Index: " + str(image.buffer_index))

    # print messurement results
    def eval(self):
        print("Acquired with: " + str(self.rate_counter.rate) + " fps")


with cvb.DeviceFactory.open(
        os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'),
        cvb.AcquisitionStack.Vin) as device:
    with MyStreamHandler(device.stream()) as handler:

        # app = QApplication([])
        # app.setApplicationName('Display Python tutorial')

        # # create an image controller to interact with the UI
        # image_controller = cvb.ui.ImageController()
        # # register the display component with QML
        # cvb.ui.ImageViewItem.register()

        # # setup the QML UI
        # view = QQuickView()
        # view.setResizeMode(QQuickView.SizeRootObjectToView)
        # context = view.rootContext()
        # context.setContextProperty("mainImage", image_controller)
        # filepath = os.path.dirname(os.path.realpath(__file__))
        # view.setSource(QUrl.fromLocalFile(os.path.join(filepath, "main.qml")))
        # view.resize(640, 480)
        # view.show()

        # # register the device image with UI controller to trigger automatic refreshes
        # image_controller.refresh(device.device_image, cvb.ui.AutoRefresh.On)

        handler.run()
        time.sleep(10)
        handler.finish()
