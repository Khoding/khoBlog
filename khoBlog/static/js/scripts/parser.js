const url = new URL(pathname);

if (url !== null) {
	let link = "";
	
	switch(link.toLowerCase()) {
    	case "google":
            link = "https://google.com";
            break;

        case "glokhodok":
            link = "https://app.gitkraken.com/glo/board/XhhL3Og6pgAQq6Ms";
            break;

        case "discordkhodok":
            link = "https://discordapp.com/invite/dwqJR9J";
            break;

        case "proxus":
            link = "https://www.proxus.co/";
            break;

        case "khowebexploding":
            link = URL . "uselessOld/explodingWebsite/menusitefesfe.html";
            break;

        case "khobatlogo":
            link = URL . "uselessNew/batmanLogoThreeJS/";
            break;

        case "khoquotes":
            link = URL . "uselessNew/quotesOfDoom/";
            break;

        case "khobuttons":
            link = URL . "uselessNew/randomButtons/";
            break;

        case "kholinks":
            link = URL . "uselessNew/linksToWeirdPages/";
            break;

        case "khotimeline":
            link = URL . "uselessNew/khodokTimeline/";
            break;

        case "khocatcher":
            link = URL . "uselessNew/catcher/";
            break;

        case "khoxmaslinze":
            link = URL . "uselessNew/christmasTreeByLinze/tree.php";
            break;

        case "khordr2":
            link = URL . "uselessNew/clockRDR2/";
            break;

        case "khodoc":
            link = URL . "uselessNew/doc/";
            break;

        case "khoera":
            link = URL . "uselessNew/erastopia/";
            break;

        case "khophptest":
            link = URL . "uselessNew/phpTest/tableaux.php";
            break;

        case "khopop":
            link = URL . "uselessNew/popMotion/";
            break;

        case "khoreactest":
            link = URL . "uselessNew/react/";
            break;

        case "khoanimator":
            link = URL . "uselessNew/spriteAnimator/dist/";
            break;

        case "khoswitch":
            link = URL . "uselessNew/switch/";
            break;

        case "khorng":
            link = URL . "uselessOld/airaingeai/";
            break;

        case "khobeebot":
            link = URL . "uselessOld/bees/beebot-go.html";
            break;

        case "khoboutonscools":
            link = URL . "uselessOld/boutonscools/";
            break;

        case "khochar":
            link = URL . "uselessOld/char/";
            break;

        case "khocheatsheet":
            link = URL . "uselessOld/CheatSheet/";
            break;

        case "khoclock":
            link = URL . "uselessOld/clock/clock.html";
            break;

        case "khodark":
            link = URL . "uselessOld/crazywebsiteofdoom/dark.html";
            break;

        case "khoddojsioc":
            link = URL . "uselessOld/ddojsioc/ddojsioc.html";
            break;

        case "khobiwan":
            link = URL . "uselessOld/designDeBase/obiwan.html";
            break;

        case "khodigitclock":
            link = URL . "uselessOld/digitClock/";
            break;

        case "khodocold":
            link = URL . "uselessOld/doc/DocNewMenu.html";
            break;

        case "kholyrics":
            link = URL . "uselessOld/lyrics/lyrics.html";
            break;

        case "khomoonpix":
            link = URL . "uselessOld/moonPixel/";
            break;

        case "khooldredirect":
            link = URL . "uselessOld/redirect/";
            break;

        case "khoshit":
            link = URL . "uselessOld/shit/";
            break;

        case "khotime":
            link = URL . "uselessOld/time/";
            break;

        case "khotodo":
            link = URL . "uselessOld/todolist/";
            break;

        case "khowinl":
            link = URL . "uselessOld/WindowsL/windowsl.html";
            break;

        case "khold":
            link = URL . "old/index.html";
            break;

        case "khoding":
            link = "https://khoding.github.io/";
            break;

        case "khodok":
            link = URL . "";
            break;

        case "khoadmin":
            link = "https://khodok.xyz:10000";
            break;

        case "disprxsgen":
            link = "https://discordapp.com/channels/387292995818618891/387292995818618895";
            break;

        case "disprxsstaff":
            link = "https://discordapp.com/channels/387292995818618891/387322490222936089";
            break;

        case "disatnadir":
            link = "https://discordapp.com/channels/@me/484332016977051648";
            break;

        case "diserastaff":
            link = "https://discordapp.com/channels/340938917450743809/537302729962291240";
            break;

        case "batman":
            link = "https://gist.github.com/Khoding/4b294572a66dea9b3ba49c838ce10737";
            break;

        case "markdown":
            link = "https://stackedit.io/app#";
            break;

        case "codepenkhodok":
            link = "https://codepen.io/khodok";
            break;

        case "kheee":
            link = URL . "uselessNew/eee";
            break;

        case "ruthinkktoobig":
            link = URL . "src/img/logos/RuthinkkTooBig.png";
            break;

        case "mikimakey":
            link = URL . "src/videos/sexy/MikiMakey.mp4";
            break;

        default:
            link = URL . "error/error404.php";
    }
}

// $page = $_GET['page'];

// if ($page != null) {

//     $link = "";

//     switch (strtolower($page)) {
//         case "google":
//             $link = "https://google.com";
//             break;

