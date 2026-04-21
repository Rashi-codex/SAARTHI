from flask import Flask, render_template, request, redirect, url_for

import sqlite3
app = Flask(__name__)
def init_db():
    conn=sqlite3.connect('learning_resources.db')
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (Email TEXT,Password TEXT,role TEXT, age_group TEXT, subject TEXT)')
    conn.commit()
    conn.close()

def get_users():
    conn=sqlite3.connect('learning_resources.db')
    c=conn.cursor()
    c.execute('SELECT * FROM users')
    users=c.fetchall()
    conn.close()
    return users

def add_user(email,password,role,age_group,subject):
    conn=sqlite3.connect('learning_resources.db')
    c=conn.cursor()
    c.execute('INSERT INTO users (Email,Password,role,age_group,subject) VALUES (?,?,?,?,?)',(email,password,role,age_group,subject))
    conn.commit()
    conn.close()

def update_user(email,password,role,age_group,subject):
    conn=sqlite3.connect('learning_resources.db')
    c=conn.cursor()
    c.execute('UPDATE users SET Password=?, role=?, age_group=?, subject=? WHERE Email=?',(password,role,age_group,subject,email))
    conn.commit()
    conn.close()

def delete_user(email):
    conn=sqlite3.connect('learning_resources.db')
    c=conn.cursor()
    c.execute('DELETE FROM users WHERE Email=?',(email,))
    conn.commit()
    conn.close()
  
# SUBJECTS & RESOURCES DATA
LEARNING_DATA = {
    "Children": {
        "Storytelling": [
            ("StoryWeaver", "https://storyweaver.org.in"),
            ("Storyberries", "https://www.storyberries.com"),
            ("YouTube - Story Time", "https://www.youtube.com/results?search_query=kids+storytelling")
        ],
        "Fun Science": [
            ("Science Kids", "https://www.sciencekids.co.nz"),
            ("National Geographic Kids", "https://kids.nationalgeographic.com"),
            ("YouTube - Fun Science", "https://www.youtube.com/results?search_query=fun+science+for+kids")
        ],
        "Basic Mathematics": [
            ("Math is Fun", "https://www.mathsisfun.com"),
            ("Khan Academy Kids", "https://learn.khanacademy.org/khan-academy-kids"),
            ("YouTube - Kids Math", "https://www.youtube.com/results?search_query=basic+math+for+kids")
        ],
        "English": [
            ("British Council Kids", "https://learnenglishkids.britishcouncil.org"),
            ("Starfall", "https://www.starfall.com"),
            ("YouTube - Kids English", "https://www.youtube.com/results?search_query=english+for+kids")
        ]
    },

    "Student": {
        "Python Programming": [
            ("W3Schools", "https://www.w3schools.com/python"),
            ("GeeksforGeeks", "https://www.geeksforgeeks.org/python-programming-language"),
            ("YouTube - CodeWithHarry", "https://www.youtube.com/@CodeWithHarry")
        ],
        "Java Programming": [
            ("JavaTpoint", "https://www.javatpoint.com/java-tutorial"),
            ("GeeksforGeeks", "https://www.geeksforgeeks.org/java"),
            ("YouTube - Telusko", "https://www.youtube.com/@Telusko")
        ],
        "Communication Skills": [
            ("British Council", "https://learnenglish.britishcouncil.org"),
            ("MindTools", "https://www.mindtools.com"),
            ("YouTube - Communication Skills", "https://www.youtube.com/results?search_query=communication+skills")
        ],
        "Aptitude": [
            ("IndiaBIX", "https://www.indiabix.com"),
            ("PrepInsta", "https://prepinsta.com"),
            ("YouTube - Aptitude", "https://www.youtube.com/results?search_query=aptitude+preparation")
        ],
        "Placement & Series": [
            ("LeetCode", "https://leetcode.com"),
            ("HackerRank", "https://www.hackerrank.com"),
            ("YouTube - Placement Prep", "https://www.youtube.com/results?search_query=placement+preparation")
        ]
    },

    "Senior": {
        "Newspaper Analysis": [
            ("The Hindu", "https://www.thehindu.com"),
            ("Indian Express", "https://indianexpress.com"),
            ("YouTube - Newspaper Analysis", "https://www.youtube.com/results?search_query=newspaper+analysis")
        ],
        "Current Affairs": [
            ("PIB", "https://pib.gov.in"),
            ("Drishti IAS", "https://www.drishtiias.com"),
            ("YouTube - Current Affairs", "https://www.youtube.com/results?search_query=current+affairs")
        ],
        "Bhakti Music": [
            ("YouTube Bhakti Songs", "https://www.youtube.com/results?search_query=bhakti+music"),
            ("Gaana Bhakti", "https://gaana.com/genre/devotional")
        ],

        "Online Banking Help": [
            ("SBI Guide", "https://sbi.co.in/web/personal-banking"),
            ("YouTube Banking Tutorial", "https://www.youtube.com/results?search_query=online+banking+tutorial")
        ],

        "Digital Learning": [
            ("Google Digital Garage", "https://learndigital.withgoogle.com"),
            ("YouTube Basics", "https://www.youtube.com/results?search_query=how+to+use+mobile+for+beginners")
        ]
    }
        
}

 

@app.route("/", methods=["GET"])
def login():
    users=get_users()
    return render_template("indexx.html",users=users)

@app.route("/dashboard", methods=["POST"])
def dashboard():
    role = request.form.get("role")
    age_group = request.form.get("age_group")
    subjects={}
    if role=="Children" and age_group=="5-12":
        subjects=LEARNING_DATA["Children"]
    elif role=="Student" and age_group=="13-24":
        subjects=LEARNING_DATA["Student"]     
    elif role=="Senior" and age_group=="Above 35":
        subjects=LEARNING_DATA["Senior"]

    return render_template("dashboard.html", role=role, age_group=age_group, subjects=subjects)


@app.route("/resources/<role>/<subjects>")
def resources(role, subjects):
    links =LEARNING_DATA[role][subjects]
    return render_template("resources.html", subjects=subjects, links=links)

@app.route('/add_user',methods=['POST'])
def add_user_route():
    email=request.form['email'] 
    password=request.form['password']
    role=request.form['role']                       
    age_group=request.form['age_group']
    subject=request.form['subject'] 
    add_user(email,password,role,age_group,subject)
    return redirect(url_for('login'))

@app.route('/update_user/<email>',methods=['GET','POST'])
def update_user_route(email=None):
    if request.method=='POST':
        password=request.form['password']
        role=request.form['role']                       
        age_group=request.form['age_group']
        subject=request.form['subject'] 
        update_user(email,password,role,age_group,subject)
        return redirect(url_for('login'))
    
    conn=sqlite3.connect('learning_resources.db')
    c=conn.cursor()
    c.execute('SELECT * FROM users WHERE Email=?',(email,))
    user=c.fetchone()
    conn.close()
    return render_template('update_user.html',user=user)

@app.route('/delete_user/<email>',methods=['GET'])
def delete_user_route(email):
    delete_user(email)
    return redirect(url_for('login'))

if __name__ == "__main__":
    init_db()

    app.run(debug=True)