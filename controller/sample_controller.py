from model.sample import Sample


class SampleController:
    def __init__(self, repo):
        self.repo = repo

    def register(self, sample_id, name, avg_production_time, yield_rate):
        sample = Sample(sample_id, name, avg_production_time, yield_rate)
        self.repo.save(sample)
        return sample

    def get(self, sample_id):
        return self.repo.find_by_id(sample_id)

    def list_all(self):
        return self.repo.find_all()

    def search(self, keyword):
        return self.repo.search(keyword)
