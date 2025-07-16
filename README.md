# JIT_Compiler
A fully functional Just-In-Time (JIT) Compiler built in Python, designed to compile and execute a simplified programming language on the fly. It uses Lark for parsing, LLVM IR via llvmlite for code generation, and features a modern Tkinter GUI for code input, execution, and output display.


Add files via upload
#  JIT Compiler for Custom Language

A fully functional **Just-In-Time (JIT) Compiler** built in Python. This project allows users to write and execute a simple custom programming language in real-time. It features a modern graphical interface and leverages **Lark** for parsing, **llvmlite** for LLVM IR code generation, and **Tkinter** for the GUI.

---

##  Features

-  **Custom Language Support**
  - Arithmetic expressions
  - Variable assignments
  - Loops (while)
  - `print()` statements

-  **Compiler Architecture**
  - **Lark** parser for grammar and AST generation
  - **LLVM IR generation** using `llvmlite`
  - **Real-time JIT execution** via LLVM engine

-  **Modern GUI Interface**
  - Syntax-highlighted editor
  - Line numbers
  - Tabs: IR Code, Execution Output, Errors
  - Console output area
  - Save & Load code
  - Clear Output button
  - Light/Dark theme toggle
  - Status bar for error/success messages

---

##  Tech Stack

| Component        | Library         |
|------------------|-----------------|
| Language         | Python 3        |
| Parser           | Lark            |
| JIT Engine       | llvmlite        |
| Code Editor GUI  | Tkinter / CustomTkinter |
| Visualization    | Syntax highlight + Output tabs |

---

##  Use Cases

-  Educational tool for compiler design and JIT concepts
-  Testbed for creating and modifying programming language grammars
- Lightweight execution environment for custom interpreted languages

---

##  Screenshots

> *(Insert screenshots here of the GUI, IR tab, and output area)*

---

##  Sample Code

```plaintext
x = 10;
y = 5;
z = x + y * 2;
print(z);
