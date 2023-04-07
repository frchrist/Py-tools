class TlModel:
    def __init__(self):
        self.data = []
        
    def get_data(self):
        return self.data
    
    def add_data(self, new_data):
        self.data.append(new_data)
