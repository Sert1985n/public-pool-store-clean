# PostgreSQL and payouts notes

This project export keeps the Miningcore templates aligned around one database set:
- host: `192.168.0.175` in the example config
- port: `5432`
- database: `miningcore`
- user: `miningcore`
- password: `miningcore`

For SOLO pools, payout addresses are expected to be written into each pool entry:
- `address`
- `rewardRecipients[0].address`

The example config in `config.current-working.example.json` reflects the server state that was validated during setup.
