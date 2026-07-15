from model.sample import Sample
from storage.json_storage import load, save


class SampleRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, sample: Sample):
        records = load(self.file_path)
        records = [r for r in records if r["sample_id"] != sample.sample_id]
        records.append(
            {
                "sample_id": sample.sample_id,
                "name": sample.name,
                "avg_production_time": sample.avg_production_time,
                "yield_rate": sample.yield_rate,
            }
        )
        save(records, self.file_path)

    def find_by_id(self, sample_id):
        records = load(self.file_path)
        for r in records:
            if r["sample_id"] == sample_id:
                return Sample(r["sample_id"], r["name"], r["avg_production_time"], r["yield_rate"])
        return None

    def search(self, keyword: str):
        records = load(self.file_path)
        return [
            Sample(r["sample_id"], r["name"], r["avg_production_time"], r["yield_rate"])
            for r in records
            if keyword in r["name"]
        ]

    def find_all(self):
        records = load(self.file_path)
        return [Sample(r["sample_id"], r["name"], r["avg_production_time"], r["yield_rate"]) for r in records]
