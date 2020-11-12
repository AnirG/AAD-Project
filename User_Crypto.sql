CREATE TABLE IF NOT EXISTS "User_Crypto" (
id INTEGER NOT NULL,
username VARCHAR,
private_key VARCHAR UNIQUE,
public_key VARCHAR UNIQUE,
net_balance VARCHAR
);