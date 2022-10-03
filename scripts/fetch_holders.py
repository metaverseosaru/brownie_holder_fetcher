import brownie.network.contract as contract
from scripts.helpful_scripts import get_account

# Generates a dictionary of (key: TokenId, value: owner_adderess) of a given contract address
# Assumes that the tokenID starts at 0.
# Uses totalSupply() for grabbing the numMinted. If your contract has a differnt way of 
# accessing that quantity, use that function instead there.

def fetch_holders(address, outfile="holders.csv"):

    account = get_account()

    # Grabbing the holders from the given contract address
    target = contract.Contract.from_explorer(address)
    numMinted = target.totalSupply({"from": account})
    output = {}
    for i in range(numMinted):
        output[i] = target.ownerOf(i, {"from":account})

    # Writting to a CSV file.
    csv_output = "Token ID, Address\n"
    for i in range(numMinted):
        csv_output += "%i, %s\n"%(i, output[i])
    f = open(outfile, "w")
    f.write(csv_output)
    f.close()

    # Printing some stats
    adds = [output[i] for i in range(numMinted)]
    adds_unique = list(set(adds))
    counts = [(adds.count(a), a) for a in adds_unique]
    counts.sort(reverse=True)
    print("=====Top Holders=====")
    for i in range(20):
        print(counts[i])

    return output

def main():
    fetch_holders("0x1ac6712cec4dbe9780671c052f80407be25050d9")

