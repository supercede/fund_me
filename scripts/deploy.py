from brownie import FundMe
from scripts.helpers import get_account


def deploy_fundme():
    account = get_account()
    fund_me = FundMe.deploy({"from": account}, publish_source=True)
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fundme()
