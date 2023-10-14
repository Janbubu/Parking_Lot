from enum import Enum
from datetime import datetime
from abc import ABC
class VehicleType(Enum):
    CAR, TRUCK, VAN, MOTORBIKE = 1, 2, 3, 4

class ParkingSpotType(Enum):
    HANDICAPPED, COMPACT, LARGE, MOTORBIKE, VIP = 1, 2, 3, 4, 5


class AccountStatus(Enum):
    ACTIVE, UNKNOWN = 1, 2


class ParkingTicketStatus(Enum):
    ACTIVE, PAID = 1, 2


class Address:
    def __init__(self, street, city, state, zip_code, country):
        self.__street_address = street
        self.__city = city
        self.__state = state
        self.__zip_code = zip_code
        self.__country = country


class Person():
    def __init__(self, name, address, email, phone):
        self.__name = name
        self.__address = address
        self.__email = email
        self.__phone = phone


class Account:
    def __init__(self, user_name, password, person, status=AccountStatus.ACTIVE):
        self.__user_name = user_name
        self.__password = password
        self.__person = person
        self.__status = status

    def reset_password(self):
        None


class Admin(Account):
    def __init__(self, user_name, password, person, status=AccountStatus.ACTIVE):
        super().__init__(user_name, password, person, status)

    def add_parking_floor(self, floor):
        None

    def add_parking_spot(self, floor_name, spot):
        None

    def add_parking_display_board(self, floor_name, display_board):
        None

    def add_entrance_panel(self, entrance_panel):
        None

    def add_exit_panel(self, exit_panel):
        None

class ParkingSpot(ABC):
    def __init__(self, number, parking_spot_type):
        self.__number = number
        self.__free = True
        self.__vehicle = None
        self.__parking_spot_type = parking_spot_type

    def is_free(self):
        return self.__free

    def assign_vehicle(self, vehicle):
        self.__vehicle = vehicle
        self.__free = False

    def remove_vehicle(self):
        self.__vehicle = None
        self.free = True


class HandicappedSpot(ParkingSpot):
    def __init__(self, number):
        super().__init__(number, ParkingSpotType.HANDICAPPED)


class CompactSpot(ParkingSpot):
    def __init__(self, number):
        super().__init__(number, ParkingSpotType.COMPACT)


class LargeSpot(ParkingSpot):
    def __init__(self, number):
        super().__init__(number, ParkingSpotType.LARGE)


class MotorbikeSpot(ParkingSpot):
    def __init__(self, number):
        super().__init__(number, ParkingSpotType.MOTORBIKE)


class VipSpot(ParkingSpot):
    def __init__(self, number):
        super().__init__(number, ParkingSpotType.VIP)


class ParkingFloor:
    def __init__(self, name):
        self.__name = name
        self.__handicapped_spots = {}
        self.__compact_spots = {}
        self.__large_spots = {}
        self.__motorbike_spots = {}
        self.__vip_spots = {}
        self.__info_portals = {}
        self.__free_handicapped_spot_count = {'free_spot': 0}
        self.__free_compact_spot_count = {'free_spot': 0}
        self.__free_large_spot_count = {'free_spot': 0}
        self.__free_motorbike_spot_count = {'free_spot': 0}
        self.__free_vip_spot_count = {'free_spot': 0}
        self.__display_board = ParkingDisplayBoard()

    def add_parking_spot(self, spot):
        switcher = {
            ParkingSpotType.HANDICAPPED: self.__handicapped_spots.put(spot.get_number(), spot),
            ParkingSpotType.COMPACT: self.__compact_spots.put(spot.get_number(), spot),
            ParkingSpotType.LARGE: self.__large_spots.put(spot.get_number(), spot),
            ParkingSpotType.MOTORBIKE: self.__motorbike_spots.put(spot.get_number(), spot),
            ParkingSpotType.VIP: self.__vip_spots.put(spot.get_number(), spot),
        }
        switcher.get(spot.get_type(), 'Wrong parking spot type')

    def assign_vehicleToSpot(self, vehicle, spot):
        spot.assign_vehicle(vehicle)
        switcher = {
            ParkingSpotType.HANDICAPPED: self.update_display_board_for_handicapped(spot),
            ParkingSpotType.COMPACT: self.update_display_board_for_compact(spot),
            ParkingSpotType.LARGE: self.update_display_board_for_large(spot),
            ParkingSpotType.MOTORBIKE: self.update_display_board_for_motorbike(spot),
            ParkingSpotType.VIP: self.update_display_board_for_vip(spot),
        }
        switcher(spot.get_type(), 'Wrong parking spot type!')

    def update_display_board_for_handicapped(self, spot):
        if self.__display_board.get_handicapped_free_spot().get_number() == spot.get_number():
            # find another free handicapped parking and assign to display_board
            for key in self.__handicapped_spots:
                if self.__handicapped_spots.get(key).is_free():
                    self.__display_board.set_handicapped_free_spot(self.__handicapped_spots.get(key))

            self.__display_board.show_empty_spot_number()

    def update_display_board_for_compact(self, spot):
        if self.__display_board.get_compact_free_spot().get_number() == spot.get_number():
            # find another free compact parking and assign to display_board
            for key in self.__compact_spots.key_set():
                if self.__compact_spots.get(key).is_free():
                    self.__display_board.set_compact_free_spot(self.__compact_spots.get(key))

            self.__display_board.show_empty_spot_number()

    def free_spot(self, spot):
        spot.remove_vehicle()
        switcher = {
            ParkingSpotType.HANDICAPPED: self.__free_handicapped_spot_count.update(
              free_spot = self.__free_handicapped_spot_count["free_spot"] + 1
            ),
            ParkingSpotType.COMPACT: self.__free_compact_spot_count.update(
              free_spot=self.__free_compact_spot_count["free_spot"] + 1
            ),
            ParkingSpotType.LARGE: self.__free_large_spot_count.update(
              free_spot=self.__free_large_spot_count["free_spot"] + 1
            ),
            ParkingSpotType.MOTORBIKE: self.__free_motorbike_spot_count.update(
              free_spot=self.__free_motorbike_spot_count["free_spot"] + 1
            ),
            ParkingSpotType.VIP: self.__free_vip_spot_count.update(
              free_spot=self.__free_vip_spot_count["free_spot"] + 1
            ),
        }

        switcher(spot.get_type(), 'Wrong parking spot type!')

    def get_parking_spots(self):
        return self.__parkign_spots

