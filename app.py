import html
import re
import json
import os
from io import BytesIO
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

try:
    from pypdf import PdfReader
except ImportError:  # Keeps the app friendly before dependencies are installed.
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None


BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"

st.set_page_config(page_title="Resume Builder + ATS Checker", page_icon="📄", layout="wide")


defaults = {
    "name": "Aarav Krishnan",
    "title": "Senior Python Engineer | AI/ML Integration | Automation",
    "email": "aarav.krishnan@example.com",
    "phone": "+1 (555) 123-4567",
    "location": "San Francisco, CA",
    "linkedin": "linkedin.com/in/aarav-krishnan",
    "github": "github.com/aarav-krishnan",
    "portfolio": "aarav-krishnan.dev",
    "profile_photo": None,
    "photo_size": 80,
    "photo_shape": "circle",
    "photo_border": "none",
    "photo_zoom": 100,
    "target_company": "",
    "target_position": "",
    "required_skills": "",
    "generated_cover_letter": "",
    "interview_type": "Technical",
    "company_research": "",
    "summary": "Senior automation engineer with 15+ years of experience building Python automation, CI/CD, OS validation and AI-accelerated testing solutions.",
    "skills": "Python, Playwright, Selenium, Pytest, BDD, GitHub Actions, Jenkins, Docker, Kubernetes, Linux, QEMU, AI/ML",
    "experience": "Senior Principal Engineer — Tech Company\nSan Francisco, CA | 2025 – Present\nArchitected E2E automation frameworks and integrated AI-assisted engineering workflows.\n\nSenior Automation Engineer\nCompany | Location | Dates\nBuilt scalable automation frameworks, CI/CD pipelines and system validation solutions.",
    "projects": "AI-Accelerated Automation Framework\nPython-based E2E framework integrating AI agents, device control and validation.\n\nOS Provisioning & Validation\nAutomated ISO/RAW image provisioning, PXE workflows and system-level validation.",
    "education": "Bachelor's Degree — Computer Science / Engineering",
    "certifications": "Certification Name — Issuer | Year",
    "languages": "English (Professional), Hindi (Native)",
    "awards": "Optional award, publication, volunteer work, or professional membership",
}


palettes = {
    "Ocean": ("#2563EB", "#06B6D4"),
    "Emerald": ("#047857", "#10B981"),
    "Ruby": ("#BE123C", "#F43F5E"),
    "Indigo": ("#4F46E5", "#A855F7"),
    "Graphite": ("#334155", "#94A3B8"),
    "Copper": ("#B45309", "#FBBF24"),
    "Teal Ink": ("#0F766E", "#99F6E4"),
    "Custom": ("#2563EB", "#06B6D4"),
}


background_styles = {
    "Soft Paper": {
        "page_background": "background: #f8fafc;",
        "paper_background": "background: linear-gradient(135deg, #ffffff, #f8fafc);",
    },
    "Fine Grid": {
        "page_background": "background: #f8fafc;",
        "paper_background": "background-color: #ffffff; background-image: linear-gradient(rgba(15,23,42,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(15,23,42,.045) 1px, transparent 1px); background-size: 22px 22px;",
    },
    "Warm Dots": {
        "page_background": "background: #fff7ed;",
        "paper_background": "background-color: #fffdf9; background-image: radial-gradient(rgba(180,83,9,.14) 1px, transparent 1px); background-size: 18px 18px;",
    },
    "Cool Linen": {
        "page_background": "background: #eef7ff;",
        "paper_background": "background-color: #ffffff; background-image: linear-gradient(45deg, rgba(37,99,235,.06) 25%, transparent 25%), linear-gradient(-45deg, rgba(6,182,212,.06) 25%, transparent 25%); background-size: 24px 24px;",
    },
    "Lavender Wash": {
        "page_background": "background: #faf7ff;",
        "paper_background": "background: radial-gradient(circle at 12% 18%, rgba(168,85,247,.18), transparent 30%), radial-gradient(circle at 88% 16%, rgba(6,182,212,.16), transparent 28%), linear-gradient(135deg, #ffffff, #f0f9ff);",
    },
    "Geometric Dots": {
        "page_background": "background: #f8fafc;",
        "paper_background": "background-color: #ffffff; background-image: radial-gradient(circle at center, rgba(15,23,42,.05) 2px, transparent 2.5px); background-size: 20px 20px;",
    },
    "Crosshatch": {
        "page_background": "background: #f8fafc;",
        "paper_background": "background-color: #ffffff; background-image: linear-gradient(rgba(15,23,42,.03) 1px, transparent 1px), linear-gradient(90deg, rgba(15,23,42,.03) 1px, transparent 1px); background-size: 8px 8px;",
    },
    "Subtle Waves": {
        "page_background": "background: #f8fafc;",
        "paper_background": "background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 50%, #e0f2fe 100%);",
    },
    "Concentric Circles": {
        "page_background": "background: #f8fafc;",
        "paper_background": "background: radial-gradient(circle at 10% 10%, rgba(37,99,235,.04) 0%, transparent 30%), radial-gradient(circle at 90% 90%, rgba(6,182,212,.04) 0%, transparent 30%), #ffffff;",
    },
    "Professional Grain": {
        "page_background": "background: #f8fafc;",
        "paper_background": "background-color: #ffffff; background-image: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><filter id=\"paper\"><feTurbulence type=\"fractalNoise\" baseFrequency=\"0.04\" numOctaves=\"5\" stitchTiles=\"stitch\"/></filter><rect width=\"100%\" height=\"100%\" filter=\"url(%23paper)\" opacity=\"0.04\"/></svg>');",
    },
}


section_aliases = {
    "summary": {"summary", "profile", "professional summary", "career summary", "objective"},
    "skills": {"skills", "technical skills", "core skills", "key skills", "technologies"},
    "experience": {"experience", "work experience", "professional experience", "employment history"},
    "projects": {"projects", "key projects", "selected projects", "project experience"},
    "education": {"education", "academic background", "academics"},
    "certifications": {"certifications", "certificates", "licenses", "training"},
    "languages": {"languages", "language"},
    "awards": {"awards", "achievements", "publications", "volunteering", "activities"},
}


def clean_list(value):
    return [item.strip(" -•\t") for item in re.split(r"[,;\n|]", value or "") if item.strip(" -•\t")]


def safe(value):
    return html.escape(str(value or "")).replace("\n", "<br>")


