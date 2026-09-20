# Resume Builder MVP

Fast local MVP built with Streamlit with AI-powered resume building features and interactive drag-and-drop layout editor.

## Features

### Core Resume Building
- **15 Professional Templates** - Modern split layouts, ATS-friendly designs, and creative templates
- **Interactive Layout Editor** - Drag-and-drop style component arrangement with visual preview
- **Component-Based Building** - 11 reusable components (Name, Skills, Experience, etc.) that can be arranged in different layout areas
- **4 Layout Structures** - Sidebar Left, Sidebar Right, Single Column, Three Column
- **4 Layout Areas** - Header, Sidebar, Main Content, Footer with component limits
- **Quick Layout Presets** - Classic, Modern Split, Minimal, Compact one-click layouts
- **Live Resume Preview** - Real-time preview updates as you edit with exact HTML match
- **Custom HTML Templates** - Upload your own templates with documented replacement tokens
- **Color System** - 7 color palettes plus custom accent and secondary colors
- **Background Textures** - 10 professional patterns (dots, grids, circles, grain, etc.)
- **Font Selection** - 5 font options (Inter, Arial, Georgia, Verdana, Tahoma)
- **Compact Spacing** - Toggle between comfortable and compact spacing

### Content Management
- **AI-Enhanced Resume Parsing** - Advanced parsing with fuzzy section detection (30+ variations) and AI validation
- **Resume Import** - Import from PDF, DOCX, and TXT with intelligent field extraction
- **Profile Photo System** - Upload from file/gallery or capture from camera with proper sizing (80-200px range)
- **Photo Beautification** - Adjust size, zoom, shape, and border styles with reasonable defaults (120px)
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

Upload PDF, DOCX, or TXT from the Import tab. The parser uses AI-enhanced parsing with fuzzy section detection (30+ variations) and optional AI validation (when OPENAI_API_KEY is configured). The parser intelligently extracts fields and can validate/correct parsed data using GPT-3.5-turbo. This provides significantly improved accuracy compared to traditional rule-based parsing.

## Interactive Layout Editor

The Template tab includes a powerful drag-and-drop style layout editor that allows you to visually arrange resume components:

### Available Components (12 total)
- 👤 **Name** - Your full name
- 💼 **Job Title** - Your professional title
- 📞 **Contact Info** - Email, phone, location
- 📸 **Profile Photo** - Your profile picture (120px default, 80-200px range)
- 📝 **Summary** - Professional summary
- 🛠️ **Skills** - Technical and soft skills
- 💻 **Experience** - Work experience entries
- 🎓 **Education** - Educational background
- 🚀 **Projects** - Project descriptions
- 📜 **Certifications** - Professional certifications
- 🌍 **Languages** - Language proficiency
- 🏆 **Awards** - Awards and achievements

### Layout Areas (4 total)
- **Header Area** - Top section (max 4 components)
- **Sidebar** - Left/right column (max 4 components)
- **Main Content** - Primary area (max 6 components)
- **Footer** - Bottom section (max 2 components)

### Layout Structures (4 total)
- **Sidebar Left** - 30% sidebar on left
- **Sidebar Right** - 30% sidebar on right
- **Single Column** - Traditional vertical layout
- **Three Column** - 25% sidebar with header/main/footer

### How to Use
1. Go to the **Template** tab
2. Scroll to **🎨 Custom Layout Editor**
3. Select a **Layout Structure** (Sidebar Left, Sidebar Right, Single Column, Three Column)
4. **Add Components** - Click "Add" to place components in available areas
5. **Arrange Components** - Use ↑↓ buttons to reorder within areas
6. **Remove Components** - Remove last component from any area
7. **Quick Presets** - Use Classic, Modern Split, Minimal, Compact for instant layouts
8. **Toggle** - Enable "Use Custom Layout Instead of Template" to use your custom arrangement
9. **Preview** - See real-time visual preview of your layout

### Layout Preview
The editor provides a real-time visual preview showing:
- Component placement in different areas
- Layout structure visualization
- Component icons and names
- Area capacity indicators
- Grid layout representation

### Custom vs Template Mode
- **Template Mode**: Uses traditional HTML templates with fixed layouts
- **Custom Mode**: Uses your component arrangement with dynamic HTML generation
- Toggle between modes instantly with the switch in the Template tab

## Current Features

The resume builder now includes all standard features found in top-tier resume builders:
- ✅ Multiple professional templates with modern designs
- ✅ Interactive drag-and-drop layout editor with component arrangement
- ✅ Component-based resume building with 11 reusable components
- ✅ 4 layout structures (Sidebar Left, Sidebar Right, Single Column, Three Column)
- ✅ Quick layout presets (Classic, Modern Split, Minimal, Compact)
- ✅ Real-time visual layout preview
- ✅ AI-enhanced resume parsing with fuzzy section detection
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
- ✅ Live preview with exact HTML match to downloaded files

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

**Live preview doesn't match downloaded HTML:**
- The preview now includes CSS injection to force full-width rendering
- This ensures the preview matches the downloaded HTML exactly
- If issues persist, clear browser cache and reload the page

**AI parsing not working:**
- Set OPENAI_API_KEY environment variable to enable AI validation
- Without the key, the system uses enhanced rule-based parsing
- AI validation requires internet connection and valid API key
- The app will show "(AI-validated)" or "(rule-based)" status for parsing

**Layout editor components not appearing:**
- Ensure you've added components to layout areas
- Check that the layout structure includes the areas you're using
- Try switching to a different layout structure
- Use quick presets to reset to a known working layout

**Profile photo covering full area in preview:**
- Photo size is controlled by both app settings and template CSS
- Default size is 120px with adjustable range of 80-200px
- Templates have fixed container sizes (100-120px) to prevent overflow
- Use the photo size slider in Details tab to adjust
- If photo still looks wrong, try a different template

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
