import re

def extract_code_from_response(response):
    pattern = r'\[Start of code\](.*?)\[End of code\]'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "No code found between [Start of code] and [End of code]"

def extract_test_cases(challenge_response):
    # Split the response into visible and hidden sections
    sections = re.split(r'#\s*Hidden test cases', challenge_response)
    
    def process_section(section):
        # Find all assert lines
        assert_lines = re.findall(r'^\s*assert.*$', section, re.MULTILINE)
        return [line.strip() for line in assert_lines]
    
    # Process visible and hidden test cases
    visible_tests = process_section(sections[0])
    hidden_tests = process_section(sections[1]) if len(sections) > 1 else []
    
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