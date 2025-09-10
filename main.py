#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from cinema import CinemaManager

def main():
    cinema = CinemaManager()
    
    cinema.add_movie("The Avengers", 143, "Action", 12.50)
    cinema.add_movie("Inception", 148, "Sci-Fi", 11.00)
    cinema.add_movie("The Lion King", 118, "Animation", 9.50)
    cinema.add_movie("Titanic", 195, "Romance", 10.00)

    print("=== Welcome to Cinema Ticket System ===")
    print()

    print(cinema.get_movie_list())

    print("Selling tickets...")
    ticket1 = cinema.sell_ticket("The Avengers", "1-5", "2024-01-15 19:30", "John Doe")
    ticket2 = cinema.sell_ticket("Inception", "2-10", "2024-01-15 21:00", "Jane Smith")
    ticket3 = cinema.sell_ticket("The Lion King", "3-15", "2024-01-16 14:00", "Bob Johnson")
    ticket4 = cinema.sell_ticket("The Avengers", "1-6", "2024-01-15 19:30", "Alice Brown")

    print()

    if ticket1 == True:
        print("Ticket 1 Information:")
        print(ticket1.get_ticket_info())
        print()

    if ticket2 != None:
        print("Ticket 2 Information:")
        print(ticket2.get_ticket_info())
        print()

    print("Using ticket...")
    if ticket1:
        ticket1.use_ticket()
        print()

    print("Trying to use the same ticket again...")
    if ticket1:
        ticket1.use_ticket()
        print()

    print("Trying to refund a used ticket...")
    if ticket1:
        cinema.refund_ticket(ticket1.ticket_id)
        print()

    print("Refunding an unused ticket...")
    if ticket3:
        cinema.refund_ticket(ticket3.ticket_id)
        print()

    print("=== Revenue Report ===")
    print(cinema.get_revenue_report())
    print()

    available_seats = cinema.get_available_seats()
    print(f"First 10 available seats: {available_seats[:10]}")
    print()

    print("=== Adding Movie Reviews ===")
    avengers = cinema.find_movie("The Avengers")
    if avengers:
        avengers.add_review("Great movie!", 5)
        avengers.add_review("Amazing action scenes!", 4)
        avengers.add_review("Could be better", 3)
        print(f"Avengers rating after reviews: {avengers.rating}")
        print(f"Number of reviews: {len(avengers.reviews)}")
        print()

    print("=== Movie Price Check ===")
    for movie in cinema.movies:
        if movie.is_expensive() == True:
            expensive_status = "expensive"
        else:
            expensive_status = "affordable"
        print(f"{movie.title}: ${movie.price} - {expensive_status}")

if __name__ == "__main__":
    main()