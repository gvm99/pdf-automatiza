import os
from pdf2image import convert_from_path
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/api/adiciona-assinatura', methods=['POST'])
def adicionaAssinatura():
    textError = "não leu"
    try :
        data = request.get_json()
        pages = convert_from_path(data['arquivo'], 500)
        textError = "leu"
        textError = "Vai dar erro no texto"
        font = ImageFont.truetype("calibri.ttf", 19)
        textError = "Não deu nada"
        text = str(data['token'])+"  "+str(data['data'])+"  "+data['hora']+"  "+ data['ip']

        table = Image.open('tabelas/tb.jpg')
        draw = ImageDraw.Draw(table)
        draw.text((703,45), text,(0,0,0),font=font)
        draw.text((273,44), "  "+data['data'],(0,0,0),font=font)
        
        tableC = Image.open('tabelas/tb-Capa.jpg')
        drawC = ImageDraw.Draw(tableC)
        drawC.text((703,45), text,(0,0,0),font=font)
        drawC.text((273,44), data['data'],(0,0,0),font=font)

        image_list = []
        i = 0
        for page in pages:
            page.save('page.jpg', 'JPEG')
            image = Image.open('page.jpg')

            beginTable = image.size[1]
            image = image.crop((0 ,0, image.size[0],image.size[1]+125))
            
            if i < 4:
                image.paste(tableC.resize((image.size[0], 125)),(0, beginTable))
            else:
                image.paste(table.resize((image.size[0], 125)),(0, beginTable))

            if i > 0:
                image_list.append(image)
            else:
                first = image
            i = i + 1
        
        first.save(data['arquivo'].replace('.pdf','-processado.pdf'), "PDF" ,resolution=100.0, quality=95, save_all=True, append_images=image_list)
        
        response = app.response_class(
            response=json.dumps({"arquivo": data['arquivo'].replace('.pdf','-processado.pdf')}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        response = app.response_class(
            response=json.dumps({"error": textError+str(e)}),
            status=500,
            mimetype='application/json'
        )
    return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port= port)
