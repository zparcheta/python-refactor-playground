from .movie import Movie
from .ticket import Ticket

class CinemaManager:
    def __init__(self):
        self.movies = []
        self.tickets = []
        self.available_seats = []
        self.total_revenue = 0
        
        # Initialize seats (very inefficient way)
        for row in range(1, 11):
            for seat in range(1, 21):
                self.available_seats.append(f"{row}-{seat}")

    def add_movie(self, title, duration, genre, price):
        movie = Movie(title, duration, genre, price)
        self.movies.append(movie)
        return movie

    def find_movie(self, title):
        # Inefficient linear search
        for movie in self.movies:
            if movie.title == title:
                return movie
        return None

    def sell_ticket(self, movie_title, seat_number, showtime, customer_name):
        movie = self.find_movie(movie_title)
        if movie == None:
            print("Movie not found!")
            return None

        # Check if seat is available (inefficient)
        seat_str = str(seat_number)
        seat_available = False
        for seat in self.available_seats:
            if seat == seat_str:
                seat_available = True
                break

        if seat_available == False:
            print("Seat not available!")
            return None

        # Create and purchase ticket
        ticket = Ticket(movie, seat_number, showtime)
        ticket.purchase(customer_name)
        
        # Remove seat from available seats (inefficient)
        for i, seat in enumerate(self.available_seats):
            if seat == seat_str:
                del self.available_seats[i]
                break

        self.tickets.append(ticket)
        self.total_revenue = self.total_revenue + movie.price
        return ticket

    def get_ticket_by_id(self, ticket_id):
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None

    def refund_ticket(self, ticket_id):
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket == None:
            print("Ticket not found!")
            return False

        if ticket.is_used == True:
            print("Cannot refund used ticket!")
            return False

        # Add seat back to available seats
        self.available_seats.append(ticket.seat_number)
        self.total_revenue = self.total_revenue - ticket.movie.price
        
        # Remove ticket from list
        for i, t in enumerate(self.tickets):
            if t.ticket_id == ticket_id:
                del self.tickets[i]
                break
        
        print(f"Ticket {ticket_id} refunded successfully!")
        return True

    def get_movie_list(self):
        if len(self.movies) == 0:
            return "No movies available."
        
        movie_list = "Available Movies:\n"
        for movie in self.movies:
            movie_list = movie_list + f"- {movie.get_info()}\n"
        return movie_list

    def get_available_seats(self):
        return self.available_seats

    def get_revenue_report(self):
        movie_counts = {}
        for ticket in self.tickets:
            movie_title = ticket.movie.title
            if movie_title in movie_counts:
                movie_counts[movie_title] = movie_counts[movie_title] + 1
            else:
                movie_counts[movie_title] = 1
        
        report = f"Total Revenue: ${self.total_revenue:.2f}\n"
        report = report + f"Total Tickets Sold: {len(self.tickets)}\n"
        report = report + "Tickets by Movie:\n"
        
        for movie_title, count in movie_counts.items():
            report = report + f"  {movie_title}: {count} tickets\n"
        
        return report