//         case "glokhodok":
//             $link = "https://app.gitkraken.com/glo/board/XhhL3Og6pgAQq6Ms";
//             break;

//         case "discordkhodok":
//             $link = "https://discordapp.com/invite/dwqJR9J";
//             break;

//         case "proxus":
//             $link = "https://www.proxus.co/";
//             break;

//         case "khowebexploding":
//             $link = URL . "uselessOld/explodingWebsite/menusitefesfe.html";
//             break;

//         case "khobatlogo":
//             $link = URL . "uselessNew/batmanLogoThreeJS/";
//             break;

//         case "khoquotes":
//             $link = URL . "uselessNew/quotesOfDoom/";
//             break;

//         case "khobuttons":
//             $link = URL . "uselessNew/randomButtons/";
//             break;

//         case "kholinks":
//             $link = URL . "uselessNew/linksToWeirdPages/";
//             break;

//         case "khotimeline":
//             $link = URL . "uselessNew/khodokTimeline/";
//             break;

//         case "khocatcher":
//             $link = URL . "uselessNew/catcher/";
//             break;

//         case "khoxmaslinze":
//             $link = URL . "uselessNew/christmasTreeByLinze/tree.php";
//             break;

//         case "khordr2":
//             $link = URL . "uselessNew/clockRDR2/";
//             break;

//         case "khodoc":
//             $link = URL . "uselessNew/doc/";
//             break;

//         case "khoera":
//             $link = URL . "uselessNew/erastopia/";
//             break;

//         case "khophptest":
//             $link = URL . "uselessNew/phpTest/tableaux.php";
//             break;

//         case "khopop":
//             $link = URL . "uselessNew/popMotion/";
//             break;

//         case "khoreactest":
//             $link = URL . "uselessNew/react/";
//             break;

//         case "khoanimator":
//             $link = URL . "uselessNew/spriteAnimator/dist/";
//             break;

//         case "khoswitch":
//             $link = URL . "uselessNew/switch/";
//             break;

//         case "khorng":
//             $link = URL . "uselessOld/airaingeai/";
//             break;

//         case "khobeebot":
//             $link = URL . "uselessOld/bees/beebot-go.html";
//             break;

//         case "khoboutonscools":
//             $link = URL . "uselessOld/boutonscools/";
//             break;

//         case "khochar":
//             $link = URL . "uselessOld/char/";
//             break;

//         case "khocheatsheet":
//             $link = URL . "uselessOld/CheatSheet/";
//             break;

//         case "khoclock":
//             $link = URL . "uselessOld/clock/clock.html";
//             break;

//         case "khodark":
//             $link = URL . "uselessOld/crazywebsiteofdoom/dark.html";
//             break;

//         case "khoddojsioc":
//             $link = URL . "uselessOld/ddojsioc/ddojsioc.html";
//             break;

//         case "khobiwan":
//             $link = URL . "uselessOld/designDeBase/obiwan.html";
//             break;

//         case "khodigitclock":
//             $link = URL . "uselessOld/digitClock/";
//             break;

//         case "khodocold":
//             $link = URL . "uselessOld/doc/DocNewMenu.html";
//             break;

//         case "kholyrics":
//             $link = URL . "uselessOld/lyrics/lyrics.html";
//             break;

//         case "khomoonpix":
//             $link = URL . "uselessOld/moonPixel/";
//             break;

//         case "khooldredirect":
//             $link = URL . "uselessOld/redirect/";
//             break;

//         case "khoshit":
//             $link = URL . "uselessOld/shit/";
//             break;

//         case "khotime":
//             $link = URL . "uselessOld/time/";
//             break;

//         case "khotodo":
//             $link = URL . "uselessOld/todolist/";
//             break;

//         case "khowinl":
//             $link = URL . "uselessOld/WindowsL/windowsl.html";
//             break;

//         case "khold":
//             $link = URL . "old/index.html";
//             break;

//         case "khoding":
//             $link = "https://khoding.github.io/";
//             break;

//         case "khodok":
//             $link = URL . "";
//             break;

//         case "khoadmin":
//             $link = "https://khodok.xyz:10000";
//             break;

//         case "disprxsgen":
//             $link = "https://discordapp.com/channels/387292995818618891/387292995818618895";
//             break;

//         case "disprxsstaff":
//             $link = "https://discordapp.com/channels/387292995818618891/387322490222936089";
//             break;

//         case "disatnadir":
//             $link = "https://discordapp.com/channels/@me/484332016977051648";
//             break;

//         case "diserastaff":
//             $link = "https://discordapp.com/channels/340938917450743809/537302729962291240";
//             break;

//         case "batman":
//             $link = "https://gist.github.com/Khoding/4b294572a66dea9b3ba49c838ce10737";
//             break;

//         case "markdown":
//             $link = "https://stackedit.io/app#";
//             break;

//         case "codepenkhodok":
//             $link = "https://codepen.io/khodok";
//             break;

//         case "kheee":
//             $link = URL . "uselessNew/eee";
//             break;

//         case "ruthinkktoobig":
//             $link = URL . "src/img/logos/RuthinkkTooBig.png";
//             break;

//         case "mikimakey":
//             $link = URL . "src/videos/sexy/MikiMakey.mp4";
//             break;

//         default:
//             $link = URL . "error/error404.php";
//     }

//     header('Location: ' . $link);
//     exit;
// }