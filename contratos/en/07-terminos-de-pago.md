# Payment Terms

> Template to be reviewed by a lawyer and an accountant (tax and invoicing). Common schedule to the Master Services Agreement, SOWs, Maintenance and Proposals.

## 1. Currency

Prices are stated in **{{moneda_nombre}} ({{moneda}})**, as set in the proposal or SOW (US dollars by default; Uruguayan pesos or Brazilian reais are also possible). If invoiced in another currency, the {{fuente_tipo_cambio}} exchange rate of the day before the invoice is used.

## 2. Taxes

- Prices **do not include {{impuesto_nombre}}**. {{impuesto_nombre}} {{impuesto_pct}} is added to the invoice where applicable.
- {{nota_impuestos}}
  *(Examples the generator fills in by provider and client: provider in Uruguay with a Uruguayan client, VAT (IVA) 22%; provider in Uruguay with a client abroad, export of services without VAT; provider in Brazil, ISS or other depending on the municipality. Confirm with the accountant.)*
- Withholdings or taxes in the Client's country are borne by the Client. The Client pays the full invoice amount, without deducting bank or transfer fees.

## 3. Payment schedule

| Type of work | How it is paid |
|---|---|
| Fixed-price project | {{anticipo_pct}}% on signature, the rest by milestones as per the SOW. Work under {{moneda}} {{monto_pago_unico}} is paid {{pct_unico}}% on signature. |
| Time & Materials | Monthly invoice in arrears with detailed hours. |
| Maintenance | Monthly fee in advance, from the 1st to the {{dia_vencimiento_cuota}} of each month. |
| Third-party expenses | In advance or with the next invoice, with receipts. |

## 4. Due date

Invoices are due **{{dias_vencimiento}} days** after issue. Payment methods: {{medios_pago}} *(e.g.: local bank transfer, international transfer, Mercado Pago, Stripe)*. Bank details: on each invoice.

## 5. Late payment

- After {{dias_gracia}} days past the due date, late interest of {{interes_mora}} per month applies. *[The lawyer must confirm the legal maximum.]*
- With more than {{dias_suspension}} days of delay, Malackath may pause work and maintenance after giving notice. Deadlines are extended for the length of the pause.
- Rights in the deliverables pass to the Client only upon full payment (see Master Services Agreement, clause 6).

## 6. Cancellation by the Client

If the Client cancels a project, it pays for the work done up to that day (by logged hours or milestone progress) and for committed expenses. The deposit is not refunded to the extent it covers that work.