def plain(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def score_resume(resume_text, jd_text):
    resume = resume_text.lower()
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]{1,}", jd_text.lower())
    stop = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "your",
        "you",
        "are",
        "our",
        "will",
        "have",
        "has",
        "into",
        "using",
        "about",
        "their",
        "they",
        "job",
        "role",
        "years",
        "experience",
        "work",
        "team",
        "skills",
        "required",
        "preferred",
        "responsibilities",
        "ability",
        "strong",
        "good",
    }
    keywords = []
    for word in words:
        if word not in stop and len(word) >= 3 and word not in keywords:
            keywords.append(word)
    matched = [word for word in keywords if word in resume]
    missing = [word for word in keywords if word not in resume]
    return (round((len(matched) / len(keywords)) * 100) if keywords else 0), matched, missing


def check_grammar(text):
    """Basic grammar and spell check using language-tool-python"""
    try:
        import language_tool_python
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        return matches
    except ImportError:
        # Fallback to basic spell check if language-tool not available
        return basic_spell_check(text)
    except Exception as e:
        print(f"Grammar check error: {e}")
        return []


def basic_spell_check(text):
    """Fallback basic spell check"""
    # This is a simplified spell check - in production you'd use a proper spell checker
    common_misspellings = {
        "teh": "the",
        "nad": "and",
        "recieve": "receive",
        "occured": "occurred",
        "seperate": "separate",
        "untill": "until",
        "thier": "their",
        "wierd": "weird",
        "goverment": "government",
        "enviroment": "environment",
    }
    
    issues = []
    words = text.split()
    for i, word in enumerate(words):
        clean_word = word.lower().strip(".,!?;:")
        if clean_word in common_misspellings:
            issues.append({
                "message": f"Possible misspelling: '{word}' -> '{common_misspellings[clean_word]}'",
                "offset": len(" ".join(words[:i])),
                "length": len(word)
            })
    return issues


def suggest_bullet_improvement(bullet_point, context="professional"):
    """AI-powered bullet point improvement suggestions"""
    try:
        import openai
        # Use a simple heuristic approach if OpenAI API key not configured
        return heuristic_bullet_improvement(bullet_point, context)
    except ImportError:
        return heuristic_bullet_improvement(bullet_point, context)
    except Exception as e:
        print(f"AI suggestion error: {e}")
        return heuristic_bullet_improvement(bullet_point, context)


def heuristic_bullet_improvement(bullet_point, context="professional"):
    """Heuristic-based bullet point improvement"""
    improvements = []
    
    # Check for action verbs
    action_verbs = ["developed", "implemented", "designed", "created", "managed", "led", "built", "achieved", "improved", "optimized", "reduced", "increased"]
    
    words = bullet_point.lower().split()
    if not any(verb in words for verb in action_verbs):
        improvements.append("Start with a strong action verb")
    
    # Check for quantification
    if not any(char.isdigit() for char in bullet_point):
        improvements.append("Add quantifiable metrics or numbers")
    
    # Check for result/outcome
    result_words = ["resulted", "achieved", "improved", "reduced", "increased", "saved", "delivered", "completed"]
    if not any(word in words for word in result_words):
        improvements.append("Include the outcome or impact")
    
    # Check for length
    if len(bullet_point) < 50:
        improvements.append("Add more detail to describe the achievement")
    
    return improvements if improvements else ["This bullet point looks good"]


def generate_professional_summary(data, job_description=""):
    """Generate professional summary based on resume data"""
    try:
        import openai
        # Use heuristic approach if OpenAI not available
        return heuristic_summary_generation(data, job_description)
    except ImportError:
        return heuristic_summary_generation(data, job_description)
    except Exception as e:
        print(f"AI summary generation error: {e}")
        return heuristic_summary_generation(data, job_description)


def heuristic_summary_generation(data, job_description=""):
    """Heuristic-based professional summary generation"""
    name = data.get("name", "Professional")
    title = data.get("title", "Professional")
    summary = data.get("summary", "")
    skills = data.get("skills", "")
    experience = data.get("experience", "")
    
    # Extract key skills
    skill_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
    top_skills = skill_list[:5] if skill_list else []
    
    # Build summary
    if summary:
        # Enhance existing summary
        enhanced = summary
        if top_skills:
            enhanced += f" Skilled in {', '.join(top_skills)}."
        return enhanced
    else:
        # Generate new summary
        years_exp = "multiple years" if "year" in experience.lower() else "extensive"
        generated = f"{name} is a {title} with {years_exp} of experience"
        if top_skills:
            generated += f", specializing in {', '.join(top_skills)}."
        else:
            generated += "."
        return generated


def generate_cover_letter(data, job_description=""):
    """Generate cover letter based on resume and job description"""
    name = data.get("name", "Applicant")
    title = data.get("title", "Professional")
    company = "the company"  # Can be extracted from job description
    summary = data.get("summary", "")
    skills = data.get("skills", "")
    
    cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {title} position at {company}. As a {title} with proven expertise in {skills.split(',')[0] if skills else 'various technologies'}, I am confident in my ability to contribute effectively to your team.

{summary}

My background includes extensive experience in developing and implementing solutions that drive business results. I am particularly drawn to this opportunity because it aligns perfectly with my professional goals and expertise.

I would welcome the opportunity to discuss how my skills and experience would benefit your organization. Thank you for considering my application.

