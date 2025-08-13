## Recommender Systems

This is a collaborative filtering based book recommendation system. It recommends similar books using user ratings and item-item similarity. Built with Flask and Bootstrap; templates use Jinja so small Python expressions/variables render in HTML.

### How it works
- Collaborative filtering over a pivot table of users vs. books (`pt.pkl`), with a precomputed similarity matrix (`similarity.pkl`).
- Given a selected book, we fetch the top-N similar books by cosine similarity.
- Book metadata (title, author, cover) is looked up from `books.pkl`.
- The UI is a simple Flask app with an autocomplete suggest feature for titles.

### Project structure
- `app.py`: Flask server and routes
- `templates/`: HTML templates
- `*.pkl`: artifacts for popularity, pivot table, similarity, and metadata. These files are generated from a data-prep script/notebook that will be added soon.
- `docs/`: screenshots used in this README (add your images here)

### Run locally
1. Create a virtual environment and install Flask (and any other requirements you need):
```bash
pip install flask
```
2. Start the server:
```bash
python app.py
```
3. Open `http://127.0.0.1:5000` in your browser.

### Screenshots
Replace these paths with your actual screenshot files inside `docs/`.

![Home](docs/home.png)
![Recommend](docs/recommend.png)
![Autocomplete](docs/autocomplete.png)
![Results](docs/results.png)
![Contact](docs/contact.png)


