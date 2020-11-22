PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "User" (
	id INTEGER NOT NULL, 
	username VARCHAR, 
	email VARCHAR, 
	password BLOB, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
CREATE TABLE IF NOT EXISTS "Transaction_Crypto" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	pbk_sender STRING,
	pbk_receiver STRING,
	amount STRING,
	date STRING,
	comments STRING,
	digital_signature STRING
);
CREATE TABLE IF NOT EXISTS "User_Crypto" (
id INTEGER NOT NULL,
username VARCHAR,
private_key VARCHAR UNIQUE,
public_key VARCHAR UNIQUE,
net_balance VARCHAR
);
CREATE TABLE IF NOT EXISTS "Public_Ledger" (
id INTEGER PRIMARY KEY AUTOINCREMENT,
pbk_sender STRING,
pbk_receiver STRING,
amount STRING,
date STRING,
comments STRING,
prev_hash STRING,
current_hash STRING,
nonce STRING,
digital_signature STRING
);
INSERT INTO Public_Ledger VALUES(1,'','','','','','',0,'','');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Transaction_Crypto',1);
INSERT INTO sqlite_sequence VALUES('Public_Ledger',1);
COMMIT;
