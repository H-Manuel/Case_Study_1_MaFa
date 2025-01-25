from serializable import Serializable
from database import DatabaseConnector
from datetime import datetime
from typing import Self


class Maintenance(Serializable):
    
    db_connector =  DatabaseConnector().get_table("maintenance")

    def __init__(self, device_id: str, start_date: datetime, end_date: datetime, interval_months: int, creation_date: datetime = None, last_update: datetime = None, id: str = None) -> None:
        if not id:
            id = f"{device_id}_Wartung_{start_date}_{end_date}"
        
        super().__init__(id, creation_date, last_update)
        self.device_id = device_id
        self.start_date = start_date
        self.end_date = end_date
        self.interval_months = interval_months
        
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['device_id'], data['start_date'], data['end_date'], data['interval_months'], data['creation_date'], data['last_update'], data['id'])

    def __str__(self):
        return f"Maintenance: for {self.device_id}: {self.start_date} - {self.end_date} -interval_months: {self.interval_months}" 

if __name__ == "__main__":
    # Create a device
    print("runnning")
    maintenance1 = Maintenance("Device1", "2021-01-01 00:00:00", "2021-01-02 00:00:00",1)
    maintenance2 = Maintenance("Device2", "2021-01-01 00:00:00", "2021-01-02 00:00:00",1)
    maintenance3 = Maintenance("Device2", "2021-01-02 00:00:00", "2021-01-03 00:00:00",1)


    maintenance1.store_data()
    maintenance2.store_data()
    maintenance3.store_data()

    loaded_maintenances = Maintenance.find_by_attribute("device_id", "Device2", num_to_return=-1)
    if loaded_maintenances:
        for loaded_maintenance in loaded_maintenances:
            print(f"Loaded: {loaded_maintenance}")
    else:
        print("Maintenance not found.")
