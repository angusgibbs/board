from time import sleep

import pygame

SEAT_SIZE = 12
SEAT_SPACING = 3
AISLE_SPACING = 18

COLOR_PLANE = 255, 255, 255
COLOR_EMPTY_SEAT = 255, 0, 0
COLOR_FULL_SEAT = 0, 255, 0
COLOR_PERSON = 255, 255, 0

class Sim:
    """Simulate the boarding of a plane.

    Args:
        plane_info (dict): A dictionary containing the following keys:
            num_rows (int): The number of rows on the plane
            num_seats (int): The number of seats in a row
            aisle_location (int): The index of the seat (from the left wall)
                that comes before the the aisle
        passenger_list (list of Passenger): The passengers who need to board
        board_order (list of int): A sorted list of passenger IDs indicating
            the order in which passengers should board
    """
    def __init__(self, plane_info, passenger_list, board_order):
        self.plane_info = plane_info
        self.passenger_list = [passenger_list[i - 1] for i in board_order]

    def board(self):
        """Render a set of passengers boarding a plane."""
        self._render_init()

        self.filled_seats = {}
        self.current_passenger = 0
        self.queued_passengers = []

        steps = 0
        while 1:
            should_quit = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True

            if (self.current_passenger == len(self.passenger_list) and
                len(self.queued_passengers) == 0):
                break

            if should_quit:
                break

            self.screen.fill(COLOR_PLANE)
            self._step()
            self._render_plane()
            self._render_passengers()

            pygame.display.flip()
            steps += 1
            sleep(0.25)

        print('{} steps needed'.format(steps))

    def _render_init(self):
        """Sets up Pygame with the correct screen size.

        Args:
            plane_info (dict): A dictionary describing the plane. See
                `render_boarding`.
        """
        pygame.init()
        self.SCREEN_HEIGHT = (SEAT_SPACING +
            self.plane_info['num_rows'] * (SEAT_SIZE + SEAT_SPACING))
        self.SCREEN_WIDTH = (AISLE_SPACING + SEAT_SPACING +
            self.plane_info['num_seats'] * (SEAT_SIZE + SEAT_SPACING))

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                               self.SCREEN_HEIGHT))

        self.screen.fill(COLOR_PLANE)

    def _step(self):
        # Look for any passengers in the queue that have reached their row and
        # thus can be seated
        new_queue = []
        for passenger in self.queued_passengers:
            if passenger['current_row'] == passenger['row']:
                self.filled_seats[(passenger['row'], passenger['seat'])] = True
            else:
                new_queue.append(passenger)
        self.queued_passengers = new_queue

        # Move everyone in the queue forward if possible
        row_used = [False] * (self.plane_info['num_rows'] + 1)
        for passenger in self.queued_passengers:
            if not row_used[passenger['current_row'] + 1]:
                passenger['current_row'] += 1
                row_used[passenger['current_row']] = True

        # Bring a new person into the queue if possible
        if not row_used[1] and self.current_passenger < len(self.passenger_list):
            self.passenger_list[self.current_passenger]['current_row'] = 1
            self.queued_passengers.append(
                self.passenger_list[self.current_passenger])
            self.current_passenger += 1

    def _render_plane(self):
        """Render a plane, with an aisle and seats."""
        seat_y = SEAT_SPACING
        for row in range(1, self.plane_info['num_rows'] + 1):
            seat_x = SEAT_SPACING
            for seat in range(1, self.plane_info['num_seats'] + 1):
                color = (COLOR_FULL_SEAT if (row, seat) in self.filled_seats
                                         else COLOR_EMPTY_SEAT)
                pygame.draw.rect(self.screen, color,
                                 [seat_x, seat_y, SEAT_SIZE, SEAT_SIZE])

                seat_x += SEAT_SIZE + SEAT_SPACING

                if seat == self.plane_info['aisle_location']:
                    seat_x += AISLE_SPACING

            seat_y += SEAT_SIZE + SEAT_SPACING

    def _render_passengers(self):
        aisle_x = (SEAT_SPACING +
                   (SEAT_SPACING + SEAT_SIZE) * self.plane_info['aisle_location'])
        for passenger in self.queued_passengers:
            pygame.draw.rect(self.screen, COLOR_PERSON,
                [aisle_x, SEAT_SPACING + (SEAT_SPACING + SEAT_SIZE) * (passenger['current_row'] - 1), SEAT_SIZE, SEAT_SIZE])
