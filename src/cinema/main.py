from cinema_manager import CinemaManager


def main():
    # Create cinema manager
    cinema = CinemaManager()

    # Add some movies
    cinema.add_movie("The Avengers", 143, "Action", 12.50)
    cinema.add_movie("Inception", 148, "Sci-Fi", 11.00)
    cinema.add_movie("The Lion King", 118, "Animation", 9.50)
    cinema.add_movie("Titanic", 195, "Romance", 10.00)

    print("=== Welcome to Cinema Ticket System ===")
    print()

    # Display available movies
    print(cinema.get_movie_list())

    # Sell some tickets
    print("Selling tickets...")
    ticket1 = cinema.sell_ticket("The Avengers", "1-5", "2024-01-15 19:30", "John Doe")
    ticket2 = cinema.sell_ticket("Inception", "2-10", "2024-01-15 21:00", "Jane Smith")
    ticket3 = cinema.sell_ticket(
        "The Lion King", "3-15", "2024-01-16 14:00", "Bob Johnson"
    )
    ticket4 = cinema.sell_ticket(
        "The Avengers", "1-6", "2024-01-15 19:30", "Alice Brown"
    )

    print()

    # Display ticket information
    if ticket1:
        print("Ticket 1 Information:")
        print(ticket1.get_ticket_info())
        print()

    if ticket2:
        print("Ticket 2 Information:")
        print(ticket2.get_ticket_info())
        print()

    # Use a ticket
    print("Using ticket...")
    if ticket1:
        ticket1.use_ticket()
        print()

    # Try to use the same ticket again
    print("Trying to use the same ticket again...")
    if ticket1:
        ticket1.use_ticket()
        print()

    # Try to refund a used ticket
    print("Trying to refund a used ticket...")
    if ticket1:
        cinema.refund_ticket(ticket1.ticket_id)
        print()

    # Refund an unused ticket
    print("Refunding an unused ticket...")
    if ticket3:
        cinema.refund_ticket(ticket3.ticket_id)
        print()

    # Display revenue report
    print("=== Revenue Report ===")
    print(cinema.get_revenue_report())
    print()

    # Display some available seats
    available_seats = cinema.get_available_seats()
    print(f"First 10 available seats: {available_seats[:10]}")
    print()

    # Add some movie reviews (demonstrating the bug in rating calculation)
    print("=== Adding Movie Reviews ===")
    avengers = cinema.find_movie("The Avengers")
    if avengers:
        avengers.add_review("Great movie!", 5)
        avengers.add_review("Amazing action scenes!", 4)
        avengers.add_review("Could be better", 3)
        print(f"Avengers rating after reviews: {avengers.rating}")
        print(f"Number of reviews: {len(avengers.reviews)}")
        print()

    # Demonstrate expensive movie check
    print("=== Movie Price Check ===")
    for movie in cinema.movies:
        expensive_status = "expensive" if movie.is_expensive() else "affordable"
        print(f"{movie.title}: ${movie.price} - {expensive_status}")


if __name__ == "__main__":
    main()
