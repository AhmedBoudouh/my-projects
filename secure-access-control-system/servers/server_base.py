from models.user import User
from logic.pin_train import extract_pin_from_train

class Server:
    # registry of all server instances (in creation order)
    registry = []

    def __init__(self, name, managed_zones):
        self.name = name
        self.default_zones = managed_zones[:]      # original ownership
        self.managed_zones = managed_zones[:]      # current ownership (can change)
        self.is_active = True
        Server.registry.append(self)

    # --- internal helpers for auto switch ---
    def _first_active_other_server(self):
        """Pick the first active server that isn't self."""
        for srv in Server.registry:
            if srv is not self and getattr(srv, "is_active", True):
                return srv
        return None

    def _distribute_zone_to_any_active(self, zone_number):
        """Give zone_number to the first active server (simple strategy)."""
        for srv in Server.registry:
            if srv is self:
                continue
            if srv.is_active and zone_number not in srv.managed_zones:
                srv.managed_zones.append(zone_number)
                print(f"[{srv.name}] Auto-taking over Zone {zone_number} (from {self.name})")
                return True
        print(f"[{self.name}] No active server available to take Zone {zone_number}")
        return False

    def _reclaim_default_zones(self):
        """On reactivation, reclaim default zones from others."""
        for z in self.default_zones:
            # If I already manage it, continue
            if z in self.managed_zones:
                continue
            # Remove from whoever has it now
            for srv in Server.registry:
                if srv is self:
                    continue
                if z in srv.managed_zones:
                    srv.managed_zones.remove(z)
                    print(f"[{self.name}] Reclaiming Zone {z} from {srv.name}")
                    break
            # Add to me
            if z not in self.managed_zones:
                self.managed_zones.append(z)
                print(f"[{self.name}] Zone {z} restored to default owner")

    # --- public switch controls (auto failover/recovery) ---
    def set_active(self, active: bool):
        # If no change, do nothing
        if self.is_active == active:
            state = "active" if active else "inactive"
            print(f"[{self.name}] Server already {state}")
            return

        self.is_active = active
        state = "active" if active else "inactive"
        print(f"[{self.name}] Server is now {state}")

        if not active:
            # Deactivate: move ALL currently managed zones away
            # (including non-default ones it had taken earlier)
            zones_to_move = self.managed_zones[:]
            self.managed_zones.clear()
            for z in zones_to_move:
                self._distribute_zone_to_any_active(z)
        else:
            # Reactivate: reclaim my defaults
            self._reclaim_default_zones()

    # --- routing helper used by UI if needed ---
    def _can_manage(self, zone_requested: int) -> bool:
        return self.is_active and (zone_requested in self.managed_zones)

    # --- unchanged scan_count validation ---
    def validate_scan_count(self, user_id, received_count):
        user = User.load_from_db(user_id)
        if not user:
            print(f"[{self.name}]  User not found.")
            return False, None

        expected = user.scan_count
        print(f"[{self.name}]  Received count: {received_count}")
        print(f"[{self.name}]  Expected count: {expected}")

        if received_count == expected:
            return True, user
        else:
            print(f"[{self.name}]  Invalid scan — possible cloning attempt.")
            return False, None

    # --- unified access for zones 1/2/3 (unchanged behavior) ---
    def process_access(
        self,
        user,
        zone_requested,
        x_used,
        pin_train=None,
        positions=None,
        entered_otp=None,
        expected_otp=None,
        biometric_train=None,
        biometric_positions=None,
    ):
        if not self._can_manage(zone_requested):
            print(f"[{self.name}]  Zone {zone_requested} not managed by this server.")
            return False

        if user.zone_level < zone_requested:
            print(f"[{self.name}]  User not authorized for Zone {zone_requested}.")
            return False

        # Zone 1 — scan_count only
        if zone_requested == 1:
            user.scan_count += x_used
            user.save_to_db()
            print(f"[{self.name}]  Access to Zone 1 granted. New scan_count = {user.scan_count}")
            return True

        # Zone 2 — PIN + OTP
        if zone_requested == 2:
            pin = extract_pin_from_train(pin_train, positions)
            if pin != user.pin_code:
                print(f"[{self.name}]  Invalid PIN.")
                return False
            if entered_otp != expected_otp:
                print(f"[{self.name}]  Invalid OTP.")
                return False
            user.scan_count += x_used
            user.save_to_db()
            print(f"[{self.name}]  Access to Zone 2 granted. New scan_count = {user.scan_count}")
            return True

        # Zone 3 — PIN + Biometric (no OTP)
        if zone_requested == 3:
            pin = extract_pin_from_train(pin_train, positions)
            if pin != user.pin_code:
                print(f"[{self.name}]  Invalid PIN (first step for biometric zone).")
                return False
            biometric_code = extract_pin_from_train(biometric_train, biometric_positions)
            if biometric_code != user.pin_code:
                print(f"[{self.name}]  Invalid biometric authentication.")
                return False
            user.scan_count += x_used
            user.save_to_db()
            print(f"[{self.name}]  Access to Zone 3 granted. New scan_count = {user.scan_count}")
            return True

        print(f"[{self.name}]  Unsupported zone {zone_requested}.")
        return False