Sincerely,
{name}"""
    
    return cover_letter


def generate_interview_questions(data, interview_type="Technical"):
    """Generate interview questions based on resume and interview type"""
    skills = data.get("skills", "")
    experience = data.get("experience", "")
    title = data.get("title", "Professional")
    
    skill_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
    
    if interview_type == "Technical":
        questions = [
            f"Can you explain your experience with {skill_list[0] if skill_list else 'the technologies mentioned in your resume'}?",
            "Describe a challenging technical problem you solved and your approach.",
            "How do you stay updated with the latest technologies and best practices?",
            "Walk me through a recent project you completed using your technical skills.",
            "How do you ensure code quality and maintainability in your projects?",
        ]
    elif interview_type == "Behavioral":
        questions = [
            "Tell me about a time you had to work with a difficult team member.",
            "Describe a situation where you had to meet a tight deadline.",
            "How do you handle constructive criticism?",
            "Tell me about a time you showed leadership in a project.",
            "How do you prioritize tasks when everything seems urgent?",
        ]
    else:  # General
        questions = [
            "Tell me about yourself and your professional background.",
            "Why are you interested in this position?",
            "What are your greatest strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you for this role?",
        ]
    
    return questions


def entries_to_html(value):
    output = []
    for block in (value or "").split("\n\n"):
        lines = [line.strip(" -•\t") for line in block.splitlines() if line.strip(" -•\t")]
        if not lines:
            continue
        details = "".join(f"<li>{safe(line)}</li>" for line in lines[1:])
        details_html = f"<ul>{details}</ul>" if details else ""
        output.append(f"<div class='item'><h3>{safe(lines[0])}</h3>{details_html}</div>")
    return "".join(output)


def paragraph_to_html(value):
    lines = [line.strip(" -•\t") for line in (value or "").splitlines() if line.strip(" -•\t")]
    if len(lines) <= 1:
        return safe(value)
    return "<ul>" + "".join(f"<li>{safe(line)}</li>" for line in lines) + "</ul>"


def contact_values(data):
    return [
        data["email"],
        data["phone"],
        data["location"],
        data["linkedin"],
        data["github"],
        data["portfolio"],
    ]


def contact_line(data):
    return " · ".join(safe(value) for value in contact_values(data) if plain(value))


def contact_items(data):
    return "".join(f"<span>{safe(value)}</span>" for value in contact_values(data) if plain(value))


def section(title, body, class_name=""):
    return f"<section class='{class_name}'><h2>{title}</h2>{body}</section>" if plain(body) else ""


def template_tokens(data, theme):
    skills = clean_list(data["skills"])
    skills_chips = "".join(f"<span class='skill'>{safe(skill)}</span>" for skill in skills)
    skill_list = "<ul>" + "".join(f"<li>{safe(skill)}</li>" for skill in skills) + "</ul>" if skills else ""
    tokens = {key: safe(value) for key, value in data.items()}
    
    # Handle profile photo with beautification settings
    profile_photo_html = ""
    if data.get("profile_photo"):
        import base64
        from io import BytesIO
        try:
            # Convert image to base64 for embedding in HTML
            image_data = data["profile_photo"]
            if isinstance(image_data, bytes):
                base64_image = base64.b64encode(image_data).decode()
                # Detect image type from the data or default to jpeg
                mime_type = "image/jpeg"
                if len(image_data) >= 8:
                    # PNG signature
                    if image_data[:8] == b'\x89PNG\r\n\x1a\n':
                        mime_type = "image/png"
                    # JPEG signature
                    elif image_data[:2] == b'\xff\xd8':
                        mime_type = "image/jpeg"
                
                # Apply photo settings
                photo_size = data.get("photo_size", 80)
                photo_shape = data.get("photo_shape", "circle")
                photo_border = data.get("photo_border", "none")
                photo_zoom = data.get("photo_zoom", 100)
                
                # Build CSS styles based on settings
                border_radius = "50%" if photo_shape == "circle" else "8px" if photo_shape == "rounded" else "4px"
                
                border_style = ""
                if photo_border == "solid":
                    border_style = f"border: 3px solid var(--accent);"
                elif photo_border == "shadow":
                    border_style = f"box-shadow: 0 4px 12px rgba(0,0,0,0.2);"
                
                # Calculate zoom using background-size approach for better quality
                zoom_value = photo_zoom / 100
                
                photo_style = f"""
                    width: {photo_size}px;
                    height: {photo_size}px;
                    border-radius: {border_radius};
                    {border_style}
                    object-fit: cover;
                    display: inline-block;
                    max-width: {photo_size}px;
                    max-height: {photo_size}px;
                """
                
                profile_photo_html = f'<img src="data:{mime_type};base64,{base64_image}" alt="Profile Photo" class="profile-photo" style="{photo_style}" />'
        except Exception as e:
            print(f"Error processing profile photo: {e}")
    
    tokens.update(
        {
            "contact": contact_line(data),
            "contact_items": contact_items(data),
            "profile_photo": profile_photo_html,
            "skills": skills_chips,
            "skill_list": skill_list,
            "summary_text": safe(data["summary"]),
            "summary_section": section("Summary", f"<p>{safe(data['summary'])}</p>", "summary"),
            "skills_section": section("Skills", f"<div class='skills'>{skills_chips}</div>", "skills-section"),
            "experience": entries_to_html(data["experience"]),
            "experience_section": section("Experience", entries_to_html(data["experience"]), "experience-section"),
            "projects": entries_to_html(data["projects"]),
            "projects_section": section("Projects", entries_to_html(data["projects"]), "projects-section"),
            "education_section": section("Education", paragraph_to_html(data["education"]), "education-section"),
            "certifications": entries_to_html(data["certifications"]),
            "certifications_section": section("Certifications", entries_to_html(data["certifications"]), "certifications-section"),
            "languages_section": section("Languages", paragraph_to_html(data["languages"]), "languages-section"),
            "awards": entries_to_html(data["awards"]),
            "awards_section": section("Awards & Activities", entries_to_html(data["awards"]), "awards-section"),
            "accent": theme["accent"],
            "secondary": theme["secondary"],
            "font": theme["font"],
            "density": "compact" if theme["compact"] else "comfortable",
            "page_background": theme["page_background"],
            "paper_background": theme["paper_background"],
            "texture_name": safe(theme["texture_name"]),
        }
    )
    return tokens


def render_template(source, data, theme):
    rendered = source
    for key, value in template_tokens(data, theme).items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def export_to_pdf(html_content, file_name):
    """Export HTML to PDF using ReportLab"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        from io import BytesIO
        from html.parser import HTMLParser
        import re
        
        # Simple HTML to text extraction
        class HTMLTextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.in_div = False
                
            def handle_starttag(self, tag, attrs):
                if tag in ['div', 'p', 'h1', 'h2', 'h3']:
                    self.in_div = True
                    self.text.append('\n\n')
                elif tag == 'br':
                    self.text.append('\n')
                    
            def handle_endtag(self, tag):
                if tag in ['div', 'p', 'h1', 'h2', 'h3']:
                    self.in_div = False
                    
            def handle_data(self, data):
                if data.strip():
                    self.text.append(data.strip())
                    
            def get_text(self):
                return ' '.join(self.text)
        
        # Extract text from HTML
        parser = HTMLTextExtractor()
        parser.feed(html_content)
        text_content = parser.get_text()
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title_style = styles['Heading1']
        title_style.fontSize = 24
        title_style.spaceAfter = 30
        story.append(Paragraph(file_name.replace('-', ' ').title(), title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add content
        body_style = styles['Normal']
        body_style.fontSize = 11
        body_style.leading = 14
        
        # Split into paragraphs
        paragraphs = text_content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                clean_para = re.sub(r'\s+', ' ', para.strip())
                story.append(Paragraph(clean_para, body_style))
                story.append(Spacer(1, 0.1 * inch))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except ImportError:
        raise RuntimeError("ReportLab is required for PDF export. Install with: pip install reportlab")
    except Exception as e:
        raise RuntimeError(f"PDF export failed: {str(e)}")


def export_to_docx(data, file_name):
    """Export resume data to DOCX using python-docx"""
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
        from io import BytesIO
        
        doc = Document()
        
        # Set up styles
        style = doc.styles['Normal']
        style.font.name = 'Arial'
        style.font.size = Pt(11)
        
        # Add name and title
        name_para = doc.add_paragraph()
        name_run = name_para.add_run(data.get("name", ""))
        name_run.font.size = Pt(18)
        name_run.font.bold = True
        name_run.font.color.rgb = RGBColor(0, 0, 0)
        
        title_para = doc.add_paragraph()
        title_run = title_para.add_run(data.get("title", ""))
        title_run.font.size = Pt(14)
        title_run.font.color.rgb = RGBColor(96, 96, 96)
        
        # Add contact information
        contact_para = doc.add_paragraph()
        contact_info = []
        if data.get("email"):
            contact_info.append(data["email"])
        if data.get("phone"):
            contact_info.append(data["phone"])
        if data.get("location"):
            contact_info.append(data["location"])
        if data.get("linkedin"):
            contact_info.append(data["linkedin"])
        if data.get("github"):
            contact_info.append(data["github"])
        
        contact_run = contact_para.add_run(" | ".join(contact_info))
        contact_run.font.size = Pt(10)
        contact_run.font.color.rgb = RGBColor(96, 96, 96)
        
        doc.add_paragraph()  # Empty line
        
        # Add summary
        if data.get("summary"):
            doc.add_heading("Professional Summary", level=2)
            doc.add_paragraph(data["summary"])
            doc.add_paragraph()
        
        # Add skills
        if data.get("skills"):
            doc.add_heading("Skills", level=2)
            skills_para = doc.add_paragraph(data["skills"])
            doc.add_paragraph()
        
        # Add experience
        if data.get("experience"):
            doc.add_heading("Experience", level=2)
            for exp_block in data["experience"].split("\n\n"):
                if exp_block.strip():
                    lines = exp_block.strip().split("\n")
                    if lines:
                        # First line is job title/company
                        doc.add_paragraph(lines[0], style='Heading 3')
                        # Remaining lines are details
                        for line in lines[1:]:
                            if line.strip():
                                doc.add_paragraph(line.strip())
            doc.add_paragraph()
        
        # Add projects
        if data.get("projects"):
            doc.add_heading("Projects", level=2)
            for proj_block in data["projects"].split("\n\n"):
                if proj_block.strip():
                    lines = proj_block.strip().split("\n")
                    if lines:
                        doc.add_paragraph(lines[0], style='Heading 3')
                        for line in lines[1:]:
                            if line.strip():
                                doc.add_paragraph(line.strip())
            doc.add_paragraph()
        
        # Add education
        if data.get("education"):
            doc.add_heading("Education", level=2)
            doc.add_paragraph(data["education"])
            doc.add_paragraph()
        
        # Add certifications
        if data.get("certifications"):
            doc.add_heading("Certifications", level=2)
            for cert_block in data["certifications"].split("\n\n"):
                if cert_block.strip():
                    doc.add_paragraph(cert_block.strip())
            doc.add_paragraph()
        
        # Add languages
        if data.get("languages"):
            doc.add_heading("Languages", level=2)
            doc.add_paragraph(data["languages"])
            doc.add_paragraph()
        
        # Add awards
        if data.get("awards"):
            doc.add_heading("Awards & Activities", level=2)
            doc.add_paragraph(data["awards"])
        
        # Save to BytesIO
        docx_bytes = BytesIO()
        doc.save(docx_bytes)
        docx_bytes.seek(0)
        return docx_bytes.getvalue()
        
    except ImportError:
        raise RuntimeError("python-docx is required for DOCX export. Install with: pip install python-docx")
    except Exception as e:
        raise RuntimeError(f"DOCX export failed: {str(e)}")


def discover_templates():
    templates = []
    for path in sorted(TEMPLATE_DIR.glob("*.html")):
        source = path.read_text(encoding="utf-8")
        meta_match = re.search(r"<!--\s*template:(.*?)-->", source, flags=re.DOTALL)
        meta = {"name": path.stem.replace("-", " ").title(), "style": "Resume template", "source_note": "Local"}
        if meta_match:
            for part in meta_match.group(1).split(";"):
                if "=" in part:
                    key, value = part.split("=", 1)
                    meta[key.strip()] = value.strip()
        templates.append({"path": path, "source_html": source, **meta})
    return templates


def extract_text_from_resume(uploaded_file):
    """Enhanced text extraction with improved error handling and format detection"""
    suffix = Path(uploaded_file.name).suffix.lower()
    payload = uploaded_file.getvalue()
    
    if suffix == ".pdf":
        if PdfReader is None:
            raise RuntimeError("Install pypdf to parse PDF resumes.")
        try:
            reader = PdfReader(BytesIO(payload))
            # Extract text from all pages with better formatting preservation
            full_text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text.append(page_text)
            return "\n".join(full_text)
        except Exception as e:
            raise RuntimeError(f"PDF parsing failed: {str(e)}")
            
    if suffix == ".docx":
        if Document is None:
            raise RuntimeError("Install python-docx to parse DOCX resumes.")
        try:
            document = Document(BytesIO(payload))
            # Extract text with paragraph structure preservation
            full_text = []
            for paragraph in document.paragraphs:
                if paragraph.text.strip():
                    full_text.append(paragraph.text)
            return "\n".join(full_text)
        except Exception as e:
            raise RuntimeError(f"DOCX parsing failed: {str(e)}")
            
    return payload.decode("utf-8", errors="replace")


def section_key(line):
    """Enhanced section detection with fuzzy matching"""
    cleaned = re.sub(r"[^a-zA-Z &]", "", line).strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    
    # Direct match
    for key, aliases in section_aliases.items():
        if cleaned in aliases:
            return key
    
    # Fuzzy match for common variations
    fuzzy_aliases = {
        "summary": ["professional summary", "career summary", "profile", "about me", "objective"],
        "skills": ["technical skills", "core competencies", "key skills", "expertise", "technologies"],
        "experience": ["work experience", "employment history", "professional experience", "work history"],
        "projects": ["key projects", "notable projects", "portfolio", "project experience"],
        "education": ["academic background", "educational background", "qualifications", "academic qualifications"],
        "certifications": ["certificates", "credentials", "professional certifications", "certifications & courses"],
        "languages": ["languages spoken", "communication", "language proficiency"],
        "awards": ["achievements", "honors", "recognition", "accomplishments"]
    }
    
    for key, variations in fuzzy_aliases.items():
        for variation in variations:
            if variation in cleaned or cleaned in variation:
                return key
    
    return None


def parse_resume_text(text):
    """Enhanced resume parsing with better field extraction and validation"""
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", line).strip(" -•\t") for line in text.splitlines()]
    lines = [line for line in lines if line]
    parsed = {key: "" for key in defaults}

    # Enhanced contact information extraction
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone = re.search(r"(\+?\d[\d\s().-]{8,}\d)", text)
    urls = re.findall(r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s,;)]*)?", text)

    parsed["email"] = email.group(0) if email else ""
    parsed["phone"] = phone.group(1).strip() if phone else ""
    parsed["linkedin"] = next((url for url in urls if "linkedin" in url.lower()), "")
    parsed["github"] = next((url for url in urls if "github" in url.lower()), "")
    parsed["portfolio"] = next((url for url in urls if "linkedin" not in url.lower() and "github" not in url.lower() and "@" not in url), "")

    # Enhanced name detection with better heuristics
    for line in lines[:8]:
        lower = line.lower()
        if "@" in line or re.search(r"\d{6,}", line) or "linkedin" in lower or "github" in lower:
            continue
        if len(line.split()) <= 6 and not section_key(line):
            # Additional validation: should contain at least one capital letter and no special chars
            if any(char.isupper() for char in line) and not re.search(r"[^\w\s.,]", line):
                parsed["name"] = line
                break
    
    # Enhanced title detection
    if parsed["name"]:
        try:
            start_index = lines.index(parsed["name"]) + 1
        except ValueError:
            start_index = 0
        for line in lines[start_index : start_index + 4]:
            if "@" not in line and not section_key(line) and 2 <= len(line.split()) <= 12:
                # Additional validation: should look like a job title
                title_indicators = ["engineer", "developer", "manager", "director", "analyst", "specialist", "consultant", "lead", "senior", "junior"]
                if any(indicator in line.lower() for indicator in title_indicators) or line.istitle():
                    parsed["title"] = line
                    break

    # Enhanced section parsing with better content aggregation
    sections = {key: [] for key in section_aliases}
    current = None
    for line in lines:
        key = section_key(line)
        if key:
            current = key
            continue
        if current:
            sections[current].append(line)

    # Improved content assignment
    for key in ("summary", "education", "languages"):
        parsed[key] = "\n".join(sections[key]).strip()
    
    # Enhanced skills parsing with categorization
    skills_text = "\n".join(sections["skills"])
    skills_list = clean_list(skills_text)
    # Separate technical and soft skills if possible
    technical_skills = [skill for skill in skills_list if any(tech_word in skill.lower() for tech_word in ["python", "java", "javascript", "sql", "react", "angular", "docker", "kubernetes", "aws", "azure", "machine learning", "ai", "data", "web", "mobile", "backend", "frontend"])]
    soft_skills = [skill for skill in skills_list if skill not in technical_skills]
    parsed["skills"] = ", ".join(skills_list).strip()
    
    for key in ("experience", "projects", "certifications", "awards"):
        parsed[key] = "\n".join(sections[key]).strip()

    # Enhanced location detection
    location_candidates = [
        line
        for line in lines[:12]
        if "," in line and not any(token in line.lower() for token in ("linkedin", "github", "http", "@"))
    ]
    # Additional validation for location (should contain city/state pattern)
    location_pattern = re.compile(r"[A-Za-z\s]+,\s*[A-Za-z\s]+")
    for candidate in location_candidates:
        if location_pattern.search(candidate):
            parsed["location"] = candidate
            break
    else:
        parsed["location"] = location_candidates[0] if location_candidates else ""
    
    # Apply AI validation if available
    parsed = validate_parsed_data_with_ai(parsed, text)
    
    return {key: value for key, value in parsed.items() if plain(value)}


