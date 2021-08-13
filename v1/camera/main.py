import os
import time
from datetime import datetime
from pathlib import Path
from secrets import token_hex
from typing import BinaryIO, Dict

import cvb
# import cvb.ui
# import numpy as np
# from PySide2.QtCore import Property, QObject, QUrl, Signal
# from PySide2.QtQuick import QQuickView
# from PySide2.QtWidgets import QApplication

# import PyNvCodec as nvc

# OUTPUT_DIR = '/mnt/data/pszdp1/Projects/vhq2'
# FRAME_RATE = 30
# WIDTH = 2064
# HEIGHT = 1544
# CODEC = 'h264'  # h264 or hevc
# GPU_ID = 0  # 0 for first (or only) GPU
# ENC_PRESET = 'hq'
# # Possible presets
# #   - default
# #   - hp
# #   - hq
# #   - bd
# #   - ll
# #   - ll_hq
# #   - ll_hp
# #   - lossless
# #   - lossless_hp
# # Refer to https://git.io/JJfvj for further information and additional
# # encoder options, e.g. { 'bitrate': '10M' }
# ENC_EXTRA_OPTIONS = {'bitrate': '16M', 'gop': str(30 * 60)}


# class QmlBridge(QObject):

#     recording_started: Signal = Signal()

#     stop_recording: Signal = Signal()

#     participant_id_changed: Signal = Signal()

#     adjust_white_balance: Signal = Signal()

#     def __init__(self, parent: QObject = None):
#         QObject.__init__(self, parent)
#         self._participant_id = ''

#     @Property(str, notify=participant_id_changed)
#     def participant_id(self) -> str:
#         return self._participant_id

#     @participant_id.setter
#     def set_participant_id(self, participant_id: str) -> None:
#         self._participant_id = participant_id
#         self.participant_id_changed.emit()


# class RGBEncoder():

#     def __init__(self, encoder_options: Dict[str, str], gpu_id: int):
#         self._outfile = None
#         self._buffer = np.ndarray(shape=(0), dtype=np.uint8)
#         self._encoder = nvc.PyNvEncoder(encoder_options, gpu_id)
#         self._uploader = nvc.PyFrameUploader(
#             self._encoder.Width(),
#             self._encoder.Height(),
#             nvc.PixelFormat.RGB,
#             gpu_id)
#         self._to_yuv = nvc.PySurfaceConverter(
#             self._encoder.Width(),
#             self._encoder.Height(),
#             nvc.PixelFormat.RGB,
#             nvc.PixelFormat.YUV420,
#             gpu_id)
#         self._to_nv12 = nvc.PySurfaceConverter(
#             self._encoder.Width(),
#             self._encoder.Height(),
#             nvc.PixelFormat.YUV420,
#             nvc.PixelFormat.NV12,
#             gpu_id)

#     def set_output_file(self, outfile: BinaryIO):
#         self._outfile = outfile

#     def save_image(self, image: cvb.StreamImage):
#         im = self._uploader.UploadSingleFrame(cvb.as_array(image, copy=False))
#         im = self._to_yuv.Execute(im)
#         im = self._to_nv12.Execute(im)
#         if self._encoder.EncodeSingleSurface(im, self._buffer, sync=False):
#             self._outfile.write(bytearray(self._buffer))

#     def flush(self):
#         if self._encoder.Flush(self._buffer):
#             self._outfile.write(bytearray(self._buffer))


# class SingleStreamCaptureHandler(cvb.SingleStreamHandler):

#     def __init__(self, device: cvb.Device, bridge: QmlBridge):
#         super().__init__(device.stream)
#         self._io = device.node_maps['Device']['Std::LineStatusAll']
#         self._bridge = bridge
#         bridge.stop_recording.connect(self.stop)
#         self._encoder = RGBEncoder({**{
#             'preset': ENC_PRESET,
#             'codec': CODEC,
#             's': f'{WIDTH}x{HEIGHT}',
#             'fps:': f'{FRAME_RATE}'}, **ENC_EXTRA_OPTIONS}, GPU_ID)
#         self._stopped = False
#         self._outfile = None

