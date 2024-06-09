from datetime import datetime


class Orders:
    id: int
    order_number: str
    po: str
    name: str
    vendor: str
    buyer: str
    quantity: int
    approval_date: datetime
    promised_date: datetime
    shipped: int
    remainder: int
    trans_data: str

    comment: str
    comment_pc: str
    count_fields = 11

    def __init__(self, data_arr: tuple):
        if len(data_arr) < self.count_fields:
            raise ValueError("init Orders by tuple not same size")

        self.id = data_arr[0]
        self.order_number = data_arr[1]
        self.po = data_arr[2]
        self.name = data_arr[3]
        self.vendor = data_arr[4]
        self.quantity = 0 if data_arr[5] is None else data_arr[5]
        self.approval_date = '' if data_arr[6] is None else data_arr[6]
        self.promised_date = '' if data_arr[7] is None else data_arr[7]
        self.shipped = 0 if data_arr[8] is None else data_arr[8]
        self.remainder = None if self.quantity is None or self.shipped is None else self.quantity - self.shipped
        self.trans_data = '' if data_arr[9] is None else data_arr[9]
        self.buyer = '' if data_arr[10] is None else data_arr[10]

        self.comment = data_arr[11] if len(data_arr) > self.count_fields else ''
        self.comment_pc = data_arr[13] if len(data_arr) > self.count_fields else ''

        if self.comment is None:
            self.comment = ''

        if self.comment_pc is None:
            self.comment_pc = ''

    @staticmethod
    def reinit(data_arr: list):
        return [Orders(order) for order in data_arr]

    def __repr__(self):
        return f"Orders: (id: {self.id}, order_number: {self.order_number}, " \
               f"po: {self.po}, name: {self.name}, vendor: {self.vendor}, " \
               f"quantity: {self.quantity}, approval_date: {self.approval_date}, promised_date: {self.promised_date}, " \
               f"shipped: {self.shipped}, remainder: {self.remainder}, trans_data: {self.trans_data}, " \
               f"comment: {self.comment}, comment_pc: {self.comment_pc})"


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
