#!/usr/bin/env python3

import exiftool
from CUSP_error_types import Error
import os
from datetime import datetime
import stat
from exiftool import ExifToolHelper
from mock_gps import *
from picamera2 import Picamera2


def device_exists(path):
    try:
        return stat.S_ISBLK(os.stat(path).st_mode)
    except:
        return False


picam2 = Picamera2()
picam2.start()


def capture_rgb():
    # Check for presence of camera
    # check ls /dev/video1
    """
    if device_exists("/dev/video1") == False:
        return Error.CAMERA_MISSING
    """

    # Set file name
    dt = datetime.now()
    filename = dt.strftime("%Y-%m-%d_%H-%M-%S") + "_RGB.jpg"
    # Capture image
    OUTPUT_PATH = "/home/sixth/images/"
    metadata = picam2.capture_file(OUTPUT_PATH + filename)
    print(metadata)

    if write_metadata(OUTPUT_PATH + filename) == Error.NO_ERROR:
        return Error.NO_ERROR

    return Error.CAPTURE_ERROR


def capture_thermal():
    # Check for presence of camera
    # check ls /dev/video0, if nothing return an error
    """
    if device_exists("/dev/video0") == False:
        return Error.CAMERA_MISSING
    """

    # Set file name
    dt = datetime.now()
    filename = dt.strftime("%Y-%m-%d_%H-%M-%S") + "_IR"
    # Capture image

    # Currently saving as RAW in the beta build
    LEPTON_DATA_COLLECTOR_PATH = (
        "sudo $HOME/CUSP/external/lepton_data_collector/lepton_data_collector"
    )
    OUTPUT_PATH = "/home/sixth/images/"
    cmd = LEPTON_DATA_COLLECTOR_PATH + " -3 -c 1 -o" + OUTPUT_PATH + filename

    os.system(cmd)
    cmd = "sudo chown sixth:sixth " + OUTPUT_PATH + filename + "000000.gray"
    os.system(cmd)

    """
    if write_metadata(OUTPUT_PATH + filename) == Error.NO_ERROR:
        return Error.NO_ERROR
    """

    # return Error.CAPTURE_ERROR
    return Error.NO_ERROR


def write_metadata(filename):
    latitude, longitude, altitude = GPS_dev.get_GPS_data()
    with ExifToolHelper() as et:
        et.set_tags(
            [filename],
            tags={
                "GPSLatitude": latitude,
                "GPSLongitude": longitude,
                "GPSAltitude": altitude,
            },
            params=["-P", "-overwrite_original"],
        )
    return Error.NO_ERROR
