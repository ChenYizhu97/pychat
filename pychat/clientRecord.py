class clientRecord():
    def __init__(self, msgsocket=None, svideosocket=None,rvideosocket=None,ip =None, window=None):
        self.msgsocket = msgsocket
        self.svideosocket = svideosocket
        self.rvideosocket = rvideosocket
        self.ip = ip
        self.window = window
