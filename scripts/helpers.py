from brownie import network, accounts, config, MockV3Aggregator

DECIMALS = 8  # Price feed aggregator usually returns 8 decimals
STARTING_PRICE = 200000000000  # 2000 + 8 decimals
LOCAL_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        print("deploying mock aggregator")
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
        print(f"deployed mock aggregator to address {mock_aggregator.address}")
