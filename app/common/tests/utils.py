def is_none_or_type(value, expected_type):
    return value is None or type(value) == expected_type


def assert_email_sent(sendgrid_mock, subject_starts_with, base_frontend_url):
    sendgrid_mock.send.assert_called_once()

    mail = sendgrid_mock.send.call_args.args[0]
    subject = mail.subject.subject
    substitutions = mail.personalizations[0].substitutions[0]

    assert subject.startswith(subject_starts_with)
    assert substitutions["-base_frontend_url-"] == base_frontend_url
