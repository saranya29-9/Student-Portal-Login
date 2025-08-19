from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # needed for sessions

# Sample student data
students = {
    "S123": {
        "password": "pass123",
        "name": "John Doe",
        "results": [
            {"subject": "Math", "grade": "A"},
            {"subject": "English", "grade": "B+"},
            {"subject": "Physics", "grade": "A-"},
            {"subject": "History", "grade": "B"},
        ],
        "attendance": {"totalDays": 180, "attendedDays": 170, "percentage": "94.4%"},
        "timetable": [
            {"day": "Monday", "schedule": ["Math", "English", "Physics"]},
            {"day": "Tuesday", "schedule": ["History", "Math", "Physical Education"]},
            {"day": "Wednesday", "schedule": ["English", "Chemistry", "Math"]},
            {"day": "Thursday", "schedule": ["Physics", "History", "Biology"]},
            {"day": "Friday", "schedule": ["Math", "Computer Science", "English"]},
        ],
    },
    "S456": {
        "password": "mypassword",
        "name": "Jane Smith",
        "results": [
            {"subject": "Math", "grade": "B+"},
            {"subject": "English", "grade": "A"},
            {"subject": "Physics", "grade": "B"},
            {"subject": "History", "grade": "A-"},
        ],
        "attendance": {"totalDays": 180, "attendedDays": 165, "percentage": "91.7%"},
        "timetable": [
            {"day": "Monday", "schedule": ["English", "Math", "Biology"]},
            {"day": "Tuesday", "schedule": ["Physics", "History", "Math"]},
            {"day": "Wednesday", "schedule": ["Chemistry", "English", "Physical Education"]},
            {"day": "Thursday", "schedule": ["Math", "Computer Science", "History"]},
            {"day": "Friday", "schedule": ["Physics", "English", "Math"]},
        ],
    },
}

# Login page
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body style="font-family: Arial; background:#283e51; color:white; display:flex; justify-content:center; align-items:center; height:100vh;">
    <div style="background:#1f2937; padding:30px; border-radius:12px; width:350px;">
        <h2 style="color:#7dd3fc; text-align:center;">Student Portal Login</h2>
        {% if error %}
        <div style="background:#f87171; padding:10px; border-radius:8px; text-align:center; margin-bottom:12px;">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <label>Student ID</label><br>
            <input type="text" name="studentId" required style="width:100%; padding:10px; margin:6px 0;"><br>
            <label>Password</label><br>
            <input type="password" name="password" required style="width:100%; padding:10px; margin:6px 0;"><br>
            <button type="submit" style="width:100%; padding:12px; margin-top:15px; background:#3b82f6; color:white; border:none; border-radius:8px;">Login</button>
        </form>
    </div>
</body>
</html>
"""

# Dashboard page
dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body { font-family: Arial; background:linear-gradient(135deg,#4b79a1,#283e51); color:white; }
        .container { background:#1f2937; margin:30px auto; padding:30px; border-radius:12px; width:800px; }
        .tabs { display:flex; margin-bottom:20px; }
        .tab { flex:1; text-align:center; padding:12px; background:#374151; cursor:pointer; }
        .tab.active { background:#3b82f6; }
        .tab-content { background:#374151; padding:20px; border-radius:8px; }
        table { width:100%; border-collapse:collapse; }
        th, td { border:1px solid #555; padding:8px; }
        th { background:#2563eb; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Student Dashboard</h2>
        <p>Welcome, {{ student.name }}!</p>

        <div class="tabs">
            <div class="tab active" data-tab="results">Results</div>
            <div class="tab" data-tab="attendance">Attendance</div>
            <div class="tab" data-tab="timetable">Timetable</div>
        </div>
        <div id="tabContent" class="tab-content"></div>

        <form method="POST" action="{{ url_for('logout') }}">
            <button type="submit" style="margin-top:20px; width:100%; padding:12px; background:#ef4444; color:white; border:none; border-radius:8px;">Logout</button>
        </form>
    </div>

    <script>
        const studentData = {{ student | tojson }};
        const tabs = document.querySelectorAll('.tab');
        const content = document.getElementById('tabContent');

        function render(tab) {
            if(tab === 'results') {
                let html = "<table><tr><th>Subject</th><th>Grade</th></tr>";
                studentData.results.forEach(r => {
                    html += `<tr><td>${r.subject}</td><td>${r.grade}</td></tr>`;
                });
                html += "</table>";
                content.innerHTML = html;
            } else if(tab === 'attendance') {
                content.innerHTML = `
                    <p><b>Total Days:</b> ${studentData.attendance.totalDays}</p>
                    <p><b>Attended Days:</b> ${studentData.attendedDays}</p>
                    <p><b>Percentage:</b> ${studentData.attendance.percentage}</p>`;
            } else if(tab === 'timetable') {
                let html = "<table><tr><th>Day</th><th>Schedule</th></tr>";
                studentData.timetable.forEach(d => {
                    html += `<tr><td>${d.day}</td><td>${d.schedule.join(", ")}</td></tr>`;
                });
                html += "</table>";
                content.innerHTML = html;
            }
        }

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                render(tab.dataset.tab);
            });
        });

        render("results");  // Default
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'student_id' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        student_id = request.form.get('studentId').strip()
        password = request.form.get('password')
        student = students.get(student_id)
        if student and student['password'] == password:
            session['student_id'] = student_id
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Student ID or Password."
    return render_template_string(login_page, error=error)

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    student = students.get(session['student_id'])
    return render_template_string(dashboard_page, student=student)

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('student_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
