from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_ENVIRONMENT_VARIABLES,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address t our fundme

    # if on a persistent network like kovan, use the associated address
    # otherwise,deploy mocks
    if network.show_active() not in LOCAL_ENVIRONMENT_VARIABLES:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
