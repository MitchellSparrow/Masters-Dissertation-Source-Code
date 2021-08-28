""" Common Vision Blox Image Manager module for Python"""

import platform as _pl
import sys as _sys
import os as _os

_platform = _pl.system()
_machine = _pl.machine()
_arch = _pl.architecture()[0]


if _platform == "Windows" and (_sys.version_info.major != 3 or _sys.version_info.minor < 5):
  raise RuntimeError("only Python >= 3.5 supported on Windows")
elif _platform == "Linux" and (_sys.version_info.major != 3 or _sys.version_info.minor < 5):
  raise RuntimeError("only Python >= 3.5 supported on Linux")


# add the cvb module path to the PYTHONPATH
try:
    site_packages = next(p for p in _sys.path if 'site-packages' in p)
    importpath = _os.path.join(site_packages,"cvb")
    _sys.path.append(importpath)
except SystemError:
    raise RuntimeError("Could not append cvb module path to PYTHONPATH")

# since python 3.8 dll load paths have to be added manually on Windows
# https://bugs.python.org/issue36085  
python38 = 38
if eval(str(_sys.version_info.major)+str(_sys.version_info.minor)) >= python38 and _platform == "Windows":
  _os.add_dll_directory(_os.environ["CVB"])

import _cvb

_mbi_id = _cvb._mbi_id

def wrapper_version():
  """()

  Get the full version string for CVBpy and all its submodules.

  Returns
  -------
	  str
		  Complete version string.
  """
  return _mbi_id()

# numpy import
try:
  from numpy import array as _cvb2np_array
  from numpy import empty as _cvb2np_empty
  from numpy import uint8 as _cvb2np_uint8
  from numpy import int8 as _cvb2np_int8
  from numpy import uint16 as _cvb2np_uint16
  from numpy import int16 as _cvb2np_int16
  from numpy import float32 as _cvb2np_float32
  from numpy import float64 as _cvb2np_float64
  _cvb2np_available = True
except ImportError:
  _cvb2np_available = False



NotifyArgs = _cvb.NotifyArgs
NotifyObservable = _cvb.NotifyObservable

_PixelDataType = _cvb.PixelDataType
PixelDataType =  _cvb.PixelDataType()
_ConnectionState = _cvb.ConnectionState
ConnectionState = _cvb.ConnectionState()
_ColorModel = _cvb.ColorModel
ColorModel =  _cvb.ColorModel()
_DeviceUpdateMode = _cvb.DeviceUpdateMode
DeviceUpdateMode =  _cvb.DeviceUpdateMode()
_PlaneNormalization = _cvb.PlaneNormalization
PlaneNormalization =  _cvb.PlaneNormalization()
_SubPixelMode = _cvb.SubPixelMode
SubPixelMode = _cvb.SubPixelMode()
_Neighborhood = _cvb.Neighborhood
Neighborhood = _cvb.Neighborhood()
_MappingOption = _cvb.MappingOption
MappingOption = _cvb.MappingOption()
_PanoramaDirection = _cvb.PanoramaDirection
PanoramaDirection = _cvb.PanoramaDirection()
_CoordinateSystemType = _cvb.CoordinateSystemType
CoordinateSystemType = _cvb.CoordinateSystemType()
_BufferLayout = _cvb.BufferLayout
BufferLayout =  _cvb.BufferLayout()

_PfncFormat = _cvb.PfncFormat
PfncFormat = _cvb.PfncFormat()

NetworkConnection = _cvb.NetworkConnection

_StopWatchMode = _cvb.StopWatchMode
StopWatchMode =  _cvb.StopWatchMode()

_DiscoveryProperties = _cvb.DiscoveryProperties
DiscoveryProperties =  _cvb.DiscoveryProperties()
_DiscoverFlags = _cvb.DiscoverFlags
DiscoverFlags =  _cvb.DiscoverFlags()
_ModuleLayer = _cvb.ModuleLayer
ModuleLayer =  _cvb.ModuleLayer()
_DeviceState = _cvb.DeviceState
DeviceState = _cvb.DeviceState()
_NotifyDataType = _cvb.NotifyDataType
NotifyDataType= _cvb.NotifyDataType()
_WaitStatus = _cvb.WaitStatus
WaitStatus =  _cvb.WaitStatus()
_RingBufferLockMode = _cvb.RingBufferLockMode
RingBufferLockMode =  _cvb.RingBufferLockMode()
_PlaybackMode = _cvb.PlaybackMode
PlaybackMode =  _cvb.PlaybackMode()
_AcquisitionInterface = _cvb.AcquisitionInterface
AcquisitionInterface =  _cvb.AcquisitionInterface()
_StreamInfo = _cvb.StreamInfo
StreamInfo =  _cvb.StreamInfo()
_DeviceControlOperation = _cvb.DeviceControlOperation
DeviceControlOperation = _cvb.DeviceControlOperation()


