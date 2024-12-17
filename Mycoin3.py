import hashlib
import json
import random
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
        self.nodes = {}
        self.total_supply = 0
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", 100, [])
        self.chain.append(genesis_block)

    def register_node(self, address):
        if address in self.nodes:
            return f"Node {address} is already registered!"
        self.nodes[address] = 0
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
        self.nodes[miner] += 10
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

    def validate_chain(self, chain):
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]
            if current.previous_hash != previous.hash():
                return False
            if not self.valid_proof(previous.hash(), current.proof):
                return False
        return True

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.validate_chain(new_chain):
            self.chain = new_chain
            return True
        return False

    def display_chain(self):
        return [block.to_dict() for block in self.chain]


# Initialize Nodes in Session State
if "nodes" not in st.session_state:
    st.session_state.nodes = {}


# Helper Functions
def create_new_node(node_name):
    if node_name in st.session_state.nodes:
        return f"Node {node_name} already exists!"
    st.session_state.nodes[node_name] = Blockchain()
    return f"Node {node_name} created!"


def sync_all_nodes():
    longest_chain = max(
        [node.chain for node in st.session_state.nodes.values()], key=len
    )
    for node in st.session_state.nodes.values():
        node.replace_chain(longest_chain)
    return "All nodes synchronized with the longest valid chain!"


# Streamlit Interface
st.title("Decentralized Blockchain Simulator")

# Create and Manage Nodes
st.subheader("Create Nodes")
node_name = st.text_input("Enter Node Name", key="node_name")
if st.button("Create Node"):
    if node_name:
        result = create_new_node(node_name)
        st.success(result)
    else:
        st.error("Node name cannot be empty!")

# Display Current Nodes
st.subheader("Current Nodes")
if st.button("Show Nodes"):
    nodes = list(st.session_state.nodes.keys())
    if nodes:
        st.write(", ".join(nodes))
    else:
        st.info("No nodes created yet.")

# Mine Block in a Specific Node
st.subheader("Mine a Block")
selected_node = st.selectbox("Select Node to Mine Block", st.session_state.nodes.keys())
miner_name = st.text_input("Miner Name", key="miner_name")
if st.button("Mine Block"):
    if selected_node and miner_name:
        blockchain = st.session_state.nodes[selected_node]
        result = blockchain.mine_block(miner_name)
        st.success(result)
    else:
        st.error("Please select a node and specify a miner.")

# Add Transaction to a Node
st.subheader("Add Transactions")
selected_node_tx = st.selectbox("Select Node for Transaction", st.session_state.nodes.keys(), key="tx_node")
sender = st.text_input("Sender", key="tx_sender")
receiver = st.text_input("Receiver", key="tx_receiver")
amount = st.number_input("Amount", min_value=0.0, step=0.1, key="tx_amount")
if st.button("Add Transaction"):
    if selected_node_tx and sender and receiver and amount > 0:
        blockchain = st.session_state.nodes[selected_node_tx]
        result = blockchain.create_transaction(sender, receiver, amount)
        st.success(result)
    else:
        st.error("Please fill in all fields correctly.")

# Sync Nodes
st.subheader("Sync All Nodes")
if st.button("Sync Nodes"):
    result = sync_all_nodes()
    st.success(result)

# Display Blockchain of a Node
st.subheader("Display Node Blockchain")
selected_node_display = st.selectbox("Select Node to Display Blockchain", st.session_state.nodes.keys(), key="display_node")
if st.button("Show Blockchain"):
    if selected_node_display:
        blockchain = st.session_state.nodes[selected_node_display]
        chain = blockchain.display_chain()
        for block in chain:
            st.json(block)
    else:
        st.error("Please select a node.")
