class VisualCriteria:
    """
    An interim class for holding & organizing information before being passed to 
    a 'logical criteria' object (that is part of the td_data_collector package)
    """
    def __init__(self, list_crit):
        self.type = 0
        if list_crit[0] == 'input':
            self.type = 1
        if self.type == 0:
            self.day1 = list_crit[1]
            self.time1 = list_crit[2]
            self.comp = list_crit[3][1]
            self.day2 = list_crit[4]
            self.day3 = list_crit[5]
        elif self.type == 1:
            self.input_field = list_crit[1]
            self.comp = list_crit[2][1]
            self.value = list_crit[3]
