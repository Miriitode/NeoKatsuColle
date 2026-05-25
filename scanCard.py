from nicegui import ui
from mainUI import mainUI


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

        # poll every 0.2 seconds
        ui.timer(0.2, check_scan)