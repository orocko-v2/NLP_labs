class Driver:
    def __init__(self, surname, name, patronymic, driver_license_category):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.driver_license_category = driver_license_category


class Transport:
    def __init__(self, producer, price, year, capacity, driver: Driver):
        self.producer = producer
        self.price = price
        self.year = year
        self.capacity = capacity
        self.driver = driver


class Rail(Transport):
    def __init__(self, schedule, depot_address, producer, price, year, capacity, driver: Driver):
        super().__init__(producer, price, year, capacity, driver)
        self.schedule = schedule
        self.depot_address = depot_address


class Trackless(Transport):
    def __init__(self, producer, price, year, capacity, height, width, length, driver: Driver):
        super().__init__(producer, price, year, capacity, driver)
        self.height = height
        self.width = width
        self.length = length


class Tram(Rail):
    def __init__(self, schedule, depot_address, producer, price, year, capacity, ticket_price, driver: Driver):
        super().__init__(schedule, depot_address, producer, price, year, capacity, driver)
        self.ticket_price = ticket_price


class Train(Rail):
    def __init__(self, schedule, depot_address, producer, price, year, capacity, departure_city, arrival_city,
                 ticket_price, driver: Driver):
        super().__init__(schedule, depot_address, producer, price, year, capacity, driver)
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.ticket_price = ticket_price


class Metro(Rail):
    def __init__(self, city, ticket_price, metro_line, schedule, depot_address, producer, price, year, capacity, driver: Driver):
        super().__init__(schedule, depot_address, producer, price, year, capacity, driver)
        self.city = city
        self.metro_line = metro_line
        self.ticket_price = ticket_price


class Bus(Trackless):
    def __init__(self, stations_list, producer, price, year, capacity, height, width, length, driver: Driver):
        super().__init__(producer, price, year, capacity, height, width, length, driver)
        self.stations_list = stations_list


class Trolleybus(Trackless):
    def __init__(self, depot, producer, price, year, capacity, height, width, length, driver: Driver):
        super().__init__(producer, price, year, capacity, height, width, length, driver)
        self.depot = depot
