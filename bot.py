# web_bot.py - YOUR code, now as a LINK
# Same shop, same messages, just works in browser
import os
import re
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

PRODUCTS = {
    "dress": 25000,
    "shoes": 40000,
    "bag": 30000,
    "tshirt": 15000,
    "wig": 55000,
}

old_customers = set()

HTML = """
<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mama's Boutique - Chat</title>
<style>
body{font-family:Arial;background:#fce4ec;padding:15px;margin:0}
.container{max-width:500px;margin:auto;background:white;padding:15px;border-radius:15px;box-shadow:0 0 10px #ddd}
h2{text-align:center;margin:5px}
#chat{background:#fff5f7;padding:12px;border-radius:10px;height:380px;overflow-y:auto;border:1px solid #f8bbd0}
.me{color:#1565c0;background:#e3f2fd;padding:8px;border-radius:10px;margin:5px 0}
.bot{color:#2e7d32;background:#e8f5e9;padding:8px;border-radius:10px;margin:5px 0}
input{padding:12px;width:100%;box-sizing:border-box;margin-top:8px;border:1px solid #ddd;border-radius:10px}
button{width:100%;padding:12px;background:#ec407a;color:white;border:none;border-radius:10px;margin-top:8px;font-size:16px}
.share{background:#25D366}
</style>
</head><body>
<div class="container">
<h2>🛍️ Mama's Boutique</h2>
<p style="text-align:center">AI is LIVE - Type quit to stop</p>
<div id="chat"><p class="bot"><b>Bot:</b> Karibu! What's your name?</p></div>
<input id="name" placeholder="Your name - e.g. Neema">
<input id="msg" placeholder="Type here... price / 2 dress / quit">
<button onclick="send()">Send ➤</button>
<button class="share" onclick="shareLink()">Share hii link kwa WhatsApp 📲</button>
<p style="text-align:center;font-size:12px;color:grey">Pay via M-Pesa to 255700000000</p>
</div>
<script>
let chat=document.getElementById('chat');
let greeted = false;
function send(){
  let name=document.getElementById('name').value.trim() || 'Customer';
  let msg=document.getElementById('msg').value.trim();
  if(!msg) return;
  chat.innerHTML+=`<p class='me'><b>${name}:</b> ${msg}</p>`;
  fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name:name, msg:msg})})
  .then(r=>r.json()).then(d=>{ chat.innerHTML+=`<p class='bot'><b>Bot:</b> ${d.reply}</p>`; chat.scrollTop=chat.scrollHeight; });
  document.getElementById('msg').value='';
}
document.getElementById('msg').addEventListener('keydown', function(e){ if(e.key==='Enter') send(); });
function shareLink(){
  let text = "Karibu Mama's Boutique! Chat na robot wetu hapa: " + window.location.href;
  window.open("https://wa.me/?text=" + encodeURIComponent(text), "_blank");
}
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return "OK", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True) or {}
    name = data.get('name', 'Customer') or 'Customer'
    user_msg = data.get('msg', '') or ''
    low = str(user_msg).lower().strip()
    low_name = name.lower().strip()

    # If customer just typed their name first time - welcome logic from your code
    if low in ["hi", "hello", "hey", "karibu", "mambo", "habari"] or low == low_name:
        if low_name in old_customers and low_name != "customer":
            return jsonify(reply=f"Welcome back {name}! Tumekumiss! Karibu tena! What do you want to buy today?<br>Type 'price' to see products")
        else:
            if low_name != "customer":
                old_customers.add(low_name)
            return jsonify(reply=f"Karibu sana {name}! What do you want to buy today?<br>Type 'price' to see products")

    if low == "quit":
        return jsonify(reply=f"Asante {name}! Karibu tena!<br><br>Thank you {name} for shopping with us! Karibu tena, welcome back anytime! ❤️")

    if "price" in low or "bei" in low or "menu" in low or "list" in low:
        reply = ""
        for item, price in PRODUCTS.items():
            reply += f"- {item}: {price} TZS<br>"
        return jsonify(reply=reply)

    # SAME LOGIC AS YOUR CODE - if they mention ANY product
    elif any(item in low for item in PRODUCTS):
        total = 0
        found = []
        for item, price in PRODUCTS.items():
            if item in low:
                m = re.search(rf"(\d+)\s*{item}", low)
                qty = int(m.group(1)) if m else 1
                total += qty * price
                found.append(f"{qty} x {item}")

        return jsonify(reply=f"Sawa {name}, umechagua: {', '.join(found)}<br>TOTAL: {total} TZS. Pay via M-Pesa to 255700000000")

    elif "my name is" in low:
        return jsonify(reply=f"I already know you, {name}! What do you want to buy?")

    else:
        return jsonify(reply=f"Samahani {name}, sikuelewa. Type 'price' or type a product name like 'dress'")

if __name__ == '__main__':
    # FIX FOR LINK - Render gives us the port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)    