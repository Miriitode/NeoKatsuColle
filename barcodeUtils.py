from nicegui import ui
import qrcode
from io import BytesIO
import base64
from barcode import Code128
from barcode.writer import ImageWriter

def generateBarcode(data):
    buffer = BytesIO()

    barcode = Code128(data, writer=ImageWriter())

    barcode.write(buffer)

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return f'data:image/png;base64,{encoded}'

def generateQR(data): #does not match the qr code in actual card, will try to figure this out sometime
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=False)

    img = qr.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return f'data:image/png;base64,{encoded}'

def showQRBarcode(card, isAikatsu = False, isBarcode = False):
    with ui.dialog() as dialog:
        with ui.card().style('min-width: 500px'):
            with ui.column().classes('w-full items-center q-gutter-md'):
                if isAikatsu and isBarcode:
                    ui.label('Card Barcode').classes('w-full text-center text-h6')
                    ui.image().set_source(generateBarcode(card["Barcode"])).style('width: 50%;')
                else:
                    ui.label('Card QR').classes('w-full text-center text-h6')
                    ui.image().set_source(generateQR(card["QR"])).style('width: 50%;')
                    ui.label(f'{card["QR"]}').classes('w-full text-center')

                ui.button('Close', on_click=dialog.close)

    dialog.open()