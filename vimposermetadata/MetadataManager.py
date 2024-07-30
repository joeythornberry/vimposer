class TimeSignatureChange:
    numerator: int  
    denominator: int

    def __init__(self, numerator, denominator) -> None:
        self.numerator = numerator
        self.denominator = denominator

class MetadataManager:
    time_signature_changes: dict[int, TimeSignatureChange]

    def __init__(self):
        self.time_signature_changes = {}
        self.record_time_signature_change(0, 4, 2)
        self.record_time_signature_change(48, 6, 3)
        self.record_time_signature_change(96, 2, 2)
    
    def record_time_signature_change(self, x: int, numerator: int, denominator_power_of_two: int):
        self.time_signature_changes[x] = TimeSignatureChange(numerator, 2**denominator_power_of_two)
