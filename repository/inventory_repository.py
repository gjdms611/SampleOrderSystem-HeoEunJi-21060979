from model.inventory import Inventory
from storage.json_storage import load, save


class InventoryRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, inventory: Inventory):
        records = load(self.file_path)
        records = [r for r in records if r["sample_id"] != inventory.sample_id]
        records.append({"sample_id": inventory.sample_id, "quantity": inventory.quantity})
        save(records, self.file_path)

    def find_by_sample_id(self, sample_id):
        records = load(self.file_path)
        for r in records:
            if r["sample_id"] == sample_id:
                return Inventory(r["sample_id"], r["quantity"])
        return None

    def find_all(self):
        records = load(self.file_path)
        return [Inventory(r["sample_id"], r["quantity"]) for r in records]
