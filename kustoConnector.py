import time
from azure.kusto.ingest import IngestionProperties, IngestionMappingKind, QueuedIngestClient
from azure.kusto.data import KustoConnectionStringBuilder
import datetime
import json
import io
import csv

class KustoConnector:
    def __init__(self):
        self.global_counter = 0
        # Load config
        with open("./KustoCredentials.json", "r") as f:
            config = json.load(f)

        self.cluster = config["host"]
        self.database = config["database"]
        self.table = config.get("table", "owls")
        print("cluster:", self.cluster, "self.database", self.database, "table:", self.table)
        # Auth and client setup
        kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(self.cluster)
        self.client = QueuedIngestClient(kcsb)

        self.ingestion_props = IngestionProperties(
            database=self.database,
            table=self.table,
        )

    def format_time(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def insert_row(self, table_row_id, interior_owl, perched_owl, chicks, egg, source_id=0):
        if all(v is None for v in [interior_owl, perched_owl, chicks, egg]):
            print("No insertions\n")
            return
        if table_row_id is None:
            table_row_id = self.global_counter
            self.global_counter += 1
        timestamp = self.format_time()
        values = [v if v is not None else 0 for v in [table_row_id, interior_owl, perched_owl, chicks, egg, source_id,timestamp]]
        print(values)
        # Write row to an in-memory CSV buffer
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow([*values])
        buffer.seek(0)

        try:
            self.client.ingest_from_stream(buffer, ingestion_properties=self.ingestion_props)
            print(f"✅ Inserted row at {timestamp}")
        except Exception as e:
            print(f"❌ Error during ingestion: {e}")


def main():
    testConnector = KustoConnector()
    for i in range(0,10,2):
        time.sleep(5)
        testConnector.insert_row(None, 1, 0, 1, 1, i//2)
        testConnector.insert_row(None, 0, 1, 0, 1, (i+1)//2)

if __name__ == "__main__":
    main()