_PointCloudFlags = _cvb.PointCloudFlags
PointCloudFlags = _cvb.PointCloudFlags()
_PointCloudLayout = _cvb.PointCloudLayout
PointCloudLayout = _cvb.PointCloudLayout()
_DownSampleMode = _cvb.DownSampleMode
DownSampleMode = _cvb.DownSampleMode()


StreamImage = _cvb.StreamImage
BufferImage = _cvb.BufferImage
RingBufferImage = _cvb.RingBufferImage
DeviceImage = _cvb.DeviceImage
VinDeviceImage = _cvb.VinImage
EmuDeviceImage = _cvb.EmuImage
VideoDeviceImage = _cvb.VideoImage

Device = _cvb.Device
VinDevice = _cvb.VinDevice
VideoDevice = _cvb.VideoDevice
EmuDevice = _cvb.EmuDevice
NonStreamingDevice = _cvb.NonStreamingDevice



_NumberRepresentation = _cvb.NumberRepresentation
NumberRepresentation =  _cvb.NumberRepresentation()
_ReadWriteVerify = _cvb.ReadWriteVerify
ReadWriteVerify =  _cvb.ReadWriteVerify()
_AccessMode = _cvb.AccessMode
AccessMode =  _cvb.AccessMode()
_CacheMode = _cvb.CacheMode
CacheMode =  _cvb.CacheMode()
_Visibility = _cvb.Visibility
Visibility =  _cvb.Visibility()


BooleanNode = _cvb.BooleanNode
CategoryNode = _cvb.CategoryNode
CommandNode = _cvb.CommandNode
EnumEntryNode = _cvb.EnumEntryNode
EnumerationNode = _cvb.EnumerationNode
FloatNode = _cvb.FloatNode
FloatRegNode = _cvb.FloatRegNode
IntRegNode = _cvb.IntRegNode
IntegerNode = _cvb.IntegerNode
Node = _cvb.Node
PortNode = _cvb.PortNode
RegisterNode = _cvb.RegisterNode
SelectorNode = _cvb.SelectorNode
StringNode = _cvb.StringNode
StringRegNode = _cvb.StringRegNode
ValueNode = _cvb.ValueNode

DigitalIO = _cvb.DigitalIO
DeviceControlCommand = _cvb.DeviceControlCommand
DeviceControl = _cvb.DeviceControl
ImageRect = _cvb.ImageRect
IndexedStream = _cvb.IndexedStream
RingBuffer = _cvb.RingBuffer
SoftwareTrigger = _cvb.SoftwareTrigger
Stream = _cvb.Stream
StreamStatistics = _cvb.StreamStatistics
NodeMap = _cvb.NodeMap
GenApiVersion = _cvb.GenApiVersion
StopWatch = _cvb.StopWatch
RateCounter = _cvb.RateCounter
DeviceFactory = _cvb.DeviceFactory

DiscoveryInformation = _cvb.DiscoveryInformation
VinConnectionInformation = _cvb.VinConnectionInformation
WhiteBalanceFactors = _cvb.WhiteBalanceFactors
LocalMaximum = _cvb.LocalMaximum














Point2D = _cvb.Point2D
Vector2D = _cvb.Point2D
Calibrator3D = _cvb.Calibrator3D
PointCloud = _cvb.PointCloud
SparsePointCloud = _cvb.SparsePointCloud
DensePointCloud = _cvb.DensePointCloud
PointCloudFactory = _cvb.PointCloudFactory
Point3D = _cvb.Point3D
Vector3D = _cvb.Point3D
Point3DH = _cvb.Point3DH
Vector3DH = _cvb.Point3DH
Size2D = _cvb.Size2D
Plane3D = _cvb.Plane3D
Rect = _cvb.Rect
Angle = _cvb.Angle
Cuboid = _cvb.Cuboid
Matrix2D = _cvb.Matrix2D
Matrix3D = _cvb.Matrix3D
Matrix3DH = _cvb.Matrix3DH
AffineMatrix3D = _cvb.AffineMatrix3D
AffineMatrix2D = _cvb.AffineMatrix2D
Area2D = _cvb.Area2D
DataType = _cvb.DataType
Image = _cvb.Image
ImagePlane = _cvb.ImagePlane
WrappedImage = _cvb.WrappedImage
PanoramicMappedImage = _cvb.PanoramicMappedImage
Circle = _cvb.Circle
Ellipse = _cvb.Ellipse
Line2D = _cvb.Line2D
NumberRange = _cvb.NumberRange
AngleRange = _cvb.AngleRange

