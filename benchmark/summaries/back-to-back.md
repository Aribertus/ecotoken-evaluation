# ASA benchmark - Algorand testnet

- Data: 2026-09-26T18:09:37.46762985
- Wallet: [NWH5QTN2APQMCW5UU4QJAYMWFCZYS6BMTNJSPBJDH2JBZGL7NUZIKJ2FNY](https://lora.algokit.io/testnet/account/NWH5QTN2APQMCW5UU4QJAYMWFCZYS6BMTNJSPBJDH2JBZGL7NUZIKJ2FNY)
- algod: https://testnet-api.algonode.cloud | indexer: https://testnet-idx.algonode.cloud
- Iterazioni: 30 | poll conferma: 50 ms | poll indexer: 200 ms
- Invio: back-to-back (ogni tx parte appena confermata la precedente)
- Fee totali pagate (warmup incluso): 0.248000 ALGO

## Transazioni (end-to-end = params + sign + submit + conferma)

| Operazione | n | min | p50 | media | p95 | max | conferma p50 | submit p50 | round medi | fee (µALGO) |
|---|---|---|---|---|---|---|---|---|---|---|
| asset_create | 30 | 5180 | 5397 | 5399 | 5546 | 5615 | 5094 | 156 | 2.00 | 1000 |
| fund_account | 30 | 4976 | 5271 | 5268 | 5565 | 5753 | 4992 | 123 | 2.00 | 1000 |
| opt_in | 30 | 4956 | 5367 | 5367 | 5583 | 5731 | 5071 | 141 | 2.00 | 1000 |
| asset_transfer | 30 | 4954 | 5393 | 5390 | 5567 | 5725 | 5102 | 134 | 2.00 | 1000 |
| asset_burn | 30 | 4015 | 4929 | 4901 | 5160 | 5786 | 4629 | 140 | 2.00 | 1000 |
| opt_out | 30 | 5109 | 5242 | 5275 | 5423 | 5874 | 4999 | 142 | 2.00 | 1000 |
| close_account | 30 | 4621 | 5362 | 5356 | 5508 | 5583 | 5092 | 130 | 2.00 | 1000 |
| asset_destroy | 30 | 4498 | 5342 | 5332 | 5531 | 5584 | 5074 | 121 | 2.00 | 1000 |

## Letture

| Operazione | n | min | p50 | media | p95 | max |
|---|---|---|---|---|---|---|
| account_info | 30 | 97 | 137 | 168 | 238 | 945 |
| account_txns | 30 | 103 | 145 | 157 | 217 | 299 |

## Ritardo indexer (conferma algod -> tx visibile su indexer)

| Operazione | n | min | p50 | media | p95 | max |
|---|---|---|---|---|---|---|
| asset_create | 30 | 100 | 145 | 150 | 218 | 278 |
| asset_transfer | 30 | 97 | 153 | 175 | 344 | 520 |
| asset_burn | 30 | 102 | 142 | 146 | 188 | 245 |

Tempi in millisecondi.
