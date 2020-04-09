import os
from fitz import fitz
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, jsonify
import json
app = Flask(__name__)
@app.route('/api/adiciona-assinatura', methods=['POST'])
def adicionaAssinatura():
    try :
        data = request.get_json()
        d = fitz.open(data['arquivo'])
        
        font = ImageFont.truetype("calibri.ttf", 19)
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
        for i in range(d.pageCount):
            doc = d.loadPage(i)
            img = doc.getPixmap(alpha = False, matrix = fitz.Matrix(2, 2))
            
            image = Image.frombytes("RGB", [img.width, img.height], img.samples)
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
        
        first.save(data['arquivo'].replace('.pdf','-processado.pdf'), "PDF" ,resolution=100.0, save_all=True, append_images=image_list)
        response = app.response_class(
            response=json.dumps({"arquivo": data['arquivo'].replace('.pdf','-processado.pdf')}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        response = app.response_class(
            response=json.dumps({"error": str(e)}),
            status=500,
            mimetype='application/json'
        )
    return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port= port)
