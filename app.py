from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os

app = Flask(__name__)
CORS(app)

# List of 50 job roles with sample keyword mapping
job_roles_keywords = {
    "Data Scientist": ["python", "machine learning", "pandas", "tensorflow", "sql"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js"],
    "Android Developer": ["java", "kotlin", "android studio", "xml", "firebase"],
    "AI Engineer": ["python", "deep learning", "nlp", "pytorch", "opencv"],
    "Backend Developer": ["node.js", "express", "mongodb", "docker", "sql"],
    "Frontend Developer": ["html", "css", "javascript", "react", "vue.js"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "jenkins", "linux"],
    "Full Stack Developer": ["html", "css", "javascript", "node.js", "react", "mongodb"],
    "Cloud Architect": ["aws", "azure", "gcp", "terraform", "cloudformation"],
    "Database Administrator": ["sql", "mysql", "postgresql", "oracle", "backup"],
    "Data Engineer": ["python", "sql", "hadoop", "spark", "airflow"],
    "ML Engineer": ["python", "scikit-learn", "tensorflow", "keras", "numpy"],
    "Cybersecurity Analyst": ["network security", "penetration testing", "firewall", "nmap", "wireshark"],
    "Business Analyst": ["excel", "sql", "power bi", "tableau", "requirement analysis"],
    "QA Engineer": ["selenium", "junit", "postman", "automation", "manual testing"],
    "UI/UX Designer": ["figma", "adobe xd", "sketch", "wireframing", "prototyping"],
    "Game Developer": ["unity", "c#", "blender", "game physics", "3d modeling"],
    "Embedded Systems Engineer": ["c", "c++", "microcontrollers", "arduino", "raspberry pi"],
    "Robotics Engineer": ["ros", "python", "c++", "opencv", "embedded systems"],
    "Blockchain Developer": ["solidity", "ethereum", "web3.js", "smart contracts", "ganache"],
    "IoT Engineer": ["iot", "mqtt", "esp32", "arduino", "sensors"],
    "System Administrator": ["linux", "windows server", "bash", "active directory", "networking"],
    "Technical Writer": ["markdown", "api documentation", "jira", "xml", "git"],
    "Network Engineer": ["routing", "switching", "cisco", "firewalls", "vpn"],
    "IT Support Specialist": ["troubleshooting", "windows", "hardware", "networking", "ticketing tools"],
    "Product Manager": ["agile", "scrum", "jira", "roadmap", "analytics"],
    "Software Engineer": ["java", "c++", "python", "git", "algorithms"],
    "NLP Engineer": ["spacy", "nltk", "transformers", "bert", "text classification"],
    "Computer Vision Engineer": ["opencv", "pytorch", "image processing", "cnn", "tensorflow"],
    "Big Data Engineer": ["hadoop", "spark", "hive", "kafka", "sqoop"],
    "AR/VR Developer": ["unity", "c#", "arcore", "arkit", "3d modeling"],
    "ETL Developer": ["etl", "informatica", "talend", "data warehouse", "sql"],
    "Salesforce Developer": ["apex", "visualforce", "salesforce", "soql", "lightning"],
    "Technical Support Engineer": ["helpdesk", "troubleshooting", "windows", "vpn", "ticketing"],
    "Site Reliability Engineer": ["monitoring", "logging", "kubernetes", "incident response", "sre"],
    "CRM Specialist": ["crm", "salesforce", "zoho", "hubspot", "customer support"],
    "Solutions Architect": ["cloud", "aws", "architecture", "design patterns", "scalability"],
    "Penetration Tester": ["metasploit", "burpsuite", "nmap", "exploit", "vulnerability"],
    "Cloud Engineer": ["aws", "azure", "devops", "linux", "cloud formation"],
    "IT Consultant": ["strategy", "cloud", "implementation", "audit", "compliance"],
    "Mobile App Developer": ["flutter", "dart", "android", "ios", "firebase"],
    "Security Analyst": ["siem", "threat hunting", "network security", "incident response", "firewall"],
    "Data Analyst": ["excel", "sql", "tableau", "python", "data visualization"],
    "AI Researcher": ["deep learning", "research papers", "pytorch", "transformers", "cv/nlp"],
    "Operations Engineer": ["scripting", "monitoring", "deployment", "incident", "linux"],
    "Digital Marketing Analyst": ["seo", "google analytics", "ppc", "content", "social media"],
    "Instructional Designer": ["storyboarding", "e-learning", "articulate", "lms", "pedagogy"],
    "Data Architect": ["data modeling", "sql", "data governance", "big data", "cloud"],
    "Bioinformatics Scientist": ["python", "genomics", "biopython", "r", "data analysis"],... add more up to 50 (or keep adding later easily)
}

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_role' not in request.form:
        return jsonify({'error': 'Missing data'}), 400

    resume_file = request.files['resume']
    job_role = request.form['job_role']

    try:
        reader = PyPDF2.PdfReader(resume_file)
        resume_text = ''
        for page in reader.pages:
            resume_text += page.extract_text() or ''

        resume_text = resume_text.lower()

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
    app.run(debug=True)