#ParkingDisplayBoard:** This class encapsulates a parking display board:

class ParkingDisplayBoard:
    def __init__(self, id):
        self.__id = id
        self.__handicapped_free_spot = None
        self.__compact_free_spot = None
        self.__large_free_spot = None
        self.__motorbike_free_spot = None
        self.__vip_free_spot = None

    def show_empty_spot_number(self):
        message = ""
        if self.__handicapped_free_spot.is_free():
            message += "Free Handicapped: " + self.__handicapped_free_spot.get_number()
        else:
            message += "Handicapped is full"
        message += "\n"

        if self.__compact_free_spot.is_free():
            message += "Free Compact: " + self.__compact_free_spot.get_number()
        else:
            message += "Compact is full"
        message += "\n"

        if self.__large_free_spot.is_free():
            message += "Free Large: " + self.__large_free_spot.get_number()
        else:
            message += "Large is full"
        message += "\n"

        if self.__motorbike_free_spot.is_free():
            message += "Free Motorbike: " + self.__motorbike_free_spot.get_number()
        else:
            message += "Motorbike is full"
        message += "\n"

        if self.__vip_free_spot.is_free():
            message += "Free Vip: " + self.__vip_free_spot.get_number()
        else:
            message += "Vip is full"

        print(message)



#ParkingLot:** Our system will have only one object of this class. This can be enforced by using the [Singleton](https://en.wikipedia.org/wiki/Singleton_pattern) pattern. In software engineering, the singleton pattern is a software design pattern that restricts the instantiation of a class to only one object.

import threading
#from .constants import *






