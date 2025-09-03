from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def landing():
    """Landing page route"""
    # Add timestamp for cache busting (like in GTA-V2)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return render_template('landing.html', timestamp=timestamp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)