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
        self.stakes = {}
        self.total_supply = 0
        self.mining_method = "PoW"  # Default to Proof of Work
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", 100, [])
        self.chain.append(genesis_block)

    def register_node(self, address):
        if address in self.nodes:
            return f"Node {address} is already registered!"
        self.nodes[address] = 0
        self.stakes[address] = 0
        return f"Node {address} added to the network."

    def create_transaction(self, sender, receiver, amount):
        if sender not in self.nodes or receiver not in self.nodes:
            return "Sender or receiver is not a registered node!"
        transaction = Transaction(sender, receiver, amount)
        self.current_transactions.append(transaction)
        return f"Transaction from {sender} to {receiver} for {amount} MyCoins added."

    def mine_block(self, miner=None):
        if self.mining_method == "PoW":
            return self.mine_block_pow(miner)
        elif self.mining_method == "PoS":
            return self.mine_block_pos()

    def mine_block_pow(self, miner):
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
        self.nodes[miner] += 10
        return f"Block {block.index} mined successfully by {miner} using Proof of Work!"

    def mine_block_pos(self):
        if not any(self.stakes.values()):
            return "No stakes available for mining. Encourage participants to stake MyCoins."

        miner = self.select_miner_by_stake()
        block = Block(
            index=len(self.chain),
            previous_hash=self.chain[-1].hash(),
            proof=0,  # Proof is not needed in PoS
            transactions=self.current_transactions,
        )
        self.chain.append(block)
        self.current_transactions = []

        # Reward miner
        reward_transaction = Transaction("System", miner, 10)
        self.total_supply += 10
        self.nodes[miner] += 10
        return f"Block {block.index} mined successfully by {miner} using Proof of Stake!"

    def proof_of_work(self, last_block):
        proof = 0
        while not self.valid_proof(last_block.hash(), proof):
            proof += 1
        return proof

    def valid_proof(self, last_hash, proof):
        guess = f"{last_hash}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def stake_currency(self, participant, amount):
        if participant not in self.nodes:
            return "Participant must be a registered node!"
        if self.nodes[participant] < amount:
            return "Insufficient balance to stake!"
        self.nodes[participant] -= amount
        self.stakes[participant] += amount
        return f"{participant} staked {amount} MyCoins."

    def select_miner_by_stake(self):
        total_stake = sum(self.stakes.values())
        weighted_choices = [(node, self.stakes[node] / total_stake) for node in self.stakes]
        return random.choices(
            population=[node for node, _ in weighted_choices],
            weights=[weight for _, weight in weighted_choices],
            k=1,
        )[0]

    def display_chain(self):
        return [block.to_dict() for block in self.chain]

    def display_balances(self):
        return {node: {"balance": self.nodes[node], "stake": self.stakes[node]} for node in self.nodes}


# Initialize Blockchain in Session State
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

# Streamlit Interface
st.title("Blockchain Interactive Visualizer with PoS (MyCoin)")

# Mining Method Selection
st.sidebar.subheader("Mining Method")
mining_method = st.sidebar.selectbox("Choose Mining Method", ["PoW", "PoS"])
blockchain.mining_method = mining_method

# Total Supply
st.subheader("Total Supply")
st.info(f"Total MyCoins in Circulation: {blockchain.total_supply}")

# Register Nodes
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

# Stake Currency
st.subheader("Stake MyCoins")
staker = st.text_input("Participant", key="staker")
stake_amount = st.number_input("Stake Amount", min_value=0.0, step=0.1, key="stake_amount")
if st.button("Stake Currency"):
    if staker and stake_amount > 0:
        result = blockchain.stake_currency(staker, stake_amount)
        if "staked" in result:
            st.success(result)
        else:
            st.error(result)
    else:
        st.error("Please provide valid participant and amount.")

# Mine Block
st.subheader("Mine a Block")
miner = st.text_input("Miner (only for PoW)", key="miner")
if st.button("Mine Block"):
    if blockchain.mining_method == "PoW" and not miner:
        st.error("Please specify a miner for Proof of Work.")
    else:
        result = blockchain.mine_block(miner)
        if "mined" in result:
            st.success(result)
        else:
            st.error(result)

# Display Balances and Stakes
st.subheader("Balances and Stakes")
if st.button("Show Balances and Stakes"):
    balances = blockchain.display_balances()
    if balances:
        st.json(balances)
    else:
        st.info("No registered nodes to show balances.")

# Display Blockchain
st.subheader("Blockchain")
if st.button("Show Blockchain"):
    chain = blockchain.display_chain()
    for block in chain:
        st.json(block)
