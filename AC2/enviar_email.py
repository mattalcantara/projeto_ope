import smtplib


def enviar_email(email_cliente, produto):
    gmail_user = 'mslogosteste@gmail.com'
    gmail_password = 'Teste@MsLogos'
    sent_from = gmail_user
    to = [email_cliente]
    subject = 'E-mail de confirmacao de Chamado \n \n'
    body = f'Muito obrigado pela preferencia! O seu chamado sobre o produto {produto} foi computado e enviaremos um profissional o mais rapido possivel!'
    email_text = """\
    From: %s
    %s
    %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)