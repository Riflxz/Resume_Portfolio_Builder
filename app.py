import os
import json
import zipfile
import shutil
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configuration
UPLOAD_FOLDER = 'static/uploads'
EXPORT_FOLDER = 'exports'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_data(data):
    """Clean and validate form data"""
    cleaned = {}
    
    # Basic info
    cleaned['name'] = data.get('name', '').strip()
    cleaned['job_title'] = data.get('job_title', '').strip()
    cleaned['description'] = data.get('description', '').strip()
    cleaned['photo'] = data.get('photo', '')
    
    # Education
    cleaned['education'] = []
    education_schools = data.getlist('education_school')
    education_degrees = data.getlist('education_degree')
    education_years = data.getlist('education_year')
    
    for i in range(len(education_schools)):
        if i < len(education_degrees) and i < len(education_years):
            if education_schools[i].strip():
                cleaned['education'].append({
                    'school': education_schools[i].strip(),
                    'degree': education_degrees[i].strip(),
                    'year': education_years[i].strip()
                })
    
    # Experience
    cleaned['experience'] = []
    exp_companies = data.getlist('experience_company')
    exp_positions = data.getlist('experience_position')
    exp_periods = data.getlist('experience_period')
    exp_descriptions = data.getlist('experience_description')
    
    for i in range(len(exp_companies)):
        if (i < len(exp_positions) and i < len(exp_periods) and 
            i < len(exp_descriptions) and exp_companies[i].strip()):
            cleaned['experience'].append({
                'company': exp_companies[i].strip(),
                'position': exp_positions[i].strip(),
                'period': exp_periods[i].strip(),
                'description': exp_descriptions[i].strip()
            })
    
    # Skills
    cleaned['skills'] = []
    skills_data = data.getlist('skills')
    for skill in skills_data:
        if skill.strip():
            cleaned['skills'].append(skill.strip())
    
    # Social media
    cleaned['social'] = {}
    social_fields = ['github', 'linkedin', 'twitter', 'website', 'email']
    for field in social_fields:
        value = data.get(f'social_{field}', '').strip()
        if value:
            cleaned['social'][field] = value
    
    return cleaned

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Handle file upload
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                photo_filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        
        # Process form data
        form_data = clean_data(request.form)
        if photo_filename:
            form_data['photo'] = photo_filename
        
        # Validate required fields
        if not form_data['name']:
            flash('Name is required', 'error')
            return redirect(url_for('index'))
        
        # Store in session for preview
        session['portfolio_data'] = form_data
        
        return redirect(url_for('preview'))
        
    except Exception as e:
        logging.error(f"Error processing form: {str(e)}")
        flash('An error occurred while processing your data', 'error')
        return redirect(url_for('index'))

@app.route('/preview')
def preview():
    portfolio_data = session.get('portfolio_data')
    if not portfolio_data:
        flash('No portfolio data found. Please fill out the form first.', 'error')
        return redirect(url_for('index'))
    
    return render_template('preview.html', data=portfolio_data)

