class CostNotFoundException(Exception):
    def __init__(self, cost_id: int):
        self.cost_id = cost_id
        self.message = f"هزینه با شناسه {cost_id} یافت نشد."
        super().__init__(self.message)
