from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests for development

# In-memory database (for demonstration purposes)
movies = []

# Helper function to find a movie by id
def find_movie_by_id(movie_id):
    return next((movie for movie in movies if movie['id'] == movie_id), None)

# Create a movie review (POST)
@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    movie_id = str(uuid.uuid4())  # Unique ID for the movie
    new_movie = {
        'id': movie_id,
        'title': data.get('title'),
        'review': data.get('review'),
        'rating': data.get('rating'),
        'date': data.get('date')
    }
    movies.append(new_movie)
    return jsonify(new_movie), 201

# Get all movie reviews (GET)
@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies), 200

# Get a single movie by ID (GET)
@app.route('/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = find_movie_by_id(movie_id)
    if movie:
        return jsonify(movie), 200
    return jsonify({"error": "Movie not found"}), 404

# Update a movie review by ID (PUT)
@app.route('/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = find_movie_by_id(movie_id)
    if movie:
        data = request.get_json()
        movie['title'] = data.get('title', movie['title'])
        movie['review'] = data.get('review', movie['review'])
        movie['rating'] = data.get('rating', movie['rating'])
        movie['date'] = data.get('date', movie['date'])
        return jsonify(movie), 200
    return jsonify({"error": "Movie not found"}), 404

# Delete a movie review by ID (DELETE)
@app.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = find_movie_by_id(movie_id)
    if movie:
        movies.remove(movie)
        return jsonify({"message": "Movie deleted"}), 200
    return jsonify({"error": "Movie not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
