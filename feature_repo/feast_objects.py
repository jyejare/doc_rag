from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.data_format import ParquetFormat
from feast.types import Array, Float32, String

# Define your entity (primary key for feature lookup)
wiki_passage = Entity(
    name="passage_id",
    join_keys=["passage_id"],
    value_type=ValueType.STRING,
    description="Unique ID of a Contract passage",
)

parquet_file_path = "data/contracts.parquet"

# Define offline source
contracts_source = FileSource(
    name="contracts_source",
    file_format=ParquetFormat(),
    path=parquet_file_path,
    timestamp_field="event_timestamp",
)

# Define the feature view for the Contract passage content
wiki_passage_feature_view = FeatureView(
    name="contracts",
    entities=[wiki_passage],
    ttl=timedelta(days=1),
    schema=[
        Field(
            name="contract_text",
            dtype=String,
            description="Content of the Contract passage",
        ),
        Field(
            name="embedding",
            dtype=Array(Float32),
            description="vectors",
            vector_index=True,
            vector_length=384,
            vector_search_metric="COSINE",
        ),
    ],
    online=True,
    source=contracts_source,
    description="Content features of Contract passages",
)
