# Resume Builder MVP

Fast local MVP built with Streamlit with AI-powered resume building features.

## Features

### Core Resume Building
- **15 Professional Templates** - Modern split layouts, ATS-friendly designs, and creative templates
- **Live Resume Preview** - Real-time preview updates as you edit
- **Custom HTML Templates** - Upload your own templates with documented replacement tokens
- **Color System** - 7 color palettes plus custom accent and secondary colors
- **Background Textures** - 10 professional patterns (dots, grids, circles, grain, etc.)
- **Font Selection** - 5 font options (Inter, Arial, Georgia, Verdana, Tahoma)
- **Compact Spacing** - Toggle between comfortable and compact spacing

### Content Management
- **Resume Import** - Import from PDF, DOCX, and TXT with best-effort field extraction
- **Profile Photo System** - Upload from file/gallery or capture from camera
- **Photo Beautification** - Adjust size, zoom, shape, and border styles
- **Extended Contact Details** - LinkedIn, GitHub, portfolio, email, phone, location
- **Complete Resume Sections** - Summary, skills, experience, projects, education, certifications, languages, awards

### AI-Powered Features
- **AI Content Assistance** - Professional summary generation and bullet point improvement suggestions
- **Grammar & Spell Check** - Real-time grammar and spelling validation
- **Cover Letter Generation** - Professional cover letters tailored to target company and position
- **Interview Preparation** - AI-generated interview questions (technical, behavioral, general)
- **ATS Optimization** - Real-time ATS keyword scoring and skill gap analysis

### Resume Management
- **Save/Load Resumes** - Save multiple resume versions and load them back
- **Version History** - Track changes and restore previous versions
- **Resume Sharing** - JSON export for data portability and backup
- **Career Research** - Salary insights guidance and company research tips
- **LinkedIn Integration** - Import placeholder and manual transfer guidance

### Export Options
- **HTML Export** - Perfect quality with all styling preserved
- **PDF Export** - Professional PDF generation (ReportLab-based)
- **DOCX Export** - Microsoft Word document export (python-docx)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git (for cloning the repository)

### Quick Start (Recommended)

For your convenience, the repository includes startup scripts for each platform:

**Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/rgeddyse/resume-builder-mvp.git
cd resume-builder-mvp

# Run the startup script (creates venv, installs dependencies, and starts app)
chmod +x start_mac.sh  # Make script executable on Linux
./start_mac.sh
```

**Windows:**
```bash
# Clone the repository
git clone https://github.com/rgeddyse/resume-builder-mvp.git
cd resume-builder-mvp

# Run the startup script (creates venv, installs dependencies, and starts app)
start_windows.bat
```

### Manual Installation

If you prefer manual setup or encounter issues with the startup scripts:

#### Linux Installation

```bash
# Clone the repository
git clone https://github.com/rgeddyse/resume-builder-mvp.git
cd resume-builder-mvp

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

#### Windows Installation

```bash
# Clone the repository
git clone https://github.com/rgeddyse/resume-builder-mvp.git
cd resume-builder-mvp

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

#### macOS Installation

```bash
# Clone the repository
git clone https://github.com/rgeddyse/resume-builder-mvp.git
cd resume-builder-mvp

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Open the URL shown by Streamlit, normally http://localhost:8501.

## Built-in and Custom Templates

Built-in templates live in `templates/`. Add a new `.html` file there and restart Streamlit
to make it appear in the template picker. You can also upload an `.html` or `.htm` file from
the template panel. The builder safely replaces these tokens with the current resume data:

**Current bundled templates (15 total):**
- Aurora Sidebar
- Clean ATS
- Consultant Grid
- Concentric Circles
- Editorial Column
- Executive Band
- Geometric Pattern
- Gradient Sidebar
- Paper Texture
- Pastel Split
- Quiet Luxury
- Ribbon Profile
- Right Panel Split
- Timeline Color

**Available tokens:**
`{{name}}`, `{{title}}`, `{{contact}}`, `{{summary}}`, `{{skills}}`, `{{experience}}`,
`{{projects}}`, `{{education}}`, `{{certifications}}`, `{{languages}}`, `{{awards}}`,
`{{summary_section}}`, `{{skills_section}}`, `{{experience_section}}`,
`{{projects_section}}`, `{{education_section}}`, `{{certifications_section}}`,
`{{languages_section}}`, `{{awards_section}}`, `{{accent}}`, `{{secondary}}`, `{{font}}`,
`{{density}}`, `{{page_background}}`, `{{paper_background}}`, `{{profile_photo}}`

For example, `color: {{accent}}` lets uploaded templates inherit the selected palette.

## Resume Import

Upload PDF, DOCX, or TXT from the Import tab. The parser extracts plain text locally and
uses section headings such as `Summary`, `Skills`, `Experience`, `Projects`, `Education`,
`Certifications`, `Languages`, and `Awards` to pre-fill the editor. This is intentionally
best-effort; scanned image PDFs still need OCR in a future version.

## Current Features

The resume builder now includes all standard features found in top-tier resume builders:
- ✅ Multiple professional templates with modern designs
- ✅ AI-powered content assistance and suggestions
- ✅ Grammar and spell checking
- ✅ ATS optimization with real-time scoring
- ✅ Cover letter generation
- ✅ Interview preparation tools
- ✅ Resume version management
- ✅ Multiple export formats (HTML, PDF, DOCX)
- ✅ Profile photo with beautification controls
- ✅ Career research and salary insights
- ✅ LinkedIn integration support

## Troubleshooting

### Common Issues

**Python not found:**
- Ensure Python 3.7+ is installed. Download from [python.org](https://python.org)
- On Windows, you may need to add Python to your PATH during installation

**pip not found:**
- Ensure you're using the Python version that includes pip
- Try `python -m pip install --upgrade pip` to upgrade pip

**Virtual environment activation fails:**
- On Windows: Use `.venv\Scripts\activate` instead of `source .venv/bin/activate`
- On Linux/macOS: Ensure you have `python3-venv` installed (sudo apt-get install python3-venv on Ubuntu)

**Dependencies fail to install:**
- Some packages (like language-tool-python) may require additional system dependencies
- If installation fails, the app will still work with fallback functionality
- For PDF export, ensure you have the required system libraries or use HTML export instead

**Streamlit doesn't start:**
- Ensure you're inside the virtual environment
- Try `pip install --upgrade streamlit` to update Streamlit
- Check that port 8501 is not already in use

**Templates don't appear:**
- Ensure the `templates/` folder exists and contains HTML files
- Restart Streamlit after adding new templates
- Check that template files have the correct `.html` extension

## Project Structure

```
resume-builder-mvp/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── start_mac.sh          # Quick start script for macOS/Linux
├── start_windows.bat     # Quick start script for Windows
├── .gitignore           # Git ignore rules
└── templates/           # HTML resume templates
    ├── aurora-sidebar.html
    ├── clean-ats.html
    ├── concentric-circles.html
    ├── consultant-grid.html
    ├── editorial-column.html
    ├── executive-band.html
    ├── geometric-pattern.html
    ├── gradient-sidebar.html
    ├── paper-texture.html
    ├── pastel-split.html
    ├── quiet-luxury.html
    ├── ribbon-profile.html
    ├── right-panel-split.html
    └── timeline-color.html
```

## License

This project is open source and available under the MIT License.
