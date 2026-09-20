# Resume Builder MVP

Fast local MVP built with Streamlit.

## Features
- Resume content editor
- Live resume preview
- Colorful template selection loaded from the `templates/` folder
- Light-background split resume templates with side panels for contact, skills, and education
- Resume upload/import from PDF, DOCX, and TXT with best-effort field extraction
- Color-palette presets plus custom accent and divider colors
- Optional uploaded HTML templates with documented replacement tokens
- Extended contact details: LinkedIn, GitHub, and portfolio
- Optional certifications, languages, awards, publications, volunteer work, and memberships
- Compact spacing option
- ATS keyword alignment checker against a pasted job description
- Download rendered HTML

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown by Streamlit, normally http://localhost:8501.

## Built-in and custom templates

Built-in templates live in `templates/`. Add a new `.html` file there and restart Streamlit
to make it appear in the template picker. You can also upload an `.html` or `.htm` file from
the template panel. The builder safely replaces these tokens with the current resume data:

Current bundled templates include Aurora Sidebar, Clean ATS, Executive Band, Timeline Color,
Pastel Split, and Right Panel Split.

`{{name}}`, `{{title}}`, `{{contact}}`, `{{summary}}`, `{{skills}}`, `{{experience}}`,
`{{projects}}`, `{{education}}`, `{{certifications}}`, `{{languages}}`, `{{awards}}`,
`{{summary_section}}`, `{{skills_section}}`, `{{experience_section}}`,
`{{projects_section}}`, `{{education_section}}`, `{{certifications_section}}`,
`{{languages_section}}`, `{{awards_section}}`, `{{accent}}`, `{{secondary}}`, `{{font}}`,
and `{{density}}`.

For example, `color: {{accent}}` lets uploaded templates inherit the selected palette.

## Resume import

Upload PDF, DOCX, or TXT from the Import tab. The parser extracts plain text locally and
uses section headings such as `Summary`, `Skills`, `Experience`, `Projects`, `Education`,
`Certifications`, `Languages`, and `Awards` to pre-fill the editor. This is intentionally
best-effort; scanned image PDFs still need OCR in a future version.

## Monetization note

The earlier ₹9 pay-per-export idea is deferred while the core product is being built. For
now, the app allows direct HTML export so templates and resume parsing can be tested quickly.

## Next roadmap items
1. DOCX/PDF export
2. Drag/drop section ordering
3. OCR support for scanned resume PDFs
4. Job-description parser and skill taxonomy
5. AI bullet rewriting with measurable impact
6. Version history, saved resumes, authentication, and deployment
# resume-builder-mvp
