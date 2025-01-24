from datetime import datetime
from dateutil.relativedelta import relativedelta
from maintenance import Maintenance
from devices_inheritance import Device
from users_inheritance import User

class MaintenanceService():
    maintenances = []
    def __init__(self) -> None:
        self.find_all_maintenances()

    @classmethod
    def find_all_maintenances(cls) -> list[Maintenance]:
        cls.maintenances = Maintenance.find_all()
        return cls.maintenances
    
    @classmethod
    def find_all_maintenances_by_device_id(cls, device_id: str) -> list[Maintenance]:
        return [maintenance for maintenance in cls.maintenances if maintenance.device_id == device_id]
    
    @staticmethod
    def device_exists(device_id: str) -> bool:
        return Device.find_by_attribute("id", device_id) is not None
    
    @classmethod
    def create_new_maintenance(cls, device_id: str, start_date: datetime, end_date: datetime,interval_months: int) -> bool:
        if not cls.device_exists(device_id):
            raise ValueError("Device does not exist")
        
        maintenance = Maintenance(device_id, start_date, end_date, interval_months)
        maintenance.store_data()
        cls.find_all_maintenances()
        return True
    
    @classmethod
    def update_all_maintenances(cls) -> None:
        cls.find_all_maintenances()
        for maintenance in cls.maintenances:
            # Sicherstellen, dass end_date und start_date korrekt sind
            if isinstance(maintenance.start_date, str):
                maintenance.start_date = datetime.strptime(maintenance.start_date, "%Y-%m-%d %H:%M:%S")
            if isinstance(maintenance.end_date, str):
                maintenance.end_date = datetime.strptime(maintenance.end_date, "%Y-%m-%d %H:%M:%S")
            
            # Sicherstellen, dass interval_months ein int ist
            #if not isinstance(maintenance.interval_months, int):
            #    raise TypeError(f"interval_months muss ein int sein, ist aber {type(maintenance.interval_months)}")
            
            while maintenance.end_date < datetime.now():
                new_start_date = maintenance.start_date + relativedelta(months=6) #Service immer 6 Monate
                new_end_date = maintenance.end_date + relativedelta(months=6)
                maintenance.start_date = new_start_date  # Aktualisieren Sie das start_date des aktuellen Wartungsobjekts
                maintenance.end_date = new_end_date  # Aktualisieren Sie das end_date des aktuellen Wartungsobjekts
                if new_end_date > datetime.now():
                    new_maintenance = Maintenance(
                    maintenance.device_id,
                    new_start_date,
                    new_end_date,
                    maintenance.interval_months
                    )
                    new_maintenance.store_data()
                    break   
        
        


if __name__== "__main__":
    print("running")
    maintenance1 = MaintenanceService.create_new_maintenance("Device1", "2025-06-06 00:00:00", "2025-06-07 00:00:00", 1)
    maintenance2 = MaintenanceService.create_new_maintenance("Device2", "2025-01-01 00:00:00", "2025-01-02 00:00:00", 6)
    maintenance3 = MaintenanceService.create_new_maintenance("Device2", "2025-01-02 00:00:00", "2025-01-04 00:00:00", 6)

    MaintenanceService.update_all_maintenances()
    loaded_maintenances = MaintenanceService.find_all_maintenances_by_device_id("Device2")
    if loaded_maintenances:
        for loaded_maintenance in loaded_maintenances:
            print(f"Loaded: {loaded_maintenance}")
    else:
        print("Maintenance not found.")