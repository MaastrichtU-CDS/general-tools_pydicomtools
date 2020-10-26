import pydicom
import os

class PatientDatabase:
    def __init__(self):
        self.patient = dict()
    
    def parseFolder(self, folderPath, show_warnings=True):
        for root, subdirs, files in os.walk(folderPath):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    dcmHeader = pydicom.dcmread(file_path)
                    patientId = dcmHeader[0x10,0x20].value
                    patient = self.getOrCreatePatient(patientId)
                    patient.addFile(file_path, dcmHeader)
                except:
                    if show_warnings:
                        print(f"Error wile reading file {file_path} as DICOM file")

    def getOrCreatePatient(self, patientId):
        if not (patientId in self.patient):
            self.patient[patientId] = Patient()
        return self.patient[patientId]
    
    def countPatients(self):
        return len(self.patient)
    
    def getPatient(self, patientId):
        if patientId in self.patient:
            return self.patient[patientId]
        else:
            return None
    
    def getPatientIds(self):
        return self.patient.keys()
    
    def doesPatientExist(self, patientId):
        return patientId in self.patient

class Patient:
    def __init__(self):
        self.series = dict()
        self.rtstruct = dict()
        self.id = ""

    def addFile(self, filePath, dcmHeader):
        self.id = dcmHeader[0x10,0x20].value
        modality = dcmHeader[0x8,0x60].value
        seriesInstanceUid = dcmHeader[0x20,0xe].value
        
        if not (seriesInstanceUid in self.series):
            if modality == "RTSTRUCT":
                self.series[seriesInstanceUid] = RTStruct()
            else:
                self.series[seriesInstanceUid] = Series()
        mySeries = self.series[seriesInstanceUid]
        mySeries.addFile(dcmHeader, filePath)
    
    def countSeries(self):
        return len(self.series)
    
    def getInstance(self, seriesInstanceUid, sopInstanceUid):
        if seriesInstanceUid in self.series:
            serie = self.series[seriesInstanceUid]
            if sopInstanceUid in serie.filePath:
                return serie.filePath[sopInstanceUid]
        return None

    def getSeries(self, seriesInstanceUid):
        if seriesInstanceUid is not None:
            if self.doesSeriesExist(seriesInstanceUid):
                return self.series[seriesInstanceUid]
        return None
    
    def getCTScans(self):
        return self.series.keys()
    
    def doesSeriesExist(self, seriesInstanceUid):
        return seriesInstanceUid in self.series
    
    def getSeriesForRTStruct(self, rtStruct):
        if rtStruct.getReferencedCTUID() is not None:
            return self.getSeries(rtStruct.getReferencedSeriesUID())
        else:
            return None

class Series:
    def __init__(self):
        self.filePath = dict()
        self.uid = None
        self.modality = None
    def addFile(self, dcmHeader, filePath):
        self.uid = dcmHeader[0x20,0xe].value
        self.modality = dcmHeader[0x8,0x60].value
        self.filePath[dcmHeader[0x8,0x18].value] = filePath
    def getFiles(self):
        return self.filePath

class RTStruct(Series):
    def __init__(self):
        super().__init__()
    def getHeader(self):
        return pydicom.dcmread(super().getFiles()[0])
    def getReferencedSeriesUID(self):
        dcmHeader = self.getHeader()
        if len(list(dcmHeader[0x3006,0x10])) > 0:
            refFrameOfRef = (dcmHeader[0x3006,0x10])[0]
            if len(list(refFrameOfRef[0x3006, 0x0012])) > 0:
                rtRefStudy = (refFrameOfRef[0x3006, 0x0012])[0]
                if len(list(rtRefStudy[0x3006,0x14])) > 0:
                    rtRefSerie = (rtRefStudy[0x3006,0x14])[0]
                    return rtRefSerie[0x20,0xe].value
        return None
    def getFileLocation(self):
        return super().getFiles()[0]