#         self.starttime = None
#         self.lasttime = None
#         self.framecount = None

#     def stop(self):
#         self._stopped = True
#         self._encoder.flush()
#         self._outfile.close()

#     def handle_async_wait_result_record(
#             self, image: cvb.StreamImage, status: cvb.WaitStatus):
#         if not self._stopped and status == cvb.WaitStatus.Ok:
#             self._encoder.save_image(image)
#             self.framecount += 1
#             t = time.time()
#             if (t - self.lasttime) > 5:
#                 self.lasttime = t
#                 fps = self.framecount / (t - self.starttime)
#                 print(f'FPS: {fps}')

#     def handle_async_wait_result(  # pylint: disable=method-hidden
#             self, image: cvb.StreamImage, status: cvb.WaitStatus):
#         if self._io.value != 0 and status == cvb.WaitStatus.Ok:
#             if self._bridge.participant_id == '':
#                 self._bridge.participant_id = token_hex(10)
#             p = Path(OUTPUT_DIR, f'{self._bridge.participant_id}.{CODEC}')
#             p2 = Path(OUTPUT_DIR, f'{self._bridge.participant_id}.txt')
#             with p2.open('w') as tstamp_file:
#                 tstamp_file.write(str(datetime.now()))
#             self._outfile = open(p, "wb")
#             self._encoder.set_output_file(self._outfile)
#             self._encoder.save_image(image)
#             self._bridge.recording_started.emit()
#             self.handle_async_wait_result = self.handle_async_wait_result_record

#             self.starttime = time.time()
#             self.lasttime = time.time()
#             self.framecount = 1


# def configure_device(device: cvb.Device) -> None:
#     dnode = device.node_maps['Device']
#     dnode['Cust::autoBrightnessMode'].value = 'Off'
#     dnode['Std::BalanceWhiteAuto'].value = 'OnDemand'
#     dnode['Std::AcquisitionFrameRate'].value = FRAME_RATE
#     dnode['Std::Width'].value = WIDTH
#     dnode['Std::Height'].value = HEIGHT
#     dnode['Std::TriggerMode'].value = 'Off'
#     #dnode['Std::GevSCPSPacketSize'].value = 8192


# def main():
#     Path(OUTPUT_DIR).mkdir(0o755, parents=True, exist_ok=True)
#     app = QApplication([])
#     app.setOrganizationName('University of Nottingham')
#     app.setOrganizationDomain('https://www.horizon.ac.uk/')
#     app.setApplicationName('VHQ2 Camera Recorder')

#     qmlBridge = QmlBridge()

#     driver = os.path.join(cvb.install_path(), 'drivers', 'GenICam.vin')
#     with cvb.DeviceFactory.open(driver, port=0) as device:
#         configure_device(device)
#         handler = SingleStreamCaptureHandler(device, qmlBridge)
#         cvb.ui.ImageViewItem.register()

#         view = QQuickView()

#         context = view.rootContext()
#         image_controller = cvb.ui.ImageController()
#         image_controller.refresh(device.device_image, cvb.ui.AutoRefresh.On)
#         qmlBridge.recording_started.connect(lambda: image_controller.refresh(
#             device.device_image, cvb.ui.AutoRefresh.Off))
#         context.setContextProperty('mainImage', image_controller)
#         context.setContextProperty('qmlBridge', qmlBridge)

#         def adjust_white_balance():
#             nm = device.node_maps['Device']
#             nm['Cust::balanceWhiteAutoOnDemandCmd'].execute()
#         qmlBridge.adjust_white_balance.connect(adjust_white_balance)

#         view.setResizeMode(QQuickView.SizeRootObjectToView)
#         view.setSource(QUrl.fromLocalFile(os.path.join(
#             os.path.dirname(os.path.realpath(__file__)), 'capture.qml')))
#         view.resize(int(WIDTH/2), int(HEIGHT/2))
#         view.show()

#         handler.run()
#         app.exec_()
#         handler.try_finish()


# if __name__ == '__main__':
#     main()
