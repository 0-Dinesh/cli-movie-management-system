import csv
import random
import sqlite3
import re

class Email:
    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def email_ID(self, Name):
        try:
            E_mail = input("Enter your Email ID : ")
            
            if not self.is_valid_email(E_mail):
                raise ValueError("Invalid email format.")
            
            userID, domain = E_mail.split('@')
            
            if domain == "movsys.com":
                print("Hello Mr.", Name)
                print("What do you want to do?")
                print(" 1. Add Movies")
                print(" 2. Import Movies from File")
                print(" 3. Update Movies")
                print(" 4. Remove Movies")  
                print(" 5. Display Movies")
                print(" 6. Exit")
                return 'admin'
            else:
                print("Welcome", Name)
                print(" A. Display Movies")
                print(" B. Suggest me a movie")
                print(" C. Exit")
                return 'user'
        except Exception as e:
            print("Error:", e)
            return None

class Movie:
    def __init__(self):
        self.conn = sqlite3.connect('movie_data.db')
        self.create_table()
        self.movies = self.load_movies()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                          (title TEXT PRIMARY KEY, genre TEXT, year TEXT)''')
        self.conn.commit()

    def load_movies(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = {}
        for row in cursor.fetchall():
            title, genre, year = row
            movies[title] = {'genre': genre, 'year': year}
        return movies

    def add_movie(self, title, genre, year):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO movies (title, genre, year) VALUES (?, ?, ?)", (title, genre, year))
            self.conn.commit()
            self.movies[title] = {'genre': genre, 'year': year}
            print("Movie '{}' added successfully.".format(title))
        except sqlite3.IntegrityError:
            print("Movie '{}' already exists.".format(title))
        except Exception as e:
            print("Error adding movie:", e)

    def update_movie(self, title, genre, year):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE movies SET genre=?, year=? WHERE title=?", (genre, year, title))
            self.conn.commit()
            if title in self.movies:
                self.movies[title] = {'genre': genre, 'year': year}
                print("Movie '{}' updated successfully.".format(title))
            else:
                print("Movie '{}' not found.".format(title))
        except Exception as e:
            print("Error updating movie:", e)

    def remove_movie(self, title):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM movies WHERE title=?", (title,))
            self.conn.commit()
            if title in self.movies:
                del self.movies[title]
                print("Movie '{}' removed successfully.".format(title))
            else:
                print("Movie '{}' not found.".format(title))
        except Exception as e:
            print("Error removing movie:", e)

    def display_movies(self):
        try:
            if self.movies:
                print("List of Movies:")
                for title, info in self.movies.items():
                    print("Title: {}, Genre: {}, Year: {}".format(title, info['genre'], info['year']))
            else:
                print("No Movies to display")
        except Exception as e:
            print("Error displaying movies:", e)

    def display_movies_by_year(self, year):
        try:
            available_years = set(info['year'] for info in self.movies.values())
            movies_by_year = {title: info for title, info in self.movies.items() if info['year'] == year}
            if movies_by_year:
                print("Movies released in", year)
                for title, info in movies_by_year.items():
                    print("Title: {}, Genre: {}, Year: {}".format(title, info['genre'], info['year']))
            else:
                print("No Movies released in", year)
            print("Available years:", ", ".join(sorted(available_years)))
        except Exception as e:
            print("Error displaying movies by year:", e)

    def display_movies_by_genre(self, genre):
        try:
            available_genres = set(info['genre'] for info in self.movies.values())
            movies_by_genre = {title: info for title, info in self.movies.items() if info['genre'] == genre}
            if movies_by_genre:
                print("Movies in the genre", genre, "genre:")
                for title, info in movies_by_genre.items():
                    print("Title: {}, Genre: {}, Year: {}".format(title, info['genre'], info['year']))
            else:
                print("No Movies found in the", genre, "genre.")
            print("Available genres:", ", ".join(sorted(available_genres)))
        except Exception as e:
            print("Error displaying movies by genre:", e)

    def get_random_movie(self):
        try:
            if self.movies:
                random_movie = random.choice(list(self.movies.keys()))
                print("Enjoy this Movie :", random_movie)
            else:
                print("No Movies available.")
        except Exception as e:
            print("Error getting movie in random :", e)

    def import_movies_from_csv(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        title, genre, year = row
                        self.add_movie(title, genre, year)
                    else:
                        print(f"Skipped invalid row: {row}")
            print("Movies are added from File.")
        except FileNotFoundError:
            print("No movies database found.")
        except Exception as e:
            print("Error importing movies from CSV:", e)

def main():
    system = Movie()
    email = Email()
    
    print("\t\t\t Movie Management System ")
    print("\nHello there!")
    Name = input("\nEnter your Name : ")
    user_type = email.email_ID(Name)

    if user_type is None:
        return
    
    while True:
        choice = input("Enter your choice : ")

        if user_type == 'admin':
            if choice == '1':
                Title = input("\nEnter movie title: ")
                Genre = input("Enter movie genre: ")
                Year = input("Enter movie release year: ")
                system.add_movie(Title, Genre, Year)
            elif choice == '2':
                filename = input("\nEnter the name of the CSV file: ")
                system.import_movies_from_csv(filename)
            elif choice == '3':
                Title = input("\nEnter movie title to update: ")
                Genre = input("Enter new genre: ")
                Year = input("Enter new release year: ")
                system.update_movie(Title, Genre, Year)
            elif choice == '4':
                Title = input("\nEnter movie title to remove: ")
                system.remove_movie(Title)
            elif choice == '5':
                system.display_movies()
            elif choice == '6':
                print("\nExiting the program.")
                break
            else:
                print("\nInvalid choice. Please enter a valid option.")

        elif user_type == 'user':
            if choice == 'A':
                print("\na. Display Movies by Year")
                print("b. Display Movies by Genre")
                Option = input("\nEnter your Choice : ")
                if Option == 'a':
                    Year = input("\nEnter the year to display movies: ")
                    system.display_movies_by_year(Year)
                elif Option == 'b':
                    Genre = input("\nEnter the genre to display movies: ")
                    system.display_movies_by_genre(Genre)
                else:
                    print("\nPlease give a valid input")
            elif choice == 'B':
                system.get_random_movie()
            elif choice == 'C':
                print("\nExiting the program.")
                break
            else:
                print("\nInvalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
