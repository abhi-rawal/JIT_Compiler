from llvmlite import binding
import ctypes

# Step 1: Initialize the LLVM JIT engine (only once)
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

def create_execution_engine():
    """
    Creates an LLVM MCJIT execution engine to JIT-compile IR.
    """
    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = binding.parse_assembly("")
    engine = binding.create_mcjit_compiler(backing_mod, target_machine)
    return engine

def compile_ir(engine, llvm_ir):
    """
    Compiles the given LLVM IR string with the provided execution engine.
    """
    mod = binding.parse_assembly(llvm_ir)
    mod.verify()
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod

def execute_ir(llvm_ir):
    """
    Compiles and executes the given LLVM IR and returns the result.
    """
    engine = create_execution_engine()
    compile_ir(engine, llvm_ir)

    func_ptr = engine.get_function_address("main")
    cfunc = ctypes.CFUNCTYPE(ctypes.c_double)(func_ptr)
    result = cfunc()
    return result
