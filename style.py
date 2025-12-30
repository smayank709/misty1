mishtee_css = """
/* General Container Styling */
.gradio-container {
    background-color: #FAF9F6 !important;
    color: #333333 !important;
    font-family: 'Times New Roman', serif;
}

/* Typography for Headings */
h1, h2, h3 {
    font-family: 'Playfair Display', 'Times New Roman', serif;
    font-weight: 400;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #333333;
    margin-bottom: 1.5rem;
}

/* Buttons - Sharp, Professional, Terracotta */
button, .primary-button {
    background-color: #C06C5C !important;
    color: #FFFFFF !important;
    border: 1px solid #C06C5C !important;
    border-radius: 0px !important;
    padding: 12px 24px !important;
    font-family: 'Inter', 'Helvetica', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    transition: all 0.3s ease;
}

button:hover {
    background-color: #FAF9F6 !important;
    color: #C06C5C !important;
}

/* Tables - Lightweight Sans-Serif */
table, .gr-table {
    font-family: 'Inter', 'Helvetica', sans-serif !important;
    border-collapse: collapse !important;
    background-color: transparent !important;
}

th, td {
    border: 1px solid #E0E0E0 !important;
    padding: 15px !important;
    font-weight: 300;
}

/* Inputs and Textboxes */
input, textarea, .gr-input {
    border: 1px solid #333333 !important;
    border-radius: 0px !important;
    background-color: transparent !important;
    padding: 10px !important;
}

/* Spacing and Borders */
.gr-block, .gr-box {
    border: 1px solid #E0E0E0 !important;
    border-radius: 0px !important;
    margin: 25px 0 !important;
    padding: 40px !important;
    box-shadow: none !important;
}

/* Remove decorative shadows/radii from any Gradio components */
* {
    box-shadow: none !important;
    border-radius: 0px !important;
}
"""
