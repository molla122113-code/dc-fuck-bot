from flask import Flask

from license_checker import (
    check_license
)

app = Flask(__name__)


@app.route("/")
def home():

    valid, data = check_license()

    status = (
        "ACTIVE"
        if valid
        else "EXPIRED"
    )

    last_payment = data.get(
        "last_payment",
        "Unknown"
    )

    expires = data.get(
        "expires",
        "Unknown"
    )

    return f"""

    <!DOCTYPE html>

    <html>

    <head>

    <title>CODEVERSE</title>

    <style>

    *{{
        margin:0;
        padding:0;
        box-sizing:border-box;
    }}

    body{{
        background:#020617;
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
        font-family:Arial;
    }}

    .card{{
        width:420px;
        background:#0f172a;
        border-radius:25px;
        padding:40px;
        color:white;
        box-shadow:
        0 0 30px rgba(0,255,255,0.2);
    }}

    h1{{
        font-size:40px;
        margin-bottom:30px;
    }}

    .status{{
        color:
        {"#22c55e" if valid else "#ef4444"};
        font-size:28px;
        margin-bottom:20px;
        font-weight:bold;
    }}

    .info{{
        font-size:18px;
        line-height:40px;
        color:#cbd5e1;
    }}

    </style>

    </head>

    <body>

    <div class="card">

    <h1>CODEVERSE</h1>

    <div class="status">
    {status}
    </div>

    <div class="info">

    Last Payment<br>
    {last_payment}

    <br><br>

    Expires<br>
    {expires}

    </div>

    </div>

    </body>

    </html>

    """


app.run(
    host="0.0.0.0",
    port=10000
)
