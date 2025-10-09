# # src/signal_controller.py

# class SignalController:
#     def __init__(self, min_green=5, yellow_time=2, red_time=5):
#         """
#         min_green: minimum green light duration (seconds)
#         yellow_time: yellow light duration (seconds)
#         red_time: red light duration (seconds)
#         """
#         self.state = "RED"
#         self.timer = 0
#         self.min_green = min_green
#         self.yellow_time = yellow_time
#         self.red_time = red_time

#     def update(self, vehicle_count, dt=1):
#         """
#         Update the traffic light state based on vehicle count and elapsed time (dt in seconds)
#         """
#         self.timer += dt

#         if self.state == "RED":
#             # If red time passed and vehicles waiting, turn green
#             if self.timer >= self.red_time and vehicle_count > 0:
#                 self.state = "GREEN"
#                 self.timer = 0

#         elif self.state == "GREEN":
#             # Keep green for min_green time, then switch to yellow
#             if self.timer >= self.min_green:
#                 self.state = "YELLOW"
#                 self.timer = 0

#         elif self.state == "YELLOW":
#             # Yellow lasts for fixed time, then go to red
#             if self.timer >= self.yellow_time:
#                 self.state = "RED"
#                 self.timer = 0

#         return self.state


# src/signal_controller.py

class SignalController:
    def __init__(self, base_green=5, base_red=5, yellow_time=2):
        self.state = "RED"
        self.timer = 0
        self.time_in_state = 0
        self.base_green = base_green
        self.base_red = base_red
        self.yellow_time = yellow_time
        self.current_duration = base_red

    def update(self, vehicle_count, dt):
        """
        Update the traffic signal based on traffic density and elapsed time.
        """

        self.time_in_state += dt

        # Adjust green duration based on vehicle density
        # More vehicles → longer green, less vehicles → shorter green
        green_duration = self.base_green + min(vehicle_count // 3, 10)
        red_duration = self.base_red

        # Transition logic between states
        if self.state == "GREEN" and self.time_in_state >= green_duration:
            self.state = "YELLOW"
            self.time_in_state = 0
            self.current_duration = self.yellow_time

        elif self.state == "YELLOW" and self.time_in_state >= self.yellow_time:
            self.state = "RED"
            self.time_in_state = 0
            self.current_duration = red_duration

        elif self.state == "RED" and self.time_in_state >= red_duration:
            self.state = "GREEN"
            self.time_in_state = 0
            self.current_duration = green_duration

        return self.state, self.current_duration - self.time_in_state