LicenseInfo = _cvb.LicenseInfo
MagicNumberEntry = _cvb.MagicNumberEntry

MultiStreamHandler = _cvb.MultiStreamHandler
SingleStreamHandler = _cvb.SingleStreamHandler

AsyncWaitResult = _cvb.AsyncWaitResult

EventCookie = _cvb.EventCookie



version = _cvb.version
map_to_8bit = _cvb.map_to_8bit
normalize_min_max = _cvb.normalize_min_max
normalize_mean_variance = _cvb.normalize_mean_variance
expand_path = _cvb.expand_path
abs = _cvb.abs
acos = _cvb.acos
asin = _cvb.asin
atan = _cvb.atan
atan2 = _cvb.atan2
cos = _cvb.cos
cosh = _cvb.cosh
sin = _cvb.sin
sinh =  _cvb.sinh
tan = _cvb.tan
tanh = _cvb.tanh
sign = _cvb.sign
max = _cvb.max
min = _cvb.min
install_path = _cvb.install_path
data_path = _cvb.data_path
get_license_info = _cvb.get_license_info
wait_for_license = _cvb.wait_for_license
get_magic_number_entries = _cvb.get_magic_number_entries
calculate_white_balance_factors = _cvb.calculate_white_balance_factors
apply_white_balance_factors = _cvb.apply_white_balance_factors
affine_transform =_cvb.affine_transform
linear_transform = _cvb.linear_transform
polar_transform = _cvb.polar_transform
inverse_polar_transform = _cvb.inverse_polar_transform
inverse_polar_transform_to_dst = _cvb.inverse_polar_transform_to_dst
histogram = _cvb.histogram
find_local_maxima = _cvb.find_local_maxima
find_local_maxima_sub = _cvb.find_local_maxima_sub

difference_map = _cvb.difference_map

def _cvb2np_data_type(data_type):
  if not _cvb2np_available:
    raise NotImplementedError("not available without numpy")

  if data_type == DataType.int8_bpp_unsigned():
    return _cvb2np_uint8
  elif data_type == DataType.int8_bpp_signed():
    return _cvb2np_int8
  elif data_type == DataType.int16_bpp_unsigned() or data_type == DataType.int10_bpp_unsigned() or data_type == DataType.int12_bpp_unsigned():
    return _cvb2np_uint16
  elif data_type == DataType.int16_bpp_signed():
    return _cvb2np_int16
  elif data_type == DataType.float32_bpp():
    return _cvb2np_float32
  elif data_type == DataType.float64_bpp():
    return _cvb2np_float64
  else:
    raise NotImplementedError("unable to map data type to numpy")

def as_array(buffer, copy=False):
  """(buffer, copy)

  Maps an image or a plane to a numpy array.

  Parameters
  ----------
  buffer : cvb.Image / cvb.ImagePlane / cvb.PointCloud
    CVB object containing buffer to be mapped (Image, PointCloud, ImagePlane).

  copy : bool
		Force to copy, otherwise try to avoid a copy if possible.

  Returns
  -------
	  numpy.array
		  Newly created array.
  """
  if not _cvb2np_available:
    raise NotImplementedError("not available without numpy")

  if buffer._np_compliant:
    np_array =  _cvb2np_array(buffer, dtype=None, copy=copy, order=None)
    return np_array



  if type(buffer) is ImagePlane:
    image = buffer.map()
  elif type(buffer) is Image:
    image = buffer

  planeCount = len(image.planes)

  np_array = _cvb2np_empty([image.height, image.width] if planeCount == 1 else [image.height, image.width, planeCount], _cvb2np_data_type(image.planes[0].data_type), order="C")
  wrappedImage = WrappedImage.from_buffer(np_array)
  image.copy(wrappedImage)
  return np_array;



