from exceptions import MinStatusCannotDownError, MaxStatusCannotUpError, CantDischargePatientError
from exceptions import PatientNotExistsError


class Hospital:
    def __init__(self, patients_db):
        self._patients_db = patients_db
        self._statuses_db = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    # todo: patient_index хотелось бы унести в отдельный метод, т.к. получение индекса есть в нескольких местах
    #  и не особо важно знать, когда читаешь код, как идет преобразование patient_id в индекс
    def get_patient_status_by_id(self, patient_id):
        self._verify_patient_exists(patient_id)
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        return self._statuses_db[status_code]

    def patient_status_up(self, patient_id):
        self._verify_patient_exists(patient_id)
        if not self.can_status_up_for_this_patient(patient_id):
            raise MaxStatusCannotUpError
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        self._patients_db[patient_index] = status_code + 1

    def patient_status_down(self, patient_id):
        self._verify_patient_exists(patient_id)
        if not self.can_status_down_for_this_patient(patient_id):
            raise MinStatusCannotDownError
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        self._patients_db[patient_index] = status_code - 1

    def get_statistics(self):
        statistics = {}
        for status_code in self._statuses_db:
            count = 0
            for patient_status_code in self._patients_db:
                if patient_status_code == status_code:
                    count += 1
            if count > 0:
                statistics[self._statuses_db[status_code]] = count
        return statistics

    def discharge_patient(self, patient_id):
        self._verify_patient_exists(patient_id)
        patient_index = patient_id - 1
        if not self.can_discharge_patient(patient_id):
            raise CantDischargePatientError
        self._patients_db.pop(patient_index)

    def patient_exists(self, patient_id):
        return patient_id <= len(self._patients_db)

    def _verify_patient_exists(self, patient_id):
        if not self.patient_exists(patient_id):
            raise PatientNotExistsError

    def can_status_up_for_this_patient(self, patient_id):
        status = self.get_patient_status_by_id(patient_id)
        return status != "Готов к выписке"

    def can_status_down_for_this_patient(self, patient_id):
        status = self.get_patient_status_by_id(patient_id)
        return status != "Тяжело болен"

    def can_discharge_patient(self, patient_id):
        status = self.get_patient_status_by_id(patient_id)
        return status == "Готов к выписке"
