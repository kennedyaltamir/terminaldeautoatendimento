import logging

logger = logging.getLogger("EmailService")

class EmailService:
    @staticmethod
    def send_reset_password_email(email: str, token: str):
        """
        Envia o e-mail de recuperação de senha.
        Em desenvolvimento, apenas imprime no console.
        """
        reset_link = f"http://localhost:3000/admin/reset-password?token={token}"
        
        # Em produção, usaríamos SMTP ou API (SendGrid/AWS SES)
        logger.info(f"📧 [MOCK EMAIL] Para: {email}")
        logger.info(f"   Assunto: Recuperação de Senha - MesaFlow")
        logger.info(f"   Link: {reset_link}")
        
        print(f"\n--- E-MAIL DE RECUPERAÇÃO ---")
        print(f"Para: {email}")
        print(f"Link: {reset_link}")
        print(f"-----------------------------\n")
        
        return True