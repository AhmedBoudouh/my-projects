import random

class VirtualCard: # Represent a smart card
    def __init__(self, user_id, initial_scan_count=0, initial_x=None, zone_level=1):
        self.user_id = user_id
        self.scan_count = int(initial_scan_count)  
        self.x = int(initial_x) if initial_x else random.randint(5, 15) 
        self.locked = False
        self.zone_level = zone_level
        self.unauthorized_zone_attempts = 0

    def scan(self, valid=True): # simulate scanning card
        if self.locked:
            return None  

        received_count = self.scan_count
        old_x = self.x
        self.scan_count += old_x
        self.x = random.randint(5, 15) #new x for next scan (important)

        return {
            "count": received_count,
            "x_used": old_x,
            "new_count": self.scan_count,
            "new_x": self.x
        }

    def lock(self):
        self.locked = True #lock card

    def is_locked(self):
        return self.locked

    def get_state(self): #current state of the card 
        return {
            "scan_count": self.scan_count,
            "x": self.x,
            "locked": self.locked,
            "zone_level": self.zone_level

        }
