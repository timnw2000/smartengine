from . import subscribe, set


class uApi(subscribe.ApiSubscription, set.ApiSetting):
    """
    A unified API class that combines functionalities from ApiSubscription and ApiSetting.

    This class serves as an aggregate interface for both subscribing to streaming data and setting configurations 
    in a network system's API. It inherits methods and properties from ApiSubscription and ApiSetting classes, 
    enabling comprehensive control over data streaming and system settings through a single interface.

    Attributes:
        Inherits all attributes from both ApiSubscription and ApiSetting, including user credentials, IP address, 
        URL formatting, and specific error codes.

    Methods:
        __repr__: Returns a formal string representation of the uApi instance.

    By combining the capabilities of ApiSubscription and ApiSetting, this class allows for seamless integration 
    of data streaming and setting functionalities, facilitating easier management of network system's API interactions.

    Example:
        uapi = uApi(user='admin', password='secret', ipv4_adress='192.168.0.10')
        response = uapi.set_scenes(location='101', scene_name='Morning')
        print(response)
        for data in uapi.stream_location_data(location=101):
            print(data)
    """

    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, {self.ip})"
    
