from brownie import network, accounts, exceptions
from scripts.helpers import get_account, LOCAL_ENVIRONMENTS
from scripts.deploy import deploy_fundme
import pytest


def test_funding_and_withdrawal():
    account = get_account()
    fund_me = deploy_fundme()
    entrance_fee = fund_me.getEntranceFee()
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
    fund_me = deploy_fundme()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
