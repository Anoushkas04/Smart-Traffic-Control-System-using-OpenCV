# src/signal_controller.py

class SignalController:
    """
    Manages the state of a 4-way intersection with two phases.
    Phase 1: North-South (NS) traffic flows.
    Phase 2: East-West (EW) traffic flows.
    """
    # Define the states for the entire intersection
    NS_GREEN = "ns_green"
    NS_YELLOW = "ns_yellow"
    EW_GREEN = "ew_green"
    EW_YELLOW = "ew_yellow"
    ALL_RED = "all_red"

    def __init__(self, min_green_time=5, max_green_time=20, yellow_time=3, all_red_time=2, default_phase=NS_GREEN):
        """
        Initializes the SignalController.
        :param min_green_time: Minimum duration for a green light.
        :param max_green_time: Maximum duration for a green light.
        :param yellow_time: Duration for a yellow light.
        :param all_red_time: Duration for the all-red clearance interval.
        :param default_phase: The starting phase of the traffic light.
        """
        self.min_green_time = min_green_time
        self.max_green_time = max_green_time
        self.yellow_time = yellow_time
        self.all_red_time = all_red_time

        self.state = default_phase
        self.previous_state = None
        self.time_in_state = 0
        self.green_duration = self.max_green_time

    def update(self, densities, dt):
        """
        Updates the intersection state based on traffic densities and elapsed time.
        :param densities: A dictionary with vehicle counts for each phase, e.g., {'ns': 10, 'ew': 3}.
        :param dt: The time delta (in seconds) since the last update.
        :return: A dictionary representing the color of each signal, e.g., {'north': 'GREEN', ...}.
        """
        self.time_in_state += dt
        ns_vehicles = densities.get('ns', 0)
        ew_vehicles = densities.get('ew', 0)

        # --- State Transition Logic ---
        if self.state == self.NS_GREEN:
            if self.time_in_state >= self.green_duration:
                self._transition_to(self.NS_YELLOW)

        elif self.state == self.NS_YELLOW:
            if self.time_in_state >= self.yellow_time:
                self._transition_to(self.ALL_RED)

        elif self.state == self.EW_GREEN:
            if self.time_in_state >= self.green_duration:
                self._transition_to(self.EW_YELLOW)

        elif self.state == self.EW_YELLOW:
            if self.time_in_state >= self.yellow_time:
                self._transition_to(self.ALL_RED)

        elif self.state == self.ALL_RED:
            if self.time_in_state >= self.all_red_time:
                # Transition to the next green phase based on which yellow phase came before
                if self.previous_state == self.NS_YELLOW:
                    self._transition_to(self.EW_GREEN)
                    self.green_duration = self._calculate_green_duration(ew_vehicles, ns_vehicles)
                else:  # Assumes previous_state was EW_YELLOW
                    self._transition_to(self.NS_GREEN)
                    self.green_duration = self._calculate_green_duration(ns_vehicles, ew_vehicles)

        return self._get_signal_colors()

    def _calculate_green_duration(self, primary_traffic, secondary_traffic):
        """
        Calculates a dynamic green light duration based on traffic conditions.
        This heuristic can be tuned for better performance.
        """
        # Start with a base of min_green_time
        duration = self.min_green_time

        # Increase duration based on the number of vehicles in the primary direction
        if primary_traffic > 5:
            duration += 5
        if primary_traffic > 10:
            duration += 5
        
        # If there's heavy traffic in the secondary direction, consider reducing the green time
        # but not below the minimum, to prevent starvation.
        if secondary_traffic > 10 and duration > self.min_green_time + 5:
            duration -= 5

        # Ensure the duration is within the min/max bounds
        return max(self.min_green_time, min(duration, self.max_green_time))

    def _transition_to(self, new_state):
        """Helper to transition to a new state and reset the timer."""
        self.previous_state = self.state
        self.state = new_state
        self.time_in_state = 0

    def _get_signal_colors(self):
        """Returns a dictionary of signal colors based on the current state."""
        if self.state == self.NS_GREEN:
            return {'north': 'GREEN', 'south': 'GREEN', 'east': 'RED', 'west': 'RED'}
        elif self.state == self.NS_YELLOW:
            return {'north': 'YELLOW', 'south': 'YELLOW', 'east': 'RED', 'west': 'RED'}
        elif self.state == self.EW_GREEN:
            return {'north': 'RED', 'south': 'RED', 'east': 'GREEN', 'west': 'GREEN'}
        elif self.state == self.EW_YELLOW:
            return {'north': 'RED', 'south': 'RED', 'east': 'YELLOW', 'west': 'YELLOW'}
        elif self.state == self.ALL_RED:
            return {'north': 'RED', 'south': 'RED', 'east': 'RED', 'west': 'RED'}
        
        # Default return for safety, though it should not be reached with proper state management
        return {'north': 'RED', 'south': 'RED', 'east': 'RED', 'west': 'RED'}
