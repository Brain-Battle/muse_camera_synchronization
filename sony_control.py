import socket
from xml.etree import ElementTree
import requests
import json
from enum import Enum

class CameraJSONErrorCodes(Enum):
    ERROR_ANY = 1
    ERROR_TIMEOUT = 2
    ERROR_ILLEGAL_ARGUMENT = 3
    ERROR_ILLEGAL_DATA_FORMAT = 4
    ERROR_ILLEGAL_REQUEST = 5
    ERROR_ILLEGAL_RESPONSE = 6
    ERROR_ILLEGAL_STATE = 7
    ERROR_ILLEGAL_TYPE = 8
    ERROR_INDEX_OUT_OF_BOUNDS= 9
    ERROR_NO_SUCH_ELEMENT = 10
    ERROR_NO_SUCH_METHOD = 11
    ERROR_NO_SUCH_FIELD = 12
    ERROR_NULL_POINTER = 13
    ERROR_UNSUPPORTED_VER = 14
    ERROR_UNSUPPORTED_OP = 15
    ERROR_SHOOT_FAIL = 40400
    ERROR_CAMERA_NOT_READY = 40401
    ERROR_POLLING_ALREADY_RUNNING = 40402
    ERROR_CAPTURING_NOT_FINISHED = 40403
    ERROR_CONTENT_CANNOT_DELETE = 41003

class CameraException(Exception):
    def __init__(self, error_code, message=None):
        self.error_code = CameraJSONErrorCodes(error_code)
        if message == None:
            super().__init__(str(self.error_code))

class CameraNotFoundException(Exception):
    def __init__(self):
        super().__init__("Could not find camera via UPNP")

