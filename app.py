from flask import Flask,render_template,request,url_for,redirect
import sqlite3

conn = sqlite3.connect("videos.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS EMBEDS (
        LINKS TEXT
    )
""")
conn.close()

def create_embed(embed):
    conn = sqlite3.connect("videos.db")
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO EMBEDS VALUES (?)",
    (embed,)
    
    )

    conn.commit()
    conn.close()

#create_embed('<iframe width="560" height="315" src="https://www.youtube.com/embed/adHUS0dwFB4?si=a9JjG257VIonfuwU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>')
def get_embeds():
  conn = sqlite3.connect('videos.db')
  cursor = conn.cursor()

  cursor.execute('SELECT links FROM EMBEDS')
  embeds = cursor.fetchall()  # Returns a list of tuples: [('link1',), ('link2',)]
  conn.close()

  if not embeds:
    return 'None'

  # Extract the string from each tuple into a list
  iframes = [row[0] for row in embeds]
  return iframes

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def hello_world():
    if request.method == "POST":
        iframe = request.form.get("iframe")
        if iframe:
            create_embed(iframe)
        return redirect(url_for("hello_world"))
    embed = get_embeds()
    return render_template("index.html",embed=embed)

app.run() 