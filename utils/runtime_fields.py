from elasticsearch import Elasticsearch

def device_field_windows10_or_11(es: Elasticsearch, index="ms-devices"):
    # Define the script for the runtime field.
    runtime_field_script = """
    if (doc["osVersion.keyword"].value.startsWith("10.0.19")) {
        emit("Windows 10");
    } else if (doc["osVersion.keyword"].value.startsWith("10.0.22")) {
        emit("Windows 11");
    } else {
        emit("Unknown");
    }
    """

    mapping = {
        "runtime": {
            "windows_version": {
                "type": "keyword",
                "script": {
                    "source": runtime_field_script
                }
            }
        }
    }

    response = es.indices.put_mapping(index=index, body=mapping)

    print(response)