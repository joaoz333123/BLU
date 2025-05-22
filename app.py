from flask import Flask, render_template, send_from_directory, request, redirect

app = Flask(__name__)

@app.before_request
def redirect_non_www():
    """Redirect non-www requests to www."""
    if not request.host.startswith('www.'):
        new_url = request.url.replace(request.host, 'www.' + request.host, 1)
        return redirect(new_url, code=301)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Página de teste
@app.route("/teste")
def teste():
    return render_template("index_teste.html")
    
# Puxar o icone
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico')



# Servir sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

# Servir robots.txt
@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