class ParkingLot:
    instance = None
    class __OnlyOne:
        def __init__(self, name, address):
            self.__name = name
            self.__address = address
            self.__parking_rate = ParkingRate()

            self.__compact_spot_count = 0
            self.__large_spot_count = 0
            self.__motorbike_spot_count = 0
            self.__electric_spot_count = 0
            self.__max_compact_count = 0
            self.__max_large_count = 0
            self.__max_motorbike_count = 0
            self.__max_electric_count = 0

            self.__entrance_panels = {}#//////////////
            self.__exit_panels = {}
            self.__parking_floors = {}

            # all active parking tickets, identified by their ticket_number
            self.__active_tickets = {}

            self.__lock = threading.Lock()

    def __init__(self, name, address):
        if not ParkingLot.instance:
            ParkingLot.instance = ParkingLot.__OnlyOne(name, address)
        else:
            ParkingLot.instance.__name = name
            ParkingLot.instance.__address = address

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_new_parking_ticket(self, vehicle):
        if self.is_full(vehicle.get_type()):
            raise Exception('Parking full!')
    # synchronizing to allow multiple entrances panels to issue a new
    # parking ticket without interfering with each other
        self.__lock.acquire()
        ticket = ParkingTicket()
        vehicle.assign_ticket(ticket)
        ticket.save_in_DB()
        # if the ticket is successfully saved in the database, we can increment the parking spot count
        self.__increment_spot_count(vehicle.get_type())
        self.__active_tickets.put(ticket.get_ticket_number(), ticket)
        self.__lock.release()
        return ticket

    def is_full(self, type):
        # trucks and vans can only be parked in LargeSpot
        if type == VehicleType.Truck or type == VehicleType.Van:
            return self.__large_spot_count >= self.__max_large_count

        # motorbikes can only be parked at motorbike spots
        if type == VehicleType.Motorbike:
            return self.__motorbike_spot_count >= self.__max_motorbike_count

        # cars can be parked at compact or large spots
        if type == VehicleType.Car:
            return (self.__compact_spot_count + self.__large_spot_count) >= (self.__max_compact_count + self.__max_large_count)

        # electric car can be parked at compact, large or electric spots
        return (self.__compact_spot_count + self.__large_spot_count + self.__electric_spot_count) >= (self.__max_compact_count + self.__max_large_count                                                                                                  + self.__max_electric_count)

    # increment the parking spot count based on the vehicle type
    def increment_spot_count(self, type):
        large_spot_count = 0
        motorbike_spot_count = 0
        compact_spot_count = 0
        vip_spot_count = 0
        if type == VehicleType.Truck or type == VehicleType.Van:
            large_spot_count += 1
        elif type == VehicleType.Motorbike:
            motorbike_spot_count += 1
        elif type == VehicleType.Car:
            if self.__compact_spot_count < self.__max_compact_count:
                compact_spot_count += 1
            else:
                large_spot_count += 1
        else:  # electric car
            if self.__vip_spot_count < self.__max_vip_count:
                vip_spot_count += 1
            elif self.__compact_spot_count < self.__max_compact_count:
                compact_spot_count += 1
            else:
                large_spot_count += 1

        def is_full(self):
            for key in self.__parking_floors:
                if not self.__parking_floors.get(key).is_full():
                    return False
            return True

        def add_parking_floor(self, floor):
            # store in database
            None

        def add_entrance_panel(self, entrance_panel):
            # store in database
            None

        def add_exit_panel(self,  exit_panel):
            # store in database
            None
        def add_parking_floor(self, floor):
            self.__parking_floors[floor.get_name()] = floor
    class EntrancePanel:
        def process_vehicle_entry(self, vehicle, parking_lot):
            # Logic to issue a parking ticket and assign a parking spot to the vehicle
            parking_ticket = ParkingTicket(vehicle, parking_lot)
            parking_lot.assign_parking_spot(vehicle, parking_ticket)
            self.print_parking_ticket(parking_ticket)

        def print_parking_ticket(self, parking_ticket):
            # Print the basic information of the vehicle on the parking ticket
            print("Parking Ticket:")
            print("Vehicle Type:", parking_ticket.get_vehicle().get_type())
            print("License Plate:", parking_ticket.get_vehicle().get_license_plate())
            print("Entry Time:", parking_ticket.get_entry_time())
            print("Assigned Parking Spot:", parking_ticket.get_parking_spot().get_number())

    # Usage example in your main code
    # Assuming you have a vehicle instance and a parking_lot instance
    entrance_panel = EntrancePanel()
    entrance_panel.process_vehicle_entry(vehicle, parking_lot)

    class ExitPanel:
        def process_payment(self, parking_ticket):
            # Calculate parking fee
            parking_fee = self.calculate_parking_fee(parking_ticket)

            # Print the final parking ticket with calculated payment
            self.print_final_parking_ticket(parking_ticket, parking_fee)
        
        def calculate_parking_fee(self, parking_ticket):
            # Calculate parking fee logic based on entry time, vehicle type, etc.
        # ...
            return parking_fee

        def print_final_parking_ticket(self, parking_ticket, parking_fee):
            # Print the final parking ticket with vehicle information and payment details
            print("Final Parking Ticket:")
            print("Vehicle Type:", parking_ticket.get_vehicle().get_type())
            print("License Plate:", parking_ticket.get_vehicle().get_license_plate())
            print("Entry Time:", parking_ticket.get_entry_time())
            print("Exit Time:", parking_ticket.get_exit_time())
            print("Assigned Parking Spot:", parking_ticket.get_parking_spot().get_number())
            print("Parking Fee:", parking_fee)

    # Usage example in your main code
    #Assuming you have a parking_ticket instance
    exit_panel = ExitPanel()
    exit_panel.process_payment(parking_ticket)

    class ParkingRate():
        def __init__(self):
            self.__hourly_rates = {
                VehicleType.CAR: 4,
                VehicleType.TRUCK: 5,
                VehicleType.VAN: 6,
                VehicleType.MOTORBIKE: 2,
                VehicleType.SPORTS_CAR: 4,
            }
        def get_hourly_rate(self, vehicle_type):
            return self.__hourly_rates.get(vehicle_type, 0)
        

    class ParkingTicket():
        #return parking ticket

        def __init__(self):
        #pnu, entered time, type of car and type
            self.__entry_time = datetime.now()

        def set_hourly_rate(self, hourly_rate):
            self.__hourly_rate = hourly_rate

        def calculate_total_charge(self):
            exit_time = datetime.now()
            hours_parked = (exit_time - self.__entry_time).second//3600
            total_charge = self.__hourly_rate * hours_parked
            return total_charge
#entrance and exit panels parking ticket -> calculation things
