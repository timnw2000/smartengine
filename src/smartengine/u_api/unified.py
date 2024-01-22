from . import subscribe, set

class uApi(subscribe.ApiSubscription, set.ApiSetting):

    def __repr__(self):
        return f"{__class__.__name__}({self.user}, {self.password}, {self.ip})"
    
    