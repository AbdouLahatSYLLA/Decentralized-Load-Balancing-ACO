class Request:
    def __init__(self, request_id, arrival_time):
        self.id = request_id
        self.arrival_time = arrival_time
        self.completion_time = None
        self.assigned_server_id = None

    def response_time(self):
        if self.completion_time:
            return self.completion_time - self.arrival_time
        return None