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
INSERT INTO User VALUES(1,'anir','anir@gmail.com',X'243262243132244f6c353458526c584d6878544d2e3059776b4730504f6b686d4f72756438483031614c32757a38784a46565a342f4d4a4d795a454f');
INSERT INTO User VALUES(2,'ganesh','ganesh@gmail.com',X'243262243132245a5147784278524d7a45366e5478623964356a4a35656476502f4b614c6130744730332e7357464d6573742e733454574f4367736d');
INSERT INTO User VALUES(3,'vijay','vijay@gmail.com',X'2432622431322455765965396b77583145724279766453626f6163752e4a34492e7133555974776f553355373761647a4e787563736b446a4c674c69');
INSERT INTO User VALUES(4,'aswin','aswin@gmail.com',X'2432622431322468456b62584c64573578634246714e3639414648626541494c386957456c384a75334444556e5a31396b3178563830594943627236');
INSERT INTO User VALUES(5,'jaiganesh','jaiganesh@gmail.com',X'24326224313224686a4a5577433438596e327969797631547370585075736b62666954794448745a763247694e724d79446d474a4c4a787338423147');
INSERT INTO User VALUES(6,'manas','manas@gmail.com',X'24326224313224543630687565412f3268656f43456f4372324d5a354f46534c473479572f553154643547796b4f366778424459473661434f547853');
INSERT INTO User VALUES(7,'pranoy','pranoy@gmail.com',X'2432622431322447724b647453763642746359786c696c68724d2e394f533654316b6c614c51592f5a42614e30576f727a4b6874564e6962334a3869');
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
CREATE TABLE IF NOT EXISTS "friends_bs" (
	user_id VARCHAR,
	friend_id VARCHAR,
	amount VARCHAR
);
INSERT INTO friends_bs VALUES('anir','ganesh','0');
INSERT INTO friends_bs VALUES('ganesh','anir','0');
INSERT INTO friends_bs VALUES('vijay','ganesh','0');
INSERT INTO friends_bs VALUES('ganesh','vijay','0');
INSERT INTO friends_bs VALUES('vijay','anir','1000.0');
INSERT INTO friends_bs VALUES('anir','vijay','-1000.0');
CREATE TABLE IF NOT EXISTS "friend_requests" (
	user_id VARCHAR,
	friend_id VARCHAR
);
INSERT INTO friend_requests VALUES('aswin','ganesh');
INSERT INTO friend_requests VALUES('jaiganesh','ganesh');
INSERT INTO friend_requests VALUES('manas','ganesh');
INSERT INTO friend_requests VALUES('pranoy','ganesh');
INSERT INTO friend_requests VALUES('aswin','anir');
INSERT INTO friend_requests VALUES('jaiganesh','anir');
INSERT INTO friend_requests VALUES('manas','anir');
INSERT INTO friend_requests VALUES('pranoy','anir');
INSERT INTO friend_requests VALUES('aswin','vijay');
INSERT INTO friend_requests VALUES('jaiganesh','vijay');
INSERT INTO friend_requests VALUES('manas','vijay');
INSERT INTO friend_requests VALUES('manas','vijay');
INSERT INTO friend_requests VALUES('pranoy','vijay');
CREATE TABLE IF NOT EXISTS "pending_transactions" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	from_id VARCHAR,
	to_id VARCHAR,
	amount VARCHAR,
	comment VARCHAR,
	date_p VARCHAR
);
INSERT INTO pending_transactions VALUES(2,'vijay','ganesh','200','2nd trans','22/11/2020');
CREATE TABLE IF NOT EXISTS "confirmed_transactions" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	from_id VARCHAR,
	to_id VARCHAR,
	amount VARCHAR,
	comment VARCHAR,
	date_p VARCHAR
);
INSERT INTO confirmed_transactions VALUES(1,'vijay','anir','1000','1st transaction','22/11/2020');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Transaction_Crypto',1);
INSERT INTO sqlite_sequence VALUES('Public_Ledger',1);
INSERT INTO sqlite_sequence VALUES('pending_transactions',2);
INSERT INTO sqlite_sequence VALUES('confirmed_transactions',1);
COMMIT;
