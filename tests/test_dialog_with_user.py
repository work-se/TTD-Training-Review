import pytest

from dialog_with_user import DialogWithUser
from exceptions import PatientIdNotIntegerError
from mock_console import MockConsole
from command_type import CommandType


def test_request_patient_id():
    console = MockConsole()
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    dialog = DialogWithUser(console)
    assert dialog.request_patient_id() == 3


def test_request_patient_id_when_id_not_integer():
    console = MockConsole()
    console.add_expected_request_and_response('Введите ID пациента: ', 'три')
    dialog = DialogWithUser(console)
    with pytest.raises(PatientIdNotIntegerError) as err:
        dialog.request_patient_id()
    assert str(err.value) == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


fixture_for_parser = [
    ('стоп', CommandType.STOP),
    ('Стоп', CommandType.STOP),
    ('stop', CommandType.STOP),
    ('STOP', CommandType.STOP),
    ('остановите программу!', CommandType.UNKNOWN),
    ('узнать статус пациента', CommandType.GET_STATUS),
    ('get status', CommandType.GET_STATUS),
    ('повысить статус пациента', CommandType.STATUS_UP),
    ('status up', CommandType.STATUS_UP),
    ('понизить статус пациента', CommandType.STATUS_DOWN),
    ('status down', CommandType.STATUS_DOWN),
    ('рассчитать статистику', CommandType.CALCULATE_STATISTICS),
    ('calculate statistics', CommandType.CALCULATE_STATISTICS),
    ('выписать пациента', CommandType.DISCHARGE_PATIENT),
    ('discharge patient', CommandType.DISCHARGE_PATIENT),
]


# todo лучше указать два имени "text_command,parsed_command" (без индексов tpl[0])
@pytest.mark.parametrize('tpl', fixture_for_parser)
def test_parse_text_to_command(tpl):
    dialog = DialogWithUser()
    assert dialog._parse_text_to_command(tpl[0]) == tpl[1]


def test_request_command():
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    dialog = DialogWithUser(console)
    assert dialog.request_command() == CommandType.STOP


def test_request_patient_discharge_confirmation():
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'да')
    dialog = DialogWithUser(console)
    assert dialog.request_patient_discharge_confirmation()


def test_request_patient_discharge_not_confirmation():
    # todo: можно параметризовать и объединить со следующим тестом
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'нет')
    dialog = DialogWithUser(console)
    assert not dialog.request_patient_discharge_confirmation()


def test_request_patient_discharge_not_confirmation_when_invalid_response():
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'не надо')
    dialog = DialogWithUser(console)
    assert not dialog.request_patient_discharge_confirmation()


def test_send_message():
    console = MockConsole()
    console.add_expected_output_message('Сообщение, посылаемое пользователю')
    dialog = DialogWithUser(console)
    dialog.send_message('Сообщение, посылаемое пользователю')


def test_send_message_when_invalid_message():
    console = MockConsole()
    console.add_expected_output_message('Сообщение, посылаемое пользователю')
    dialog = DialogWithUser(console)
    with pytest.raises(AssertionError):
        dialog.send_message('Некорректное сообщение')
