class SSMResponse:
    def __init__(self):
        self.data = None
        self.error = None
        self.additional_info = None
        self.is_error = None
        self.response = {}

    def add_error_field(self, **kwargs):
        self.is_error = True
        self.error = self.error if self.error else {}

        for keyword in kwargs:
            self.error[keyword] = kwargs[keyword]

    def add_data_field(self, **kwargs):
        self.is_error = False
        self.data = self.data if self.data else {}

        for keyword in kwargs:
            self.data[keyword] = kwargs[keyword]

    def add_additional_info_field(self, **kwargs):
        self.additional_info = self.additional_info if self.additional_info else {}
        for keyword in kwargs:
            self.additional_info[keyword] = kwargs[keyword]

    def get_response(self):

        if self.is_error:
            self.data = None
        else:
            self.error = None

        self.response = {
            "data": self.data,
            "error": self.error,
            "additional_info": self.additional_info,
        }

        return self.response
