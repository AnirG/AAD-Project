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
INSERT INTO User_Crypto VALUES(3,'vijay','60391611808233396924504171732799085747413100590409132761604958926626803581421','7106469907006712108043421764464517986850857491865775559380180240878675670070.28912862890370921163983526430049309651080988304613688281776025925084651211807.0','1025.0');
INSERT INTO User_Crypto VALUES(1,'anir','36618697430794806279310709439771316600364410440854006460425799757630403928494','32113560881369808816791660435440266669803884866128612046206384695475857168005.33274877329529114296564975649391010931202237236767036010804478017707186753242.0','975.0');
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
INSERT INTO Public_Ledger VALUES(2,'32113560881369808816791660435440266669803884866128612046206384695475857168005.33274877329529114296564975649391010931202237236767036010804478017707186753242.0','7106469907006712108043421764464517986850857491865775559380180240878675670070.28912862890370921163983526430049309651080988304613688281776025925084651211807.0',25,'24/11/2020','1st transaction',0,'0f232be08926602e3f02191e496a6f02c33ad65ee482ac4a52e2f73eb6e014e6',4,'MEYCIQDNkFICYdrQ3vPMamWEWmxaUSj01z+McbFrnndZLTKasAIhAJGw+rN3dy0EmB7e+VyGuxla20ONZ32Ux5k/cYIoCs83');
CREATE TABLE IF NOT EXISTS "friends_bs" (
	user_id VARCHAR,
	friend_id VARCHAR,
	amount VARCHAR
);
INSERT INTO friends_bs VALUES('anir','ganesh','0');
INSERT INTO friends_bs VALUES('ganesh','anir','0');
INSERT INTO friends_bs VALUES('vijay','ganesh','0');
INSERT INTO friends_bs VALUES('ganesh','vijay','0');
INSERT INTO friends_bs VALUES('vijay','anir','0');
INSERT INTO friends_bs VALUES('anir','vijay','0');
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
INSERT INTO confirmed_transactions VALUES(2,'ganesh','','','settled with anir vijay ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(3,'anir','','','settled with ganesh vijay ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(4,'vijay','','','settled with ganesh anir ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(5,'ganesh','','','settled with anir vijay ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(6,'anir','','','settled with ganesh vijay ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(7,'vijay','','','settled with ganesh anir ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(8,'vijay','anir','1000','22','24/11/2020');
INSERT INTO confirmed_transactions VALUES(9,'ganesh','','','settled with vijay anir ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(10,'vijay','','','settled with ganesh anir ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(11,'anir','','','settled with ganesh vijay ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(12,'anir','vijay','1000','1','24/11/2020');
INSERT INTO confirmed_transactions VALUES(13,'anir','','','settled with vijay ','24/11/2020');
INSERT INTO confirmed_transactions VALUES(14,'vijay','','','settled with anir ','24/11/2020');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Transaction_Crypto',2);
INSERT INTO sqlite_sequence VALUES('Public_Ledger',2);
INSERT INTO sqlite_sequence VALUES('pending_transactions',4);
INSERT INTO sqlite_sequence VALUES('confirmed_transactions',14);
COMMIT;