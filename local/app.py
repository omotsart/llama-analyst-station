import ui
import models

if __name__ == "__main__":
    # 1. Authorization and loading of models
    models.init_huggingface()
    models.load_all()
    
    # 2. Launching the interface
    ui.demo.queue().launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True
    )