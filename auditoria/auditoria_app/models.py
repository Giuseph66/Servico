from django.db import models

class Usuario(models.Model):    
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    cell = models.IntegerField()
    gmail = models.EmailField(max_length=500)
    senha = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.id_usuario)
    
class precosse(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.TextField(max_length=1000)
    def __str__(self) -> str:
        return str(self.id)
    

class Conexao(models.Model):
    ip = models.CharField(max_length=50)
    hostname = models.CharField(max_length=255, default="Nao cadastrado")
    user_agent = models.TextField()
    referer = models.CharField(max_length=255, default='Direct Access')
    language = models.CharField(max_length=255, default='Mudinho')
    session_id = models.CharField(max_length=50, unique=True)
    host = models.CharField(max_length=255, default='impossivel')
    connection_type = models.CharField(max_length=50, default='limpo')
    data_conexao = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.ip} - {self.session_id}"