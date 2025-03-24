from flask import Flask, request, render_template, redirect, url_for, session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Selenium setup
def get_search_results(query):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for faster scraping
    service = Service('chromedriver.exe')  # Path to ChromeDriver

    # Initialize driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    driver.get(url)

    # Get content from Wikipedia (modify if using other websites)
    try:
        title = driver.find_element(By.ID, "firstHeading").text
        content = driver.find_element(By.CLASS_NAME, "mw-parser-output").text
        result = {"title": title, "content": content[:1000] + "..."}  # Limiting content for brevity
    except Exception as e:
        result = {"title": "No Results", "content": "No relevant information found."}

    driver.quit()
    return result

# Home route
@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('search.html')  # Show search page if logged in
    return render_template('index.html')  # Show login/skip page if not logged in

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Simple hardcoded credentials (can be changed later)
    if username == 'admin' and password == 'password':
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        return render_template('index.html', error="Invalid credentials. Try again!")

# Skip login route
@app.route('/skip')
def skip():
    return render_template('skip.html')  # Show only front page

# Search route (only if logged in)
@app.route('/search', methods=['POST'])
def search():
    if 'logged_in' in session:
        query = request.form.get('query')
        if query:
            result = get_search_results(query)
            return render_template('results.html', result=result, query=query)
        return render_template('search.html', error="Please enter a valid query.")
    else:
        return redirect(url_for('index'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
