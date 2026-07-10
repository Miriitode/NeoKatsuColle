def clamp(value, minimum=0, maximum=255):
    return max(minimum, min(maximum, value))


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*(clamp(int(v)) for v in rgb))


def lighten_hex(hex_color, amount=0.15):
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex((r + (255 - r) * amount, g + (255 - g) * amount, b + (255 - b) * amount))


def darken_hex(hex_color, amount=0.15):
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex((r * (1 - amount), g * (1 - amount), b * (1 - amount)))


def ui_cardcolor(cardType, elem, isPlanetType=False):
    if not isPlanetType:
        if cardType == "キュート":
            match elem:
                case 'fg':
                    return "#ff8ec1"
                case 'bg':
                    return "#ffdde0"
                case 't1':
                    return "#ffffff" 
                case "t2":
                    return "#67493c"
                case "t3":
                    return "#fffcd4"
                case 'a1':
                    return "#ff919b"
                case 'a2':
                    return "#fffeef"
        elif cardType == "クール":
            match elem:
                case 'fg':
                    return "#6dbfff"
                case 'bg':
                    return "#c6e6ff"
                case 't1':
                    return "#ffffff" 
                case "t2":
                    return "#67493c"
                case "t3":
                    return "#fffcd4"
                case 'a1':
                    return "#4bb8f7"
                case 'a2':
                    return "#fffeef"
        elif cardType == "セクシー":
            match elem:
                case 'fg':
                    return "#b383f3"
                case 'bg':
                    return "#ead8ff"
                case 't1':
                    return "#ffffff" 
                case "t2":
                    return "#67493c"
                case "t3":
                    return "#fffcd4"
                case 'a1':
                    return "#b561e6"
                case 'a2':
                    return "#fffeef"
        elif cardType == 'ポップ':
            match elem:
                case 'fg':
                    return "#fec500"
                case 'bg':
                    return "#fff2a7"
                case 't1':
                    return "#ffffff" 
                case "t2":
                    return "#67493c"
                case "t3":
                    return "#fffcd4"
                case 'a1':
                    return "#ffab3d"
                case 'a2':
                    return "#fffeef"
        else:
            match elem:
                case 'fg':
                    return "#6d6d6d"
                case 'bg':
                    return "#a3a3a3"
                case 't1':
                    return "#ffffff" 
                case "t2":
                    return "#67493c"
                case "t3":
                    return "#fffcd4"
                case 'a1':
                    return "#525252"
                case 'a2':
                    return "#fffeef"
    else:
        typeColors = {
            "フェアリー": ("#ffb6d5", "#e75480"),        # Pink
            "ジュエル": ("#b3e0ff", "#007fff"),         # Blue
            "ホロスコープ": ("#7fffd4", "#014942"),     # Aquamarine
            "ミュージック": ("#ffb3b3", "#ff0000"),     # Red
            "ストーリー": ("#ccff99", "#32cd32"),       # Lime
            "スウィーツ": ("#e1b3ff", "#a259e6"),      # Light Purple
            "フラワー": ("#ff66cc", "#850656"),        # Magenta
            "コスメ": ("#ffd699", "#ff9900"),          # Orange
            "カフェ": ("#ffe5b4", "#ffb347"),          # Peach
            "フルーツ": ("#ffff99", "#ffd700"),        # Yellow
            "アクアリウム": ("#b3ecff", "#00bfff"),     # Light Blue
            "メルティーハウス": ("#20b2aa", "#008080"), # Teal
        }
        match elem:
            case 'fg':
                return (typeColors[cardType[0]][0], typeColors[cardType[-1]][1])
            case 'bg':
                return (lighten_hex(typeColors[cardType[0]][0], 0.14), lighten_hex(typeColors[cardType[-1]][1], 0.50))
            case 't1':
                return "#000000" 
            case "t2":
                return "#67493c"
            case "t3":
                return "#686108"
            case 'a1':
                return (darken_hex(typeColors[cardType[0]][0], 0.12), darken_hex(typeColors[cardType[-1]][1], 0.50))
            case 'a2':
                return "#fffeef"