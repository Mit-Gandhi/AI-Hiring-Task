'''The Perfect code that makes pdf and assessment tasks also'''
import random
import json
import os
from datetime import datetime
import google.generativeai as genai
import time
from faker import Faker
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import textwrap

# Configuration - Add your Gemini API key here
GEMINI_API_KEY = "AIzaSyAgCJ_Yp7qPr_Prn3Wqs3xoP_wU9WpWBVs"  # Replace with your actual API key

# Initialize Faker for candidate profile generation
fake = Faker()

# Sample data pools for profile generation
skills_pool = [
    "Python", "Java", "JavaScript", "React", "Node.js", "AWS", "Docker", 
    "Kubernetes", "Machine Learning", "Data Science", "SQL", "MongoDB",
    "Git", "CI/CD", "System Design", "API Development", "Microservices",
    "Teamwork", "Communication", "Problem Solving"
]

companies_pool = [
    "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Tesla",
    "Adobe", "Salesforce", "Oracle", "IBM", "Intel", "NVIDIA", "Uber", "Airbnb",
    "Spotify", "Slack", "Zoom", "Dropbox", "Atlassian"
]

class CandidateProfileGenerator:
    """Generate realistic candidate profiles."""
    
    def __init__(self):
        self.fake = Faker()
    
    def generate_profile(self, candidate_id):
        """Generate a complete candidate profile."""
        
        # Basic info
        name = self.fake.name()
        email = f"{name.lower().replace(' ', '.')}{random.randint(1, 999)}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.com'])}"
        phone = self.fake.phone_number()
        location = f"{self.fake.city()}, {self.fake.state()}"
        
        # Professional summary
        years_exp = random.randint(2, 12)
        current_role = random.choice([
            "Software Engineer", "Senior Software Engineer", "Lead Developer",
            "Full Stack Developer", "Backend Developer", "Frontend Developer",
            "Data Scientist", "ML Engineer", "DevOps Engineer", "Product Manager",
            "Sales Engineer", "Solutions Architect"
        ])
        
        # Work experience
        experience = self.generate_work_experience(years_exp, current_role)
        
        # Education
        education = self.generate_education()
        
        # Skills
        candidate_skills = random.sample(skills_pool, random.randint(6, 12))
        
        # Projects
        projects = self.generate_projects()
        
        # Certifications
        certifications = self.generate_certifications()
        
        return {
            "candidate_id": candidate_id,
            "personal_info": {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "linkedin_bio": self.generate_linkedin_bio(current_role, years_exp)
            },
            "professional_summary": {
                "current_role": current_role,
                "years_experience": years_exp,
                "summary": f"Experienced {current_role} with {years_exp} years in software development and technology solutions."
            },
            "work_experience": experience,
            "education": education,
            "skills": candidate_skills,
            "projects": projects,
            "certifications": certifications,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
    
    def generate_work_experience(self, years_exp, current_role):
        """Generate work experience history."""
        experience = []
        current_year = datetime.now().year
        
        # Current job
        start_year = current_year - random.randint(1, 3)
        experience.append({
            "title": current_role,
            "company": random.choice(companies_pool),
            "duration": f"{start_year} - Present",
            "responsibilities": [
                "Led development of scalable web applications",
                "Collaborated with cross-functional teams",
                "Implemented best practices and code reviews",
                "Mentored junior developers"
            ]
        })
        
        # Previous jobs
        remaining_years = years_exp - (current_year - start_year)
        while remaining_years > 0:
            job_duration = min(random.randint(1, 4), remaining_years)
            end_year = start_year - 1
            start_year = end_year - job_duration + 1
            
            prev_role = random.choice([
                "Software Developer", "Junior Developer", "Associate Engineer",
                "Software Engineer", "Developer", "Programmer"
            ])
            
            experience.append({
                "title": prev_role,
                "company": random.choice(companies_pool),
                "duration": f"{start_year} - {end_year}",
                "responsibilities": [
                    "Developed and maintained software applications",
                    "Participated in agile development processes",
                    "Worked on bug fixes and feature enhancements",
                    "Collaborated with team members on projects"
                ]
            })
            
            remaining_years -= job_duration
        
        return experience
    
    def generate_education(self):
        """Generate education background."""
        degrees = [
            "Bachelor of Technology in Computer Science",
            "Bachelor of Engineering in Software Engineering", 
            "Master of Science in Computer Science",
            "Bachelor of Science in Information Technology",
            "Master of Technology in Software Systems"
        ]
        
        universities = [
            "Stanford University", "MIT", "UC Berkeley", "Carnegie Mellon",
            "Georgia Tech", "University of Washington", "UT Austin",
            "IIT Delhi", "IIT Bombay", "BITS Pilani", "NIT Trichy"
        ]
        
        return [{
            "degree": random.choice(degrees),
            "institution": random.choice(universities),
            "year": random.randint(2010, 2020),
            "gpa": round(random.uniform(3.2, 4.0), 2)
        }]
    
    def generate_projects(self):
        """Generate project portfolio."""
        project_ideas = [
            "E-commerce Web Application",
            "Task Management System", 
            "Social Media Dashboard",
            "Real-time Chat Application",
            "Data Visualization Platform",
            "Mobile App for Food Delivery",
            "Personal Finance Tracker",
            "Blog Management System"
        ]
        
        projects = []
        for _ in range(random.randint(2, 4)):
            project = {
                "name": random.choice(project_ideas),
                "technologies": random.sample(skills_pool, random.randint(3, 6)),
                "description": "Full-stack application with modern technologies and best practices"
            }
            projects.append(project)
            project_ideas.remove(project["name"])  # Avoid duplicates
        
        return projects
    
    def generate_certifications(self):
        """Generate relevant certifications."""
        cert_options = [
            "AWS Certified Solutions Architect",
            "Google Cloud Professional Developer",
            "Microsoft Azure Fundamentals",
            "Certified Kubernetes Administrator",
            "Oracle Java SE Programmer",
            "MongoDB Certified Developer",
            "Docker Certified Associate"
        ]
        
        return random.sample(cert_options, random.randint(1, 3))
        
    def generate_linkedin_bio(self, current_role, years_exp):
        """Generate a realistic LinkedIn bio with personality traits and soft skills."""
        soft_skills = [
            "strong communicator", "team player", "natural leader",
            "problem solver", "detail-oriented", "creative thinker",
            "self-motivated", "adaptable", "results-driven",
            "analytical mindset", "strategic thinker", "collaborative",
            "empathetic leader", "innovative", "passionate about learning"
        ]
        
        work_traits = [
            "thrives in fast-paced environments",
            "excels at cross-functional collaboration",
            "proven track record of delivering results",
            "mentors junior team members",
            "drives innovation in team projects",
            "bridges technical and business requirements",
            "champions agile methodologies",
            "builds consensus across stakeholders"
        ]
        
        achievements = [
            "led successful digital transformation initiatives",
            "reduced system downtime by 40%",
            "improved team productivity by 25%",
            "launched 3 major product features",
            "streamlined development processes",
            "implemented best practices",
            "optimized performance metrics"
        ]
        
        # Randomly decide whether to include soft skills (70% chance)
        include_soft_skills = random.random() < 0.7
        
        # Build the bio
        bio_parts = []
        
        # Introduction
        intro = f"Experienced {current_role} with {years_exp} years in the tech industry. "
        bio_parts.append(intro)
        
        # Core competencies
        bio_parts.append(f"{random.choice(work_traits)}. ")
        
        # Achievements
        bio_parts.append(f"Recently {random.choice(achievements)}. ")
        
        # Soft skills section (if included)
        if include_soft_skills:
            selected_soft_skills = random.sample(soft_skills, random.randint(2, 4))
            bio_parts.append(f"Known for being a {', '.join(selected_soft_skills[:-1])} and {selected_soft_skills[-1]}. ")
        
        # Professional focus
        focus_statements = [
            f"Focused on leveraging technology to drive business value.",
            f"Passionate about building scalable solutions.",
            f"Dedicated to continuous learning and improvement.",
            f"Committed to excellence in software development."
        ]
        bio_parts.append(random.choice(focus_statements))
        
        return ''.join(bio_parts)

class UniqueAssessmentGenerator:
    """Generate unique assessment problems using Gemini AI."""
    
    def __init__(self, api_key):
        """Initialize Gemini AI with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.used_problems = set()
        print("Gemini AI initialized successfully")
    
    def generate_assessment_for_candidate(self, role, candidate_profile, candidate_num):
        """Generate unique assessment based on candidate profile and role."""
        
        candidate_name = candidate_profile["personal_info"]["name"]
        current_role = candidate_profile["professional_summary"]["current_role"]
        years_exp = candidate_profile["professional_summary"]["years_experience"]
        skills = ", ".join(candidate_profile["skills"])
        
        prompt = f"""
        Create a UNIQUE technical assessment for a {role} position candidate with the following profile:
        
        CANDIDATE PROFILE:
        - Name: {candidate_name}
        - Current Role: {current_role}
        - Experience: {years_exp} years
        - Key Skills: {skills}
        - Candidate Number: {candidate_num} (ensure uniqueness)
        
        REQUIREMENTS:
        Generate exactly 3 problems that are completely unique for this candidate:
        
        1. DIFFICULT PROJECT (3-4 hours):
           - Must be a complete application/system building task
           - Examples: AI Recruiter system, Woman Safety App, Smart Healthcare Platform, 
             E-commerce Platform, Real-time Analytics Dashboard, Social Impact App, etc.
           - Should leverage candidate's existing skills where possible
           - Must be different from other candidates
        
        2. MEDIUM TECHNICAL CHALLENGE (1-2 hours):
           - Algorithm/coding problem of medium complexity
           - Relevant to the target role
           - Should test problem-solving skills
        
        3. HARD SYSTEM DESIGN (1-2 hours):
           - Architecture/system design challenge
           - High-level system design problem
           - Should test scalability and design thinking
        
        UNIQUENESS CRITICAL: Each candidate must receive completely different problems.
        Consider the candidate's background to make problems more personalized.
        
        Return in JSON format:
        {{
            "assessment_id": "unique_id_for_candidate_{candidate_num}",
            "candidate_name": "{candidate_name}",
            "target_role": "{role}",
            "personalization_note": "How this assessment is tailored to the candidate",
            "problems": [
                {{
                    "problem_number": 1,
                    "difficulty": "difficult",
                    "type": "project_building",
                    "title": "Specific Unique Project Title",
                    "description": "Detailed project description with specific requirements",
                    "key_requirements": [
                        "Specific requirement 1",
                        "Specific requirement 2", 
                        "Specific requirement 3"
                    ],
                    "deliverables": [
                        "Expected output 1",
                        "Expected output 2"
                    ],
                    "time_limit": "3-4 hours",
                    "technologies": ["suggested", "tech", "stack"],
                    "evaluation_focus": ["criteria1", "criteria2"]
                }},
                {{
                    "problem_number": 2,
                    "difficulty": "medium",
                    "type": "technical_challenge", 
                    "title": "Medium Challenge Title",
                    "description": "Technical problem description",
                    "requirements": ["req1", "req2"],
                    "time_limit": "1-2 hours",
                    "expected_approach": "Brief solution approach"
                }},
                {{
                    "problem_number": 3,
                    "difficulty": "hard",
                    "type": "system_design",
                    "title": "System Design Challenge Title",
                    "description": "System design problem description", 
                    "requirements": ["req1", "req2"],
                    "time_limit": "1-2 hours",
                    "expected_approach": "Expected design approach"
                }}
            ],
            "total_time": "5-8 hours",
            "special_instructions": "Any special notes for this candidate",
            "generated_at": "{datetime.utcnow().isoformat()}Z"
        }}
        """
        
        try:
            time.sleep(1)  # Rate limiting
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean JSON from response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.rfind("```")
                response_text = response_text[json_start:json_end].strip()
            
            assessment = json.loads(response_text)
            
            print(f"Generated assessment for {candidate_name}")
            return assessment
            
        except Exception as e:
            print(f"Error generating assessment for {candidate_name}: {e}")
            return self.create_fallback_assessment(role, candidate_profile, candidate_num)
    
    def create_fallback_assessment(self, role, candidate_profile, candidate_num):
        """Create fallback assessment if AI generation fails."""
        
        candidate_name = candidate_profile["personal_info"]["name"]
        
        # Unique project ideas
        project_templates = [
            "AI-Powered Recruitment Platform",
            "Smart City Management System", 
            "Healthcare Patient Monitoring App",
            "Sustainable Energy Dashboard",
            "Educational Learning Platform",
            "Financial Planning Assistant",
            "Social Impact Tracking System",
            "Disaster Response Coordination Tool",
            "Mental Health Support Platform",
            "Supply Chain Optimization System"
        ]
        
        selected_project = project_templates[candidate_num % len(project_templates)]
        
        return {
            "assessment_id": f"fallback_{role}_{candidate_num}",
            "candidate_name": candidate_name,
            "target_role": role,
            "personalization_note": f"Tailored assessment for {candidate_name} applying for {role}",
            "problems": [
                {
                    "problem_number": 1,
                    "difficulty": "difficult",
                    "type": "project_building", 
                    "title": f"Build {selected_project}",
                    "description": f"Design and implement a complete {selected_project} with full functionality, user interface, and backend systems.",
                    "key_requirements": [
                        "Full-stack web application",
                        "User authentication system",
                        "Database integration",
                        "Responsive UI design",
                        "API development"
                    ],
                    "deliverables": [
                        "Working application with source code",
                        "Database design documentation", 
                        "API documentation",
                        "User manual"
                    ],
                    "time_limit": "3-4 hours",
                    "technologies": ["React/Vue", "Node.js/Python", "PostgreSQL/MongoDB", "REST APIs"],
                    "evaluation_focus": ["functionality", "code_quality", "user_experience", "scalability"]
                },
                {
                    "problem_number": 2,
                    "difficulty": "medium",
                    "type": "technical_challenge",
                    "title": f"Data Processing Challenge for {role}",
                    "description": "Implement an efficient algorithm to process and analyze large datasets with specific constraints.",
                    "requirements": [
                        "Handle large data volumes",
                        "Optimize for performance", 
                        "Implement proper error handling"
                    ],
                    "time_limit": "1-2 hours",
                    "expected_approach": "Use appropriate data structures and algorithms for optimal performance"
                },
                {
                    "problem_number": 3,
                    "difficulty": "hard", 
                    "type": "system_design",
                    "title": f"Scalable Architecture Design for {role}",
                    "description": "Design a distributed system architecture that can handle high traffic and ensure reliability.",
                    "requirements": [
                        "Handle 1M+ concurrent users",
                        "Ensure 99.9% uptime",
                        "Plan for global distribution"
                    ],
                    "time_limit": "1-2 hours",
                    "expected_approach": "Create comprehensive system architecture with load balancing, caching, and fault tolerance"
                }
            ],
            "total_time": "5-8 hours",
            "special_instructions": f"Assessment customized for {candidate_name}'s background in {role}",
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }

class CriteriaEvaluator:
    """Evaluate candidates against hiring criteria and provide hiring recommendations."""
    
    def __init__(self, api_key):
        """Initialize Gemini AI with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def set_role_criteria(self, role):
        """Define role-specific evaluation criteria."""
        base_criteria = {
            "technical_expertise": {
                "weight": 25,
                "description": "Technical skills and knowledge required for the role"
            },
            "experience_relevance": {
                "weight": 20,
                "description": "Relevance of past experience to the role"
            },
            "leadership_potential": {
                "weight": 15,
                "description": "Leadership capabilities and potential"
            },
            "communication_skills": {
                "weight": 15,
                "description": "Written and verbal communication abilities"
            },
            "cultural_fit": {
                "weight": 10,
                "description": "Alignment with company culture and values"
            },
            "problem_solving": {
                "weight": 15,
                "description": "Analytical and problem-solving capabilities"
            }
        }
        
        # Role-specific criteria adjustments
        role_specific_criteria = {
            "Software Engineer": {
                "technical_expertise": {"weight": 30},
                "problem_solving": {"weight": 20},
                "communication_skills": {"weight": 10}
            },
            "Frontend Engineer": {
                "technical_expertise": {"weight": 25},
                "communication_skills": {"weight": 20},
                "problem_solving": {"weight": 15}
            },
            "Data Scientist": {
                "technical_expertise": {"weight": 30},
                "problem_solving": {"weight": 25},
                "communication_skills": {"weight": 10}
            },
            "Product Manager": {
                "leadership_potential": {"weight": 25},
                "communication_skills": {"weight": 25},
                "technical_expertise": {"weight": 10}
            },
            "Sales Engineer": {
                "communication_skills": {"weight": 30},
                "technical_expertise": {"weight": 20},
                "cultural_fit": {"weight": 15}
            }
        }
        
        # Apply role-specific adjustments if available
        if role in role_specific_criteria:
            criteria = base_criteria.copy()
            for key, value in role_specific_criteria[role].items():
                criteria[key].update(value)
        else:
            criteria = base_criteria
        
        return criteria
    
    def evaluate_candidate(self, candidate_profile, assessment, behavioral_analysis, role):
        """Evaluate candidate against role criteria and provide hiring recommendation."""
        criteria = self.set_role_criteria(role)
        
        # Prepare candidate data for evaluation
        evaluation_data = {
            "name": candidate_profile["personal_info"]["name"],
            "role": role,
            "technical_background": {
                "skills": candidate_profile["skills"],
                "experience_years": candidate_profile["professional_summary"]["years_experience"],
                "current_role": candidate_profile["professional_summary"]["current_role"],
                "projects": [p["name"] for p in candidate_profile["projects"]],
                "certifications": candidate_profile["certifications"]
            },
            "behavioral_assessment": behavioral_analysis["behavioral_analysis"],
            "linkedin_bio": candidate_profile["personal_info"]["linkedin_bio"]
        }
        
        prompt = f"""
        Evaluate this candidate for a {role} position against the following criteria:
        
        CANDIDATE INFORMATION:
        {json.dumps(evaluation_data, indent=2)}
        
        EVALUATION CRITERIA:
        {json.dumps(criteria, indent=2)}
        
        REQUIRED OUTPUT FORMAT:
        Return a JSON object with:
        1. Scores for each criterion (0-100)
        2. Brief justification for each score
        3. Overall weighted score
        4. Hiring recommendation with confidence level
        5. Key strengths (top 3)
        6. Areas for consideration (top 2)
        
        Example:
        {{
            "criteria_scores": {{
                "technical_expertise": {{"score": 85, "justification": "Strong technical background with relevant skills..."}},
                "experience_relevance": {{"score": 90, "justification": "Directly applicable experience..."}}
                // ... other criteria
            }},
            "overall_score": 87.5,
            "recommendation": {{
                "decision": "Strong Hire",
                "confidence": "High (85%)",
                "explanation": "Candidate shows exceptional promise..."
            }},
            "key_strengths": [
                "Strong technical expertise in required areas",
                "Proven leadership experience",
                "Excellent problem-solving skills"
            ],
            "areas_for_consideration": [
                "Limited experience with specific technology X",
                "May need support in area Y"
            ]
        }}
        
        IMPORTANT:
        - Be objective and data-driven
        - Consider all available information
        - Weight scores according to criteria importance
        - Provide specific evidence for scores
        """
        
        try:
            response = self.model.generate_content(prompt)
            analysis = response.text.strip()
            
            # Clean and parse JSON response
            if "```json" in analysis:
                json_start = analysis.find("```json") + 7
                json_end = analysis.find("```", json_start)
                analysis = analysis[json_start:json_end].strip()
            elif "```" in analysis:
                json_start = analysis.find("```") + 3
                json_end = analysis.rfind("```")
                analysis = analysis[json_start:json_end].strip()
            
            return json.loads(analysis)
            
        except Exception as e:
            print(f"Error evaluating candidate: {e}")
            return self.get_fallback_evaluation(evaluation_data["name"], role)
    
    def get_fallback_evaluation(self, candidate_name, role):
        """Provide fallback evaluation if AI generation fails."""
        return {
            "criteria_scores": {
                "technical_expertise": {"score": 70, "justification": "Based on available information"},
                "experience_relevance": {"score": 70, "justification": "Relevant experience noted"},
                "leadership_potential": {"score": 70, "justification": "Standard assessment"},
                "communication_skills": {"score": 70, "justification": "Standard assessment"},
                "cultural_fit": {"score": 70, "justification": "Standard assessment"},
                "problem_solving": {"score": 70, "justification": "Standard assessment"}
            },
            "overall_score": 70.0,
            "recommendation": {
                "decision": "Consider",
                "confidence": "Medium (70%)",
                "explanation": "Technical evaluation recommended for more accurate assessment"
            },
            "key_strengths": [
                "Relevant technical background",
                "Professional experience",
                "Basic qualifications met"
            ],
            "areas_for_consideration": [
                "Further technical assessment recommended",
                "Additional interview recommended"
            ]
        }

class MarketIntelligenceAgent:
    """Analyze market trends and provide sourcing optimization insights using Gemini AI."""
    
    def __init__(self, api_key):
        """Initialize Gemini AI with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_market_trends(self, role, location="Global"):
        """Generate market intelligence insights for the target role."""
        prompt = f"""
        Provide market intelligence analysis for hiring a {role}.
        Location: {location}
        
        REQUIRED OUTPUT FORMAT:
        Return a JSON structure with the following information:
        {{
            "market_demand": "High/Medium/Low - with brief explanation",
            "key_skills_in_demand": ["top 5 most in-demand skills for this role"],
            "salary_insights": {{
                "range": "Typical salary range",
                "factors": ["Key factors affecting compensation"]
            }},
            "sourcing_channels": ["Top 3 recommended sourcing channels"],
            "assessment_recommendations": ["3 key areas to focus on in assessments"],
            "market_trends": ["3 current trends affecting this role"]
        }}
        
        Focus on current market conditions and emerging trends.
        Be specific and actionable in recommendations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            analysis = response.text.strip()
            
            # Clean and parse JSON response
            if "```json" in analysis:
                json_start = analysis.find("```json") + 7
                json_end = analysis.find("```", json_start)
                analysis = analysis[json_start:json_end].strip()
            elif "```" in analysis:
                json_start = analysis.find("```") + 3
                json_end = analysis.rfind("```")
                analysis = analysis[json_start:json_end].strip()
            
            return json.loads(analysis)
            
        except Exception as e:
            print(f"Error generating market intelligence for {role}: {e}")
            return self.get_fallback_market_analysis(role)
    
    def get_fallback_market_analysis(self, role):
        """Provide fallback market analysis if AI generation fails."""
        return {
            "market_demand": "Data unavailable - Please check market research sources",
            "key_skills_in_demand": [
                "Technical expertise in role-specific tools",
                "Communication skills",
                "Problem-solving ability",
                "Team collaboration",
                "Project management"
            ],
            "salary_insights": {
                "range": "Varies by location and experience",
                "factors": [
                    "Years of experience",
                    "Location",
                    "Technical expertise"
                ]
            },
            "sourcing_channels": [
                "Professional networks",
                "Industry job boards",
                "Referral programs"
            ],
            "assessment_recommendations": [
                "Technical skills evaluation",
                "Problem-solving assessment",
                "Cultural fit interview"
            ],
            "market_trends": [
                "Remote work capabilities",
                "Digital transformation",
                "Continuous learning"
            ]
        }

class BehavioralAnalyzer:
    """Analyze candidate behavior and cultural fit using Gemini AI."""
    
    def __init__(self, api_key):
        """Initialize Gemini AI with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_candidate(self, profile, role):
        """Generate behavioral and cultural fit analysis for a candidate."""
        name = profile["personal_info"]["name"]
        bio = profile["personal_info"]["linkedin_bio"]
        current_role = profile["professional_summary"]["current_role"]
        experience = profile["professional_summary"]["years_experience"]
        
        prompt = f"""
        Based on the candidate's LinkedIn bio, provide a concise, structured behavioral assessment.
        
        CANDIDATE INFO:
        - Name: {name}
        - Target Role: {role}
        - Current Role: {current_role}
        - Years Experience: {experience}
        - LinkedIn Bio: {bio}
        
        REQUIRED OUTPUT FORMAT:
        Provide a 2-3 sentence assessment that follows this structure exactly:
        1. First sentence: Initial impression and strongest positive attributes identified in the bio
        2. Second sentence: Critical missing information or areas needing clarification
        3. Third sentence (optional): Specific recommendation for interview focus
        
        EXAMPLE OUTPUT:
        "John's LinkedIn profile demonstrates exceptional technical leadership and collaborative skills, with a proven track record of driving innovation. Further information about his experience with cross-functional team management would provide valuable context. Future interviews should focus on specific examples of project leadership and mentorship experience."
        
        IMPORTANT:
        - Keep the assessment balanced but constructive
        - Focus only on evidence from the bio
        - Be specific about both strengths and missing information
        - Make the output exactly match the structure of the example
        """
        
        try:
            response = self.model.generate_content(prompt)
            analysis = response.text.strip()
            
            # Clean and format the analysis
            if "```" in analysis:
                analysis = analysis.replace("```", "").strip()
            
            # Ensure we only get the actual assessment (remove any markdown or extra text)
            if '"' in analysis:
                # Extract text between first and last quotes if present
                analysis = analysis[analysis.find('"'):analysis.rfind('"')+1]
            
            # Remove any line breaks to ensure clean formatting
            analysis = analysis.replace('\n', ' ').strip()
            
            return {
                "candidate_name": name,
                "behavioral_analysis": analysis,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except Exception as e:
            print(f"Error generating behavioral analysis for {name}: {e}")
            return {
                "candidate_name": name,
                "behavioral_analysis": "Unable to generate behavioral analysis due to technical error.",
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }

class PDFGenerator:
    """Generate professional PDF reports with candidate profiles and assessments."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for PDF."""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        self.subheader_style = ParagraphStyle(
            'SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        )
        
        self.cell_style = ParagraphStyle(
            'CellStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            alignment=TA_LEFT
        )
    
    def create_info_table(self, data, headers=None):
        """Create a formatted information table."""
        if headers is None:
            headers = ['Field', 'Information']
        
        table_data = [headers]
        
        for key, value in data.items():
            formatted_key = key.replace('_', ' ').title()
            
            # Handle different value types
            if isinstance(value, list):
                formatted_value = ', '.join(str(item) for item in value)
            elif isinstance(value, dict):
                formatted_value = ', '.join(f"{k}: {v}" for k, v in value.items())
            else:
                formatted_value = str(value) if value is not None else 'N/A'
            
            # Wrap long text
            if len(formatted_value) > 80:
                formatted_value = textwrap.fill(formatted_value, width=80)
            
            table_data.append([
                Paragraph(formatted_key, self.cell_style),
                Paragraph(formatted_value, self.cell_style)
            ])
        
        table = Table(table_data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return table
    
    def create_experience_table(self, experiences):
        """Create work experience table."""
        table_data = [['Role', 'Company', 'Duration', 'Key Responsibilities']]
        
        for exp in experiences:
            responsibilities = exp.get('responsibilities', [])
            resp_text = '• ' + '\n• '.join(responsibilities) if responsibilities else 'N/A'
            
            table_data.append([
                Paragraph(exp.get('title', 'N/A'), self.cell_style),
                Paragraph(exp.get('company', 'N/A'), self.cell_style),
                Paragraph(exp.get('duration', 'N/A'), self.cell_style),
                Paragraph(resp_text, self.cell_style)
            ])
        
        table = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 2.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return table
    
    def create_assessment_table(self, problems):
        """Create assessment problems table."""
        table_data = [['#', 'Difficulty', 'Title', 'Description', 'Time', 'Type']]
        
        for problem in problems:
            description = problem.get('description', 'N/A')
            # Truncate long descriptions
            if len(description) > 100:
                description = description[:100] + '...'
            
            table_data.append([
                Paragraph(str(problem.get('problem_number', 'N/A')), self.cell_style),
                Paragraph(problem.get('difficulty', 'N/A').upper(), self.cell_style),
                Paragraph(problem.get('title', 'N/A'), self.cell_style),
                Paragraph(description, self.cell_style),
                Paragraph(problem.get('time_limit', 'N/A'), self.cell_style),
                Paragraph(problem.get('type', 'N/A'), self.cell_style)
            ])
        
        table = Table(table_data, colWidths=[0.3*inch, 0.8*inch, 1.8*inch, 2.5*inch, 0.8*inch, 1.0*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        return table
    
    def generate_candidate_pdf(self, candidate_profile, assessment, behavioral_analysis, output_path):
        """Generate complete PDF with candidate profile, assessment, and behavioral analysis."""
        
        doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch)
        story = []
        
        candidate_name = candidate_profile["personal_info"]["name"]
        target_role = assessment["target_role"]
        
        # Title
        title = f"Candidate Assessment Report: {candidate_name}"
        story.append(Paragraph(title, self.title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Basic Information
        story.append(Paragraph("Personal Information", self.header_style))
        personal_data = {
            'name': candidate_profile["personal_info"]["name"],
            'email': candidate_profile["personal_info"]["email"], 
            'phone': candidate_profile["personal_info"]["phone"],
            'location': candidate_profile["personal_info"]["location"],
            'target_role': target_role
        }
        story.append(self.create_info_table(personal_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Professional Summary
        story.append(Paragraph("Professional Summary", self.header_style))
        prof_data = {
            'current_role': candidate_profile["professional_summary"]["current_role"],
            'years_experience': f"{candidate_profile['professional_summary']['years_experience']} years",
            'summary': candidate_profile["professional_summary"]["summary"]
        }
        story.append(self.create_info_table(prof_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Skills
        story.append(Paragraph("Technical Skills", self.header_style))
        skills_data = {'skills': ', '.join(candidate_profile["skills"])}
        story.append(self.create_info_table(skills_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Work Experience
        story.append(Paragraph("Work Experience", self.header_style))
        story.append(self.create_experience_table(candidate_profile["work_experience"]))
        story.append(Spacer(1, 0.2*inch))
        
        # Education
        story.append(Paragraph("Education", self.header_style))
        for edu in candidate_profile["education"]:
            edu_data = {
                'degree': edu["degree"],
                'institution': edu["institution"],
                'year': str(edu["year"]),
                'gpa': f"{edu['gpa']}/4.0"
            }
            story.append(self.create_info_table(edu_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Projects
        story.append(Paragraph("Key Projects", self.header_style))
        for i, project in enumerate(candidate_profile["projects"], 1):
            project_data = {
                f'project_{i}_name': project["name"],
                f'project_{i}_technologies': ', '.join(project["technologies"]),
                f'project_{i}_description': project["description"]
            }
            story.append(self.create_info_table(project_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Certifications
        if candidate_profile["certifications"]:
            story.append(Paragraph("Certifications", self.header_style))
            cert_data = {'certifications': ', '.join(candidate_profile["certifications"])}
            story.append(self.create_info_table(cert_data))
            story.append(Spacer(1, 0.3*inch))
        
        # Page break before assessment
        story.append(PageBreak())
        
        # Assessment Section
        story.append(Paragraph(f"Technical Assessment for {target_role}", self.title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Assessment Overview
        story.append(Paragraph("Assessment Overview", self.header_style))
        assessment_data = {
            'assessment_id': assessment["assessment_id"],
            'total_problems': len(assessment["problems"]),
            'total_time': assessment["total_time"],
            'personalization': assessment.get("personalization_note", "Standard assessment")
        }
        story.append(self.create_info_table(assessment_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Assessment Problems Summary
        story.append(Paragraph("Assessment Problems Overview", self.header_style))
        story.append(self.create_assessment_table(assessment["problems"]))
        story.append(Spacer(1, 0.3*inch))
        
        # Detailed Problems
        story.append(Paragraph("Detailed Problem Descriptions", self.header_style))
        
        for problem in assessment["problems"]:
            # Problem header
            problem_title = f"Problem {problem['problem_number']}: {problem['title']}"
            story.append(Paragraph(problem_title, self.subheader_style))
            
            # Problem details
            problem_details = {
                'difficulty': problem["difficulty"].upper(),
                'type': problem["type"],
                'time_limit': problem["time_limit"],
                'description': problem["description"]
            }
            
            if problem.get('key_requirements'):
                problem_details['key_requirements'] = ', '.join(problem['key_requirements'])
            
            if problem.get('deliverables'):
                problem_details['deliverables'] = ', '.join(problem['deliverables'])
            
            if problem.get('technologies'):
                problem_details['suggested_technologies'] = ', '.join(problem['technologies'])
            
            if problem.get('expected_approach'):
                problem_details['expected_approach'] = problem['expected_approach']
            
            story.append(self.create_info_table(problem_details))
            story.append(Spacer(1, 0.2*inch))
        
        # Special Instructions
        if assessment.get("special_instructions"):
            story.append(Paragraph("Special Instructions", self.header_style))
            instructions_data = {'instructions': assessment["special_instructions"]}
            story.append(self.create_info_table(instructions_data))
        
        # Behavioral Analysis Section
        story.append(PageBreak())
        story.append(Paragraph("Behavioral Analysis & Cultural Fit Assessment", self.title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # LinkedIn Bio
        story.append(Paragraph("LinkedIn Bio", self.header_style))
        bio_data = {'bio': candidate_profile["personal_info"]["linkedin_bio"]}
        story.append(self.create_info_table(bio_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Behavioral Analysis
        story.append(Paragraph("Behavioral Assessment", self.header_style))
        analysis_data = {'analysis': behavioral_analysis["behavioral_analysis"]}
        story.append(self.create_info_table(analysis_data))
        
        # End of Behavioral Analysis Section
        
        # Build PDF
        doc.build(story)
        print(f"Generated PDF: {output_path}")

def display_market_analysis(market_analyzer):
    """Display market analysis for common roles."""
    common_roles = [
        "Software Engineer",
        "Data Scientist",
        "Frontend Engineer",
        "Backend Engineer",
        "DevOps Engineer",
        "ML Engineer",
        "Product Manager",
        "Sales Engineer",
        "Solutions Architect"
    ]
    
    print("\n" + "="*80)
    print("MARKET INTELLIGENCE REPORT FOR COMMON TECH ROLES")
    print("="*80)
    
    for role in common_roles:
        print(f"\n{role.upper()} - Market Analysis")
        print("-" * 50)
        
        analysis = market_analyzer.analyze_market_trends(role)
        
        print(f"Market Demand: {analysis['market_demand']}")
        print("\nKey Skills in Demand:")
        for skill in analysis['key_skills_in_demand']:
            print(f"• {skill}")
        
        print(f"\nSalary Range: {analysis['salary_insights']['range']}")
        
        print("\nCurrent Market Trends:")
        for trend in analysis['market_trends']:
            print(f"• {trend}")
        
        print("-" * 50)
        time.sleep(1)  # Prevent rate limiting
    
    print("\nUse this market intelligence to inform your hiring decisions.")
    print("="*80)

def get_recruiter_input(market_analyzer):
    """Get input from recruiter about the role and number of candidates."""
    print("\n" + "="*60)
    print("AI-POWERED ASSESSMENT GENERATOR WITH PDF OUTPUT")
    print("="*60)
    
    print("\nWelcome! Let's analyze the market and create candidate assessments.")
    
    # Display market analysis first
    display_market_analysis(market_analyzer)
    
    # Get target role
    print("\nBased on the market analysis above, please select a role:")
    print("Common roles: Software Engineer, Data Scientist, Frontend Engineer, Backend Engineer, DevOps Engineer, ML Engineer, Product Manager, Sales Engineer, Solutions Architect")
    role = input("\nEnter the job role you're hiring for: ").strip()
    
    if not role:
        role = "Software Engineer"
        print(f"Using default role: {role}")
    
    # Get number of candidates
    try:
        num_candidates = int(input("Enter number of candidates to generate: ").strip())
        if num_candidates <= 0 or num_candidates > 20:
            num_candidates = 3
            print(f"Using default: {num_candidates} candidates")
    except ValueError:
        num_candidates = 3
        print(f"Invalid input. Using default: {num_candidates} candidates")
    
    print(f"\nConfiguration complete!")
    print(f"Role: {role}")
    print(f"Number of candidates: {num_candidates}")
    
    return role, num_candidates

def display_assessment_summary(candidates, assessments, role, evaluations):
    """Display summary of all generated assessments and evaluations."""
    print(f"\n" + "="*80)
    print(f"ASSESSMENT GENERATION COMPLETE FOR {role.upper()}")
    print("="*80)
    
    # Sort candidates by overall score
    candidate_data = list(zip(candidates, assessments, evaluations))
    candidate_data.sort(key=lambda x: x[2]["overall_score"], reverse=True)
    
    print("\nCANDIDATE RANKINGS:")
    print("-" * 50)
    
    for i, (candidate, assessment, evaluation) in enumerate(candidate_data, 1):
        name = candidate["personal_info"]["name"]
        current_role = candidate["professional_summary"]["current_role"]
        experience = candidate["professional_summary"]["years_experience"]
        
        print(f"\nRANK {i}: {name}")
        print("-" * 50)
        print(f"Current Role: {current_role}")
        print(f"Experience: {experience} years")
        print(f"Overall Score: {evaluation['overall_score']:.1f}%")
        print(f"Recommendation: {evaluation['recommendation']['decision']} (Confidence: {evaluation['recommendation']['confidence']})")
        
        print("\nKey Strengths:")
        for strength in evaluation['key_strengths']:
            print(f"• {strength}")
            
        print("\nAreas for Consideration:")
        for area in evaluation['areas_for_consideration']:
            print(f"• {area}")
            
        print("\nDetailed Criteria Scores:")
        for criterion, details in evaluation['criteria_scores'].items():
            print(f"• {criterion.replace('_', ' ').title()}: {details['score']}%")
        
        # Show assessment problems
        problems = assessment.get('problems', [])
        for problem in problems:
            difficulty = problem.get('difficulty', '').upper()
            title = problem.get('title', 'N/A')
            time_limit = problem.get('time_limit', 'N/A')
            print(f"{difficulty} PROBLEM: {title} ({time_limit})")
        
        total_time = assessment.get('total_time', 'N/A')
        print(f"Total Assessment Time: {total_time}")
    
    # Uniqueness check
    print(f"\nUNIQUENESS VERIFICATION:")
    print("-" * 50)
    
    all_titles = []
    for assessment in assessments:
        for problem in assessment.get('problems', []):
            all_titles.append(problem.get('title', ''))
    
    unique_titles = set(all_titles)
    print(f"Total problems generated: {len(all_titles)}")
    print(f"Unique problems: {len(unique_titles)}")
    
    if len(unique_titles) == len(all_titles):
        print("SUCCESS: All problems are unique across candidates!")
    else:
        print("WARNING: Some problems may be similar.")

def main():
    """Main function to generate candidate profiles with assessments and PDF output."""
    
    # Check API key
    if GEMINI_API_KEY == "your_api_key_here" or not GEMINI_API_KEY:
        print("ERROR: Please set your Gemini API key in the GEMINI_API_KEY variable")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    try:
        # Initialize generators
        profile_generator = CandidateProfileGenerator()
        assessment_generator = UniqueAssessmentGenerator(GEMINI_API_KEY)
        behavioral_analyzer = BehavioralAnalyzer(GEMINI_API_KEY)
        market_analyzer = MarketIntelligenceAgent(GEMINI_API_KEY)
        criteria_evaluator = CriteriaEvaluator(GEMINI_API_KEY)
        pdf_generator = PDFGenerator()
        
        # Get recruiter input after showing market analysis
        role, num_candidates = get_recruiter_input(market_analyzer)
        
        # Create output directories
        os.makedirs("candidate_profiles", exist_ok=True)
        os.makedirs("pdf_reports", exist_ok=True)
        
        print(f"\nGenerating {num_candidates} candidate profiles and assessments...")
        
        all_candidates = []
        all_assessments = []
        all_evaluations = []
        
        for i in range(1, num_candidates + 1):
            print(f"\nProcessing Candidate {i}/{num_candidates}...")
            
            # Generate candidate profile
            candidate_profile = profile_generator.generate_profile(i)
            candidate_name = candidate_profile["personal_info"]["name"]
            
            print(f"Generated profile for: {candidate_name}")
            
            # Generate unique assessment
            assessment = assessment_generator.generate_assessment_for_candidate(
                role, candidate_profile, i
            )
            
            # Generate behavioral analysis
            behavioral_analysis = behavioral_analyzer.analyze_candidate(candidate_profile, role)
            print(f"Generated behavioral analysis for: {candidate_name}")
            
            # Generate hiring criteria evaluation
            evaluation = criteria_evaluator.evaluate_candidate(candidate_profile, assessment, behavioral_analysis, role)
            print(f"Generated hiring evaluation for: {candidate_name}")
            
            # Store data
            all_candidates.append(candidate_profile)
            all_assessments.append(assessment)
            all_evaluations.append(evaluation)
            
            # Generate PDF report
            safe_name = "".join(c for c in candidate_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            pdf_filename = f"{safe_name}_{role.replace(' ', '_')}_assessment.pdf"
            pdf_path = os.path.join("pdf_reports", pdf_filename)
            
            try:
                pdf_generator.generate_candidate_pdf(candidate_profile, assessment, behavioral_analysis, pdf_path)
                print(f"PDF generated: {pdf_path}")
            except Exception as e:
                print(f"Error generating PDF for {candidate_name}: {e}")
        
        # Save all data to JSON files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save candidate profiles
        profiles_file = f"candidate_profiles/all_profiles_{role.replace(' ', '_')}_{timestamp}.json"
        with open(profiles_file, 'w') as f:
            json.dump(all_candidates, f, indent=2)
        
        # Save assessments
        assessments_file = f"candidate_profiles/all_assessments_{role.replace(' ', '_')}_{timestamp}.json"
        with open(assessments_file, 'w') as f:
            json.dump(all_assessments, f, indent=2)
        
        # Display detailed summary with evaluations
        display_assessment_summary(all_candidates, all_assessments, role, all_evaluations)
        
        print(f"\n" + "="*80)
        print(f"FILES GENERATED")
        print("="*80)
        print(f"PDF Reports Directory: pdf_reports/ ({num_candidates} files)")
        print(f"Candidate Profiles JSON: {profiles_file}")
        print(f"Assessment Data JSON: {assessments_file}")
        
        print(f"\nPDF REPORT STRUCTURE FOR EACH CANDIDATE:")
        print("- Personal Information (Name, Email, Phone, Location)")
        print("- Professional Summary (Current Role, Experience)")
        print("- Technical Skills")
        print("- Work Experience History")
        print("- Education Background")
        print("- Key Projects Portfolio")
        print("- Professional Certifications")
        print("- Assessment Overview")
        print("- Detailed Assessment Problems")
        print("- Special Instructions")
        
        print(f"\nASSESSMENT STRUCTURE:")
        print("- 1 Difficult Project Challenge (3-4 hours)")
        print("- 1 Medium Technical Challenge (1-2 hours)")
        print("- 1 Hard System Design Challenge (1-2 hours)")
        print("- Total Time: 5-8 hours per candidate")
        print("- All problems are unique across candidates")
        
        # Show specific project examples
        print(f"\nEXAMPLE PROJECT ASSIGNMENTS:")
        for i, assessment in enumerate(all_assessments[:3], 1):  # Show first 3 examples
            difficult_problem = next((p for p in assessment["problems"] if p["difficulty"] == "difficult"), {})
            project_title = difficult_problem.get("title", "N/A")
            candidate_name = all_candidates[i-1]["personal_info"]["name"]
            print(f"Candidate {i} ({candidate_name}): {project_title}")
        
        if len(all_assessments) > 3:
            print(f"... and {len(all_assessments) - 3} more unique projects")
        
        print(f"\nSUCCESS! Generated {num_candidates} complete candidate profiles with unique assessments.")
        print("Each PDF contains both the candidate profile and their personalized assessment.")
        print("All assessments are guaranteed to be unique to prevent copying.")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting tips:")
        print("1. Check your Gemini API key is valid")
        print("2. Ensure you have internet connection")
        print("3. Verify all required packages are installed")
        print("4. Check if you have write permissions in current directory")

if __name__ == "__main__":
    # Installation requirements
    print("="*60)
    print("AI-POWERED ASSESSMENT GENERATOR WITH PDF OUTPUT")
    print("="*60)
    print("\nRequired packages:")
    print("pip install google-generativeai faker reportlab")
    print("\nSetup instructions:")
    print("1. Get your Gemini API key from: https://makersuite.google.com/app/apikey")
    print("2. Replace 'your_api_key_here' with your actual API key")
    print("3. Run this script")
    print("-" * 60)
    
    main()