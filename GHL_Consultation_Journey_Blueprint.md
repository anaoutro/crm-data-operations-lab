# GoHighLevel | Aura Client Journey

**Estado:** especificação, amostra e textos prontos; não implementado dentro de um sub-account HighLevel nesta sessão. Não apresentar como automação ativa.

## Objetivo comercial

Uma marca fictícia de bem-estar recebe pedidos de consulta através de um formulário e precisa registrar origem, qualificar o interesse, agendar atendimento e acompanhar o funil. O conceito visual **Aura** foi criado em Figma; o CRM abaixo usa a mesma marca para formar um caso coerente.

## Estrutura proposta

**Pipeline:** New inquiry → Needs review → Consultation booked → Proposal → Won / Lost.

**Campos de contato:** Service Interest (Ritual / Corporate Wellness / Other), Preferred City, Requested Date, Marketing Consent (Yes/No), Lead Source, Follow-up Owner.

**Campos de oportunidade:** Service Package, Estimated Value (somente após proposta real), Consultation Date, Qualification Notes. O valor inicial fica vazio.

**Tags:** `AURA_DEMO` em registros sintéticos; `AURA_WEB_INQUIRY` em formulários reais; `AURA_CONSENT_YES` somente quando a escolha explícita estiver registrada.

## Formulário

Nome, email, cidade, interesse, data preferida, contexto em texto livre e uma opção separada de consentimento de marketing. Texto do botão: **Request a consultation**. O formulário não promete reserva automática; confirma apenas o recebimento da solicitação.

## Workflow 01 | Intake and review

**Trigger:** Form Submitted, formulário Aura Consultation.

1. Criar oportunidade em New inquiry, evitando duplicar uma oportunidade aberta do mesmo contato.
2. Salvar origem e interesse. Criar tarefa interna para revisar o pedido.
3. Se faltar contexto ou houver duplicata, manter Needs review e atribuir a um responsável.
4. Se a pessoa marcou consentimento, registrar a tag correspondente. O consentimento deve ser verificável.
5. Não ativar envio automático até testar o formulário, descadastro, fuso horário e remetente dentro da conta.

## Workflow 02 | Consultation

**Trigger:** agendamento confirmado no calendário correto.

1. Mover oportunidade para Consultation booked.
2. Criar tarefa de preparação com interesse e contexto.
3. Enviar confirmação apenas quando canal, remetente e autorização estiverem configurados. Parar sequências de convite redundantes.
4. Após a consulta, uma pessoa decide se há proposta. Não mover automaticamente para Won.

## Qualidade e teste

- Importar os 8 registros de `ghl_contacts_demo.csv` apenas em um sub-account de teste, com emails `.example` e `Marketing Consent=No`.
- Deixar workflows de mensagens desativados até uma revisão; não gerar custos de SMS.
- Testar cada ramificação com dados sintéticos, capturar tela do formulário, pipeline e execução de workflow.
- Criar Snapshot somente depois de construir e validar o sub-account. O Snapshot guarda configuração, mas não contatos ou conversas.

Referências oficiais: [pipelines e oportunidades](https://help.gohighlevel.com/support/solutions/articles/155000005062), [Create Opportunity em workflow](https://help.gohighlevel.com/support/solutions/articles/155000004752-workflow-action-create-opportunity), [campos personalizados](https://help.gohighlevel.com/support/solutions/articles/155000008031-how-to-use-custom-fields), [Snapshots](https://help.gohighlevel.com/support/solutions/articles/48000982512-creating-new-snapshots-in-highlevel).
