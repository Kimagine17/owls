import time
import csv
import json
from datetime import datetime, timezone
import os
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties
from azure.kusto.data import KustoConnectionStringBuilder
from azure.identity import DefaultAzureCredential

class CSVConnector:
    def __init__(self, counter=0, start_time=None, output_path="kusto_output.csv"):
        self.global_counter = counter
        self.start_time = None
        self.previous = None
        self.output_path = output_path
        if start_time:
            self.start_time = start_time
            self.real_start_time = datetime.now(timezone.utc)

        # Create CSV file and write header if it doesn't exist
        if not os.path.exists(self.output_path):
            with open(self.output_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['table_row_id', 'interior_owl', 'perched_owl', 'chicks', 'egg', 'source_id', 'timestamp'])

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

        timestamp = self.format_old_time() if self.start_time else self.format_time()
        values = [v if v is not None else 0 for v in [table_row_id, interior_owl, perched_owl, chicks, egg, source_id, timestamp]]

        try:
            with open(self.output_path, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(values)
            print(f"✅ Wrote row to CSV at {timestamp}")
        except Exception as e:
            print(f"❌ Error writing to CSV: {e}")

    def upload(self, kusto_config_path="./KustoCredentials.json"):
        # Load config
        try:
            with open(kusto_config_path, "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load Kusto config: {e}")
            return

        cluster = config["host"]
        database = config["database"]
        table = config.get("table", "owls")

        # Set up Kusto connection with token provider
        try:
            kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(cluster)
            client = QueuedIngestClient(kcsb)
            ingestion_props = IngestionProperties(database=database, table=table)

            with open(self.output_path, 'r', newline='') as f:
                print(f"📦 Uploading {self.output_path} to Kusto table '{table}'...")
                client.ingest_from_stream(f, ingestion_properties=ingestion_props)
                print(f"✅ Successfully uploaded {self.output_path} to Kusto.")
        except Exception as e:
            print(f"❌ Error uploading CSV to Kusto: {e}")

def test_old():
    old_time_str = '2024-03-14 17:38:52'
    old_time = datetime.strptime(old_time_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    testConnector = CSVConnector(counter=150, start_time=old_time)
    for i in range(0, 10, 2):
        time.sleep(1)
        testConnector.insert_row(None, 1, 0, 1, 1, i // 2)
        testConnector.insert_row(None, 0, 1, 0, 1, (i + 1) // 2)

def test():
    testConnector = CSVConnector(counter=200)
    for i in range(0, 10, 2):
        time.sleep(1)
        testConnector.insert_row(None, 1, 0, 1, 1, i // 2)
        testConnector.insert_row(None, 0, 1, 0, 1, (i + 1) // 2)

if __name__ == "__main__":
    # test()
    csv_connector = CSVConnector()
    csv_connector.upload()
    # test_old()
    # print("Uncomment test() or test_old() to run")

