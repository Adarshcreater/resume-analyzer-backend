from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os

app = Flask(__name__)
CORS(app)

# Job keywords
job_roles_keywords = {
    "Data Analyst": ["excel", "sql", "tableau", "python", "data visualization"],
    "Software Engineer": ["java", "c++", "python", "git", "algorithms"],
    "AI Engineer": ["python", "deep learning", "nlp", "pytorch", "opencv"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js"],
    "Cloud Engineer": ["aws", "azure", "devops", "linux", "cloud formation"],
    "Backend Developer": ["node.js", "express", "mongodb", "docker", "sql"],
    "Frontend Developer": ["html", "css", "javascript", "react", "vue.js"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "jenkins", "linux"],
    "Database Admin": ["sql", "mysql", "postgresql", "oracle", "backup"],
    "Cybersecurity Analyst": ["network security", "penetration testing", "firewall", "nmap", "wireshark"],
    # Add more if needed
}

@app.route('/')
def home():
    return "Resume Analyzer Backend is Live!"

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_role' not in request.form:
        return jsonify({'error': 'Missing resume or job role'}), 400

    resume_file = request.files['resume']
    job_role = request.form['job_role']

    try:
        reader = PyPDF2.PdfReader(resume_file)
        resume_text = ''.join([page.extract_text() or '' for page in reader.pages]).lower()

        keywords = job_roles_keywords.get(job_role, [])
        score = sum(1 for keyword in keywords if keyword in resume_text)
        match_percent = int((score / len(keywords)) * 100) if keywords else 0

        return jsonify({
            'job_role': job_role,
            'score': score,
            'total_keywords': len(keywords),
            'match_percent': match_percent,
            'keywords_matched': [k for k in keywords if k in resume_text]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
