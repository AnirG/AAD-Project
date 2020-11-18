CREATE TABLE IF NOT EXISTS "friends_bs" (
	user_id VARCHAR,
	friend_id VARCHAR,
	amount VARCHAR
);
CREATE TABLE IF NOT EXISTS "friend_requests" (
	user_id VARCHAR,
	friend_id VARCHAR
);
CREATE TABLE IF NOT EXISTS "pending_transactions" (
	from_id VARCHAR,
	to_id VARCHAR,
	amount VARCHAR,
	comment VARCHAR,
	date_p VARCHAR
);
CREATE TABLE IF NOT EXISTS "confirmed_transactions" (
	from_id VARCHAR,
	to_id VARCHAR,
	amount VARCHAR,
	comment VARCHAR,
	date_p VARCHAR
);
