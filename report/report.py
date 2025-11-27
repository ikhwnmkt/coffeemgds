# Kode bagian report
import json
from datetime import datetime
from typing import List, Dict
from collections import defaultdict
from employees.models import pegawai

class DataLoader:
    def __init__(self, json_files:Dict[str, str]=None):
        
        if json_files is None:
            self.json_files = {
                'main': 'assets/database/data.json',
                'employees': 'assets/database/pegawai.json',
                'logistics': 'assets/database/logistik.json',
                'customers': 'assets/database/customers.json',
            }
        else:
            self.json_files = json_files

        self.data= {}
    
    def load_data(self, key:str=None) -> Dict:
        if key:
            return self.load_single_file(key)
        else:
            return self.load_all_files()
    
    def load_single_file(self, key:str) -> Dict:
        file_path = self.json_files.get(key)
        if not file_path:
            raise ValueError(f"File untuk key '{key}' tidak ditemukan.")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print(f"File {file_path} tidak ditemukan.")
            return {}
        except json.JSONDecodeError:
            print(f"File {file_path} bukan file JSON yang valid.")
            return {}
        
    def load_all_files(self) -> Dict:
        all_data ={}
        for key, file_path in self.json_files.items():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    all_data[key] = data

            except FileNotFoundError:
                print(f"File {file_path} tidak ditemukan.")
                all_data[key] = {}
                
            except json.JSONDecodeError:
                print(f"File {file_path} bukan file JSON yang valid.")
                all_data[key] = {}
        
        return all_data
    

class Report:
    def __init__(self, title:str):
        self.title = title
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.content = {}
        self.data_loader = DataLoader()

    def generate(self):
        raise NotImplementedError("Subclasses harus mengimplementasikan metode generate().")
    
    def dictConverter(self):
        return {
            "title": self.title,
            "report_date": self.report_date,
            "content": self.content
        }
    
class EmployeeReport(Report):
    def __init__(self):
        super().__init__("Laporan Karyawan")
        self.best_employee = None
        self.employee = []

    def generate(self):
        employees = self.data_loader.load_data('employees')

        if not employees:
            self.content = {'message': 'Tidak ada data karyawan'}
            return self.content
        
        self.employee_stats = []

        for emp in employees:
            gaji_pokok = emp.get('gaji_per_jam', 0) * emp.get('jam_kerja', 0)
            bonus = emp.get('bonus_per_minuman', 0) * emp.get('minuman_terjual', 0)
            total_gaji = gaji_pokok + bonus

            performance = (emp.get('minuman_terjual', 0) * 10) + (emp.get('jam_kerja', 0) * 5)

            employee_data = {
                'id_pegawai': emp.get('id_pegawai'),
                'nama': emp.get('nama'),
                'posisi': emp.get('posisi'),
                'shift': emp.get('shift'),
                'jam_kerja': emp.get('jam_kerja', 0),
                'minuman_terjual': emp.get('minuman_terjual', 0),
                'gaji_pokok': f"Rp {gaji_pokok:,}",
                'bonus': f"Rp {bonus:,}",
                'total_gaji': f"Rp {total_gaji:,}",
                'performance_score': performance
            }

            self.employee_stats.append(employee_data)
        
        self.employee_stats.sort(key=lambda x: x['performance_score'], reverse=True)
        self.best_employee = self.employee_stats[0] if self.employee_stats else None

        self.content = {
            'total_pegawai': len(employees),
            'total_minuman_terjual': sum(emp.get('minuman_terjual', 0) for emp in employees),
            'total_jam_kerja': sum(emp.get('jam_kerja', 0) for emp in employees),
            'rata_rata_minuman_per_pegawai': sum(emp.get('minuman_terjual', 0) for emp in employees) / len(employees),
            'pegawai_terbaik': {
                'nama' : self.best_employee['nama'],
                'minuman_terjual': self.best_employee['minuman_terjual'],
                'performance_score': self.best_employee['performance_score']
            } if self.best_employee else None,
            'detail_pegawai': self.employee_stats
        }

        return self.content
    
class InventoryReport(Report):
    pass

class CustomerReport(Report):
    def __init__(self):
        super().__init__("Laporan Pelanggan")

class SalesReport(Report):
    def __init__(self):
        super().__init__("Laporan Karyawan")
        

class ReportManager:
    def __init__(self):
        self.reports = []

    def generate_all(self):
        employees = EmployeeReport()
        employees.generate()
        self.reports.append(employees)

        inventory = InventoryReport()
        inventory.generate()
        self.reports.append(inventory)

        customer = CustomerReport()
        customer.generate()
        self.reports.append(customer)

        sales = SalesReport()
        sales.generate()
        self.reports.append(sales)
        return self.reports
    
    def get_report(self, report_type:str):
        report_map = {
            'employee': EmployeeReport,
            'inventory': InventoryReport,
            'customer': CustomerReport,
            'sales': SalesReport
        }
        report_class = report_map.get(report_type.lower())
        if report_class:
            report = report_class()
            report.generate()
            return report
        else:
            raise ValueError(f"Tipe laporan '{report_type}' tidak dikenali.")
        
    def get_best_employee(self):
        employee_report = EmployeeReport()
        employee_report.generate()
        return employee_report.best_employee
    
