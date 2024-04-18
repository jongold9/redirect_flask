from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from_urls = request.form["from_urls"].split('\n')
        to_urls = request.form["to_urls"].split('\n')
        redirect_type = request.form["redirect_type"]
        
        redirects = []
        for from_url, to_url in zip(from_urls, to_urls):
            from_path = extract_path_from_url(from_url)
            redirect = format_redirect(from_path, to_url, redirect_type)
            redirects.append(redirect)

        redirects_str = '\n'.join(redirects)
        return render_template('index.html', redirects=redirects_str, from_urls=request.form["from_urls"], to_urls=request.form["to_urls"], redirect_type=redirect_type)
    
    return render_template('index.html', redirects='', from_urls='', to_urls='', redirect_type='')

def extract_path_from_url(url):
    match = re.search(r'https?://[^/]+(/.*)', url)
    return match.group(1) + ('' if match.group(1).endswith('/') else '/') if match else '/'

def format_redirect(from_path, to_url, redirect_type):
    if redirect_type == 'Redirect 301':
        return f"Redirect 301 {from_path} {to_url}\n"
    elif redirect_type == 'RewriteRule':
        return f"RewriteRule ^{from_path.strip('/')}$(/.*)? {to_url} [R=301,L]\n"
    elif redirect_type == 'RewriteRule with subpaths':
        return f"RewriteRule ^{from_path.strip('/')}(/.*)?$ {to_url} [R=301,L]\n"
    elif redirect_type == 'Directory redirect with subpaths':
        from_directory = from_path.split('/')[1] if '/' in from_path else from_path
        to_directory = to_url.split('/')[3] if len(to_url.split('/')) > 3 else to_url
        return f"RewriteRule ^{from_directory.strip('/')}(/.*)?$ /{to_directory.strip('/')}\\$1 [R=301,L]\n"

if __name__ == "__main__":
    app.run(debug=True)
