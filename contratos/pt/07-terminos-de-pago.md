# Termos de Pagamento

> Modelo a ser revisado por um advogado e pelo contador (impostos e faturamento). Anexo comum do Contrato de Prestação de Serviços, SOWs, Manutenção e Propostas.

## 1. Moeda

Os preços são expressos em **{{moneda_nombre}} ({{moneda}})**, conforme a proposta ou o SOW (por padrão dólares americanos; também pesos uruguaios ou reais). Se for faturado em outra moeda, usa-se a taxa de câmbio {{fuente_tipo_cambio}} do dia anterior à fatura.

## 2. Impostos

- Os preços **não incluem {{impuesto_nombre}}**. Soma-se {{impuesto_nombre}} {{impuesto_pct}} na fatura quando aplicável.
- {{nota_impuestos}}
  *(Exemplos que o gerador preenche conforme a contratada e o cliente: contratada no Uruguai com cliente uruguaio, IVA 22%; contratada no Uruguai com cliente no exterior, exportação de serviços sem IVA; contratada no Brasil, ISS ou outro conforme o município. Validar com o contador.)*
- As retenções ou impostos do país do Cliente correm por conta dele. O Cliente paga o valor integral da fatura, sem descontar tarifas bancárias nem de transferência.

## 3. Esquema de pagamento

| Tipo de trabalho | Como é pago |
|---|---|
| Projeto por preço fechado | {{anticipo_pct}}% na assinatura, o restante por etapas conforme o SOW. Trabalhos abaixo de {{moneda}} {{monto_pago_unico}} são pagos {{pct_unico}}% na assinatura. |
| Time & Materials | Fatura mensal no mês seguinte, com detalhe das horas. |
| Manutenção | Mensalidade antecipada, do dia 1 ao dia {{dia_vencimiento_cuota}} de cada mês. |
| Despesas de terceiros | Antecipadas ou com a fatura seguinte, com comprovante. |

## 4. Vencimento

As faturas vencem **{{dias_vencimiento}} dias** após a emissão. Formas de pagamento: {{medios_pago}} *(ex.: transferência bancária local, transferência internacional, Pix, Mercado Pago, Stripe)*. Dados bancários: em cada fatura.

## 5. Atrasos

- Após {{dias_gracia}} dias do vencimento, aplicam-se juros de mora de {{interes_mora}} ao mês. *[O advogado deve confirmar o limite legal.]*
- Com mais de {{dias_suspension}} dias de atraso, a Malackath pode pausar o trabalho e a manutenção, com aviso prévio. Os prazos são prorrogados pelo tempo da pausa.
- Os direitos sobre as entregas passam ao Cliente somente com o pagamento total (ver Contrato de Prestação de Serviços, cláusula 6).

## 6. Cancelamento pelo Cliente

Se o Cliente cancelar um projeto, paga o trabalho feito até aquele dia (pelas horas registradas ou pelo avanço da etapa) e as despesas comprometidas. O sinal não é devolvido na parte que cobrir esse trabalho.
