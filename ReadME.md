# Serviço de Assinatura de PDFs
Esse serviço é capaz de gerar assinaturas seguindo o padrão de propostas do Venda Online PJ e PF. O serviço aceita qualquer tipo de PDF.

## Instalando o projeto
Para instalar as depêndencias, é necessário instalar o poppler:
```bash
sudo apt-get install -y poppler-utils
```
E após instalar, instale o python e as bibliotecas pdf2image, flask , pillow e pandas.

E rode o projeto:
```bash
python3 app.py
```


## Rotas
Endpoint | MÉTODO | Autenticação necessária | Descrição
--- | --- | --- | --- 
/api/adiciona-assinatura | POST | Não | Realiza a Assinatura da Proposta do PF
/api/adiciona-paginacao | GET | Não | Realiza a paginação dos Documentos.
/previsao-leitos/dias | POST | Não | Realiza a previsão de dias no Gerenciamento de Leitos.
/api/adiciona-pj | POST | Sim | Realiza a Assinatura da Proposta do PJ.

## Ambientes
### Homologação
    * Servidor: 10.0.8.147
    * Caminho: /home/zemis/pdf-automatiza/

### Produção
    * Servidor: 10.0.8.252
    * Caminho:/srv/srv-python/pdf-automatiza/

OBS: Ambos rodam utilizando a porta 3000.