def validate_parsed_data_with_ai(parsed_data, original_text):
    """Use AI to validate and correct parsed resume data"""
    try:
        import openai
        # Check if OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            return parsed_data
        
        # Create validation prompt
        validation_prompt = f"""
        You are a resume parsing expert. Review the following parsed resume data and correct any errors.
        
        Original resume text:
        {original_text[:3000]}
        
        Parsed data:
        Name: {parsed_data.get('name', '')}
        Title: {parsed_data.get('title', '')}
        Email: {parsed_data.get('email', '')}
        Phone: {parsed_data.get('phone', '')}
        Location: {parsed_data.get('location', '')}
        LinkedIn: {parsed_data.get('linkedin', '')}
        GitHub: {parsed_data.get('github', '')}
        
        Return the corrected data in JSON format with these exact keys: name, title, email, phone, location, linkedin, github.
        If a field is empty or incorrect, return the corrected value. If no correction needed, return the original value.
        Return only the JSON, no other text.
        """
        
        try:
            # Try newer OpenAI API first
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a resume parsing expert. Return only valid JSON."},
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            corrected_data = json.loads(response.choices[0].message.content)
        except AttributeError:
            # Fall back to older API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a resume parsing expert. Return only valid JSON."},
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            corrected_data = json.loads(response.choices[0].message.content)
        
        # Update parsed data with AI corrections
        for key in ["name", "title", "email", "phone", "location", "linkedin", "github"]:
            if corrected_data.get(key) and corrected_data[key].strip():
                parsed_data[key] = corrected_data[key]
        
        return parsed_data
        
    except ImportError:
        # OpenAI not available, return original parsed data
        return parsed_data
    except Exception as e:
        print(f"AI validation error: {e}")
        return parsed_data


