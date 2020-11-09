
N = 10

prev_hash = 'NULL'.hex()

for i in range(N):
    pbk_sender = generate_KeyPair()[1]
    pvk_sender = generate_KeyPair()[0]
    pbk_receiver = generate_KeyPair()[1]
    amount = random.randint(10,1000)
    date = '31/10/2020'
    comments = 'hahah'

    message = pbk_sender + pvk_sender + pbk_receiver + amount + date + comments
    
    digital_signature = create_Signature(message, pvk_sender) 
    
    nonce = random.randint(10,1000)   # to be determined externallysssss

    current_hash = SHA256(message + digital_signature + nonce)
    
    prev_hash = current_hash

    data = Public_Ledger(pbk_sender,pbk_receiver,pvk_sender,amount,date,comments,prev_hash,current_hash,nonce,digital_signature)
    
    db.session.add(data)
    db.session.commit() 

