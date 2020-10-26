from pydicomtools.DicomDatabase import PatientDatabase, Patient, Series
myDb = PatientDatabase()
myDb.parseFolder('C:\\Users\\johan\\Documents\\Repositories\\projects\\covid-19\\ctp-batch-service\\before')