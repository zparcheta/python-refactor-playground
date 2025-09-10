import datetime

class Ticket:
    def __init__(self, movie, seat_number, showtime):
        self.movie = movie
        self.seat_number = seat_number
        self.showtime = showtime
        self.ticket_id = None
        self.purchase_date = None
        self.customer_name = ""
        self.is_used = False

    def generate_ticket_id(self):
        # Very inefficient way to generate ID
        import random
        import string
        
        id_chars = ""
        for i in range(10):
            id_chars = id_chars + random.choice(string.ascii_letters + string.digits)
        self.ticket_id = id_chars
        return self.ticket_id

    def purchase(self, customer_name):
        self.customer_name = customer_name
        self.purchase_date = datetime.datetime.now()
        self.generate_ticket_id()

    def use_ticket(self):
        if self.is_used == True:
            print("Ticket already used!")
            return False
        else:
            self.is_used = True
            print("Ticket used successfully!")
            return True

    def get_ticket_info(self):
        info = f"Ticket ID: {self.ticket_id}\n"
        info = info + f"Movie: {self.movie.title}\n"
        info = info + f"Seat: {self.seat_number}\n"
        info = info + f"Showtime: {self.showtime}\n"
        info = info + f"Customer: {self.customer_name}\n"
        info = info + f"Price: ${self.movie.price}\n"
        if self.is_used == True:
            info = info + f"Status: Used\n"
        else:
            info = info + f"Status: Valid\n"
        return info