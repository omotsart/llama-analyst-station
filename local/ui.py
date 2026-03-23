import gradio as gr
import config
import transcribe
import analysis
import export

# --- Interface style ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');
* { font-family: 'Syne', sans-serif !important; }
code, .mono { font-family: 'JetBrains Mono', monospace !important; }
body, .gradio-container { background: #0d0f14 !important; }
.output-box {
    background: #12151d !important;
    color: #e8eaf0 !important;
    border: 1px solid #ff6600 !important;
    border-radius: 8px;
    padding: 20px;
    min-height: 420px;
}
.output-box h1, .output-box h2, .output-box h3 { color: #ff6600 !important; }
.gr-button-primary { background: linear-gradient(135deg, #ff6600, #ff9900) !important; border: none !important; font-weight: 700 !important; }
.gr-button-secondary { border: 1px solid #ff6600 !important; color: #ff6600 !important; }
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="orange")) as demo:
    gr.Markdown("# 🎙️ Llama 3 · Professional Analyst Station\n*Local Version — Whisper + LLaMA 3.2 3B*")

    with gr.Row():
        # ---- LEFT COLUMN: Input and Transcription ----
        with gr.Column(scale=1):
            with gr.Tabs():
                with gr.TabItem("📁 Audio/Video"):
                    file_in = gr.Audio(sources=["upload", "microphone"], type="filepath", label=None)
                with gr.TabItem("🎬 Video"):
                    video_in = gr.Video(label=None)

            mode_sel = gr.Radio(
                choices=["🎙️ Standard transcript", "🕐 With timecodes", "👥 Identify speakers"],
                value="🎙️ Standard transcript",
                label="Transcription mode",
            )

            txt_raw = gr.Textbox(label="📝 Transcript (Whisper)", lines=12, show_copy_button=True)

            with gr.Row():
                btn_fix = gr.Button("✏️ Fix grammar (LLaMA)", variant="secondary")
                btn_dl_full = gr.Button("💾 Download .txt", variant="primary")
                btn_dl_full_docx = gr.Button("📝 Download .docx", variant="primary")

            out_full = gr.File(label="Transcript (.txt)")
            out_full_docx = gr.File(label="Transcript (.docx)")

        # ---- RIGHT COLUMN: Analysis ----
        with gr.Column(scale=1):
            query_in = gr.Textbox(label="❓ Your question", placeholder="Leave blank for auto-summary...", lines=2)
            role_sel = gr.Dropdown(choices=list(config.ROLES.keys()), value="📊 Analyst", label="🎭 Analyst role")

            with gr.Row():
                lang_sel = gr.Radio(choices=["ru", "en"], value="ru", label="🌍 Language", scale=1)
                btn_run = gr.Button("🚀 Run analysis", variant="primary", scale=2)

            out_md = gr.Markdown(value="### 🤖 Waiting for request...", elem_classes="output-box")

            with gr.Row():
                btn_dl_sum = gr.Button("💾 .md", variant="primary")
                btn_dl_pdf = gr.Button("📄 PDF", variant="primary")
                btn_dl_docx = gr.Button("📝 DOCX", variant="primary")

            out_sum = gr.File(label="Analysis (.md)")
            out_pdf = gr.File(label="Analysis (.pdf)")
            out_docx = gr.File(label="Analysis (.docx)")

    # ---- EVENTS (Linking buttons to functions from modules) ----
    file_in.change(fn=transcribe.transcribe_auto, inputs=[file_in, mode_sel], outputs=txt_raw)
    video_in.change(fn=transcribe.transcribe_auto, inputs=[video_in, mode_sel], outputs=txt_raw)

    btn_fix.click(fn=analysis.fix_grammar_llama, inputs=txt_raw, outputs=txt_raw)
    
    btn_dl_full.click(fn=lambda x: export.save_result(x, "full"), inputs=txt_raw, outputs=out_full)
    btn_dl_full_docx.click(fn=export.save_as_docx, inputs=txt_raw, outputs=out_full_docx)

    btn_run.click(fn=analysis.generate_analysis_stream, inputs=[txt_raw, query_in, lang_sel, role_sel], outputs=out_md)

    btn_dl_sum.click(fn=lambda x: export.save_result(x, "summary"), inputs=out_md, outputs=out_sum)
    btn_dl_pdf.click(fn=export.save_as_pdf, inputs=out_md, outputs=out_pdf)
    btn_dl_docx.click(fn=export.save_as_docx, inputs=out_md, outputs=out_docx)
