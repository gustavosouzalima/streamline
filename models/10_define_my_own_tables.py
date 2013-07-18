db.define_table("shipment",
    Field("date_shipment", "date", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
    Field("volume_transported", "double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
    Field("distance_ship", "double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
    Field("minimum_distance_ship", "double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
    Field("value_meter_km", "double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
    )