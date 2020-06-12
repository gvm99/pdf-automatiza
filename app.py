import os
from pdf2image import convert_from_path
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def numerar(numeroAtual, total):
  #/home/zemis/pdf-automatiza/
  #/anexos/vendaonline/
  pathOfEnv = ""
  
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

@app.route('/api/adiciona-assinatura', methods=['POST'])
def adicionaAssinatura():
    try :
        #LISTA DE PATHS
        #/home/zemis/pdf-automatiza/
        #/anexos/vendaonline/
        pathOfEnv = ""
        pathOfFile = ""

        data = request.get_json()
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

        first.save(pathOfFile + data['arquivo'].replace('.pdf','-processado.pdf'), "PDF" ,resolution=100.0, quality=95, save_all=True, append_images=image_list)
      

        response = app.response_class(
            response=json.dumps({"arquivo": data['arquivo'].replace("-processado",'').replace('.pdf','-processado.pdf')}),
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
        pathOfEnv = ""
        pathOfFile = ""

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

        first.save(pathOfFile + data['arquivo'].replace('.pdf','-processado.pdf'), "PDF" ,resolution=100.0, quality=95, save_all=True, append_images=image_list)
      

        response = app.response_class(
            response=json.dumps({"arquivo": data['arquivo'].replace('.pdf','-processado.pdf')}),
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port= port)