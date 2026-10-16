"""Public job metadata only. No credentials, candidate documents or messages."""
import datetime as dt
import html
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))

def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFD', str(value or '').lower()) if unicodedata.category(c) != 'Mn')

def plain(value):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', value or ''))).strip()

def get_json(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'ThaianeJobTracker/1.0 (public job discovery)', 'Accept': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=35) as response:
                return json.load(response)
        except Exception:
            if attempt == 2: raise
            time.sleep(2 * (attempt + 1))

def classify(job):
    title = norm(job['title'])
    text = norm(job.get('description', ''))
    missing, rejected = [], []
    role = bool(re.search(r'design|diretor.*arte|direcao.*arte|branding', title))
    if re.search(r'ux|ui\b|product design|produto|web design|instrucional|interiores|moda|game|engineer|frontend|front.end|design system|experiencia do usuario|service design|content design|designer de sites|fp&a|analista de processos|employer branding', title):
        rejected.append('Especialidade fora do foco principal do perfil')
    if re.search(r'estagi|junior|\bjr\b|aprendiz', title):
        rejected.append('Senioridade inicial fora do foco desta busca')
    if not role: rejected.append('Cargo fora do foco')
    if not job.get('active', True): rejected.append('Inscrições encerradas ou vaga inativa')
    if job['workMode'] == 'hybrid':
        if norm(job.get('city')) != norm(CONFIG['criteria']['hybridCity']):
            if job.get('city'): rejected.append('Híbrido fora de Belo Horizonte')
            else: missing.append('cidade do trabalho híbrido')
        days = job.get('officeDays')
        if days is None: missing.append('quantidade de dias presenciais por semana')
        elif days > CONFIG['criteria']['maxOfficeDays']: rejected.append('Mais de 2 dias presenciais por semana')
    elif job['workMode'] != 'remote':
        if job['workMode'] == 'unknown': missing.append('modalidade remota ou híbrida')
        else: rejected.append('Trabalho presencial')
    if job.get('requiresEnglish'): rejected.append('Exige inglês; busca restrita a português')
    if not job.get('portugueseConfirmed'): missing.append('idioma de trabalho em português')
    salary = job.get('salary') or {}
    low, high = salary.get('min'), salary.get('max')
    if salary.get('currency') != 'BRL' or salary.get('period') != 'monthly':
        missing.append('remuneração mensal em reais')
    elif low is None:
        if high is not None and high <= 7000: rejected.append('Salário até R$ 7.000')
        else: missing.append('salário mensal fixo acima de R$ 7.000')
    elif low <= 7000:
        if high is None or high <= 7000: rejected.append('Salário não supera R$ 7.000')
        else: missing.append('oferta efetiva acima de R$ 7.000 (faixa cruza o limite)')
    signals = [s for s in ['photoshop', 'illustrator', 'indesign', 'identidade visual', 'editorial', 'campanhas', 'direcao de arte'] if s in text]
    score = min(95, 50 + len(signals) * 6) if role else 0
    job.update(score=score, signals=signals, missing=list(dict.fromkeys(missing)), rejectionReasons=rejected,
               eligibility='excluded' if rejected else ('pending' if missing else 'eligible'))
    return job

