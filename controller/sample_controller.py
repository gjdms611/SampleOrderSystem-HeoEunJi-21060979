from model.sample import Sample


class SampleController:
    def __init__(self, repo, inventory_repo):
        self.repo = repo
        self.inventory_repo = inventory_repo

    def register(self, sample_id, name, avg_production_time, yield_rate):
        existing = self.repo.find_by_id(sample_id)
        if existing is not None:
            return existing, False

        sample = Sample(sample_id, name, avg_production_time, yield_rate)
        self.repo.save(sample)
        return sample, True

    def get(self, sample_id):
        sample = self.repo.find_by_id(sample_id)
        if sample is None:
            return None
        return self._with_quantity(sample)

    def list_all(self):
        return [self._with_quantity(sample) for sample in self.repo.find_all()]

    def search(self, keyword):
        return [self._with_quantity(sample) for sample in self.repo.search(keyword)]

    def _with_quantity(self, sample):
        inventory = self.inventory_repo.find_by_sample_id(sample.sample_id)
        quantity = inventory.quantity if inventory is not None else 0
        return sample, quantity