@app.route('/export')
def export_portfolio():
    portfolio_data = session.get('portfolio_data')
    if not portfolio_data:
        flash('No portfolio data found. Please fill out the form first.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Create export directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_name = f"portfolio_{timestamp}"
        export_path = os.path.join(EXPORT_FOLDER, export_name)
        os.makedirs(export_path, exist_ok=True)
        
        # Generate HTML
        html_content = generate_portfolio_html(portfolio_data)
        with open(os.path.join(export_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generate CSS
        css_content = generate_portfolio_css()
        with open(os.path.join(export_path, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Copy profile photo if exists
        if portfolio_data.get('photo'):
            src_photo = os.path.join(UPLOAD_FOLDER, portfolio_data['photo'])
            if os.path.exists(src_photo):
                dst_photo = os.path.join(export_path, 'profile_photo.jpg')
                shutil.copy2(src_photo, dst_photo)
        
        # Create ZIP file
        zip_filename = f"{export_name}.zip"
        zip_path = os.path.join(EXPORT_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(export_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, export_path)
                    zipf.write(file_path, arcname)
        
        # Clean up temporary directory
        shutil.rmtree(export_path)
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
    except Exception as e:
        logging.error(f"Error exporting portfolio: {str(e)}")
        flash('An error occurred while exporting your portfolio', 'error')
        return redirect(url_for('preview'))

def generate_portfolio_html(data):
    """Generate standalone HTML for portfolio"""
    photo_src = 'profile_photo.jpg' if data.get('photo') else ''
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', 'Portfolio')} - Portfolio</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="profile-section">
                {f'<img src="{photo_src}" alt="Profile Photo" class="profile-photo">' if photo_src else '<div class="profile-placeholder"><i class="fas fa-user"></i></div>'}
                <h1 class="name">{data.get('name', '')}</h1>
                <h2 class="job-title">{data.get('job_title', '')}</h2>
                <p class="description">{data.get('description', '')}</p>
            </div>
        </header>

        <main class="content">
            {generate_education_section(data.get('education', []))}
            {generate_experience_section(data.get('experience', []))}
            {generate_skills_section(data.get('skills', []))}
            {generate_social_section(data.get('social', {}))}
        </main>
    </div>
</body>
</html>"""
    return html

def generate_education_section(education):
    if not education:
        return ""
    
    html = '<section class="section"><h3 class="section-title"><i class="fas fa-graduation-cap"></i> Education</h3><div class="section-content">'
    for edu in education:
        html += f"""
        <div class="item">
            <h4 class="item-title">{edu.get('degree', '')}</h4>
            <p class="item-subtitle">{edu.get('school', '')}</p>
            <p class="item-date">{edu.get('year', '')}</p>
        </div>"""
    html += '</div></section>'
    return html

def generate_experience_section(experience):
    if not experience:
        return ""
    
    html = '<section class="section"><h3 class="section-title"><i class="fas fa-briefcase"></i> Experience</h3><div class="section-content">'
    for exp in experience:
        html += f"""
        <div class="item">
            <h4 class="item-title">{exp.get('position', '')}</h4>
            <p class="item-subtitle">{exp.get('company', '')}</p>
            <p class="item-date">{exp.get('period', '')}</p>
            <p class="item-description">{exp.get('description', '')}</p>
        </div>"""
    html += '</div></section>'
    return html

def generate_skills_section(skills):
    if not skills:
        return ""
    
    html = '<section class="section"><h3 class="section-title"><i class="fas fa-cogs"></i> Skills</h3><div class="section-content"><div class="skills-grid">'
    for skill in skills:
        html += f'<span class="skill-tag">{skill}</span>'
    html += '</div></div></section>'
    return html

def generate_social_section(social):
    if not social:
        return ""
    
    icons = {
        'github': 'fab fa-github',
        'linkedin': 'fab fa-linkedin',
        'twitter': 'fab fa-twitter',
        'website': 'fas fa-globe',
        'email': 'fas fa-envelope'
    }
    
    html = '<section class="section"><h3 class="section-title"><i class="fas fa-link"></i> Contact</h3><div class="section-content"><div class="social-links">'
    for platform, url in social.items():
        icon = icons.get(platform, 'fas fa-link')
        display_url = url if not url.startswith('http') else url
        link_url = url if url.startswith('http') else f'https://{url}' if platform != 'email' else f'mailto:{url}'
        html += f'<a href="{link_url}" class="social-link" target="_blank"><i class="{icon}"></i> {display_url}</a>'
    html += '</div></div></section>'
    return html

def generate_portfolio_css():
    """Generate CSS for the portfolio"""
    return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 60px 40px;
}

.profile-section {
    max-width: 500px;
    margin: 0 auto;
}

.profile-photo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 5px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.profile-placeholder {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 30px;
    border: 5px solid rgba(255, 255, 255, 0.2);
}

.profile-placeholder i {
    font-size: 60px;
    color: rgba(255, 255, 255, 0.7);
}

.name {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.job-title {
    font-size: 1.3rem;
    font-weight: 400;
    margin-bottom: 20px;
    opacity: 0.9;
}

.description {
    font-size: 1.1rem;
    line-height: 1.8;
    opacity: 0.9;
    max-width: 600px;
    margin: 0 auto;
}

.content {
    padding: 60px 40px;
}

.section {
    margin-bottom: 50px;
}

.section:last-child {
    margin-bottom: 0;
}

.section-title {
    font-size: 1.8rem;
    font-weight: 600;
    color: #667eea;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    gap: 15px;
}

.section-title i {
    font-size: 1.5rem;
}

.section-content {
    margin-left: 40px;
}

.item {
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid #eee;
}

.item:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.item-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
}

.item-subtitle {
    font-size: 1.1rem;
    color: #667eea;
    font-weight: 500;
    margin-bottom: 5px;
}

.item-date {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 10px;
    font-weight: 500;
}

.item-description {
    color: #555;
    line-height: 1.7;
}

.skills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.skill-tag {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 8px 16px;
    border-radius: 25px;
    font-size: 0.9rem;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.social-links {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.social-link {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
    padding: 10px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.social-link:hover {
    background: #f8f9ff;
    color: #764ba2;
    transform: translateX(5px);
}

.social-link i {
    font-size: 1.2rem;
    width: 24px;
}

@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .header {
        padding: 40px 20px;
    }
    
    .content {
        padding: 40px 20px;
    }
    
    .name {
        font-size: 2rem;
    }
    
    .job-title {
        font-size: 1.1rem;
    }
    
    .description {
        font-size: 1rem;
    }
    
    .section-content {
        margin-left: 0;
    }
    
    .section-title {
        font-size: 1.5rem;
    }
    
    .skills-grid {
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .profile-photo, .profile-placeholder {
        width: 120px;
        height: 120px;
    }
    
    .profile-placeholder i {
        font-size: 48px;
    }
    
    .name {
        font-size: 1.8rem;
    }
    
    .container {
        border-radius: 15px;
    }
}
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
