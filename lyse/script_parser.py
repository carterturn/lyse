import re
import json

def parse_ipynb(fname):
    globals = {}
    code = ''
    
    with open(fname, 'r') as f:
        cells = json.loads(f.read())['cells']
    
    for _cell in cells:
        _code = _cell['source']
        if len(_code) > 0:
            if (_code[0] == "### Static ###\n"
                or _code[0] == "### Analysis Script ###\n"
                or _code[0] == "### Plots ###\n"):
                for line in _code:
                    code += line

            if _code[0] == "### Modifiable Parameters ###\n":
                for line in _cell['source'][1:]:
                    m = re.match('(\w+)\s*=\s*([\W\w]*)', line.strip())
                    if m != None:
                        key = m.group(1)
                        val = m.group(2)
                        try:
                            globals[key] = eval(val)
                        except:
                            globals[key] = val

    return code, globals

def parse_py(fname):
    globals = {}
    code = ''

    # Load globals from script into dictionary
    with open(self.filepath, 'r') as script_file:
        code = script_file.read()
        script_tree = ast.parse(code)
        setup_globals_func = None
        for func in [f for f in script_tree.body if isinstance(f, ast.FunctionDef)]:
            if func.name == 'SETUP_GLOBALS':
                setup_globals_func = func
        if setup_globals_func is not None:
            try:
                setup_globals_script = ast.unparse(setup_globals_func) + '\nSETUP_GLOBALS()'
                setup_globals_code = compile(setup_globals_script, self.filepath, 'exec')
                exec(setup_globals_code, globals)
            except Exception:
                app.output_box.output('Unable to execute SETUP_GLOBALS for \n'%self.shortname, red=True)
    # Don't load "private" variables (or builtins)
    rm_keys = ['SETUP_GLOBALS']
    for key in globals.keys():
        if key.startswith('_'):
            rm_keys.append(key)
    for key in rm_keys:
        globals.pop(key)

    return code, globals
