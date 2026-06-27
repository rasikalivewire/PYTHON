movies = {
    "Action": [
        "John Wick", "Mad Max", "The Dark Knight", "Gladiator",
        "Die Hard", "Mission Impossible", "Top Gun Maverick",
        "The Avengers", "Black Panther", "Extraction"
    ],

    "Comedy": [
        "Mr. Bean", "Home Alone", "The Mask", "Jumanji",
        "Rush Hour", "Central Intelligence", "The Hangover",
        "Ted", "Johnny English", "Free Guy"
    ],

    "Sci-Fi": [
        "Interstellar", "Avatar", "Inception", "The Matrix",
        "Gravity", "Dune", "Blade Runner 2049",
        "The Martian", "Arrival", "Tenet"
    ],

    "Horror": [
        "The Conjuring", "Insidious", "Annabelle", "IT",
        "The Nun", "A Quiet Place", "Smile",
        "The Ring", "The Grudge", "Evil Dead Rise"
    ]
}

watchlist = []
ratings = {}

# Display Movies by Genre
def recommend_movies(genre):
    if genre in movies:
        print("\nRecommended Movies:")
        for movie in movies[genre]:
            print("-", movie)
    else:
        print("Genre not found!")

# Search Movie
def search_movie(movie_name):

    movie_name = movie_name.lower()

    for genre in movies:
        for movie in movies[genre]:

            if movie.lower() == movie_name:
                print("\nMovie Found!")
                print("Movie :", movie)
                print("Genre :", genre)
                return

    print("Movie not found.")

# Add Movie to Watchlist
def add_watchlist(movie):

    if movie not in watchlist:
        watchlist.append(movie)
        print(movie, "added to watchlist.")
    else:
        print(movie, "already exists in watchlist.")

# View Watchlist
def view_watchlist():

    if len(watchlist) == 0:
        print("Watchlist is empty.")
    else:
        print("\n===== WATCHLIST =====")

        for i, movie in enumerate(watchlist, start=1):
            print(i, ".", movie)

# Remove Movie from Watchlist
def remove_watchlist(movie):

    if movie in watchlist:
        watchlist.remove(movie)
        print(movie, "removed from watchlist.")
    else:
        print("Movie not found in watchlist.")

# Rate Movie
def rate_movie(movie, rating):

    if rating >= 1 and rating <= 5:
        ratings[movie] = rating
        print("Rating saved successfully.")
    else:
        print("Rating must be between 1 and 5.")

# Show Ratings
def show_ratings():

    if len(ratings) == 0:
        print("No ratings available.")
    else:

        print("\n===== MOVIE RATINGS =====")

        total = 0

        for movie, rating in ratings.items():
            print(movie, "=", rating, "/5")
            total += rating

        average = total / len(ratings)

        print("Average Rating =", round(average, 2))

# Main Program
while True:

    print("\n====================================")
    print("   MOVIE RECOMMENDATION SYSTEM")
    print("====================================")
    print("1. View Genres & Recommendations")
    print("2. Search Movie")
    print("3. Add Movie to Watchlist")
    print("4. View Watchlist")
    print("5. Remove Movie from Watchlist")
    print("6. Rate Movie")
    print("7. View Ratings")
    print("8. Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:

        print("\nAvailable Genres:")

        for genre in movies:
            print("-", genre)

        genre = input("\nEnter Genre: ")

        recommend_movies(genre)

    elif choice == 2:

        movie_name = input("Enter Movie Name: ")
        search_movie(movie_name)

    elif choice == 3:

        movie = input("Enter Movie Name: ")
        add_watchlist(movie)

    elif choice == 4:

        view_watchlist()

    elif choice == 5:

        movie = input("Enter Movie Name to Remove: ")
        remove_watchlist(movie)

    elif choice == 6:

        movie = input("Enter Movie Name: ")
        rating = int(input("Enter Rating (1-5): "))

        rate_movie(movie, rating)

    elif choice == 7:

        show_ratings()

    elif choice == 8:

        print("Thank You!")
        break

    else:

        print("Invalid Choice. Please Try Again.")