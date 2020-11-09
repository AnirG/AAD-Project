CREATE TABLE IF NOT EXISTS "Public_Ledger" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	pbk_sender STRING NOT NULL,
	pbk_receiver STRING NOT NULL,
	pvk_sender STRING NOT NULL,
	amount STRING NOT NULL,
	date STRING NOT NULL,
	comments STRING NOT NULL,
	prev_hash STRING NOT NULL,
	current_hash STRING NOT NULL,
	nonce STRING NOT NULL,
	digital_signature STRING NOT NULL
);