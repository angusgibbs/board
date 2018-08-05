import random

from sim import Sim

plane_info = {
  'num_rows': 38,
  'num_seats': 6,
  'aisle_location': 3
}

passenger_list = []
for row in range(1, plane_info['num_rows'] + 1):
  for seat in range(1, plane_info['num_seats'] + 1):
    passenger_list.append({
      'id': len(passenger_list) + 1,
      'row': row,
      'seat': seat
    })

board_order = list(range(1, len(passenger_list) + 1))
random.shuffle(board_order)

# board_order = list(range(len(passenger_list), 0, -1))

simulator = Sim(plane_info, passenger_list, board_order)
simulator.board()
