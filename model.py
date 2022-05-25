from dataclasses import dataclass
from typing import Optional, Set, List

from datetime import date

from exceptions import OutOfStock


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    quantity: int


class Batch:
    def __init__(self, reference: str, sku: str, quantity: str, eta: Optional[date]) -> None:
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations = set() # type: Set[OrderLine]
    
    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.quantity
    
    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch: Batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)

        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
