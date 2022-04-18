from brownie import FundMe, config, network, MockV3Aggregator
from scripts.helpers import get_account, deploy_mocks, LOCAL_ENVIRONMENTS


def deploy_fundme():
    account = get_account()
    if network.show_active() not in LOCAL_ENVIRONMENTS:

        print(f"using {network.show_active()} environment")

        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print("using development environment")
        deploy_mocks()

        price_feed_address = MockV3Aggregator[-1].address
        print(f"using mock aggregator at {price_feed_address}")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fundme()
