import hashlib
import json
import random
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from time import time

# --- Blockchain Classes ---
class Transaction:
    def __init__(self, sender, receiver, amount, fee=0):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee

    def to_dict(self):
        return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount, "fee": self.fee}


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
        self.create_genesis_block()
        self.total_supply = 1000000  # MyCoin total supply
        self.participants = {"System": self.total_supply}  # Initial supply goes to "System"
        self.stakes = {}  # Track participants' stakes for PoS
        self.mining_mode = 'PoW'  # Default to PoW mode

    def create_genesis_block(self):
        genesis_block = Block(0, "0", 100, [])
        self.chain.append(genesis_block)

    def register_node(self, address):
        self.nodes.add(address)
        self.participants[address] = 0  # Add new participant with zero balance
        self.stakes[address] = 0  # Initial stake of 0
        return f"Node {address} added to the network."

    def create_transaction(self, sender, receiver, amount, fee=0):
        if sender not in self.nodes or receiver not in self.nodes:
            return "Sender or receiver is not a registered node!"
        if self.participants[sender] < amount + fee:
            return "Sender has insufficient balance!"
        
        transaction = Transaction(sender, receiver, amount, fee)
        self.current_transactions.append(transaction)
        self.participants[sender] -= (amount + fee)
        self.participants[receiver] += amount
        return f"Transaction from {sender} to {receiver} for {amount} MyCoins added."

    def mine_block(self, miner):
        if miner not in self.nodes:
            return "Miner must be a registered node!"
        
        if self.mining_mode == 'PoW':
            proof = self.proof_of_work(self.chain[-1])
        elif self.mining_mode == 'PoS':
            proof = self.proof_of_stake(miner)

        block = Block(
            index=len(self.chain),
            previous_hash=self.chain[-1].hash(),
            proof=proof,
            transactions=self.current_transactions,
        )
        self.chain.append(block)
        self.current_transactions = []

        # Reward miner
        self.create_transaction("System", miner, 10)  # Reward 10 MyCoins for mining
        return f"Block {block.index} mined successfully by {miner}!"

    def proof_of_work(self, last_block):
        proof = 0
        while not self.valid_proof(last_block.hash(), proof):
            proof += 1
        return proof

    def proof_of_stake(self, miner):
        total_stake = sum(self.stakes.values())
        if total_stake == 0:
            return 0
        stake_probability = self.stakes[miner] / total_stake
        return int(stake_probability * 100)

    def valid_proof(self, last_hash, proof):
        guess = f"{last_hash}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def display_balances(self):
        return self.participants

    def display_chain(self):
        return [block.to_dict() for block in self.chain]

    def toggle_mining_mode(self):
        if self.mining_mode == 'PoW':
            self.mining_mode = 'PoS'
        else:
            self.mining_mode = 'PoW'


# --- Streamlit Interface ---
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

st.title("MyCoin Blockchain")

# Task 1: Display Total Supply and Manage Nodes
st.subheader("Total Supply of MyCoin")
st.write(f"Total supply of MyCoin: {blockchain.total_supply} MyCoins")

# Register Nodes
st.subheader("Register Nodes")
new_node = st.text_input("Enter Node Name (Unique)", key="new_node")
if st.button("Register Node"):
    if new_node:
        result = blockchain.register_node(new_node)
        st.success(result)
    else:
        st.error("Please enter a valid node name.")

# Task 2: Display Pending Transactions
st.subheader("Pending Transactions")
for tx in blockchain.current_transactions:
    st.write(f"{tx.sender} → {tx.receiver}: {tx.amount} MyCoins (Fee: {tx.fee})")

# Task 3: Add Proof of Stake (PoS) and PoW
st.subheader("Mining Mode: Proof of Work (PoW) / Proof of Stake (PoS)")
st.write(f"Current mining mode: {blockchain.mining_mode}")

if st.button("Toggle Mining Mode"):
    blockchain.toggle_mining_mode()
    st.write(f"Mining mode switched to: {blockchain.mining_mode}")

# Task 4: Simulate Mining a Block
miner_name = st.text_input("Enter Miner Name", key="miner_name")
if st.button("Mine Block"):
    if miner_name:
        result = blockchain.mine_block(miner_name)
        st.success(result)
    else:
        st.error("Please enter a valid miner name.")

# Task 5: Visualize Blockchain
st.subheader("Blockchain Visualization")

# Generate Blockchain graph using NetworkX
G = nx.DiGraph()
for block in blockchain.chain:
    for tx in block.transactions:
        G.add_edge(tx.sender, tx.receiver, weight=tx.amount)

# Use NetworkX to create a graph
fig, ax = plt.subplots(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=5000, node_color="lightblue", font_size=10, ax=ax)
st.pyplot(fig)

# Add Pie Chart for Balances
st.subheader("Participant Balances - Pie Chart")
balances = blockchain.display_balances()
labels = list(balances.keys())
values = list(balances.values())
fig = px.pie(names=labels, values=values, title="Balances of Participants")
st.plotly_chart(fig)

# Display Blockchain in JSON format
st.subheader("Blockchain")
chain_data = blockchain.display_chain()
st.write(chain_data)

# Clear Transactions Button
if st.button("Clear Transactions"):
    blockchain.current_transactions.clear()
    st.success("Transactions cleared!")
