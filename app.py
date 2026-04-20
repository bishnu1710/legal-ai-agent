# @bishnu- legal_ai_agent app.py

import streamlit as st
from graph.workflow import run_workflow
from utils.pdf_reader import extract_text_from_pdf
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from rag.memory_store import save_contract


def generate_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    content = []

    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 8))

    doc.build(content)
    buffer.seek(0)

    return buffer


# PAGE CONFIG
st.set_page_config(
    page_title="Legal AI Agent",
    layout="wide",
    page_icon="⚖️"
)

# CUSTOM CSS
st.markdown("""
<style>
.main {
    background-color: #f9fafb;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.title {
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
}
.subtitle {
    font-size: 18px;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

#  HEADER
st.markdown('<div class="title">⚖️ Multi-Agent Legal Document Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered contract analysis using multi-agent systems</div>', unsafe_allow_html=True)

st.divider()

#  INPUT SECTION
st.markdown("### 📄 Upload or Enter Document")

uploaded_file = st.file_uploader("Upload Contract (PDF or TXT)", type=["pdf", "txt"])

text_input = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text_input = extract_text_from_pdf(uploaded_file)
    else:
        text_input = uploaded_file.read().decode("utf-8")

    st.success("✅ Document loaded successfully!")

    with st.expander("📄 Preview Document"):
        preview_text = text_input[:2500].replace("$", "\\$")
        st.markdown(
            f"""
            <div style='background:#f8fafc; padding:15px; border-radius:10px;
                        border:1px solid #e5e7eb; max-height:400px; overflow:auto;
                        font-family:monospace; white-space:pre-wrap'>
            {preview_text}
            </div>
            """,
            unsafe_allow_html=True
        )

#  MANUAL INPUT
manual_text = st.text_area("Or paste document manually")

if manual_text:
    text_input = manual_text

#  ANALYZE BUTTON
if st.button("🚀 Analyze Document"):
    if text_input.strip() == "":
        st.warning("⚠️ Please upload or enter a document.")
    else:
        with st.spinner("🤖 AI agents analyzing contract..."):
            try:
                result = run_workflow(text_input)
                save_contract(text_input[:3000])
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.stop()

        st.divider()


        report_text = result["final_report"]
        report_text = re.sub(r"\*\*(.*?)\*\*", r"\1", report_text)
        report_text = report_text.replace("\\n", "\n")
        report_text = report_text.replace("[", "").replace("]", "")

        # Table styling
        table_style = """
        <style>
        .legal-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            margin: 16px 0;
        }
        .legal-table thead tr {
            background-color: #1f2937;
            color: #ffffff;
        }
        .legal-table th, .legal-table td {
            padding: 10px 14px;
            border: 1px solid #e5e7eb;
            text-align: left;
            vertical-align: top;
        }
        .legal-table tbody tr:nth-child(even) {
            background-color: #f9fafb;
        }
        .legal-table tbody tr:hover {
            background-color: #f0f4ff;
        }
        .legal-table td:nth-child(3) {
            font-weight: bold;
        }
        </style>
        """

        # Add class to table and color risk levels
        report_html = report_text.replace("<table>", '<table class="legal-table">')
        report_html = re.sub(r'(?<!\w)(High)(?!\w)',
            r'<span style="color:#dc2626">🔴 \1</span>', report_html)
        report_html = re.sub(r'(?<!\w)(Medium)(?!\w)',
            r'<span style="color:#d97706">🟠 \1</span>', report_html)
        report_html = re.sub(r'(?<!\w)(Low)(?!\w)',
            r'<span style="color:#16a34a">🟢 \1</span>', report_html)

        st.markdown(table_style, unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='background:#ffffff; padding:20px; border-radius:12px;
                        border:1px solid #e5e7eb; line-height:1.6'>
            {report_html}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)
        pdf_file = generate_pdf(report_text)

        st.download_button(
            label="📄 Download Report as PDF",
            data=pdf_file,
            file_name="legal_report.pdf",
            mime="application/pdf"
        )
        #  RISKS & COMPLIANCE
        col1, col2 = st.columns(2)

        #  RISKS
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ⚠️ Risks")

            if result["risks"]:
                risk_text = result["risks"][0]
                risk_text = re.sub(r"\*\*(.*?)\*\*", r"\1", risk_text)
                risk_text = risk_text.replace("\\n", "\n")

                lines = risk_text.split("\n")

                for line in lines:
                    line = line.strip()

                    if not line or "|" in line:
                        continue

                    if "High" in line:
                        st.markdown(
                            f"""
                            <div style='background:#ffe6e6; padding:10px; border-radius:8px;
                                        border-left:5px solid red; margin-bottom:8px'>
                            🔴 <b>{line}</b>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    elif "Medium" in line:
                        st.markdown(
                            f"""
                            <div style='background:#fff4e6; padding:10px; border-radius:8px;
                                        border-left:5px solid orange; margin-bottom:8px'>
                            🟠 {line}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:
                        st.markdown(
                            f"<div style='padding:6px; margin-bottom:6px'>{line}</div>",
                            unsafe_allow_html=True
                        )

            st.markdown('</div>', unsafe_allow_html=True)

        #  COMPLIANCE
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📋 Compliance Issues")

            if result["compliance_issues"]:
                comp_text = result["compliance_issues"][0]
                comp_text = re.sub(r"\*\*(.*?)\*\*", r"\1", comp_text)
                comp_text = comp_text.replace("\\n", "\n")

                st.markdown(comp_text)

            st.markdown('</div>', unsafe_allow_html=True)

        # EXPLANATIONS (FIXED NUMBERING)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🧠 Clause Explanations")

        if result["explanations"]:
            exp_text = result["explanations"][0]
            exp_text = re.sub(r"\*\*(.*?)\*\*", r"\1", exp_text)
            exp_text = exp_text.replace("\\n", "\n")

            lines = exp_text.split("\n")
            clean_lines = []

            for line in lines:
                line = line.strip()

                # fix duplicate numbering
                line = re.sub(r"^(\d+)\.\s*(\d+)\.", r"\1.", line)

                if line:
                    clean_lines.append(line)

            st.markdown(
                f"<div style='line-height:1.8'>{'<br>'.join(clean_lines)}</div>",
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)