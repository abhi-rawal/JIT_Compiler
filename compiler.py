from llvmlite import ir

class CodeGenerator:
    def __init__(self):
        self.module = ir.Module(name="jit_module")
        func_type = ir.FunctionType(ir.DoubleType(), [])
        self.func = ir.Function(self.module, func_type, name="main")
        block = self.func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        self.variables = {}  # Stores variable pointers (alloca)

    def compile(self, tree_list):
        result = None
        for stmt in tree_list.children:
            result = self._eval(stmt)
        if result is not None:
            self.builder.ret(result)
        else:
            self.builder.ret(ir.Constant(ir.DoubleType(), 0.0))
        return str(self.module)

    def _eval(self, node):
        if isinstance(node, list):  # handle nested blocks
            result = None
            for stmt in node:
                result = self._eval(stmt)
            return result

        if isinstance(node, tuple):
            node_type = node[0]

            if node_type == "assign":
                name, value = node[1], self._eval(node[2])
                ptr = self.variables.get(name)
                if ptr is None:
                    ptr = self.builder.alloca(ir.DoubleType(), name=name)
                    self.variables[name] = ptr
                self.builder.store(value, ptr)
                return value

            elif node_type == "var":
                ptr = self.variables.get(node[1])
                if ptr is None:
                    raise NameError(f"Variable '{node[1]}' not defined")
                return self.builder.load(ptr, name=node[1])

            elif node_type == "print":
                val = self._eval(node[1])
                # Placeholder: IR printing needs printf or similar setup
                return val

            elif node_type == "add":
                return self.builder.fadd(self._eval(node[1]), self._eval(node[2]), name="addtmp")
            elif node_type == "sub":
                return self.builder.fsub(self._eval(node[1]), self._eval(node[2]), name="subtmp")
            elif node_type == "mul":
                return self.builder.fmul(self._eval(node[1]), self._eval(node[2]), name="multmp")
            elif node_type == "div":
                return self.builder.fdiv(self._eval(node[1]), self._eval(node[2]), name="divtmp")
            elif node_type == "neg":
                return self.builder.fsub(ir.Constant(ir.DoubleType(), 0), self._eval(node[1]), name="negtmp")

            elif node_type == "while":
                cond, body = node[1], node[2]
                cond_block = self.builder.append_basic_block("while.cond")
                body_block = self.builder.append_basic_block("while.body")
                end_block = self.builder.append_basic_block("while.end")

                self.builder.branch(cond_block)
                self.builder.position_at_end(cond_block)
                cond_val = self._eval_condition(cond)
                self.builder.cbranch(cond_val, body_block, end_block)

                self.builder.position_at_end(body_block)
                self._eval(body)
                self.builder.branch(cond_block)

                self.builder.position_at_end(end_block)
                return ir.Constant(ir.DoubleType(), 0.0)

            elif node_type == "condition":
                return self._eval_condition(node)

        elif isinstance(node, float):
            return ir.Constant(ir.DoubleType(), node)

    def _eval_condition(self, cond_node):
        _, lhs, op, rhs = cond_node
        left = self._eval(lhs)
        right = self._eval(rhs)

        if op == ">":
            return self.builder.fcmp_ordered(">", left, right, name="cmptmp")
        elif op == "<":
            return self.builder.fcmp_ordered("<", left, right, name="cmptmp")
        elif op == "==":
            return self.builder.fcmp_ordered("==", left, right, name="cmptmp")
        elif op == "!=":
            return self.builder.fcmp_ordered("!=", left, right, name="cmptmp")
        else:
            raise NotImplementedError(f"Unknown comparison: {op}")
