# drive_integration.py

from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleDriveManager:
    def __init__(self):
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.service = build('drive', 'v3', credentials=creds)
        self.folders = self._setup_folders()

    def _setup_folders(self):
        names = [
            '01_Propostas','02_Pedidos','03_Imagens',
            '04_Tabelas_de_Precos','05_Relatorios','06_Backup_Sistema'
        ]
        ids = {}
        for name in names:
            query = f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
            results = self.service.files().list(q=query, fields='files(id)').execute()
            files = results.get('files', [])
            if files:
                ids[name] = files[0]['id']
            else:
                md = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
                folder = self.service.files().create(body=md, fields='id').execute()
                ids[name] = folder['id']
        return ids
