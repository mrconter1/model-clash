import re

def extract_code_from_response(response):
    pattern = r'\[Start of code\](.*?)\[End of code\]'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "No code found between [Start of code] and [End of code]"

def extract_test_cases(extracted_code):
    code_lines = extracted_code.split('\n')
    
    visible_tests = []
    hidden_tests = []
    current_list = visible_tests
    
    for line in code_lines:
        if '# Visible test cases' in line:
            current_list = visible_tests
            continue
        if '# Hidden test cases' in line:
            current_list = hidden_tests
            continue
        if 'assert' in line:
            line = line.strip()
            line = re.sub(r'assert\s+\w+', 'assert X', line)
            line = re.sub(r'\s*#.*$', '', line)
            current_list.append(line)

    if not visible_tests and not hidden_tests:
        print("Warning: No test cases found in extracted code.")
        print(extracted_code)
    
    return visible_tests, hidden_tests

def run_tests(implementation_code, visible_tests, hidden_tests):
    try:
        exec(implementation_code, globals())
    except Exception:
        return False

    for test in visible_tests + hidden_tests:
        try:
            exec(test)
        except:
            return False
    
    if 'X' in globals():
        del globals()['X']
    
    return True