# Radar de oportunidades — Thaiane Siao

Painel público de vagas para design gráfico, direção de arte, branding, campanhas e editorial.

Site: https://thaianegsilva-svg.github.io/thaiane-job-tracker/

## Critérios

- Remuneração **mensal em BRL estritamente acima de R$ 7.000**. Faixa que cruza o limite exige confirmação.
- Remoto ou híbrido **somente em Belo Horizonte, até 2 dias presenciais/semana**.
- Trabalho em português. Anúncio em português, sozinho, não confirma o idioma de trabalho.
- Avaliação de todas as exigências da vaga antes de envio; UX/produto não é presumido como especialidade da candidata.

Perfil público: [LinkedIn](https://www.linkedin.com/in/thaiane-siao/) e [Behance](https://www.behance.net/thaianesilva3). Currículo e dados de contato ficam fora deste repositório público.

## O que funciona

O workflow `radar.yml` coleta metadados públicos da Remotar (até três páginas para cada termo em `config.json`), classifica, preserva histórico e publica no GitHub Pages. Executa diariamente às **15:00 UTC = 12:00 America/Sao_Paulo** e em push/manual. O GitHub pode atrasar ou suspender agendas por inatividade; consulte Actions. A coleta usa o endpoint público usado pela própria listagem. Mudanças no provedor são exibidas como falha/parcial, sem apagar registros anteriores.

Uma automação assistida do Codex complementa a pesquisa nas outras fontes, revisa requisitos e tenta os envios autorizados quando houver acesso e dados suficientes. Ela depende do computador ligado e do Codex em execução. A coleta do GitHub funciona independentemente do computador.

**O GitHub Pages é estático:** não contém credenciais nem envia candidaturas ou mensagens por conta própria. Botões abrem a candidatura e preparam uma mensagem para solicitar os dados faltantes. Só registrar `applied` ou `contacted` compartilhado quando houver evidência real do envio. Nunca confundir geração de mensagem com envio.

## Acompanhamento

- Busca, modalidade, aderência/recência, favoritos, detalhes e etapas de candidatura.
- Notas, favoritos e etapas manuais são salvos **no navegador**, sem sincronização automática entre dispositivos. Exportação/importação JSON permite backup e transferência.
- Atualizar painel consulta o último JSON publicado; não inicia uma coleta no servidor. Para coletar imediatamente, execute o workflow em Actions.
- `data/jobs.json` guarda registros compartilhados de coleta/ações verificadas. Não publicar telefone, endereço, currículo, e-mail pessoal, credenciais nem conteúdo privado de conversas.
- `data/verified.json` preserva verificações assistidas da página original, incluindo seleções encerradas que o agregador ainda divulga. Remover ou revisar uma marca de encerramento somente com evidência nova da fonte original.
- `data/assisted.json` contém vagas revisadas manualmente no LinkedIn e respectivos estados verificados. Atualizar o registro neste arquivo para persistir novas respostas ou candidaturas; o coletor o incorpora a cada execução. Datas relativas do anúncio são aproximadas; a data da consulta é explícita. Conversas e comprovantes privados permanecem em `.private/` (ignorado pelo Git).
- `score` é uma heurística por sinais de ferramentas e especialidades, **não uma probabilidade de contratação**. Sempre conferir todos os requisitos no anúncio original.
- Vagas fora dos critérios ficam automaticamente com etapa **Encerrada** no acompanhamento. O motivo e o histórico de contatos são preservados; isso não significa que a empresa encerrou as inscrições.
- Resultados não revisitados há 48h ficam desatualizados. Uma vaga ainda listada pela fonte pode já estar encerrada na empresa; validar na candidatura.

## Fontes priorizadas

1. [Remotar](https://remotar.com.br/): foco em remoto e categorias Design/Marketing, agregando páginas de empresas e ATS.
2. [trampos](https://trampos.co/): criação, design e marketing, útil para direção de arte e branding.
3. [LinkedIn Jobs](https://www.linkedin.com/jobs/): cobertura ampla e descoberta de recrutadores; requer conta correta para candidatura.
4. [Gupy](https://portal.gupy.io/): fonte original de várias empresas brasileiras; requisitos e formulários variam.
5. [99jobs](https://www.99jobs.com/): complemento de empresas brasileiras, com conferência de senioridade/modalidade.
6. [Behance Jobs](https://www.behance.net/joblist?locale=pt_BR): ampliação diária para criação, branding e direção de arte, priorizando anúncios do Brasil e contratos recorrentes.
7. [Indeed Brasil](https://br.indeed.com/q-designer-gr%C3%A1fico-l-remoto-vagas.html): ampliação diária para anúncios brasileiros; conferir a empresa original e remover duplicatas e ofertas expiradas.
8. [Domestika Jobs](https://www.domestika.org/pt/jobs/full_time/where/remote/forever): consulta complementar por disciplinas criativas. A interface em português não confirma o idioma ou a localização do trabalho.
9. [Remotive Design](https://remotive.com/remote-jobs/design): consulta complementar com filtros de localização e idioma, limitada a informações públicas. Não contratar plano pago sem autorização.

Behance e Indeed foram incorporados à pesquisa assistida em 26/10/2026. Domestika e Remotive têm prioridade menor para esta busca por sua cobertura internacional. A coleta automática continua restrita à Remotar; incluir um site nesta lista não cria integração ou candidatura automática. Vagas repetidas, como a BR2 encontrada em Behance e Indeed, preservam um único acompanhamento na página original da empresa.

As prioridades são uma avaliação de aderência, não um ranking absoluto. Fontes além da Remotar exigem pesquisa assistida; o painel distingue a cobertura.

## Executar localmente

```text
python -m unittest discover -s tests -v
python scripts/collect.py
python -m http.server 4174 --bind 127.0.0.1
```

Não há dependências Python externas. JavaScript sem build. Ações oficiais de Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Procedimento diário assistido

1. Sincronizar `main` sem sobrescrever alterações locais. Conferir execução e cobertura do coletor.
2. Consultar os comprovantes privados em `.private/*-contact.json` e verificar respostas na conta correta, sem reenviar solicitações já registradas. Nunca publicar os comprovantes ou links das conversas.
3. Pesquisar as fontes de `config.json`, incluindo Behance Jobs e Indeed Brasil além das cinco fontes iniciais; consultar Domestika e Remotive como complemento. Validar anúncios originais dos cargos em português. Deduplicar pelo link original/empresa/cargo; não inventar vagas, salário ou contato.
4. Revalidar modalidade, BH/dias, salário fixo mensal em reais, idioma, atividade da vaga e todos os requisitos obrigatórios contra o currículo privado.
5. Quando faltar salário, idioma ou dias presenciais, procurar o recrutador identificado no anúncio. Enviar uma pergunta objetiva somente por canal verificado e com a identidade real do remetente; mencionar que está auxiliando a candidata se a conta for de outra pessoa. Sem contato verificável, registrar bloqueio, sem adivinhar e-mail.
6. Tentar candidatar apenas com dados verdadeiros e a conta da candidata. Não responder perguntas pessoais desconhecidas nem aceitar termos/compromissos em nome dela. Interromper no ponto que exigir intervenção humana.
7. Registrar envio somente com protocolo, URL ou evidência verificável. Comprovantes privados ficam privados. Publicar apenas situação e referência pública, sem conteúdo de mensagens.
8. Atualizar `data/jobs.json`, validar, fazer commit/push e conferir deploy. Notificar somente novas oportunidades relevantes, envios, falhas ou ação necessária.
