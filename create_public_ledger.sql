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
	verify_digital_signature BOOLEAN
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
