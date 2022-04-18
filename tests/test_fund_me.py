from brownie import network, accounts, exceptions
from scripts.helpers import get_account, LOCAL_ENVIRONMENTS
from scripts.deploy import deploy_fundme
import pytest


def test_funding_and_withdrawal():
    account = get_account()
    print(f"account ==> {account}")
    fund_me = deploy_fundme()
    print(f"fund_me ==> {fund_me}")
    entrance_fee = fund_me.getEntranceFee() + 100
    print(f"entrance_fee ==> {entrance_fee}")

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.fundersMap(account.address) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.fundersMap(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_ENVIRONMENTS:
        pytest.skip("This test only runs in local environments")
    bad_actor = accounts.add()
    # print(f"bad actor ==> {bad_actor}")
    fund_me = deploy_fundme()
    # print(f"price {fund_me.getPrice()}")
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor, "gas_limit": 6721973})
