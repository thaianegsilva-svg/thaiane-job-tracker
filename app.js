'use strict';
const $ = s => document.querySelector(s);
const esc = v => String(v ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeUrl = value => { try { const u=new URL(value); return u.protocol==='https:' ? esc(u.href) : '#'; } catch { return '#'; } };
const fold = s => String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const formatDate = s => s ? new Date(s).toLocaleString('pt-BR',{timeZone:'America/Sao_Paulo',dateStyle:'short',timeStyle:'short'}) : 'Não disponível';
const money = n => new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL',maximumFractionDigits:0}).format(n);
const statuses={not_applied:'Não enviada',preparing:'Em preparação',contacted:'Contato realizado',applied:'Candidatura enviada',interview:'Entrevista',closed:'Encerrada'};
const key='thaiane-job-tracker-v1';
let local={};try{local=JSON.parse(localStorage.getItem(key)||'{}');if(!local||Array.isArray(local)||typeof local!=='object')local={};}catch{}
let payload={jobs:[],runs:[]},config={},tab='focus',openedId=null;
function saveLocal(){try{localStorage.setItem(key,JSON.stringify(local));}catch{$('#feedback').textContent='Não foi possível salvar neste navegador. Exporte seu acompanhamento.';}}
const state=j=>({...j,...(local[j.id]||{})});
const stale=j=>Date.now()-new Date(j.checkedAt).getTime()>48*60*60*1000;
function salary(j){const s=j.salary||{}; if(s.min==null&&s.max==null)return 'Salário não divulgado';if(s.currency!=='BRL')return 'Moeda / remuneração a confirmar';return `${s.min!=null?money(s.min):'Até'}${s.max!=null&&s.max!==s.min?' – '+money(s.max):''}${s.period==='monthly'?' / mês':' · período a confirmar'}`;}
function render(){
  const all=payload.jobs.map(state),focus=all.filter(j=>j.eligibility!=='excluded'&&j.active);
  $('#count-all').textContent=focus.length;$('#count-eligible').textContent=focus.filter(j=>j.eligibility==='eligible'&&!stale(j)).length;$('#count-pending').textContent=focus.filter(j=>j.eligibility==='pending').length;$('#count-applied').textContent=all.filter(j=>['applied','interview'].includes(j.applicationStatus)).length;
  const search=fold($('#search').value),mode=$('#mode').value;
  let jobs=all.filter(j=>{
    if(tab==='focus'&&(j.eligibility==='excluded'||!j.active))return false;
    if(tab==='eligible'&&(j.eligibility!=='eligible'||stale(j)||!j.active))return false;
    if(tab==='pending'&&(j.eligibility!=='pending'||!j.active))return false;
    if(tab==='excluded'&&j.eligibility!=='excluded'&&j.active)return false;
    if(tab==='saved'&&!j.saved)return false;
    if(tab==='applied'&&!['applied','interview'].includes(j.applicationStatus))return false;
    if(mode!=='all'&&j.workMode!==mode)return false;
    if(mode==='hybrid'&&fold(j.city)!=='belo horizonte')return false;
    return fold([j.title,j.company,...(j.signals||[])].join(' ')).includes(search);
  });
  jobs.sort($('#sort').value==='recent'?(a,b)=>new Date(b.publishedAt)-new Date(a.publishedAt):(a,b)=>b.score-a.score||new Date(b.publishedAt)-new Date(a.publishedAt));
  $('#results').textContent=`${jobs.length} ${jobs.length===1?'oportunidade encontrada':'oportunidades encontradas'} · Aderência é um índice de sinais do perfil, não uma garantia de elegibilidade.`;
  $('#jobs').innerHTML=jobs.length?jobs.map(j=>`<article class="job"><div class="job-top"><div class="company"><span class="company-icon" aria-hidden="true">${esc(j.company.slice(0,2).toUpperCase())}</span><span>${esc(j.company)}</span></div><button class="save" data-save="${esc(j.id)}" aria-label="${j.saved?'Remover dos favoritos':'Salvar vaga'}" aria-pressed="${!!j.saved}">${j.saved?'★':'☆'}</button></div><h3>${esc(j.title)}</h3><p class="subtitle">${esc(salary(j))}</p><div class="tags"><span class="tag">${j.workMode==='remote'?'Remoto':j.workMode==='hybrid'?'Híbrido · '+esc(j.city||'Cidade a confirmar'):'Modalidade a conferir'}</span><span class="tag purple">${esc(j.score)} / 100 · aderência</span><span class="tag ${j.eligibility==='eligible'?'green':j.eligibility==='excluded'?'rose':'purple'}">${j.eligibility==='eligible'?'Critérios confirmados':j.eligibility==='excluded'?'Fora dos critérios':'Informações pendentes'}</span>${stale(j)?'<span class="tag rose">Verificação há mais de 48h</span>':''}</div><p class="signal">${j.signals?.length?'Conexões: '+esc(j.signals.slice(0,4).join(' · ')):'Confira requisitos e portfólio solicitado na fonte original.'}</p><div class="status">${j.rejectionReasons?.length?esc(j.rejectionReasons.join(' · ')):j.missing?.length?'Confirmar: '+esc(j.missing.join(' · ')):'Requisitos objetivos atendidos; revisar exigências específicas.'}<br><strong>${esc(statuses[j.applicationStatus]||'Não enviada')}</strong> · Fonte: ${esc(j.source)}</div><div class="job-actions"><button class="button outline" data-detail="${esc(j.id)}">Detalhes e acompanhamento ↗</button><a href="${safeUrl(j.applyUrl||j.url)}" target="_blank" rel="noopener noreferrer" class="text-button">Ver vaga ↗</a></div></article>`).join(''):'<div class="empty"><strong>Nenhuma vaga nesta seleção.</strong><p>As oportunidades aparecem quando atendem ao filtro escolhido.<br>Vagas com salário ou idioma desconhecidos ficam em “A confirmar”.</p></div>';
}
function message(j){const list=j.missing?.length?j.missing.join('; '):'a disponibilidade da vaga e os próximos passos';return `Olá! Estou acompanhando a oportunidade de ${j.title} na ${j.company} (${j.url}). Poderia, por gentileza, confirmar ${list}? Buscamos trabalho em português, com remuneração mensal fixa acima de R$ 7.000, remoto ou híbrido em Belo Horizonte com até dois dias presenciais por semana. Obrigado(a)!`;}
function detail(id){
  openedId=id;const j=state(payload.jobs.find(j=>j.id===id));
  $('#detail-body').innerHTML=`<span class="eyebrow">${esc(j.company)} / ${esc(j.source)}</span><h2>${esc(j.title)}</h2><p><strong>${esc(salary(j))}</strong> · ${j.workMode==='remote'?'Remoto':j.workMode==='hybrid'?'Híbrido':'Modalidade a confirmar'}</p><p>${esc(j.description||'Consulte o anúncio original para ver a descrição completa.')}</p><p>Publicado: ${formatDate(j.publishedAt)}<br>Última consulta: ${formatDate(j.checkedAt)}<br>Idioma do anúncio: ${j.adLanguage==='pt-BR'?'Português':'Não confirmado'} · Idioma do trabalho: ${j.portugueseConfirmed?'Português confirmado':'A confirmar'}</p><h3>O que falta conferir</h3><ul>${(j.rejectionReasons?.length?j.rejectionReasons:j.missing?.length?j.missing:['Revisar todos os requisitos específicos da vaga original.']).map(m=>`<li>${esc(m)}</li>`).join('')}</ul><p>${esc(j.applicationNote||'Envio assistido depende do acesso correto à conta da candidata.')}</p>${j.applicationEvidence?`<p>Comprovante: ${esc(j.applicationEvidence)}</p>`:''}<div class="dialog-links"><a class="button" target="_blank" rel="noopener noreferrer" href="${safeUrl(j.applyUrl||j.url)}">Abrir candidatura ↗</a><a class="button outline" target="_blank" rel="noopener noreferrer" href="${safeUrl(j.url)}">Fonte original ↗</a>${j.recruiterUrl?`<a class="button outline" href="${safeUrl(j.recruiterUrl)}" target="_blank" rel="noopener noreferrer">Contato verificado ↗</a>`:''}</div><label for="message">Mensagem para solicitar informações</label><textarea id="message" readonly>${esc(message(j))}</textarea><button class="button outline" id="copy-message">Copiar mensagem</button><p id="copy-status" role="status">${j.recruiterUrl?'Abra o contato verificado para enviar.':'Recrutador ainda não identificado. Nenhuma mensagem foi enviada por este site.'}</p><label for="stage">Etapa do acompanhamento (registro manual neste navegador)</label><select id="stage">${Object.entries(statuses).map(([value,label])=>`<option value="${value}" ${j.applicationStatus===value?'selected':''}>${label}</option>`).join('')}</select><label for="notes">Notas privadas neste navegador</label><textarea id="notes" placeholder="Próximos passos e lembretes…">${esc(j.notes||'')}</textarea><button class="button" id="save-note">Salvar acompanhamento</button><p id="note-status" role="status"></p>`;
  $('#copy-message').onclick=async()=>{try{await navigator.clipboard.writeText($('#message').value);$('#copy-status').textContent='Mensagem copiada. Envie pelo canal do recrutador.';}catch{$('#message').select();$('#copy-status').textContent='Selecione e copie a mensagem acima.';}};
  $('#save-note').onclick=()=>{local[id]={...local[id],applicationStatus:$('#stage').value,notes:$('#notes').value.slice(0,10000),updatedAt:new Date().toISOString()};saveLocal();render();$('#note-status').textContent='Acompanhamento salvo neste navegador.';};
  if(!$('#detail').open)$('#detail').showModal();
}
async function load(){
  $('#refresh').disabled=true;$('#sync').textContent='Consultando última coleta…';
  try{
    const responses=await Promise.all([fetch('data/jobs.json?t='+Date.now(),{cache:'no-store'}),fetch('config.json')]);
    if(responses.some(r=>!r.ok))throw Error('Dados indisponíveis');
    [payload,config]=await Promise.all(responses.map(r=>r.json()));
    if(!Array.isArray(payload.jobs))throw Error('Formato inválido');
    const outdated=Date.now()-new Date(payload.updatedAt).getTime()>48*60*60*1000;
    $('#sync').textContent=`${outdated?'⚠ Dados desatualizados. ':''}Última coleta: ${formatDate(payload.updatedAt)} · ${payload.runs[0]?.status==='success'?'Concluída':payload.runs[0]?.status==='partial'?'Parcial; confira atividade':'Falha; confira atividade'}`;
    $('#coverage').textContent=payload.coverage;
    $('#sources').innerHTML=config.sources.map(s=>`<article class="source"><span class="eyebrow">PRIORIDADE ${esc(s.priority)} · ${esc(s.mode)}</span><h3>${esc(s.name)}</h3><p>${esc(s.reason)}</p><a href="${safeUrl(s.url)}" target="_blank" rel="noopener noreferrer">Explorar vagas ↗</a></article>`).join('');
    $('#runs').innerHTML=payload.runs.slice(0,7).map(r=>`<div class="run ${r.errors.length?'run-error':''}"><span>${formatDate(r.at)}</span><strong>${r.status==='success'?'Coleta concluída':r.status==='partial'?'Coleta parcial':'Coleta falhou'}</strong><span>${r.fetched} vagas consultadas · ${r.pages} páginas${r.errors.length?' · '+r.errors.length+' falha(s)':''}</span></div>`).join('');
    render();
  }catch{ $('#sync').textContent='Não foi possível carregar as vagas. Tente atualizar o painel.';$('#jobs').innerHTML='<div class="empty"><strong>Os dados estão indisponíveis.</strong><p>Atualize o painel ou consulte a atividade no GitHub.</p></div>'; }
  finally{$('#refresh').disabled=false;}
}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{tab=b.dataset.tab;document.querySelectorAll('[data-tab]').forEach(t=>{t.classList.toggle('active',t===b);t.setAttribute('aria-pressed',String(t===b));});render();});
['search','mode','sort'].forEach(id=>$('#'+id).addEventListener(id==='search'?'input':'change',render));
$('#jobs').onclick=e=>{const save=e.target.closest('[data-save]'),button=e.target.closest('[data-detail]');if(save){const id=save.dataset.save;local[id]={...local[id],saved:!local[id]?.saved};saveLocal();render();}if(button)detail(button.dataset.detail);};
$('#refresh').onclick=load;
$('#export').onclick=()=>{const blob=new Blob([JSON.stringify({version:1,exportedAt:new Date().toISOString(),records:local},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='thaiane-acompanhamento.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('#import').onchange=async e=>{try{const file=e.target.files[0];if(!file)return;if(file.size>2e6)throw Error();const data=JSON.parse(await file.text());if(data.version!==1||!data.records||typeof data.records!=='object'||Array.isArray(data.records))throw Error();for(const [id,record] of Object.entries(data.records)){if(!/^[a-z0-9-]+$/i.test(id)||!record||typeof record!=='object')continue;local[id]={saved:record.saved===true,notes:String(record.notes||'').slice(0,10000),applicationStatus:Object.hasOwn(statuses,record.applicationStatus)?record.applicationStatus:'not_applied'};}saveLocal();render();$('#feedback').textContent='Acompanhamento importado neste navegador.';}catch{$('#feedback').textContent='Arquivo inválido. Use uma exportação deste painel (até 2 MB).';}e.target.value='';};
load();
