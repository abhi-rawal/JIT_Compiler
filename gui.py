
import customtkinter as ctk
from tkinter import filedialog, messagebox
from my_parser import parse_code
from compiler import CodeGenerator
from engine import execute_ir

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class JITCompilerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(" JIT Compiler with Enhanced GUI")
        self.geometry("1000x720")
        self.configure(padx=10, pady=10)
        self._create_widgets()

    def _create_widgets(self):
        # Top Theme Toggle and Buttons Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", pady=(0, 10))

        self.theme_btn = ctk.CTkButton(top_frame, text="Toggle Theme", command=self._toggle_theme)
        self.theme_btn.pack(side="left", padx=5)

        load_btn = ctk.CTkButton(top_frame, text="Load Code", command=self._load_code)
        load_btn.pack(side="left", padx=5)

        save_btn = ctk.CTkButton(top_frame, text="Save Code", command=self._save_code)
        save_btn.pack(side="left", padx=5)

        run_btn = ctk.CTkButton(top_frame, text="Compile & Run", command=self._compile_and_run)
        run_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(top_frame, text="Clear Output", command=self._clear_output)
        clear_btn.pack(side="left", padx=5)

        # Code Input Text Area
        self.code_input = ctk.CTkTextbox(self, height=200, font=("Consolas", 14))
        self.code_input.pack(fill="both", expand=False, pady=(0, 10))
        self.code_input.insert("1.0", "// Write your code here...\n")

        # Output Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        self.ir_tab = self.tabview.add("LLVM IR")
        self.result_tab = self.tabview.add("Result")
        self.error_tab = self.tabview.add("Errors")

        self.ir_output = ctk.CTkTextbox(self.ir_tab, wrap="none")
        self.ir_output.pack(fill="both", expand=True, padx=5, pady=5)

        self.result_output = ctk.CTkTextbox(self.result_tab)
        self.result_output.pack(fill="both", expand=True, padx=5, pady=5)

        self.error_output = ctk.CTkTextbox(self.error_tab)
        self.error_output.pack(fill="both", expand=True, padx=5, pady=5)

        # Status Bar
        self.status_bar = ctk.CTkLabel(self, text="Status: Ready", anchor="w")
        self.status_bar.pack(fill="x", pady=(5, 0))

    def _toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    def _load_code(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.code_input.delete("1.0", "end")
                self.code_input.insert("1.0", file.read())
                self._set_status("Code loaded from file.")

    def _save_code(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.code_input.get("1.0", "end").strip())
                self._set_status("Code saved successfully.")

    def _clear_output(self):
        self.ir_output.delete("1.0", "end")
        self.result_output.delete("1.0", "end")
        self.error_output.delete("1.0", "end")
        self._set_status("Output cleared.")

    def _compile_and_run(self):
        code = self.code_input.get("1.0", "end").strip()
        self._clear_output()
        try:
            tree = parse_code(code)
            generator = CodeGenerator()
            llvm_ir = generator.compile(tree)
            result = execute_ir(llvm_ir)

            self.ir_output.insert("1.0", llvm_ir)
            self.result_output.insert("1.0", str(result))
            self._set_status("Compiled and executed successfully.")

        except Exception as e:
            self.error_output.insert("1.0", str(e))
            self._set_status("Compilation failed.")

    def _set_status(self, message):
        self.status_bar.configure(text=f"Status: {message}")

if __name__ == "__main__":
    app = JITCompilerGUI()
    app.mainloop()
