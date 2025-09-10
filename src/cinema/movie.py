class Movie:
    def __init__(self, title, duration, genre, price):
        self.title = title
        self.duration = duration
        self.genre = genre
        self.price = price
        self.rating = 0
        self.reviews = []

    def add_review(self, review_text, rating):
        self.reviews.append(review_text)
        # This is wrong calculation - should be average of all ratings
        self.rating = (self.rating + rating) / 2

    def get_info(self):
        return f"Movie: {self.title}, Duration: {self.duration} minutes, Genre: {self.genre}, Price: ${self.price}"

    def is_expensive(self):
        if self.price > 10:
            return True
        else:
            return False