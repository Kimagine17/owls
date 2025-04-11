import time
from azure.kusto.ingest import IngestionProperties, IngestionMappingKind, QueuedIngestClient
from azure.kusto.data import KustoConnectionStringBuilder
from azure.identity import AzureCliCredential
from azure.kusto.data import KustoConnectionStringBuilder
from datetime import datetime, timezone
import json
import io
import csv
from azure.identity import DefaultAzureCredential
from azure.kusto.data import KustoConnectionStringBuilder

# credential = DefaultAzureCredential()

# def token_callback(context):
#     token = credential.get_token(context.resource)
#     return token.token  # Only return the token string
class KustoConnector:
    def __init__(self, counter=0, start_time=None):
        self.global_counter = counter
        self.start_time = None
        self.previous = None
        if start_time:
            self.start_time = start_time
            self.real_start_time = datetime.now(timezone.utc)

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

        # # credential = AzureCliCredential()
        # kcsb = KustoConnectionStringBuilder.with_async_token_provider(self.cluster, token_callback)
        # self.client = QueuedIngestClient(kcsb)

        self.ingestion_props = IngestionProperties(
            database=self.database,
            table=self.table,
        )

    def format_time(self):
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def format_old_time(self):
        virtual_now = self.start_time + (datetime.now(timezone.utc) - self.real_start_time)
        return virtual_now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    def insert_row(self, table_row_id, interior_owl, perched_owl, chicks, egg, source_id):
        if all(v is None for v in [interior_owl, perched_owl, chicks, egg]):
            print("No insertions\n")
            return
        if self.previous and self.previous == [interior_owl, perched_owl, chicks, egg, source_id]:
            return
        self.previous = [interior_owl, perched_owl, chicks, egg, source_id]
        if table_row_id is None:
            table_row_id = self.global_counter
            self.global_counter += 1
        if self.start_time:
            timestamp = self.format_old_time()
        else:
            timestamp = self.format_time()
        values = [v if v is not None else 0 for v in [table_row_id, interior_owl, perched_owl, chicks, egg, source_id,timestamp]]
        # Write row to an in-memory CSV buffer
        print(values)
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow([*values])
        buffer.seek(0)

        try:
            self.client.ingest_from_stream(buffer, ingestion_properties=self.ingestion_props)
            print(f"✅ Inserted row at {timestamp}")
        except Exception as e:
            print(f"❌ Error during ingestion: {e}")


def test_old():
    old_time_str = '2024-03-14 17:38:52'
    old_time = datetime.strptime(old_time_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    print(old_time)
    testConnector = KustoConnector(counter=150, start_time=old_time)
    for i in range(0, 10, 2):
        time.sleep(5)
        testConnector.insert_row(None, 1, 0, 1, 1, i // 2)
        testConnector.insert_row(None, 0, 1, 0, 1, (i + 1) // 2)
def test():
    testConnector = KustoConnector(counter=200)
    for i in range(0, 10, 2):
        time.sleep(5)
        testConnector.insert_row(None, 1, 0, 1, 1, i // 2)
        testConnector.insert_row(None, 0, 1, 0, 1, (i + 1) // 2)
if __name__ == "__main__":
    test()
    # test_old()
    print("Uncomment test to run")
