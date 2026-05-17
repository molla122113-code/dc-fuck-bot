from flask import Flask
import hashlib
import base64

app = Flask(__name__)



# CODEVERSE
encoded_title = "Q09ERVZFUlNF"


encoded_status = "Qm90IEFjdGl2YXRlZA=="


encoded_dev = "TUQgU2hvem9uIEFoYW1hZCBTaGVoYWI="



title = base64.b64decode(encoded_title).decode()
status = base64.b64decode(encoded_status).decode()
developer = base64.b64decode(encoded_dev).decode()



real_hash = hashlib.sha256(
    developer.encode()
).hexdigest()



@app.route("/")
def home():

    
    check_hash = hashlib.sha256(
        developer.encode()
    ).hexdigest()

    if check_hash != real_hash:
        return """
        <html>
        <head>
            <title>ERROR</title>

            <style>
                body{
                    background:black;
                    color:red;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    height:100vh;
                    font-size:100px;
                    font-family:Arial;
                    font-weight:bold;
                }
            </style>
        </head>

        <body>
            FUCK
        </body>
        </html>
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>{title}</title>

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
                overflow:hidden;
            }}

            .card{{
                width:400px;
                background:rgba(15,23,42,0.9);
                border:1px solid rgba(0,255,255,0.2);
                border-radius:25px;
                padding:40px;
                text-align:center;
                box-shadow:
                0 0 30px rgba(0,255,255,0.2),
                0 0 60px rgba(0,255,255,0.1);
                backdrop-filter:blur(10px);
            }}

            .online{{
                color:#22c55e;
                font-size:28px;
                font-weight:bold;
                margin-bottom:20px;
            }}

            h1{{
                color:white;
                font-size:42px;
                letter-spacing:3px;
                margin-bottom:25px;
            }}

            .dev{{
                color:#94a3b8;
                font-size:18px;
                line-height:35px;
            }}

            .glow{{
                position:absolute;
                width:300px;
                height:300px;
                background:cyan;
                filter:blur(140px);
                opacity:0.1;
                border-radius:50%;
            }}

            .g1{{
                top:-100px;
                left:-100px;
            }}

            .g2{{
                bottom:-100px;
                right:-100px;
            }}

        </style>

    </head>

    <body>

        <div class="glow g1"></div>
        <div class="glow g2"></div>

        <div class="card">

            <div class="online">
                ✅ {status}
            </div>

            <h1>
                {title}
            </h1>

            <div class="dev">
                Developer<br>
                {developer}
            </div>

        </div>

    </body>

    </html>
    """

app.run(
    host="0.0.0.0",
    port=10000
)