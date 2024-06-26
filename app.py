from flask import Flask, render_template, request, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
from forms import PostForm

app = Flask(__name__)
#app.config['SECRET_KEY'] = "Zeki_1234"

# Initialize Firestore DB
cred = credentials.Certificate('firebase-key.json')
default_app = initialize_app(cred)
db = firestore.client()
posts_ref = db.collection('posts')
images_ref = db.collection('images')

@app.route('/')
def index():
    posts = []
    images_doc = images_ref.list_documents()
    firstimages = []
    ids = []
    for doc_ref in images_doc:
        doc = doc_ref.get()
        ids.append(doc.id)
        doc_dict = doc.to_dict()
        first_string = next((value for value in doc_dict.values() if isinstance(value, str)), None)
        if first_string is not None:
            firstimages.append(first_string)
    for doc in posts_ref.stream():
        post = doc.to_dict()
        post['id'] = doc.id  
        posts.append(post)
    return render_template('index.html', posts=posts,ids=ids,firstimages=firstimages)

@app.route('/post/<string:post_id>')
def post(post_id):
    post_doc = posts_ref.document(post_id).get()
    images_doc = images_ref.document(post_id.lower()).get()
    imgs = images_doc.to_dict()
    images = [img for img in imgs.values()]
    if post_doc.exists:
        post = post_doc.to_dict()
        post['id'] = post_id
        return render_template('post.html', post=post,images=images)
    else:
        return "Post not found", 404

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'content': form.content.data
        }
        posts_ref.document(form.title.data).set(data)  # Add new post without specifying document ID
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@app.route('/edit/<string:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    
    if request.method == 'GET':
        
        post_doc = posts_ref.document(post_id).get()
        if post_doc.exists:
            post = post_doc.to_dict()
            
            form = PostForm(title=post.get('title'), content=post.get('content'))
            return render_template('edit_post.html',post=post,form=form, post_id=post_id)
        else:
            return "Post not found", 404

    if request.method == 'POST':
        
        post_doc = posts_ref.document(post_id).get()
        if post_doc.exists:
            post = post_doc.to_dict()
            form = PostForm(request.form)
            print(form.content)
            if form.validate_on_submit():
               
                if form.title.data != post.get('title'):
                    # Delete old post and create new post
                    posts_ref.document(post_id).delete()
                    new_post_id = form.title.data
                    posts_ref.document(new_post_id).set({
                        'title': form.title.data,
                        'content': form.content.data
                    })
                else:
                    # Update existing post
                    posts_ref.document(post_id).update({'content': form.content.data})
                return redirect(url_for('index'))
            else:
                return "Post not found", 404
        else:
            return render_template('edit_post.html', form=form, post_id=post_id, errors=form.errors)

@app.route('/delete/<string:post_id>', methods=['POST'])
def delete_post(post_id):
    post_doc = posts_ref.document(post_id).get()
    if post_doc.exists:
        posts_ref.document(post_id).delete()
        return redirect(url_for('index'))
    else:
        return "Post not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=3333)
