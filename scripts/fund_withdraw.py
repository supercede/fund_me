from brownie import FundMe, accounts


def fund():
    fund_me = FundMe[-1]
    account = accounts[0]
    entrance_fee = fund_me.getEntranceFee()
    print("The current entrance fee is {entrance_fee}")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = accounts[0]

    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
