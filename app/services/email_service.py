# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 22:15:00
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("EmailService")

class EmailService:
    @staticmethod
    def send_reset_password_email(email: str, token: str):
        """
        Envia e-mail de recuperação de senha via SMTP.
        Se as variáveis de ambiente não estiverem configuradas, faz fallback para log.
        """
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        sender_email = os.getenv("SMTP_FROM_EMAIL", "noreply@mesaflow.com.br")
        
        # Link de recuperação (Frontend)
        frontend_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:3000").replace("/api", "")
        reset_link = f"{frontend_url}/admin/reset-password?token={token}"

        # Fallback para Log (Dev/Sem Config)
        if not smtp_server or not smtp_user:
            logger.warning("⚠️  SMTP não configurado. Exibindo link no log.")
            logger.info(f"📧 [MOCK EMAIL] Para: {email} | Link: {reset_link}")
            return True

        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = "Recuperação de Senha - MesaFlow"

            body = f"""
            Olá,

            Recebemos uma solicitação para redefinir sua senha no MesaFlow.
            Clique no link abaixo para criar uma nova senha:

            {reset_link}

            Se você não solicitou isso, ignore este e-mail.

            Atenciosamente,
            Equipe MesaFlow
            """
            msg.attach(MIMEText(body, "plain"))

            # Conexão SMTP Segura
            server = smtplib.SMTP(smtp_server, int(smtp_port or 587))
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()

            logger.info(f"✅ E-mail de recuperação enviado para {email}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao enviar e-mail via SMTP: {e}")
            # Fallback de segurança: Loga o link para não trancar o usuário em caso de erro de infra
            logger.warning(f"   Link de recuperação (Fallback): {reset_link}")
            return False
