from mock import MagicMock


def is_none_or_type(value, expected_type):
    return value is None or type(value) == expected_type


def setup_sendgrid_mock(m_set_up_sendgrid):
    sendgrid_mock = MagicMock()
    m_set_up_sendgrid.return_value = (sendgrid_mock, MagicMock(name="from_email_mock"))
    return sendgrid_mock


def get_sent_email_details(sendgrid_mock):
    mail = sendgrid_mock.send.call_args.args[0]
    subject = mail.subject.subject
    substitutions = mail.personalizations[0].substitutions[0]
    return subject, substitutions
