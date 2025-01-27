import os
from flask import Flask, render_template,url_for,redirect, request

app = Flask(__name__)
app.secret_key = 'hello' 

def load_data():
    data = {}
    job_data_path = "job_data"

    for root, dirs, files in os.walk(job_data_path):
        category_name = os.path.basename(root) 
        
        jobs = []

        
        for filename in files:
            if filename.endswith(".txt"):
                job_path = os.path.join(root, filename)
                with open(job_path, 'r', encoding='utf-8') as f:
                    job_data = f.read().splitlines()
                    if len(job_data) >= 3:
                        job = {"title": job_data[0], "company": job_data[1], "description": job_data[2]}
                        jobs.append(job)
                    else:
                        # Print the data that doesn't meet the expected format
                        print(f"Invalid data in file: {job_path}")
                        print(f"Data lines: {job_data}")

        if jobs:
            data[category_name] = jobs

    return data


job_data = load_data()

@app.route('/')
def job_index():
    image_url = url_for('static', filename='images/1.jpg')
    return render_template('name_input.html',image_url=image_url)

@app.route('/process_name', methods=['POST'])
def process_name():
    image_url = url_for('static', filename='images/1.jpg')
    user_name = request.form.get('name')
    return render_template('role_select.html', name=user_name,image_url=image_url)

@app.route('/role_select/<name>')
def role_select(name):
    return render_template('role_select.html', name=name)

@app.route('/job_seeker/<name>')
def job_seeker(name):
    image_url = url_for('static', filename='images/1.jpg')
    return render_template('job_seeker.html', name=name,image_url=image_url)


@app.route('/employer')
def employer():
    image_url = url_for('static', filename='images/1.jpg')
    return render_template('employer.html',image_url=image_url)

@app.route('/job_listing_created', methods=['GET', 'POST'])
def create_job_listing():
    image_url = url_for('static', filename='images/1.jpg')
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        category = request.form['category']

        
        if category not in job_data:
            job_data[category] = []

       
        job = {"title": title, "company": company, "description": description}
        job_data[category].append(job)

        

        return redirect(url_for('index'))

    return render_template('job_listing_created.html',image_url=image_url)



@app.route('/index')
def index():
    image_url = url_for('static', filename='images/1.jpg')
    return render_template('index.html', jobs=job_data,image_url=image_url)


@app.route('/category_select')
def category_select():
    image_url = url_for('static', filename='images/1.jpg')
    return render_template('category_select.html',image_url=image_url)

@app.route('/category/<category_name>')
def category(category_name):
    image_url = url_for('static', filename='images/1.jpg')
    if category_name in job_data:
        category_jobs = job_data[category_name]
        return render_template('category.html', category=category_name, jobs=category_jobs,image_url=image_url)
    else:
        return "Category not found"



@app.route('/job/<category_name>/<int:job_id>')
def job(category_name, job_id):
    image_url = url_for('static', filename='images/1.jpg')
    if category_name in job_data and 0 <= job_id < len(job_data[category_name]):
        job = job_data[category_name][job_id]
        return render_template('job.html', job=job, category_name=category_name,image_url=image_url)
    else:
        return "Job not found"

if __name__ == '__main__':
    app.run(debug=True)
