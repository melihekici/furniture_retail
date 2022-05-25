import model
import sqlalchemy


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        """
        INSERT INTO order_lines (orderid, sku, quantity) VALUES
         ("order1", "READ-CHAIR", 12),
         ("order1", "RED-TABLE", 13),
         ("order3", "BLUE-LIPSTICK", 14)
        """
    )

    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]

    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, quantity FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]