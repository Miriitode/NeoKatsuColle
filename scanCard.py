from nicegui import ui
from mainUI import mainUI

@ui.page('/scanCard')
def scanner_page():

    mainUI('NeoKatsuColle | Scan a card!')
    scan_result = ui.label('No code scanned yet')

    ui.label('QR / Barcode Scanner').classes('text-2xl font-bold')

    # scanner container
    ui.html('<div id="reader" style="max-width:100%; "></div>')

    # load library
    ui.add_body_html('''
    <script src="https://unpkg.com/html5-qrcode"></script>
    ''')

    # run scanner javascript
    ui.run_javascript('''
        setTimeout(() => {

            const html5QrCode = new Html5Qrcode("reader");

            const size = Math.min(window.innerWidth * 0.7, 320);

            const qrConfig = {
                fps: 10,
                qrbox: {
                    width: size,
                    height: size,
                },
            };

            function onScanSuccess(decodedText) {

                window.dispatchEvent(
                    new CustomEvent("scan_result", {
                        detail: decodedText
                    })
                );
            }

            html5QrCode.start(
                { facingMode: "environment" },
                qrConfig,
                onScanSuccess
            ).catch(err => {
                console.error(err);
            });

        }, 500);
    ''')

    ui.on(
        'scan_result',
        lambda e: scan_result.set_text(f'Scanned: {e.args}')
    )

