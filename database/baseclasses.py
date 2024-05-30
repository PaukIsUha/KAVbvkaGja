from datetime import datetime


class Orders:
    id: int
    order_number: str
    po: str
    name: str
    vendor: str
    comment: str
    count_fields = 5

    def __init__(self, data_arr: tuple):
        if len(data_arr) < self.count_fields:
            raise ValueError("init Orders by tuple not same size")

        self.id = data_arr[0]
        self.order_number = data_arr[1]
        self.po = data_arr[2]
        self.name = data_arr[3]
        self.vendor = data_arr[4]
        self.comment = data_arr[5] if len(data_arr) > self.count_fields else ''

        if self.comment is None:
            self.comment = ''

    @staticmethod
    def reinit(data_arr: list):
        return [Orders(order) for order in data_arr]

    def __repr__(self):
        return f"Orders: (id: {self.id}, order_number: {self.order_number}, " \
               f"po: {self.po}, name: {self.name}, vendor: {self.vendor}, " \
               f"comment: {self.comment})"


class Comments:
    id: int
    order_id: int
    comment: str
    created: datetime
    count_fields = 4

    def __init__(self, data_arr: tuple):
        if len(data_arr) != self.count_fields:
            raise ValueError("init Orders by tuple not same size")

        self.id = data_arr[0]
        self.order_id = data_arr[1]
        self.comment = data_arr[2]
        self.created = data_arr[3]

    @staticmethod
    def reinit(data_arr: list):
        return [Comments(cmnt) for cmnt in data_arr]

    def __repr__(self):
        return f"Comments: (id: {self.id}, order_id: {self.order_id}," \
               f" comment: {self.comment}, created: {self.created})"
