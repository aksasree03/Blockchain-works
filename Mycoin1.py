import hashlib
import json
from time import time
import streamlit as st

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount}


class Block:
    def __init__(self, index, previous_hash, proof, transactions, timestamp=None):
        self.index = index
        self.timestamp = timestamp or time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "proof": self.proof,
            "previous_hash": self.previous_hash,
        }

    def hash(self):
        block_string = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.total_supply = 0
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", 100, [])
        self.chain.append(genesis_block)

    def register_node(self, address):
        self.nodes.add(address)
        return f"Node {address} added to the network."

    def create_transaction(self, sender, receiver, amount):
        if sender not in self.nodes or receiver not in self.nodes:
            return "Sender or receiver is not a registered node!"
        transaction = Transaction(sender, receiver, amount)
        self.current_transactions.append(transaction)
        return f"Transaction from {sender} to {receiver} for {amount} MyCoins added."

    def mine_block(self, miner):
        if miner not in self.nodes:
            return "Miner must be a registered node!"

        proof = self.proof_of_work(self.chain[-1])
        block = Block(
            index=len(self.chain),
            previous_hash=self.chain[-1].hash(),
            proof=proof,
            transactions=self.current_transactions,
        )
        self.chain.append(block)
        self.current_transactions = []

        # Reward miner
        reward_transaction = Transaction("System", miner, 10)
        self.total_supply += 10
        self.current_transactions.append(reward_transaction)
        return f"Block {block.index} mined successfully by {miner}!"

    def proof_of_work(self, last_block):
        proof = 0
        while not self.valid_proof(last_block.hash(), proof):
            proof += 1
        return proof

    def valid_proof(self, last_hash, proof):
        guess = f"{last_hash}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def check_balance(self, node):
        if node not in self.nodes:
            return f"Node {node} is not registered!"
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == node:
                    balance -= tx.amount
                if tx.receiver == node:
                    balance += tx.amount
        return balance

    def display_chain(self):
        return [block.to_dict() for block in self.chain]

    def display_balances(self):
        balances = {}
        for node in self.nodes:
            balances[node] = self.check_balance(node)
        return balances


# Initialize Blockchain in Session State
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

# Streamlit Interface
st.title("Blockchain Interactive Visualizer (MyCoin)")

# Total Supply
st.subheader("Total Supply")
st.info(f"Total MyCoins in Circulation: {blockchain.total_supply}")

# Add Nodes
st.subheader("Register Nodes")
new_node = st.text_input("Enter Node Name (Unique)", key="new_node")
if st.button("Register Node"):
    if new_node:
        result = blockchain.register_node(new_node)
        st.success(result)
    else:
        st.error("Please enter a valid node name.")

# Add Transactions
st.subheader("Add Transactions")
sender = st.text_input("Sender", key="sender")
receiver = st.text_input("Receiver", key="receiver")
amount = st.number_input("Amount", min_value=0.0, step=0.1, key="amount")
if st.button("Add Transaction"):
    if sender and receiver and amount > 0:
        result = blockchain.create_transaction(sender, receiver, amount)
        if "added" in result:
            st.success(result)
        else:
            st.error(result)
    else:
        st.error("Please fill in all fields correctly.")

# Display Pending Transactions
st.subheader("Pending Transactions")
if blockchain.current_transactions:
    st.write("Transactions awaiting inclusion in the next block:")
    pending_data = [tx.to_dict() for tx in blockchain.current_transactions]
    st.table(pending_data)
else:
    st.info("No pending transactions.")

# Clear Pending Transactions
if st.button("Clear Pending Transactions"):
    blockchain.current_transactions = []
    st.success("Pending transactions cleared.")

# Mine Block
st.subheader("Mine a Block")
miner = st.text_input("Miner", key="miner")
if st.button("Mine Block"):
    if miner:
        result = blockchain.mine_block(miner)
        if "mined" in result:
            st.success(result)
        else:
            st.error(result)
    else:
        st.error("Please specify a miner.")

# Display Blockchain
st.subheader("Blockchain")
if st.button("Show Blockchain"):
    chain = blockchain.display_chain()
    for block in chain:
        st.json(block)

# Check Balances
st.subheader("Participant Balances")
if st.button("Show Balances"):
    balances = blockchain.display_balances()
    if balances:
        st.json(balances)
    else:
        st.info("No registered nodes to show balances.")

# Validate Blockchain
st.subheader("Validate Blockchain")
if st.button("Validate Blockchain"):
    is_valid = all(
        [
            blockchain.chain[i].previous_hash == blockchain.chain[i - 1].hash()
            for i in range(1, len(blockchain.chain))
        ]
    )
    if is_valid:
        st.success("Blockchain is valid!")
    else:
        st.error("Blockchain is invalid!")
