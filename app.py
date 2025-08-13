from flask import Flask,render_template,request, jsonify
import pickle
import numpy as np
import difflib
popular_df=pickle.load(open("../br system/popular_df.pkl", "rb"))
pt=pickle.load(open("../br system/pt.pkl", "rb"))
books=pickle.load(open("../br system/books.pkl", "rb"))
similarity=pickle.load(open("../br system/similarity.pkl", "rb"))
app=Flask(__name__)

# Precompute title list for fast suggestions
all_titles = [str(x) for x in pt.index.tolist()]
@app.route('/')
def index():
    return render_template("index.html",
                            book_name=list(popular_df["Book-Title"].values),
                            author = list(popular_df["Book-Author"].values),
                            image = list(popular_df["Image-URL-M"].values),
                            votes = list(popular_df["num_ratings"].values),
                            ratings = list(popular_df["avg_ratings"].values)
                           )
@app.route('/recommend')
def recommendation():
    return render_template("recommendation.html")

@app.route('/suggest_titles')
def suggest_titles():
    query_raw = request.args.get('q', '')
    query = query_raw.strip()
    if not query:
        return jsonify([])

    query_lower = query.lower()

    # 1) Prefix matches
    prefix_matches = [t for t in all_titles if t.lower().startswith(query_lower)]

    # 2) Contains matches (excluding already included)
    if len(prefix_matches) < 8:
        contains_matches = [
            t for t in all_titles
            if (query_lower in t.lower()) and (t not in prefix_matches)
        ]
        prefix_matches.extend(contains_matches[: max(0, 8 - len(prefix_matches))])

    # 3) Fuzzy fallback using difflib
    if len(prefix_matches) < 8:
        fuzzy_needed = 8 - len(prefix_matches)
        fuzzy_candidates = difflib.get_close_matches(query, all_titles, n=fuzzy_needed, cutoff=0.5)
        for title in fuzzy_candidates:
            if title not in prefix_matches:
                prefix_matches.append(title)

    return jsonify(prefix_matches[:8])

@app.route('/recommend_books',methods=['post'])
def recommend():
    book_name=request.form.get("user_input")
    ind = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity[ind])), key=lambda x: x[1], reverse=True)[1:5]
    data = []

    for i in similar_items:
        item = []
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Book-Title"]))
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Book-Author"]))
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Image-URL-M"]))
        data.append(item)

    return render_template('recommendation.html', data=data, query_title=book_name)

@app.route('/contact')
def contacts():
    return render_template("contact.html")
if __name__=='__main__':
    app.run(debug=True)