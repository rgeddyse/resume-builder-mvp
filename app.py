import html
import re
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
    "name": "Rameshkrishnan Geddy Sekar",
    "title": "Senior Python Engineer | AI/ML Integration | Automation",
    "email": "your.email@example.com",
    "phone": "+91 XXXXX XXXXX",
    "location": "Bangalore, India",
    "linkedin": "linkedin.com/in/your-profile",
    "github": "github.com/your-profile",
    "portfolio": "portfolio.example.com",
    "summary": "Senior automation engineer with 15+ years of experience building Python automation, CI/CD, OS validation and AI-accelerated testing solutions.",
    "skills": "Python, Playwright, Selenium, Pytest, BDD, GitHub Actions, Jenkins, Docker, Kubernetes, Linux, QEMU, AI/ML",
    "experience": "Senior Principal Engineer — Dell Technologies\nBangalore, India | 2025 – Present\nArchitected E2E automation frameworks for ThinOS and integrated AI-assisted engineering workflows.\n\nSenior Automation Engineer\nCompany | Location | Dates\nBuilt scalable automation frameworks, CI/CD pipelines and system validation solutions.",
    "projects": "AI-Accelerated Automation Framework\nPython-based E2E framework integrating AI agents, device control and validation.\n\nOS Provisioning & Validation\nAutomated ISO/RAW image provisioning, PXE workflows and system-level validation.",
    "education": "Bachelor's Degree — Computer Science / Engineering",
    "certifications": "Certification Name — Issuer | Year",
    "languages": "English (Professional), Tamil (Native)",
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
        "page_background": "background: linear-gradient(135deg, #f8fafc, #eef7f6);",
        "paper_background": "background: #ffffff;",
    },
    "Fine Grid": {
        "page_background": "background-color: #f8fafc; background-image: linear-gradient(rgba(15,23,42,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(15,23,42,.045) 1px, transparent 1px); background-size: 22px 22px;",
        "paper_background": "background: #ffffff;",
    },
    "Warm Dots": {
        "page_background": "background-color: #fff7ed; background-image: radial-gradient(rgba(180,83,9,.14) 1px, transparent 1px); background-size: 18px 18px;",
        "paper_background": "background: #fffdf9;",
    },
    "Cool Linen": {
        "page_background": "background-color: #eef7ff; background-image: linear-gradient(45deg, rgba(37,99,235,.06) 25%, transparent 25%), linear-gradient(-45deg, rgba(6,182,212,.06) 25%, transparent 25%); background-size: 24px 24px;",
        "paper_background": "background: #ffffff;",
    },
    "Lavender Wash": {
        "page_background": "background: radial-gradient(circle at 12% 18%, rgba(168,85,247,.18), transparent 30%), radial-gradient(circle at 88% 16%, rgba(6,182,212,.16), transparent 28%), linear-gradient(135deg, #faf7ff, #f0f9ff);",
        "paper_background": "background: rgba(255,255,255,.97);",
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
    tokens.update(
        {
            "contact": contact_line(data),
            "contact_items": contact_items(data),
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
    suffix = Path(uploaded_file.name).suffix.lower()
    payload = uploaded_file.getvalue()
    if suffix == ".pdf":
        if PdfReader is None:
            raise RuntimeError("Install pypdf to parse PDF resumes.")
        reader = PdfReader(BytesIO(payload))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        if Document is None:
            raise RuntimeError("Install python-docx to parse DOCX resumes.")
        document = Document(BytesIO(payload))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    return payload.decode("utf-8", errors="replace")


def section_key(line):
    cleaned = re.sub(r"[^a-zA-Z &]", "", line).strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    for key, aliases in section_aliases.items():
        if cleaned in aliases:
            return key
    return None


def parse_resume_text(text):
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", line).strip(" -•\t") for line in text.splitlines()]
    lines = [line for line in lines if line]
    parsed = {key: "" for key in defaults}

    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone = re.search(r"(\+?\d[\d\s().-]{8,}\d)", text)
    urls = re.findall(r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s,;)]*)?", text)

    parsed["email"] = email.group(0) if email else ""
    parsed["phone"] = phone.group(1).strip() if phone else ""
    parsed["linkedin"] = next((url for url in urls if "linkedin" in url.lower()), "")
    parsed["github"] = next((url for url in urls if "github" in url.lower()), "")
    parsed["portfolio"] = next((url for url in urls if "linkedin" not in url.lower() and "github" not in url.lower() and "@" not in url), "")

    for line in lines[:8]:
        lower = line.lower()
        if "@" in line or re.search(r"\d{6,}", line) or "linkedin" in lower or "github" in lower:
            continue
        if len(line.split()) <= 6 and not section_key(line):
            parsed["name"] = line
            break
    if parsed["name"]:
        try:
            start_index = lines.index(parsed["name"]) + 1
        except ValueError:
            start_index = 0
        for line in lines[start_index : start_index + 4]:
            if "@" not in line and not section_key(line) and 2 <= len(line.split()) <= 12:
                parsed["title"] = line
                break

    sections = {key: [] for key in section_aliases}
    current = None
    for line in lines:
        key = section_key(line)
        if key:
            current = key
            continue
        if current:
            sections[current].append(line)

    for key in ("summary", "education", "languages"):
        parsed[key] = "\n".join(sections[key]).strip()
    parsed["skills"] = ", ".join(clean_list("\n".join(sections["skills"]))).strip()
    for key in ("experience", "projects", "certifications", "awards"):
        parsed[key] = "\n".join(sections[key]).strip()

    location_candidates = [
        line
        for line in lines[:12]
        if "," in line and not any(token in line.lower() for token in ("linkedin", "github", "http", "@"))
    ]
    parsed["location"] = location_candidates[0] if location_candidates else ""
    return {key: value for key, value in parsed.items() if plain(value)}


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
    import_tab, details_tab, template_tab, ats_tab = st.tabs(["Import", "Details", "Template", "ATS"])

    with import_tab:
        st.subheader("Upload Existing Resume")
        resume_file = st.file_uploader("PDF, DOCX, or TXT resume", type=["pdf", "docx", "txt"])
        if resume_file:
            try:
                extracted_text = extract_text_from_resume(resume_file)
                parsed = parse_resume_text(extracted_text)
                found_fields = ", ".join(parsed.keys()) or "no structured fields"
                st.success(f"Parsed {found_fields}.")
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

    with details_tab:
        st.subheader("Personal Details")
        st.text_input("Full name", key="name")
        st.text_input("Professional title", key="title")
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
        st.text_area("Professional summary", key="summary", height=105)
        st.text_area("Skills - comma/new-line separated", key="skills", height=85)
        st.text_area("Experience - separate jobs with a blank line", key="experience", height=230)
        st.text_area("Projects - separate projects with a blank line", key="projects", height=145)
        st.text_area("Education", key="education", height=75)
        with st.expander("Additional details"):
            st.text_area("Certifications - separate entries with a blank line", key="certifications", height=100)
            st.text_input("Languages", key="languages")
            st.text_area("Awards, publications, volunteering or memberships", key="awards", height=90)

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

if jd.strip():
    ats, matched, missing = score_resume(" ".join(str(value) for value in data.values()), jd)
    with editor:
        with ats_tab:
            st.metric("ATS keyword alignment", f"{ats}%")
            st.progress(ats / 100)
            st.write("Matched keywords:", ", ".join(matched[:40]) or "None")
            st.write("Potentially missing keywords:", ", ".join(missing[:40]) or "None")
            st.caption("Heuristic keyword checker only; it cannot reproduce a specific employer's ATS score.")

with preview:
    top_row, action_row = st.columns([1, 1])
    with top_row:
        st.subheader("Live Preview")
    with action_row:
        safe_file_base = re.sub(r"[^a-z0-9]+", "-", plain(data["name"]).lower()).strip("-") or "resume"
        safe_template = re.sub(r"[^a-z0-9]+", "-", selected_name.lower()).strip("-")
        file_name = f"{safe_file_base}-{safe_template}.html"
        st.download_button("Download HTML", rendered_html, file_name=file_name, mime="text/html", use_container_width=True)
    components.html(rendered_html, height=1020, scrolling=True)
