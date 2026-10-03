# Fieldwork | B2B Lead Operations

Projeto de portfólio implementado em 29/09/2026. **B2B** significa que o possível comprador é uma empresa. Aqui, o cenário é um software de agendamento que pesquisa empresas de beleza, barbearia e bem-estar na África do Sul.

## O que foi realmente feito

- Pesquisa de **10 empresas reais**, em páginas públicas oficiais, com URL e observação por linha. São **contas candidatas**, ainda não leads de venda verificados.
- Duas linhas duplicadas foram inseridas intencionalmente para demonstrar a fila de qualidade. O arquivo original tem 12 linhas; a exportação limpa tem 10 contas.
- `lead_ops.py` lê o CSV original e gera pesquisa enriquecida, fila de exceções, rascunho de importação de contas para CRM, hipóteses de campanha e manifesto com hash do arquivo de entrada.
- `Fieldwork_B2B_Lead_Operations.xlsx` apresenta painel, entrada preservada, fila com fórmulas, plano de marketing e método com as fontes.
- Campos de comprador e necessidade permanecem como **não verificados**. Não houve coleta de email pessoal, envio de mensagens ou resultado de vendas.

## Executar a automação

Requer Python 3.10 ou mais recente. Usa apenas a biblioteca padrão.

```bash
python lead_ops.py source_accounts.csv generated
```

No Windows, se `python` não estiver disponível, use `py lead_ops.py source_accounts.csv generated`.

Arquivos produzidos:

1. `01_account_research.csv` - todas as linhas com score, status e próximo passo.
2. `02_review_queue.csv` - exceções que precisam de revisão humana.
3. `03_crm_account_draft.csv` - somente contas únicas; **rascunho**, sem contato verificado.
4. `04_campaign_hypotheses.csv` - segmentos e mensagens para validar.
5. `05_run_manifest.json` - contagens, escopo e SHA-256 da fonte.
6. `06_records.json` - saída estruturada para outras integrações.

O Excel entregue é a apresentação interativa da execução de exemplo. Editar a aba **Source Intake** recalcula a fila e o painel dentro da própria planilha. Para gerar novos CSVs, edite `source_accounts.csv` e rode o comando acima. A pontuação prioriza **pesquisa**, não mede interesse de compra.

## Como este projeto cobre as habilidades

| Habilidade | Evidência no projeto |
|---|---|
| Lead generation | definição de mercado, pesquisa de empresas, links de fonte e priorização de contas |
| Data entry | contrato de campos, entrada preservada e saída estruturada |
| Excel automatizado | fórmulas, flags de duplicidade, painel e contagem por segmento |
| CRM | rascunho de importação de contas com gate de qualidade |
| B2B marketing | segmento, hipótese de mensagem, canal, métrica e plano de capacidade |

## Regras de confiança

Os sites mudam. Verifique novamente cada empresa e confirme pessoa compradora, necessidade, autorização e formato do CRM antes de usar dados em uma campanha real. Sites com agendamento próprio ou outra plataforma foram marcados como oportunidade de integração a investigar; o projeto não presume que precisem de substituição.

**Fontes públicas oficiais:** Barber Club, being, Sorbet, Perfect 10, Camelot Spa, Life Day Spa, Legends Barber, Sirina Thai Spa, Hair City e Hermanos. As URLs por registro estão na aba **Source Intake** e no arquivo `source_accounts.csv`.
