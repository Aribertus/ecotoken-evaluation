# ASA benchmark - Algorand testnet

- Data: 2026-09-26T18:12:54.574471974
- Wallet: [NWH5QTN2APQMCW5UU4QJAYMWFCZYS6BMTNJSPBJDH2JBZGL7NUZIKJ2FNY](https://lora.algokit.io/testnet/account/NWH5QTN2APQMCW5UU4QJAYMWFCZYS6BMTNJSPBJDH2JBZGL7NUZIKJ2FNY)
- algod: https://testnet-api.algonode.cloud | indexer: https://testnet-idx.algonode.cloud
- Iterazioni: 30 | poll conferma: 50 ms | poll indexer: 200 ms
- Invio: attesa casuale 0-3000 ms prima di ogni tx (arrivo non sincronizzato coi blocchi)
- Fee totali pagate (warmup incluso): 0.248000 ALGO

## Transazioni (end-to-end = params + sign + submit + conferma)

| Operazione | n | min | p50 | media | p95 | max | conferma p50 | submit p50 | round medi | fee (µALGO) |
|---|---|---|---|---|---|---|---|---|---|---|
| asset_create | 30 | 3101 | 4543 | 4499 | 5596 | 5643 | 4269 | 129 | 2.07 | 1000 |
| fund_account | 30 | 3188 | 4371 | 4485 | 5801 | 6166 | 4106 | 129 | 2.03 | 1000 |
| opt_in | 30 | 3217 | 4852 | 4668 | 5533 | 6309 | 4514 | 129 | 2.03 | 1000 |
| asset_transfer | 30 | 3173 | 4938 | 4743 | 5655 | 6259 | 4652 | 127 | 2.07 | 1000 |
| asset_burn | 30 | 3162 | 4477 | 4451 | 5620 | 5829 | 4209 | 146 | 2.07 | 1000 |
| opt_out | 30 | 3039 | 4535 | 4556 | 5617 | 5821 | 4228 | 128 | 2.07 | 1000 |
| close_account | 30 | 3052 | 4776 | 4619 | 5643 | 5694 | 4523 | 143 | 2.07 | 1000 |
| asset_destroy | 30 | 3163 | 4507 | 4509 | 5542 | 5931 | 4195 | 144 | 2.07 | 1000 |

## Letture

| Operazione | n | min | p50 | media | p95 | max |
|---|---|---|---|---|---|---|
| account_info | 30 | 98 | 135 | 146 | 232 | 293 |
| account_txns | 30 | 111 | 157 | 166 | 255 | 260 |

## Ritardo indexer (conferma algod -> tx visibile su indexer)

| Operazione | n | min | p50 | media | p95 | max |
|---|---|---|---|---|---|---|
| asset_create | 30 | 115 | 146 | 158 | 217 | 233 |
| asset_transfer | 30 | 116 | 171 | 190 | 271 | 560 |
| asset_burn | 30 | 110 | 146 | 157 | 225 | 249 |

Tempi in millisecondi.
