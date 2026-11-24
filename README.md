GlacierCTF – Teamcheck
Category: Web
Vulnerability: Blind Server-Side Template Injection (SSTI)

### 1. Vulnerability Discovery

The application had a `/check_team` endpoint that accepted a user-controlled `teamname` parameter. By looking at the source code, I noticed that the application used Flask's `render_template_string()` to render a string containing the user input.

The only security check blocked the characters `{{` and `}}`. However, it did not prevent the use of `{%` and `%}`, which are also part of Jinja2's template syntax. This meant that I could potentially inject template statements and bypass the filter.



### 2. Exploitation

I used Jinja2's `{% if %}` statement to inject a condition into the template.

To confirm the vulnerability, I created a simple payload that returned `MATCH` if the injected condition was true and `NO` otherwise. Receiving `MATCH` confirmed that the SSTI was exploitable and that the injected template code was being executed.

Since the challenge was a blind SSTI, I could not directly see the contents of the flag. Instead, I used Jinja2's `lipsum.__globals__` object to access Python built-ins, import the `os` module and execute `cat /flag.txt`.

### 3. Flag Extraction

I automated the extraction process using a Python script and the `requests` library.
The script tested possible characters one by one using a predefined alphabet. For each character, it checked whether the beginning of the flag file matched the current candidate.
If the server returned `MATCH`, the character was added to the flag. This process continued until the closing `}` character was found.
This allowed me to extract the flag character by character without directly displaying the file contents.


### 4. Root Cause & Mitigation

The main issue was the use of `render_template_string()` with unsanitized user input. The blacklist filtering was also insufficient because it only blocked two specific characters instead of preventing template injection.

To prevent this vulnerability:
- Never pass untrusted user input directly into template source code.
- Pass user-controlled values as template variables instead.
- Avoid blacklist-based filtering as a security mechanism.
- Apply proper input handling and use a safe separation between application data and template logic.

**Conclusion:** The challenge demonstrated how an incomplete security filter combined with unsafe Jinja2 template rendering can lead to SSTI and, ultimately, arbitrary command execution and flag disclosure.
