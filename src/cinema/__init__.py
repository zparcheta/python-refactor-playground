"""
Cinema Ticket Management System

A simple cinema ticket management system with movies, tickets, and revenue tracking.
"""

from .cinema_manager import CinemaManager
from .movie import Movie
from .ticket import Ticket

__all__ = ["CinemaManager", "Movie", "Ticket"]