def convert(raw, now):
    tags = [t.get('tag', {}).get('name', '') for t in raw.get('jobTags', [])]
    description = plain(raw.get('description', '') + ' ' + ' '.join(r.get('description', '') for r in raw.get('jobRequirements', [])))
    salary = raw.get('jobSalary') or {}
    def number(value):
        # Remotar stores money in cents (e.g. 300000 renders as R$ 3.000).
        # Zero means undisclosed in this feed, not an offer of zero salary.
        try: return float(value) / 100 if value is not None and float(value) > 0 else None
        except (TypeError, ValueError): return None
    # Keep the provider's period explicit. Unknown units must never pass the filter.
    salary_type = norm(salary.get('type'))
    period = 'monthly' if salary_type in ['monthly', 'month', 'mensal'] else salary_type
    currency = salary.get('currency')
    currency = 'BRL' if norm(currency) in ['brl', 'r$', 'real', 'reais'] else currency
    text = norm(description)
    days = re.search(r'(\d)\s*dias?\s*(?:presencia|no escritorio|por semana)', text)
    pt_explicit = bool(re.search(r'(?:idioma|lingua|trabalho|comunicacao).{0,35}portugues|portugues.{0,25}(?:fluente|nativo|obrigatorio)', text))
    job = classify({
        'id': 'remotar-' + str(raw['id']), 'title': raw['title'],
        'company': raw.get('companyDisplayName') or (raw.get('company') or {}).get('name') or 'Empresa não informada',
        'url': 'https://remotar.com.br/job/' + str(raw['id']),
        'applyUrl': raw.get('externalLink') if str(raw.get('externalLink', '')).startswith('https://') else 'https://remotar.com.br/job/' + str(raw['id']),
        'source': 'Remotar', 'sourceSystem': raw.get('integrationSource'),
        'publishedAt': raw.get('createdAt'), 'checkedAt': now,
        'workMode': {'remote': 'remote', 'hybrid': 'hybrid', 'onsite': 'onsite', 'in-person': 'onsite'}.get(raw.get('type'), 'unknown'),
        'city': raw.get('city'), 'officeDays': int(days[1]) if days else None,
        'salary': {'min': number(salary.get('from')), 'max': number(salary.get('to')), 'currency': currency, 'period': period, 'sourceType': salary.get('type')},
        'portugueseConfirmed': pt_explicit, 'adLanguage': 'pt-BR' if any(w in text for w in ['experiencia', 'responsabilidades', 'requisitos']) else 'unknown',
        'requiresEnglish': any('ingles' in norm(t) for t in tags) or bool(re.search(r'ingles\s+(?:avancado|fluente|obrigatorio)|english\s+(?:required|fluent)|fluencia em ingles', text)),
        'tags': tags, 'description': description[:16000],
        'active': bool(raw.get('active')) and not raw.get('expired', False),
        'recruiterUrl': None, 'applicationStatus': 'not_applied',
        'applicationNote': 'Aguardando validação dos requisitos e acesso à conta da candidata.'
    })
    # Publish a short excerpt, linking to the complete source description.
    job['description'] = description[:650] + ('…' if len(description) > 650 else '')
    return job

def main():
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    path = ROOT / 'data' / 'jobs.json'
    old = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'jobs': [], 'runs': []}
    jobs = {j['id']: j for j in old['jobs']}
    override_path = ROOT / 'data' / 'verified.json'
    overrides = json.loads(override_path.read_text(encoding='utf-8')) if override_path.exists() else {}
    errors, fetched = [], set()
    pages = 0
    for query in CONFIG['queries']:
        try:
            for page in range(1, 4):
                url = 'https://api.remotar.com.br/jobs?' + urllib.parse.urlencode({'search': query, 'page': page, 'active': 'true'})
                payload = get_json(url)
                if not isinstance(payload.get('data'), list): raise ValueError('Formato da fonte mudou')
                pages += 1
                for raw in payload['data']:
                    if not re.search(r'design|diretor.*arte|branding', norm(raw.get('title'))): continue
                    job = convert(raw, now)
                    previous = jobs.get(job['id'], {})
                    for key in ['applicationStatus', 'applicationNote', 'applicationEvidence', 'recruiterUrl', 'contactStatus', 'contactEvidence']:
                        if key in previous: job[key] = previous[key]
                    job['firstSeenAt'] = previous.get('firstSeenAt', now)
                    jobs[job['id']] = job
                    fetched.add(job['id'])
                if page >= payload.get('meta', {}).get('last_page', 1): break
                time.sleep(.6)
        except Exception as exc:
            errors.append({'source': 'Remotar', 'query': query, 'error': type(exc).__name__})
    for job_id, override in overrides.items():
        if job_id not in jobs: continue
        job = jobs[job_id]
        job['verification'] = override
        job['applicationNote'] = override['note']
        if override.get('closed'):
            job['active'] = False
            job['eligibility'] = 'excluded'
            job['rejectionReasons'] = list(dict.fromkeys(job['rejectionReasons'] + ['Inscrições encerradas na página original']))
    run = {'at': now, 'fetched': len(fetched), 'pages': pages, 'errors': errors, 'status': 'failed' if not pages else ('partial' if errors else 'success')}
    result = {'updatedAt': now, 'lastSuccessAt': now if not errors else old.get('lastSuccessAt'),
              'coverage': 'Remotar: até 3 páginas por termo. Outras fontes: pesquisa assistida pelo Codex.',
              'jobs': sorted(jobs.values(), key=lambda j: (j['eligibility'] == 'excluded', -j['score'], j.get('publishedAt') or '' )),
              'runs': ([run] + old.get('runs', []))[:30]}
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(run))
    if not pages: raise SystemExit(1)

if __name__ == '__main__': main()