class SonyControl:
    def __init__(self):
        self._camera_url = None

    def pair_camera(self):
        """
            Gets API URL from the camera via UPNP M-Search method.

            URL is internal, so user does not see it.

            If this method fails, either try again after a while or

        """

        # Create socket, set time out of 10 secs
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.settimeout(10)

        # Multicast IP and Port
        server_ip = "239.255.255.250"
        port = 1900

        # M-Search message for UPNP
        message = 'M-SEARCH * HTTP/1.1\r\n' + \
                'HOST:239.255.255.250:1900\r\n' + \
                'MAN:\"ssdp:discover\"\r\n' + \
                'MX:10\r\n' + \
                'ST:urn:schemas-sony-com:service:ScalarWebAPI:1\r\n' + \
                '\r\n'

        try:
            # Send the message
            server.sendto(message.encode(), (server_ip, port))

            # Receiving times out after 10 secs
            resp = server.recv(1024)
        except:
            raise CameraNotFoundException()
        
        server.close()

        # Find the camera XML location 
        response = resp.split("\r\n")
        for line in response:
            if line.startswith("LOCATION: "):
                xml_location = line
                xml_location.replace("LOCATION: ", "")

        # Get XML describing the camera
        response = requests.get(xml_location)

        # Construct XML tree
        root = ElementTree.fromstring(response.content)

        # Namespaces of the XML tree
        namespace = {
            "ns0": "urn:schemas-upnp-org:device-1-0",
            "av": "urn:schemas-sony-com:av",
        }

        # Find service URL
        device = root.find("ns0:device", namespace)
        device_info = device.find("av:X_ScalarWebAPI_DeviceInfo", namespace)
        service_list = device_info.find("av:X_ScalarWebAPI_ServiceList", namespace)
        service = service_list.find("av:X_ScalarWebAPI_Service", namespace)
        service_url = service.find("av:X_ScalarWebAPI_ActionList_URL", namespace)

        camera_url = service_url.text + "/camera"

        self._camera_url = camera_url

        print(self._camera_url)

    def check_for_errors(self, json_text):
        # Raise error according to json
        if "error" in json_text:
            raise CameraException(int(json_text["error"][0]))

    def set_camera_url(self, camera_url):
        """
            Sets the camera URL. Requests are posted to this URL.
        """
        self._camera_url = camera_url

    def get_shoot_mode(self):
        data = {
            "method": "getShootMode",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        response = requests.post(self._camera_url, data=json_data)
        json_response = json.loads(response.text)
        self.check_for_errors(json_response)
        return json_response
    
    def get_supported_shoot_mode(self):
        data = {
            "method": "getSupportedShootMode",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        response = requests.post(self._camera_url, data=json_data)
        json_response = json.loads(response.text)
        self.check_for_errors(json_response)
        return json_response


    def set_shoot_mode(self, mode: str):
        data = {
            "method": "setShootMode",
            "params": [mode],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        response = requests.post(self._camera_url, data=json_data)
        json_response = json.loads(response.text)
        self.check_for_errors(json_response)
        return json_response

    def take_picture(self):
        data = {
            "method": "actTakePicture",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def await_take_picture(self):
        data = {
            "method": "awaitTakePicture",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def start_movie_recording(self):
        data = {
            "method": "startMovieRec",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def stop_movie_recording(self):
        data = {
            "method": "stop_movie_recording",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def start_live_view(self):
        data = {
            "method": "startLiveview",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def stop_live_view(self):
        data = {
            "method": "stopLiveview",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def start_live_view_with_size(self, size):
        data = {
            "method": "startLiveviewWithSize",
            "params": [size],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def get_live_view_size(self):
        data = {
            "method": "getLiveviewsize",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def get_supported_live_view_size(self):
        data = {
            "method": "getSupportedLiveviewSize",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def set_live_view_frame_info(self, info: bool):
        bool_text = "true" if True else "false"

        data = {
            "method": "setLiveviewFrameInfo",
            "params": [bool_text],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def get_live_view_frame_info(self):
        data = {
            "method": "getLiveviewFrameInfo",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def act_zoom(self, direction: str, movement: str):
        """
            Performs a defined zoom action on the camera.

            Arguments:
            - direction (str): Can be "in" or "out", sets if camera zooms in or out
            - movement (str): Can be "start", "stop", or "1push". "start" starts the 
            zoom action, "stop" stops the zoom action, "1push" performs a slight movement and stops.
            
            Every "start" action should be followed by another act_zoom() call with a "stop".
            For example, after calling act_zoom("in", "start"), users should call act_zoom("in", "stop")
            to stop the movement.

            Returns:
            - json_response: The response from the API, in JSON format.
        """
        
        data = {
            "method": "actZoom",
            "params": [direction, movement],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def set_zoom_setting(self, setting: str):
        """
            Set the zoom settings of the camera.

            Arguments:
            - setting (str): This is the setting to apply. Can be one of the following:
                - "optical_only": Makes the camera use optical zoom only
                - "smart_only": Makes the camera use smart zoom only
                - "clear_image": Turns on the clear image zoom feature
                - "on_digital_zoom": Turns on the digital zoom feature
                - "off_digital_zoom": Turns off the digital zoom feature 

            Returns:
            - json_response: The response from the API, in JSON format.
        """

        zoom_settings = {
            "optical_only": "Optical Zoom Only",
            "smart_only": "Smart Zoom Only",
            "clear_image": "On:Clear Image Zoom",
            "on_digital_zoom": "On:Digital Zoom",
            "off_digital_zoom": "Off:Digital Zoom"
        }

        data = {
            "method": "setZoomSetting",
            "params": [zoom_settings[setting]],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def get_zoom_setting(self):
        data = {
            "method": "getZoomSetting",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def get_supported_zoom_setting(self):
        data = {
            "method": "getSupportedZoomSetting",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def act_half_press_shutter(self):
        data = {
            "method": "actHalfPressShutter",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def cancel_half_press_shutter(self):
        data = {
            "method": "cancelHalfPressShutter",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def setTouchAFPosition(self, x: float, y: float):
        """
            Set the touch AF position of the camera.

            Arguments:
            - x (float): x coordinate as a float
            - y (float): y coordinate as a float

            Returns:
            - json_response: The response from the API, in JSON format.
        """
        
        data = {
            "method": "getAvailableApiList",
            "params": [x, y],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def get_touch_af_position(self):
        data = {
            "method": "getTouchAFPosition",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def cancel_touch_af_position(self):
        data = {
            "method": "cancelTouchAFPosition",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def act_tracking_focus(self, x_pos: float, y_pos: float):
        data = {
            "method": "actTrackingFocus",
            "params": [{
                "xPosition": x_pos,
                "yPosition": y_pos
            }],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def cancel_tracking_focus(self):
        data = {
            "method": "cancelTrackingFocus",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def set_tracking_focus(self, mode: str):
        """
            Set tracking focus mode.

            Arguments:
            - mode (str): Can be one of the following.
                - "off": Turns off tracking focus
                - "on": Turns on tracking focus
                - "track": Tracks a subject
                - "no_track": Does not track a subject
        """
        
        tf_settings = {
            "off": "Off",
            "on": "On",
            "track": "Tracking",
            "no_track": "Not Tracking"
        }

        data = {
            "method": "setTrackingFocus",
            "params": [{
                "trackingFocus": tf_settings[mode]
            }],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def get_tracking_focus(self):
        data = {
            "method": "getTrackingFocus",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def get_supported_tracking_focus(self):
        data = {
            "method": "getSupportedTrackingFocus",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response


    def set_self_timer(self, time: int):
        """
            Sets the timer of the camera.

            Arguments:
            - time (int): time in seconds        
        """
        
        data = {
            "method": "setSelfTimer",
            "params": [time],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def get_self_timer(self):
        data = {
            "method": "getSelfTimer",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response
    
    def get_supported_self_timer(self):
        data = {
            "method": "getSupportedSelfTimer",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def get_available_apis(self):
        data = {
            "method": "getAvailableApiList",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response

    def take_picture(self):
        data = {
            "method": "actTakePicture",
            "params": [],
            "id": 1,
            "version": "1.0"
        }

        json_data = json.dumps(data)
        json_response = requests.post(self._camera_url, data=json_data)
        self.check_for_errors(json_response)
        return json_response