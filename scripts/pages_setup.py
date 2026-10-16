"""Enable the explicitly requested repository's Pages using the existing Git login.
Credentials are retrieved into memory, sent only to api.github.com, never printed.
"""
import json
import subprocess
import urllib.error
import urllib.request

REPO = 'thaianegsilva-svg/thaiane-job-tracker'
def main():
    result = subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,check=True)
    credential = dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)
    token = credential.get('password')
    if not token: raise SystemExit('Nenhuma credencial GitHub disponível.')
    def api(path, method='GET', body=None):
        req=urllib.request.Request('https://api.github.com/repos/'+REPO+path,method=method,data=json.dumps(body).encode() if body is not None else None,
            headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'ThaianeJobTrackerSetup'})
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.load(r) if r.status != 204 else {}
    try:
        repo=api('')
        print(json.dumps({'repository':repo['full_name'],'permissions':repo.get('permissions')}))
        try:
            page=api('/pages')
            if page.get('build_type')!='workflow': page=api('/pages','PUT',{'build_type':'workflow'})
        except urllib.error.HTTPError as exc:
            if exc.code!=404: raise
            page=api('/pages','POST',{'build_type':'workflow'})
        print(json.dumps({'pages_url':page.get('html_url'),'build_type':page.get('build_type'),'status':page.get('status')}))
    except urllib.error.HTTPError as exc:
        print(json.dumps({'error':'GitHub API','status':exc.code,'detail':exc.read().decode()[:600]}))
        raise SystemExit(1)

if __name__=='__main__':main()
