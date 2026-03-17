import json
import unittest

from utils.trading_utils import process_accept_offer


class DummySubsession:
    def __init__(self):
        self.executed_trades = '[]'
        self.start_time = 0


class DummyPlayer:
    def __init__(self, pid, cash=1000, permits=1):
        self.id_in_group = pid
        self.current_cash = cash
        self.current_permits = permits
        self.total_bought = 0
        self.total_sold = 0
        self.total_spent = 0
        self.total_earned = 0


class DummyGroup:
    def __init__(self, players, buy_orders=None, sell_orders=None):
        self.players = {p.id_in_group: p for p in players}
        self.buy_orders = json.dumps(buy_orders or [])
        self.sell_orders = json.dumps(sell_orders or [])
        self.subsession = DummySubsession()

    def get_player_by_id(self, pid):
        return self.players[pid]


class ProcessAcceptOfferTests(unittest.TestCase):
    def test_accept_sell_offer_fails_if_order_already_gone(self):
        buyer = DummyPlayer(1, cash=1000, permits=0)
        seller = DummyPlayer(2, cash=1000, permits=1)
        group = DummyGroup([buyer, seller], sell_orders=[])

        result = process_accept_offer(
            buyer,
            group,
            offer_type='sell',
            target_id=2,
            price=50,
            quantity=1,
            item_name='碳權',
            item_field='current_permits',
        )

        self.assertEqual(result['type'], 'fail')
        self.assertIn('已成交或已取消', result['notifications'][1])
        self.assertEqual(buyer.current_permits, 0)
        self.assertEqual(seller.current_permits, 1)
        self.assertEqual(group.subsession.executed_trades, '[]')

    def test_accept_buy_offer_fails_if_order_already_gone(self):
        seller = DummyPlayer(1, cash=1000, permits=1)
        buyer = DummyPlayer(2, cash=1000, permits=0)
        group = DummyGroup([seller, buyer], buy_orders=[])

        result = process_accept_offer(
            seller,
            group,
            offer_type='buy',
            target_id=2,
            price=50,
            quantity=1,
            item_name='碳權',
            item_field='current_permits',
        )

        self.assertEqual(result['type'], 'fail')
        self.assertIn('已成交或已取消', result['notifications'][1])
        self.assertEqual(seller.current_permits, 1)
        self.assertEqual(buyer.current_permits, 0)
        self.assertEqual(group.subsession.executed_trades, '[]')


if __name__ == '__main__':
    unittest.main()
