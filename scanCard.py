from nicegui import ui
from headerUI import mainUI
from identifiers import load_identifiers
import json
from pathlib import Path

aikatsuList = load_identifiers('aikatsu')
starsList = load_identifiers('stars')
friendsList = load_identifiers('friends')
paradeList = load_identifiers('planet')
encoreList = load_identifiers('encore')

all_cards = []

for i, _ in enumerate(aikatsuList):
    with open(f'Database/aikatsu/aikatsu_Data-{i}.json','r',encoding='utf-8') as cardData:
        cards = json.load(cardData)

        for card in cards:
            card['_folder'] = i

        all_cards.extend(cards)

def find_card(scan_code):
    for card in all_cards:
        if str(card.get('QR', '')) == str(scan_code) or str(card.get('Barcode', '')) == str(scan_code):
            return card
        
    return None

def show_card_popup(card):
    folder = card['_folder']
    image_path = (
        f'Assets/Cards/aikatsu/cardimg-{card["_folder"]}/'
        f'{card["ID"]}.png'
    )

    with ui.dialog() as dialog:
        with ui.card().style('min-width: 700px'):
            with ui.column().classes('w-full items-center q-gutter-md'):
                ui.label('Card successfully added!') \
                    .classes('w-full text-center text-h6')

                ui.image('/' + image_path).style('width: 250px')
                ui.label(
                    f'{card["Name"]}'
                ).classes('w-full text-center')

                ui.button('Close', on_click=dialog.close)

    dialog.open()

@ui.page('/scanCard')
def scanner_page():

    mainUI('NeoKatsuColle | Scan a Card!')

    with ui.column().classes(
        'w-full items-center'
    ).style(
        '''
        height: calc(100vh - 64px);
        overflow: hidden;
        '''
    ):

        # scanner area grows to fill space
        ui.html('''
        <div
            id="reader"
            style="
                flex-grow: 1;
                width: min(95vw, 1200px);
                margin: auto;
                overflow: hidden;
            ">
        </div>
        ''')

        ui.add_body_html('''
        <script src="https://unpkg.com/html5-qrcode"></script>
        ''')

        # initialize scanner
        ui.run_javascript('''
            setTimeout(() => {

                window.latestScan = "";

                const html5QrCode =
                    new Html5Qrcode("reader");

                html5QrCode.start(
                    { facingMode: "environment" },

                    {
                        fps: 10,

                        qrbox: (w, h) => {

                            let size =
                                Math.floor(
                                    Math.min(w, h) * 0.7
                                );

                            return {
                                width: size,
                                height: size
                            };
                        }
                    },

                    (decodedText) => {

                        window.latestScan = decodedText;

                    }

                ).then(() => {

                    const video =
                        document.querySelector("#reader video");

                    if (video) {

                        video.style.width = "100%";
                        video.style.height = "100%";

                        video.style.maxHeight = "75vh";

                        video.style.objectFit = "cover";

                        video.style.borderRadius = "16px";
                    }

                }).catch(err => console.error(err));

            }, 500);
        ''')

        result_label = ui.label(
            'No code scanned yet'
        )
        last_result = {'value': ''}

        async def check_scan():

            result = await ui.run_javascript('''
                return window.latestScan || "";
            ''')

            if result and result != last_result['value']:

                last_result['value'] = result

                result_label.set_text(
                    f'Scanned: {result}'
                )

                card = find_card(result)

                if card:
                    show_card_popup(card)
                else:
                    ui.notify(
                        f'Card not found: {result}',
                        type='negative'
                    )

        ui.timer(0.2, check_scan)