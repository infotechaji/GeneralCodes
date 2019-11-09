import azure
from azure.storage.blob import BlobService

def get_blobs
blob_service = BlobService(account_name='<account_name>', account_key='<account_key>')
containers = blob_service.list_containers()

from azure.storage.blob import BlobService

blob_service = BlobService(account_name='<storage account name>', account_key='<storage account key>')

blobs = []
marker = None
while True:
    batch = blob_service.list_blobs('<blob container name>', marker=marker)
    blobs.extend(batch)
    if not batch.next_marker:
        break
    marker = batch.next_marker
for blob in blobs:
    print(blob.name)


if __name__=="__main__":
for c in containers:
    print(c.name)