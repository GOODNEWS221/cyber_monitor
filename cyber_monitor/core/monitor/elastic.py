from elasticsearch import Elasticsearch
from .models import NetworkLog


es = Elasticsearch(hosts=["http://localhost:9200"])

INDEX_NAME = "network_logs"


def index_log(log: NetworkLog):
    doc = {
        "src_ip": log.src_ip,
        "dst_ip": log.dst_ip,
        "protocol": log.protocol,
        "packet_size": log.packet_size,
        "timestamp": log.timestamp.isoformat(),
        "company_id": log.company.id
    }
    es.index(index= INDEX_NAME, document=doc)
    