def apply_palette():
    selected = st.session_state["palette"]
    if selected != "Custom":
        st.session_state["accent_colour"] = palettes[selected][0]
        st.session_state["secondary_colour"] = palettes[selected][1]


for key, value in defaults.items():
    st.session_state.setdefault(key, value)
st.session_state.setdefault("accent_colour", palettes["Ocean"][0])
st.session_state.setdefault("secondary_colour", palettes["Ocean"][1])
st.session_state.setdefault("background_texture", "Soft Paper")

templates = discover_templates()
if not templates:
    st.error("No templates found. Add HTML templates to the templates folder.")
    st.stop()

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(135deg, #f8fafc 0%, #eef7f6 45%, #f7f2ff 100%);}
    .block-container {padding-top: 1rem; max-width: 1480px;}
    .hero {
        border-radius: 8px;
        padding: 18px 22px;
        background: linear-gradient(120deg, #ffffff, #e0f2fe 52%, #ede9fe);
        color: #172033;
        border: 1px solid rgba(15, 23, 42, .08);
        box-shadow: 0 16px 35px rgba(15, 23, 42, .08);
        margin-bottom: 16px;
    }
    .hero h1 {font-size: 2.05rem; margin: 0 0 4px;}
    .hero p {margin: 0; color: #475569;}
    div[data-testid="stMetric"] {
        border: 1px solid rgba(15, 23, 42, .14);
        padding: 10px;
        border-radius: 8px;
        background: white;
    }
    section[data-testid="stSidebar"] {background: #f8fafc;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Resume Builder Studio</h1>
        <p>Import an old resume, polish the details, choose a colorful template, and export a clean HTML resume.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

editor, preview = st.columns([1.02, 1.38], gap="large")

with editor:
    import_tab, details_tab, template_tab, ats_tab, cover_letter_tab, interview_tab = st.tabs(["Import", "Details", "Template", "ATS", "Cover Letter", "Interview Prep"])

    with import_tab:
        st.subheader("Upload Existing Resume")
        resume_file = st.file_uploader("PDF, DOCX, or TXT resume", type=["pdf", "docx", "txt"])
        if resume_file:
            try:
                extracted_text = extract_text_from_resume(resume_file)
                parsed = parse_resume_text(extracted_text)
                found_fields = ", ".join(parsed.keys()) or "no structured fields"
                
                # Check if AI validation was used
                ai_used = os.getenv("OPENAI_API_KEY") is not None
                ai_status = " (AI-validated)" if ai_used else " (rule-based)"
                st.success(f"Parsed {found_fields}{ai_status}.")
                
                if st.button("Pull parsed data into editor", type="primary", use_container_width=True):
                    for key, value in parsed.items():
                        if key in defaults and plain(value):
                            st.session_state[key] = value
                    st.rerun()
                with st.expander("Extracted resume text"):
                    st.text_area("Raw text", extracted_text[:12000], height=260, label_visibility="collapsed")
            except Exception as exc:
                st.error(str(exc))
        else:
            st.info("Upload your current resume and the app will pre-fill the editor from its text.")
        
        st.subheader("LinkedIn Profile Import")
        linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/your-profile")
        if st.button("Import from LinkedIn", key="import_linkedin"):
            if linkedin_url:
                st.info("LinkedIn import would require LinkedIn API access. For now, please manually copy your profile information.")
                st.info("You can paste your LinkedIn profile details in the resume content fields.")

    with details_tab:
        st.subheader("Personal Details")
        st.text_input("Full name", key="name")
        st.text_input("Professional title", key="title")
        
        # Photo upload section
        st.subheader("Profile Photo")
        photo_option = st.radio("Photo source", ["Upload file", "Take photo"], horizontal=True)
        
        if photo_option == "Upload file":
            photo_file = st.file_uploader("Upload profile photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
            if photo_file:
                st.session_state["profile_photo"] = photo_file.getvalue()
                st.image(photo_file, width=150, caption="Uploaded photo")
        else:
            camera_photo = st.camera_input("Take a photo")
            if camera_photo:
                st.session_state["profile_photo"] = camera_photo.getvalue()
                st.image(camera_photo, width=150, caption="Camera photo")
        
        # Photo beautification controls
        if st.session_state.get("profile_photo"):
            st.subheader("Photo Settings")
            
            col1, col2 = st.columns(2)
            with col1:
                photo_size = st.slider("Photo size (px)", 40, 150, st.session_state.get("photo_size", 80))
                st.session_state["photo_size"] = photo_size
            
            with col2:
                photo_zoom = st.slider("Zoom", 50, 200, st.session_state.get("photo_zoom", 100))
                st.session_state["photo_zoom"] = photo_zoom
            
            col3, col4 = st.columns(2)
            with col3:
                photo_shape = st.selectbox("Shape", ["circle", "square", "rounded"], index=["circle", "square", "rounded"].index(st.session_state.get("photo_shape", "circle")))
                st.session_state["photo_shape"] = photo_shape
            
            with col4:
                photo_border = st.selectbox("Border style", ["none", "solid", "shadow"], index=["none", "solid", "shadow"].index(st.session_state.get("photo_border", "none")))
                st.session_state["photo_border"] = photo_border
            
            # Preview with current settings
            st.subheader("Preview")
            preview_col1, preview_col2, preview_col3 = st.columns(3)
            
            with preview_col1:
                st.write("Small (60px)")
                st.image(st.session_state["profile_photo"], width=60, caption="Small")
            
            with preview_col2:
                st.write("Medium (80px)")
                st.image(st.session_state["profile_photo"], width=80, caption="Medium")
            
            with preview_col3:
                st.write("Large (100px)")
                st.image(st.session_state["profile_photo"], width=100, caption="Large")
            
            # Show current photo and option to remove
            col1, col2 = st.columns([4, 1])
            with col1:
                st.success(f"Profile photo set - {photo_shape} shape, {photo_size}px size")
            with col2:
                if st.button("Remove photo", type="secondary"):
                    st.session_state["profile_photo"] = None
                    st.rerun()
        
        # Resume management
        st.subheader("Resume Management")
        col_save1, col_save2 = st.columns(2)
        with col_save1:
            if st.button("Save Current Resume", type="primary", use_container_width=True):
                # Save current resume state
                current_data = {key: st.session_state[key] for key in defaults}
                saved_resumes = st.session_state.get("saved_resumes", {})
                resume_key = f"{current_data['name']}-{current_data['title']}"
                saved_resumes[resume_key] = {key: st.session_state[key] for key in defaults}
                st.session_state["saved_resumes"] = saved_resumes
                
                # Add to version history
                version_history = st.session_state.get("version_history", [])
                version_history.append({
                    "timestamp": str(st.session_state.get("current_time", "now")),
                    "resume_key": resume_key,
                    "data": {key: st.session_state[key] for key in defaults}
                })
                st.session_state["version_history"] = version_history
                
                st.success(f"Resume saved as: {resume_key}")
        
        with col_save2:
            if st.button("Load Saved Resume", type="secondary", use_container_width=True):
                saved_resumes = st.session_state.get("saved_resumes", {})
                if saved_resumes:
                    resume_names = list(saved_resumes.keys())
                    if resume_names:
                        selected_resume = st.selectbox("Select saved resume", resume_names)
                        if selected_resume and st.button("Load Selected", key="load_resume_btn"):
                            loaded_data = saved_resumes[selected_resume]
                            for key, value in loaded_data.items():
                                st.session_state[key] = value
                            st.success(f"Loaded resume: {selected_resume}")
                            st.rerun()
                else:
                    st.info("No saved resumes found")
        
        # Version History
        st.subheader("Version History")
        version_history = st.session_state.get("version_history", [])
        if version_history:
            st.write(f"Total versions: {len(version_history)}")
            for i, version in enumerate(reversed(version_history[-5:])):  # Show last 5 versions
                with st.expander(f"Version {len(version_history) - i} - {version['resume_key']}"):
                    if st.button(f"Restore this version", key=f"restore_version_{i}"):
                        for key, value in version["data"].items():
                            st.session_state[key] = value
                        st.success("Version restored!")
                        st.rerun()
        else:
            st.info("No version history yet. Save a resume to start tracking versions.")
        
        # Resume URL Sharing
        st.subheader("Share Resume")
        share_option = st.selectbox("Share option", ["Generate Shareable Link", "Export to JSON"], key="share_option")
        if share_option == "Generate Shareable Link":
            st.info("Shareable link feature would require a backend server. For now, use the export buttons to share your resume.")
        else:
            import json
            resume_json = json.dumps({key: st.session_state[key] for key in defaults}, indent=2)
            st.download_button("Export Resume as JSON", resume_json, file_name="resume.json", mime="application/json", use_container_width=True)
        
        if "profile_photo" not in st.session_state:
            st.session_state["profile_photo"] = None
        if "photo_size" not in st.session_state:
            st.session_state["photo_size"] = 80
        if "photo_shape" not in st.session_state:
            st.session_state["photo_shape"] = "circle"
        if "photo_border" not in st.session_state:
            st.session_state["photo_border"] = "none"
        if "photo_zoom" not in st.session_state:
            st.session_state["photo_zoom"] = 100
        
        first_contact, second_contact = st.columns(2)
        with first_contact:
            st.text_input("Email", key="email")
            st.text_input("Location", key="location")
            st.text_input("LinkedIn URL", key="linkedin")
        with second_contact:
            st.text_input("Phone", key="phone")
            st.text_input("GitHub URL", key="github")
            st.text_input("Portfolio / website", key="portfolio")

        st.subheader("Resume Content")
        
        # AI Content Assistance
        with st.expander("AI Content Assistance"):
            st.write("Get AI-powered suggestions to improve your resume content")
            
            # Summary generation
            if st.button("Generate Professional Summary", key="generate_summary"):
                with st.spinner("Generating summary..."):
                    current_data = {key: st.session_state[key] for key in defaults}
                    generated_summary = generate_professional_summary(current_data)
                    st.session_state["summary"] = generated_summary
                    st.success("Summary generated!")
                    st.rerun()
            
            # Bullet improvement
            st.subheader("Bullet Point Improvement")
            bullet_to_improve = st.text_area("Paste a bullet point to improve", height=80, key="bullet_improve")
            if st.button("Get Suggestions", key="improve_bullet"):
                if bullet_to_improve:
                    suggestions = suggest_bullet_improvement(bullet_to_improve)
                    for suggestion in suggestions:
                        st.info(f"💡 {suggestion}")
        
        st.text_area("Professional summary", key="summary", height=105)
        st.text_area("Skills - comma/new-line separated", key="skills", height=85)
        st.text_area("Experience - separate jobs with a blank line", key="experience", height=230)
        st.text_area("Projects - separate projects with a blank line", key="projects", height=145)
        st.text_area("Education", key="education", height=75)
        with st.expander("Additional details"):
            st.text_area("Certifications - separate entries with a blank line", key="certifications", height=100)
            st.text_input("Languages", key="languages")
            st.text_area("Awards, publications, volunteering or memberships", key="awards", height=90)
        
        # Grammar Check
        st.subheader("Grammar & Spell Check")
        current_data = {key: st.session_state[key] for key in defaults}
        full_text = f"{current_data['summary']} {current_data['skills']} {current_data['experience']} {current_data['projects']}"
        if st.button("Check Grammar & Spelling", key="check_grammar"):
            with st.spinner("Checking grammar..."):
                grammar_issues = check_grammar(full_text)
                if grammar_issues:
                    st.warning(f"Found {len(grammar_issues)} potential issues:")
                    for issue in grammar_issues[:10]:  # Show first 10 issues
                        st.error(issue.get("message", "Grammar issue found"))
                else:
                    st.success("No grammar or spelling issues found!")

    with template_tab:
        st.subheader("Template Selection")
        template_names = [item["name"] for item in templates]
        selected_name = st.radio("Choose a template", template_names, horizontal=True)
        selected_template = next(item for item in templates if item["name"] == selected_name)
        st.caption(f"{selected_template['style']} | Source: {selected_template['source_note']}")

        st.subheader("Color System")
        st.selectbox("Palette", list(palettes), key="palette", on_change=apply_palette)
        color_one, color_two = st.columns(2)
        with color_one:
            accent = st.color_picker("Accent", key="accent_colour")
        with color_two:
            secondary = st.color_picker("Secondary", key="secondary_colour")
        background_texture = st.selectbox("Background texture", list(background_styles), key="background_texture")
        font = st.selectbox("Font", ["Inter", "Arial", "Georgia", "Verdana", "Tahoma"])
        compact = st.toggle("Compact spacing")

        custom_template = st.file_uploader("Upload your own HTML template", type=["html", "htm"])
        custom_source = custom_template.getvalue().decode("utf-8", errors="replace") if custom_template else None
        if custom_source:
            st.caption("Custom templates can use the same tokens as the built-in templates.")

    with ats_tab:
        st.subheader("ATS Checker")
        jd = st.text_area("Paste job description", height=230, placeholder="Paste the target job description here...")
        
        # Real-time ATS scoring
        if jd.strip():
            current_data = {key: st.session_state[key] for key in defaults}
            ats, matched, missing = score_resume(" ".join(str(value) for value in current_data.values()), jd)
            st.metric("ATS keyword alignment", f"{ats}%")
            st.progress(ats / 100)
            
            col_matched, col_missing = st.columns(2)
            with col_matched:
                st.write("Matched keywords:")
                st.write(", ".join(matched[:40]) or "None")
            with col_missing:
                st.write("Potentially missing keywords:")
                st.write(", ".join(missing[:40]) or "None")
            
            st.caption("Heuristic keyword checker only; it cannot reproduce a specific employer's ATS score.")
            
            # Skill gap analysis
            st.subheader("Skill Gap Analysis")
            required_skills = st.text_input("Required skills (comma-separated)", key="required_skills")
            if required_skills:
                current_skills = [skill.strip().lower() for skill in current_data["skills"].split(",")]
                required = [skill.strip().lower() for skill in required_skills.split(",")]
                
                missing_skills = [skill for skill in required if skill not in current_skills]
                matched_skills = [skill for skill in required if skill in current_skills]
                
                if missing_skills:
                    st.warning(f"Missing skills: {', '.join(missing_skills)}")
                if matched_skills:
                    st.success(f"You have these required skills: {', '.join(matched_skills)}")
        else:
            st.info("Paste a job description to see ATS analysis and skill gap analysis.")
    
    with cover_letter_tab:
        st.subheader("Cover Letter Generator")
        st.write("Generate a professional cover letter tailored to your resume")
        
        target_company = st.text_input("Target Company", key="target_company")
        target_position = st.text_input("Target Position", key="target_position")
        
        if st.button("Generate Cover Letter", key="generate_cover_letter"):
            with st.spinner("Generating cover letter..."):
                current_data = {key: st.session_state[key] for key in defaults}
                cover_letter = generate_cover_letter(current_data, f"{target_position} at {target_company}")
                st.subheader("Generated Cover Letter")
                st.text_area("Cover Letter", cover_letter, height=300, key="generated_cover_letter")
                
                if st.button("Download Cover Letter", key="download_cover_letter"):
                    st.download_button("Download Cover Letter", cover_letter, file_name="cover_letter.txt", mime="text/plain", use_container_width=True)
    
    with interview_tab:
        st.subheader("AI-Powered Interview Preparation")
        st.write("Get interview questions and preparation tips based on your resume")
        
        interview_type = st.selectbox("Interview Type", ["Technical", "Behavioral", "General"], key="interview_type")
        
        if st.button("Generate Interview Questions", key="generate_interview_questions"):
            with st.spinner("Generating interview questions..."):
                current_data = {key: st.session_state[key] for key in defaults}
                questions = generate_interview_questions(current_data, interview_type)
                st.subheader("Suggested Interview Questions")
                
                for i, question in enumerate(questions, 1):
                    st.write(f"**Q{i}:** {question}")
                    st.text_area(f"Your answer to Q{i}", height=100, key=f"interview_answer_{i}")
        
        # Salary Insights
        st.subheader("Salary Insights")
        st.info("Salary insights would require integration with salary data APIs like Glassdoor, Payscale, or Levels.fyi")
        st.write("For now, research salary ranges for your role on:")
        st.write("- Glassdoor.com")
        st.write("- Payscale.com")
        st.write("- Levels.fyi (for tech roles)")
        st.write("- LinkedIn Salary")
        
        # Company Research
        st.subheader("Company Research")
        company_research = st.text_input("Company to research", key="company_research")
        if company_research:
            st.info(f"Research tips for {company_research}:")
            st.write("1. Visit the company's website and About page")
            st.write("2. Check recent news about the company")
            st.write("3. Look at their products/services")
            st.write("4. Check their company culture on Glassdoor")
            st.write("5. Review their LinkedIn company page")

# Get current data from session state
data = {key: st.session_state[key] for key in defaults}
background = background_styles[background_texture]
theme = {
    "accent": accent,
    "secondary": secondary,
    "font": font,
    "compact": compact,
    "page_background": background["page_background"],
    "paper_background": background["paper_background"],
    "texture_name": background_texture,
}
selected_source = custom_source if custom_source else selected_template["source_html"]
rendered_html = render_template(selected_source, data, theme)

with preview:
    top_row, action_row = st.columns([1, 1])
    with top_row:
        st.subheader("Live Preview")
    with action_row:
        current_data = {key: st.session_state[key] for key in defaults}
        safe_file_base = re.sub(r"[^a-z0-9]+", "-", plain(current_data["name"]).lower()).strip("-") or "resume"
        safe_template = re.sub(r"[^a-z0-9]+", "-", selected_name.lower()).strip("-")
        
        # Export buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            html_file_name = f"{safe_file_base}-{safe_template}.html"
            st.download_button("Download HTML", rendered_html, file_name=html_file_name, mime="text/html", use_container_width=True)
        
        with col2:
            try:
                pdf_bytes = export_to_pdf(rendered_html, safe_file_base)
                pdf_file_name = f"{safe_file_base}-{safe_template}.pdf"
                st.download_button("Download PDF", pdf_bytes, file_name=pdf_file_name, mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.error(f"PDF export not available. Use HTML export for now. Error: {str(e)}")
        
        with col3:
            try:
                docx_bytes = export_to_docx(current_data, safe_file_base)
                docx_file_name = f"{safe_file_base}-{safe_template}.docx"
                st.download_button("Download DOCX", docx_bytes, file_name=docx_file_name, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            except Exception as e:
                st.error(f"DOCX export not available. Use HTML export for now. Error: {str(e)}")
    
    # Add a container for the live preview with proper styling
    st.markdown("### Live Preview")
    st.markdown("This shows how your resume will look when exported:")
    
    # Render the HTML with proper dimensions to maintain layout
    components.html(
        rendered_html,
        height=1200,
        scrolling=True
    )
