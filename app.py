import os
from pdf2image import convert_from_path
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import json
from datetime import datetime

app = Flask(__name__)

def numerar(numeroAtual, total):
  #/home/zemis/pdf-automatiza/
  #/anexos/vendaonline/
  #/srv/srv-python/pdf-automatiza
  #pathOfEnv = "/srv/srv-python/pdf-automatiza/"
  pathOfEnv = "/home/zemis/pdf-automatiza/"
  numeracao = Image.open(pathOfEnv+'tabelas/numeracao.jpg')
  font = ImageFont.truetype(pathOfEnv+"calibri.ttf", 14)

  drawnumeracao = ImageDraw.Draw(numeracao)
  if len(numeroAtual)  == 1:
       drawnumeracao.text((839, 9), numeroAtual,(0,0,0),font=font)
  elif len(numeroAtual) == 2:
       drawnumeracao.text((835, 9), numeroAtual,(0,0,0),font=font)
  else:
       drawnumeracao.text((831, 9), numeroAtual,(0,0,0),font=font)
  drawnumeracao.text((863, 9), total,(0,0,0),font=font)

  return numeracao


def prepareData(data):
    dfCid = pd.read_pickle('/srv/srv-python/pdf-automatiza/filesLeitos/dC.pickle')
    dfPrestadorCid = pd.read_pickle('/srv/srv-python/pdf-automatiza/filesLeitos/dPreC.pickle')
    dfProcedimentoCid = pd.read_pickle('/srv/srv-python/pdf-automatiza/filesLeitos/dProC.pickle')

    prestador_cid = data['CD_PRESTADOR']+"-"+data['CD_CID']
    pro_cid = data['CD_CID']+"-"+data['CD_PRO_INT']
    sexo = 0 if data['TP_SEXO'] == 'M' else 1
    
    cid = dfCid[dfCid['CD_CID'] == data['CD_CID']]['y'].values[0]
    
    try:
        preCid = dfPrestadorCid[dfPrestadorCid['PRESTADOR_CID'] == prestador_cid]['y'].values[0]
    except:
        preCid = cid
    
    if preCid != preCid:
        preCid = cid

    try:
        proCid = dfProcedimentoCid[dfProcedimentoCid['PRO_CID'] == pro_cid]['y'].values[0]
    except:
        proCid = (preCid + cid) / 2

    if proCid != proCid:
        proCid = (preCid + cid) / 2
    
    if cid != cid:
        return [[np.nan,np.nan,np.nan,np.nan]]

    return [[sexo, cid, proCid, preCid]]

@app.route('/api/adiciona-assinatura', methods=['POST'])
def adicionaAssinatura():
    try :
        #LISTA DE PATHS
        #/home/zemis/pdf-automatiza/
        #/anexos/vendaonline/
        #/srv/srv-python/pdf-automatiza
        pathOfEnv = "/srv/srv-python/pdf-automatiza/"
        pathOfFile = "/anexos/vendaonline/"

        data = request.get_json()
        if '-procassin' in data['arquivo']:
            data['arquivo'] = data['arquivo'].split('-procassin')[0] + '.pdf'

        pages = convert_from_path(pathOfFile + data['arquivo'], dpi = 100)
        font = ImageFont.truetype(pathOfEnv+"calibri.ttf", 14)
        
        text = str(data['token'])+"  "+str(data['data'])+"  "+data['hora']+"  "+ data['ip']

        table = Image.open(pathOfEnv+'tabelas/tb.jpg')
        draw = ImageDraw.Draw(table)
        draw.text((487,33), text,(0,0,0),font=font)
        draw.text((200,33), "  "+data['data'],(0,0,0),font=font)
        
        tableC = Image.open(pathOfEnv+'tabelas/tb-Capa.jpg')
        drawC = ImageDraw.Draw(tableC)
        drawC.text((487,33), text,(0,0,0),font=font)
        drawC.text((200,33), data['data'],(0,0,0),font=font)

        image_list = []
        i = 0
        for image in pages:
            beginTable = image.size[1]
            numeracao = numerar(str(i+1), str(len(pages)))

            image = image.crop((0 ,0, image.size[0], image.size[1]+124))
            
            if i < 4:
                image.paste(tableC.resize((image.size[0], 95)),(0, beginTable))
            else:
                image.paste(table.resize((image.size[0], 95)),(0, beginTable))
            
            image.paste(numeracao.resize((image.size[0], 25)),(0, beginTable+95))
            if i > 0:
                image_list.append(image)
            else:
                first = image
            i = i + 1
	
        str_processado = '-procassin'+datetime.now().strftime('%d%m%Y%H%M%S')
        first.save(pathOfFile + data['arquivo'].replace('.pdf',str_processado+'.pdf'), "PDF" ,resolution=100.0, quality=95, save_all=True, append_images=image_list)
      

        response = app.response_class(
            response=json.dumps({"arquivo": data['arquivo'].replace('.pdf',str_processado+'.pdf')}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        response = app.response_class(
            response=json.dumps({"error": str(e) }),
            status=500,
            mimetype='application/json'
        )
    return response

@app.route('/api/adiciona-paginacao', methods=['POST'])
def adicionaPaginacao():
    try :
        #LISTA DE PATHS
        #/home/zemis/pdf-automatiza/
        #/anexos/vendaonline/
        #/srv/srv-python/pdf-automatiza/
        pathOfEnv = "/srv/srv-python/pdf-automatiza/"
        pathOfFile = "/anexos/vendaonline/"

        data = request.get_json()
        pages = convert_from_path(pathOfFile + data['arquivo'], dpi = 100)

        image_list = []
        i = 0
        for image in pages:
           
            numeracao = numerar(str(i+1), str(len(pages)))
            
            image = image.crop((0 ,0, image.size[0], image.size[1]+25))
            
            image.paste(numeracao.resize((image.size[0], 25)),(0, image.size[1] - 25))
            if i > 0:
                image_list.append(image)
            else:
                first = image
            i = i + 1

        str_processado = 'pag'+datetime.now().strftime('%d%m%Y%H%M%S')
        first.save(pathOfFile + data['arquivo'].replace('.pdf',str_processado+'.pdf'), "PDF" ,resolution=100.0, quality=95, save_all=True, append_images=image_list)
      

        response = app.response_class(
            response=json.dumps({"arquivo": data['arquivo'].replace('.pdf',str_processado+'.pdf')}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        response = app.response_class(
            response=json.dumps({"error": str(e) }),
            status=500,
            mimetype='application/json'
        )
    return response

@app.route('/previsao-leitos/dias', methods=['POST'])
def home():
    data = request.get_json()
    model = pickle.load(open('/srv/srv-python/pdf-automatiza/filesLeitos/model.pickle', 'rb'))
    try:
        previsaoAlta = round(model.predict(prepareData(data))[0], 0)
        response = app.response_class(
            response=json.dumps({"DiasPrevistos": previsaoAlta}),
            status=200,
            mimetype='application/json'
        )
    except:
        response = app.response_class(
            response=json.dumps({"err": "Massa de dados insuficiente"}),
            status=500,
            mimetype='application/json'
        )

    
    return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port= port)
