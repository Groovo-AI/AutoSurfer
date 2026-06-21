import urllib.request, json, os, ssl, shutil
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
token = os.environ.get("GITHUB_TOKEN")
payload = {"title": "Fix for issue #12", "body": "Closes #12\n\nImplemented automated fix.", "head": "KartavyaDikshit:fix-issue-12", "base": "main"}
req = urllib.request.Request("https://api.github.com/repos/developeranku/AutoSurfer/pulls", data=json.dumps(payload).encode(), headers={'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json', 'Content-Type': 'application/json'}, method='POST')
try:
    with urllib.request.urlopen(req, context=ctx) as r: 
        print("[+] PR Created:", json.loads(r.read())['html_url'])
        os.chdir("..")
        shutil.rmtree("/Users/kartavyadikshit/Projects/Open Source/AutoSurfer_bounty_parallel_1", ignore_errors=True)
except Exception as e: print("[!] PR Failed:", e)
