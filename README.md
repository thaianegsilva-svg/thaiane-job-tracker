# Radar de oportunidades — Thaiane Siao

Painel público de vagas para design gráfico, direção de arte, branding, campanhas e editorial.

Site: https://thaianegsilva-svg.github.io/thaiane-job-tracker/

## Critérios

- Vagas sem salário divulgado podem seguir para candidatura. Quando houver remuneração divulgada, ela deve ser **mensal em BRL e estritamente acima de R$ 7.000**; faixa que cruza o limite exige confirmação.
- Remoto ou híbrido **somente em Belo Horizonte, até 2 dias presenciais/semana**.
- Idioma não divulgado não bloqueia a candidatura. Exigências explícitas de proficiência continuam sendo avaliadas contra o currículo.
- Avaliação de todas as exigências da vaga antes de envio; UX/produto não é presumido como especialidade da candidata.

Perfil público: [LinkedIn](https://www.linkedin.com/in/thaiane-siao/) e [Behance](https://www.behance.net/thaianesilva3). Currículo e dados de contato ficam fora deste repositório público.

## O que funciona

O workflow `radar.yml` coleta metadados públicos da Remotar (até três páginas para cada termo em `config.json`), classifica, preserva histórico e publica no GitHub Pages. Executa diariamente às **15:00 UTC = 12:00 America/Sao_Paulo** e em push/manual. O GitHub pode atrasar ou suspender agendas por inatividade; consulte Actions. A coleta usa o endpoint público usado pela própria listagem. Mudanças no provedor são exibidas como falha/parcial, sem apagar registros anteriores.

Uma automação assistida do Codex complementa a pesquisa nas outras fontes, revisa requisitos e tenta os envios autorizados quando houver acesso e dados suficientes. Ela depende do computador ligado e do Codex em execução. A coleta do GitHub funciona independentemente do computador.

**O GitHub Pages é estático:** não contém credenciais nem envia candidaturas ou mensagens por conta própria. Botões abrem a candidatura e preparam uma apresentação profissional. Só registrar `applied` ou `contacted` compartilhado quando houver evidência real do envio. Nunca confundir geração de mensagem com envio.

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
8. [Glassdoor Brasil](https://www.glassdoor.com.br/): vagas brasileiras e informações sobre empresas. Estimativas salariais não comprovam o salário oferecido pela empresa; deduplicar com outros portais.
9. [Catho](https://www.catho.com.br/vagas/designer-grafico/): design gráfico e criação no Brasil; verificar modalidade e remuneração na vaga individual. Registrar bloqueios de leitura ou login sem contorná-los.
10. [InfoJobs](https://www.infojobs.com.br/vagas-de-designer-grafico-trabalho-home-office.aspx): busca brasileira de design em home office; separar trabalho recorrente de projetos por demanda.
11. [Vagas.com](https://www.vagas.com.br/vagas-de-designer): anúncios de empresas brasileiras, com filtros de remoto/híbrido e conferência da especialidade e senioridade.
12. [Empregos.com.br](https://www.empregos.com.br/): complemento nacional; resultados amplos exigem conferir cargo, modalidade e anúncio original.
13. [Domestika Jobs](https://www.domestika.org/pt/jobs/full_time/where/remote/forever): consulta complementar por disciplinas criativas. A interface em português não confirma o idioma ou a localização do trabalho.
14. [Remotive Design](https://remotive.com/remote-jobs/design): consulta complementar com filtros de localização e idioma, limitada a informações públicas. Não contratar plano pago sem autorização.
15. [MeuHome Design](https://www.meuhome.com.br/vagas/design): reúne vagas brasileiras de design coletadas dos portais oficiais das empresas e informa atualização diária.
16. [Robô de Vagas — Design](https://app.robodevagas.com.br/vagas-remotas/design): fonte complementar brasileira atualizada ao longo do dia; filtrar a categoria ampla para design gráfico, branding, campanhas e editorial.
17. [Remote Rocketship](https://www.remoterocketship.com/br/vagas/designer-grafico/): agregador internacional com filtros por Brasil, nível e salário; validar sempre o anúncio original e os critérios de idioma e moeda.

Behance e Indeed foram incorporados à pesquisa assistida em 26/10/2026. MeuHome, Robô de Vagas e Remote Rocketship foram adicionados em 03/11/2026 após avaliação de cobertura, atualização e acesso ao anúncio original. Domestika, Remotive e Remote Rocketship têm prioridade menor quando a oferta é internacional. Workana não entrou na rotina principal porque prioriza projetos freelance, e Jooble ficou fora por ser um agregador amplo com maior risco de duplicação. A coleta automática continua restrita à Remotar; incluir um site nesta lista não cria integração ou candidatura automática. Vagas repetidas preservam um único acompanhamento na página original da empresa.

As prioridades são uma avaliação de aderência, não um ranking absoluto. Fontes além da Remotar exigem pesquisa assistida; o painel distingue a cobertura.

Glassdoor, Catho, InfoJobs, Vagas.com e Empregos.com.br foram acrescentados em 26/10/2026 após a revisão dos sites sugeridos pelo usuário. ZipRecruiter, Monster e CareerBuilder não entraram na rotina principal: os resultados consultados têm menor aderência à exigência de trabalho em português, contratação a partir do Brasil e salário fixo em reais. Isso não caracteriza esses sites como inválidos; podem ser revisitados se aparecer uma oportunidade que confirme todos os critérios. Usar os domínios oficiais em HTTPS, sem os redirecionamentos de segurança do LinkedIn.

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
3. Pesquisar as fontes de `config.json`: Remotar, trampos, LinkedIn, Gupy, 99jobs, Behance, Indeed, Glassdoor, Catho, InfoJobs, Vagas.com, MeuHome e Robô de Vagas; consultar Empregos.com.br, Domestika, Remotive e Remote Rocketship como complemento. Validar anúncios originais dos cargos em português. Deduplicar pelo link original/empresa/cargo; não inventar vagas, salário ou contato. Não usar médias ou estimativas de mercado como salário confirmado da vaga.
4. Revalidar modalidade, BH/dias, atividade da vaga e todos os requisitos obrigatórios contra o currículo privado. Não exigir confirmação do idioma quando ele estiver ausente; exigências explícitas de proficiência continuam sendo avaliadas. Salário ausente não bloqueia; salário divulgado precisa ser fixo mensal em reais e estritamente acima de R$ 7.000.
5. Para cada vaga aderente com salário ausente ou suficiente, criar em `.private/` um currículo DOCX específico e compatível com ATS, partindo do currículo mestre em `.private/curriculo-ats/`. Usar somente fatos comprovados, adaptar resumo, título, competências e palavras-chave ao anúncio e renderizar para verificar a diagramação antes do envio. Nunca versionar ou publicar o currículo.
6. Tentar candidatar com o currículo específico, dados verdadeiros e a conta correta da candidata. Não inventar respostas pessoais, contornar CAPTCHA nem aceitar novos termos ou compromissos em nome dela; interromper no ponto que exigir intervenção humana.
7. Quando houver recrutador ou canal institucional verificado, enviar uma apresentação profissional curta depois da candidatura, com a identidade real da remetente e referência à vaga. Não inventar destinatário, não reenviar mensagem duplicada e não usar conta de terceiros como se fosse Thaiane.
8. Registrar candidatura e contato somente com protocolo, URL ou evidência verificável. Comprovantes, mensagens e currículos ficam privados. Publicar apenas situação e referência pública.
9. Atualizar `data/jobs.json`, validar, fazer commit/push e conferir deploy. Notificar somente novas oportunidades relevantes, envios, falhas ou ação necessária.
