import hashlib
import json
import time
import random

class Block:
    def __init__(self, block_id, transaction_list, prev_block_hash, complexity=2):
        """Initialize a block with essential data."""
        self.block_id = block_id
        self.timestamp = time.time()
        self.transaction_list = transaction_list
        self.prev_block_hash = prev_block_hash
        self.nonce = random.randint(0, 10000)  
        self.complexity = complexity
        self.block_hash = self.generatedblock_hash()
    
    def generatedblock_hash(self):
        """Compute hash of the block based on its data."""
        block_contents = json.dumps({
            "block_id": self.block_id,
            "timestamp": self.timestamp,
            "transaction_list": self.transaction_list,
            "prev_block_hash": self.prev_block_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_contents.encode()).hexdigest()
    
    def proof_of_work(self, maxattempts = 1000000):
        
        attempts = 0
        while not self.block_hash.startswith('0' * self.complexity):
            self.nonce += 1
            self.block_hash = self.generatedblock_hash()
            attempts += 1
            if attempts > maxattempts:
             print("Minning failed")
             break

class Blockchain:
    def __init__(self):
        """Create a blockchain with the first block (genesis block)."""
        self.chain = [self.genesis_block()]
    
    def genesis_block(self):
        """Manually create the first block with no previous hash."""
        return Block(0, ["Initial Block"], "0000")

    def append_new_block(self, transactions):
        """Create and add a mined block to the chain."""
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, prev_block.block_hash)
        new_block.proof_of_work()  # Ensure mining difficulty
        self.chain.append(new_block)
    
    def validate_blockchain(self):
        """Ensure the chain is consistent and untampered."""
        for idx in range(1, len(self.chain)):
            current = self.chain[idx]
            previous = self.chain[idx - 1]

            if current.block_hash != current.generatedblock_hash():
                return False

            # Ensure proper linkage
            if current.prev_block_hash != previous.block_hash:
                return False
        
        return True

    def display_chain(self):
        """Print the details of each block in the chain."""
        for block in self.chain:
            print(f"Block {block.block_id}:")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transaction_list}")
            print(f"Previous Hash: {block.prev_block_hash}")
            print(f"Current Hash: {block.block_hash}\n")

# Testing the blockchain
if __name__ == "__main__":
    ledger = Blockchain()

    
    ledger.append_new_block(["Harsh sends 2 BTC to Shayak"])
    ledger.append_new_block(["Harsh pays 1 BTC to Shayak"])
    
    # Display the blockchain
    ledger.display_chain()

    print("Blockchain Integrity:", "Valid" if ledger.validate_blockchain() else "Tampered")

    # Simulate tampering
    print("\nModifying data...\n")
    ledger.chain[1].transaction_list = ["Harsh sends 50 BTC to Ananya"]
    print("Blockchain Integrity after modification:", "Valid" if ledger.validate_blockchain() else "Tampered")
