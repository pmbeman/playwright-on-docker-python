from playwright.sync_api import sync_playwright
import requests
import re
import time
from instagrapi import Client
import requests
from moviepy.editor import VideoFileClip
import json
import pymongo


def get_last_video_url(username):
    with sync_playwright() as p:
        for navigator in [p.chromium, p.firefox]:
            browser = navigator.launch(headless=False)
            page = browser.new_page()
            page.goto("http://tiktok.com/@{}".format(username))
            latest_video = page.query_selector(
            'xpath=/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/a')
        url = latest_video.get_property('href')
        browser.close()
        return url
    
def get_download_url(username):
    url = get_last_video_url(username)
    if url == None:
        return None
    url = str(url) + '/'
    print(username)
    video_id = re.findall(
        r'https\:\/\/www\.tiktok\.com\/@{}\/video\/(.*?)\/'.format(username), url)[0]
    resopnses = requests.get(
        'https://api-v1.majhcc.com/api/tk?url={}'.format(url))
    print(resopnses.text)
    return resopnses.json()['link'], video_id

#connect mongo
MongoClient = pymongo.MongoClient("mongodb+srv://tiktoins:90y5FMeQvWZoZOlv@cluster0.nfxml.mongodb.net/?retryWrites=true&w=majority")

class TIbot:

    def __init__(self, username: str, password: str, sleep: int, tiktok_usernames: list) -> None:
        self.username = username
        self.password = password
        self.sleep = sleep
        self.tiktok_usernames = tiktok_usernames
        self.video_ids = []
        self.cl = Client()
        if self.cl.login(self.username, self.password):
            print("Login sucscessful")

    def video_download(self, url: str, filename: str) -> None:
        chunk_size = 256
        r = requests.get(url, stream=True)
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)

    def video_uploadO(self, filename: str) -> None:
        self.cl.clip_upload(filename, caption="In this page @farzadrgh , we publish new videos regularly and without interruption, please follow us first to support us, then story any video you like and send it directly to 5 of your friends.💡💡DM for credit or removal request (no copyright infringement intended)💡💡🔗All rights and credits reserved to the respective owner(s).#Viral #viralreels #reelsviral #reels #reelsinsta #viralreels #instagram #insta #explore")

    def get_last_video_id_form_tiktok(self, tiktokusername: str) -> str:
        return tiktok.get_download_url(tiktokusername)

    def run(self) -> None:
        while True:
            for tiktokusername in self.tiktok_usernames:
                try:
                    video_url, video_id = self.get_last_video_id_form_tiktok(
                        tiktokusername)
                    #db
                    #get mongo collect
                    mdb = MongoClient["ticktok"]
                    mcol = mdb["videos"]

                    #find in mongo
                    mdoc = mcol.find_one({"video_id": video_id})
                    if mdoc is None:
                        print("video is not in mongo")
                        mcol.insert_one({"video_id": video_id})
                        #time sleep
                        #time.sleep(5400)
                    else:
                        print("video is in mongo")
                        continue

                    if video_id in self.video_ids:
                        print("No new video found")
                        continue
                    else:
                        self.video_download(video_url, "video.mp4")
                        clip = VideoFileClip("video.mp4")
                        duration = clip.duration
                        if duration > 60:
                            print("Video is too long")
                            continue
                        else:
                            try:
                                self.video_uploadO("video.mp4")
                                print("{} uploaded {}".format(
                                    tiktokusername, video_id))
                                self.video_ids.append(video_id)
                                time.sleep(5400)
                            except:
                                print("Upload failed")
                                continue
                except Exception as e:
                    print("for error!")
                    print(e)
            #print("Sleeping for 5400 seconds")
            #time.sleep(5400)

#in time sleepe
TIbot("farzadrgh", "ES}t#bLnhBmZ!zXJ", 0, ["selenagomez", "willsmith", "jasonderulo", "justinbieber", "gordonramsayofficial", "badbunny", "edsheeran", "tombrady", "snoopdogg", "karolg", "madonna", "marshmellomusic", "nickiminaj", "camilacabello", "mileycyrus", "therock", "livbedumb", "postmalone", "vancityreynolds", "daddyyankee", "shaq", "shakira", "samsmith", "imkevinhart", "thegr8khalid", "r.e.m.beauty", "jbalvin", "theweeknd", "maddieziegler", "alexwaarren", "thecelebrit1es", "marcotrunzo", "hhadleygrace", "claragnds", "steveioe", "mariabecerra_22", "murphslife", "danethegreatt", "iankacristinii", "richblackguy", "yummy_pp_lera", "mundinho_dos_memes_", "texasbushman", "anokhinalz", "jaydencroes", "ktlynraps", "juliazugaj", "odakei_6", "1_alkaisr_1", "haqiemstopa", "nildachiaraviglio", "_itsjusttoby", "rubius", "keirariff", "nannymaw", "tommylyon_", "minhnghia13522", "zubarefff", "hshq", "lelandjohanseniv2", "joerauth_", "lilyxgarcia", "_.the.meme.hub._", "edsheeran", "gabrielabee", "devon_palmer", "athallanaufall", "havaianas", "bigfootjinx", "beniju03", "madozilla", "manlikeisaac", "roy.0fficial", "selenagomez", "mryang_english", "naomineo", "carolcastromx", "spicyycam_", "straange_56guuuuy", "conangray", "bmbsh7", "mrizkybillar", "thomassanders", "andy.and.michelle", "mellacarli", "losariasbrothers", "josephmachines", "yailinlamasviraloficial_", "theresa.leung", "mister.emerson", "iknowayrel", "kulubotnabetl0g", "sehataqua", "iamhear_official", "adella_wulandarii", "theandrewschulz", "charlidamelio", "westbrouck", "jdiasss_", "xtnam1", "anxietycouple", "megagonefree", "carolinarinconf", "zen2art", "cookiescandlecrafts", "jairsanchezzz", "calebcrawdad", "fedevigevani", "agc.andy", "leanadeeb", "axelwebber", "bbysquirrel22", "fukada0318", "cheffotto", "rival_amir03", "maiaknight", "domi.nate", "karenos11", "szivsz", "carolvillanes", "eduincaz5", "terryreloaded", "ambarzitaa", "_carolfigueira", "zaksheinman", "xmamx8", "danisoomin", "samadhiza_", "antonibumba", "ella.whatkins", "familyfeud", "tiahranelson", "yurielkysojeda", "rubentuestaok", "alexailacad_", "plasma", "jahdedios.77", "jordanemel", "gabimfmoura", "pablitocastilloo", "larrayeeee", "irwanprasetiyo", "7ooty", "reyhairstylist", "ox_zung", "skaijackson", "jamesllewis", "ricklimatv", "mrbeast", "fadlyfsl_", "gusttavolima", "rafaelsantos", "spaghettirome", "drewafualo", "jellybeannotvince", "how.kev.eats", "sxmplyni", "annaxsitar", "khaby_llaame", "shortestblockbusters", "onlyshitposts2", "spider_slack", "brodywellmaker", "sabrinacarpenter", "ikercasillas", "emilmario69", "user17.32", "pietro_storti", "ajkhiphop", "rocio.cordova", "ildiij", "slim_drawk", "soysuco", "bene.schulz", "gashi", "adventuringwithnala", "seguimeahora", "2ky1ar", "yefersoncossio", "beatrixisabel", "iloveyourmomscatt", "n.vv3", "alexiaa.sk", "yahia_x", "yaboi_travon", "ramizeinn", "fabru_blacutt", "mamalindy", "thep00lguy", "piperrockelle", "marcelldegen", "imreddtv", "goldenboybrow", "twice_tiktok_official", "ddlovato", "yarenalaca", "shxtsngigs", "vascorossi", "nelkboys", "abbieherbert", "enhypen", "yazidzohri", "amauryguichon", "la_lerma", "rosalia", "jhothsa", "mihaiapostol11", "akamztwenty20", "max7424453118", "datdo0803", "jay.ozuna", "monicaxbianca", "edwnttv", "_ikyikyyy", "ramonvitor", "davidgalvanv", "tuananh_villa699", "alphonsodavies", "billlnai", "yun_bao", "badbaarbie", "simuliu", "vilmeijuga", "jeff_bryant17", "bryceheemjames", "thoriqhal", "hotpennies", "ive.official", "phamvinh99", "francoescamillaofficial", "awildani13", "totochegang", "vanrezaputra", "lizzza", "kjsmoothh", "rahafalq50", "gemelasabello2", "karterdaniels55", "namyulenka", "jblaudio", "mattsturniolo", "aichangemoy_", "kristian_ph", "unkabogableviceganda", "efdewee", "just.hamilton", "hutskoen", "lukecombs", "saafiir_", "pakoyaso_", "itsmenicksmithy2", "hayleygeorgiamorris", "khaby.lame", "celinaspookyboo", "heinthukyaw13", "mastercorbuzier", "machikayt", "wm5d", "rubirose", "low._.motivation", "outtpig", "antrobo10", "loganpaul", "hiagodosvideos", "strangehumano", "montpantoja", "arigameplays", "lana_mohd89", "hi_arvans", "eupereiraoficial", "umranto", "swagboygorringe", "marsaimartin", "kervo.dolo", "jaimeonod", "lance210", "judeinggg", "duythamchannel", "stellajero16", "jackjos3ph", "drew.nori", "supermariotrener", "cx_.q", "lyricoo__", "itsqcp", "casaltoxico", "dermdoctor", "markcannatarofilms", "jakepaul", "benoftheweek", "hegyzy", "fitxander", "npastronot", "giannis_an34", "dojacat", "besttoks", "lights.are.off", "trevorwallace", "ugolord", "jeison_giraldo", "nianaguerrero", "camxnie", "leaelui", "alexpickering", "fredziownik_art", "luvadepedreiro", "nabela", "nicollefigueroaa", "sonrixs_", "nick.digiovanni", "qamar_altaey", "leal_stephany", "c4tluvr666", "austinandlexi", "juandamc", "mateus_hwang", "ericsuerez", "scarlettsspam2", "iamjonathanpeter", "_rarelyy_", "sweet_essence_", "yzn47", "dakay_", "vzelivx", "germangarmendia", "reyyhaan31", "iben_ma", "ninefivegarage", "vincentgiganteee", "luczyfer", "charlidameilo", "twenty4tim", "bennydrama7", "jumpersjump", "ssanwhere", "dilanjaniyar", "matsudake", "christianfabiannn", "santa.feklan473", "elrodcontreras", "rika7897", "susymourizz", "gevids", "jake2r", "uthmaniee", "chikakiku", "otakoyakisoba", "ryanbakery", "camilo", "soymariannita", "oscar_mezar", "kopke613", "caeflx", "baurigo", "lowcarbstateofmind", "soydanielaalfaro", "avani", "enolls", "leesiyoung38", "nazormaya", "deeptomcruise", "cabimducorte", "charlieputh", "official_kep1er", "fortnitekanal.exe", "bankiii", "olisboa", "priimoraa", "juju", "theonlycb3", "ferchuuiiiuu", "faryanggaa", "homm9k", "meme_man_78", "freeritzyralph", "davidgetial", "_monaalawi", "lkzinhu", "leosanz33", "mikaylahau", "zachjustice", "mc.kelvin.kw", "augustogimenez", "ogikdp", "snerixx", "marleyandkuba", "howtobasic", "zodiac.boyfriend", "yogurtplssss", "boredtrophyhusband", "ltsjbrad", "haileybieber", "mandinhasiilvaa", "jeminorjaman", "cam.smh", "officialkingsmitty", "la.maraaa", "datvilla94", "pepperonimuffin", "babybella777", "danythegaggio", "pedrinhuol", "hardhat96", "troyesivan", "dilanjaniyar_2", "corpse_husband", ".johnnydepp1", "theestallion", "mikaelatesta", "tubbolive", "i_o1", "ferideozdinco", "ouchigokko", "tiagodionisio", "mrpudidi", "e.m.caris", "polya_tuti", "soylapizito", "angiedelaney6", "beca", "andweaso", "snoopdogg", "tombrady", "sibenitoo", "fabiiospinoso", "rachelmnazario", "fwm.kalebb", "alexandrosharizanis", "jgcruz3d", "peakwak", "savv.labrant", "adrianbliss", "oficialmarcuseni", "kathijunes", "hippiearab", "vienvibi_899", "arfaytb", "deborahyowa", "donny_kc", "kaaramoo", "bulsjarz", "inspirationonlyforyou", "fontvne", "hoootdogs", "randyfeltface", "funnycheetoman", "pacodemiguel", "filmcooper", "ssmaaaryy", "thaycouuto", "fanniraz", "eatwithalyssa", "motchutnho_plus", "colewalliser", "taniadulce1", "softbulletgun97", "jaxwritessongs", "sfioraree", "fadiljaidi", "juanchimy", "jen_wolff", "brittany_broski", "themerkins", "pipelgapapaan", "derivakat", "leidys_sotolongo", "eddy_skabeche", "sssniperwolf", "leleburnier", "iamrilan", "joycaledelire", "semkavkvadrate", "victtoriamedeiros", "philiptanasas", "nansartt", "felipeneto", "yianni2k", "diiegospyckerzs", "logfive", "thebenjishow", "luongthingocha", "snoopdogg", "notraymodeli", "othiagoventura", "ediramatiktok", "renpc_", "yajanaaa", "attahalilintar", "nourmar5", "riaricis", "mackenzieziegler", "itsmanners_10", "nosoychaparro", "ianboggs", "pongfinity", "tu.terapeuta.en.tiktok", "seventeen17_official", "fyp", "aha.urmad", "jojoahmed7213", "thecoreyb", "elsupertrucha1", "bellapoarch", "so_andreyy", "davis.diley", "shehabeldin100", "rooflegend", "bikedasher", "isoyreddit", "basementgang", "doubledragontwins", "sabbyandsophia", "emiliamernes", "bigdirtytoe250", "klrdubs", "esen_alva", "yoangelolo", "fidelisfalante", "jacksepticeye", "maxtaylorlifts", "officialsalicerose", "cciinnn", "teukuryantr", "dasigantung", "dannapaola", "andersonprofetaa", "boywithuke", "paytonking", "mindfkdwithpj", "jonata_26", "royaltietuxedos3", "itsmatheuscosta", "padeeyuhh", "marifereyes9", "nickiminaj", "xie.520", "jimmydarts", "tnx_football", "shuibsepahtu", "cemresolmaz", "tiktokmena", "russmillions", "omarelkarwan122", "_andrewcurtiss", "shingeki_anime_official", "baldybrobryzxz", "alastairmadeit", "official_nct", "brentrivera", "lossiblings_", "itsmenicksmithy", "peetmontzingo", "thelavignes", "kevinprieto077", "markcannatarofilms", "abbycasselberry", "trevorrisica", "misocolorful", "alexiatamiraa", "ayanakamachi", "1.000.000_times", "japeth023", "kodasteven", "ayesebastien", "fyfb.citlalii", "tuckerbudzyn", "soydekko", "animalize21", "mimiermakeup", "blythe", "jajad5", "datkhoi", "nics.orense01", "miakhalifa", "realuser_1", "nouvalshr0", "official_kep1er", "esnyrdump", "mandrake1984real", "s4mkroon", "sarahtabin", "fallenmarauder", "justthenobodys", "zayaperysian", "lonely.moods", "royashariat", "devincaherly", "tebaklokesyen", "christophersturniolo", "nastasyashinee", "abir.sag", "ustazebitlew", "mir_glazami_microscopa", "shougalhady", "daisykeech", "josh1morris", "42psy42", "mattiastanga", "hamadokka.24", "chedurena", "cool__bad", "coleandersonj", "mell_editz0", "plastic_by_sisters_lapay", "tobias_krick", "garett__nolan", "discord", "sa_ro01", "pjmxck", "soniabasill", "ivanovik.83", "fahmi.nm", "kathjosh1923", "brookemonk_", "emilyfauver", "werethatmomndad", "etisalatmisr", "ana_eusse", "larissagloor", "artistadasencasa", "boxlapse", "arroncrascall", "khaicakhia99", "cellat36", "benoit_chevalier", "happykelli", "jamescharles", "rickylemon99", "squeezie", "bigtimerush", "khairulaming", "mayanelsayed", "thesupercole", "bittersweetbynajla", "onlyjayus", "truanlegacy", "justinbieber", "diegovaldesmusic", "cheekyboyos", "erictro", "vidhia_r", "lelepons", "xibibrothers", "albertinasacaca1", "calebrownn", "jen_ny69", "realuser_1", "mikaylanogueira", "pienin777", "lucaslopezvilet", "junpei.zaki", "ynchq", "elchaparrito951", "lornes_", "adrianathrr", "hlaroushdyofficial", "lachama4_ff", "qpark", "oli_natu", "morimura", "victormelo", "dovecameron", "benbaldwin45", "caocuongvu", "mcdonalds_br", "larasilvan", "missionaryjack", "itsjessibaby", "maitreyiramakrishnan", "gabe", "hasnafire", "iixelio", "jfe_hatem", "zeth", "jadepicon", "ani__mel", "more.annapaul", "jonathanpm72", "lorengray", "com.yamato0515", "brawlstars", "danivallem", "e_lhoy", "joaoferdnan", "ninja", "jubiandxian", "cerolzera", "edmatthewstokky", "bara_ze", "brandonspam_", "aileenchristineee", "josyanedomingos", "ndn2307", "lilwangle", "moutawakil90", "bangtoink93", "therealhammytv", "daniel.labelle", "maverickbaker", "spencer_serafica", "albert_cancook", "julesleblanc", "connor", "keemokazi", "summerwalker", "gustavomoulin", "nessaabarrett", "ch3rbet", "beasteater", "nicolegarcia", "el_chico_dinosaurio", "bayashi.tiktok", "triple_rc_media", "scottseiss", "soojinicoreana", "jumpintobliss", "nicocaponecomedy", "youngdinuu", "kpp2179393999", "hannahncortez", "songsforlittles", "cerenyaldz", "q.gal", "kallmekris", "fuu_2003", "huntersolo", "perro_rabioso_2.0", "emilen_im", "alejwho", "cacaaaachu", "juaniquilador", "katiavlogss", "veganpastrychef", "zachking", "ten_yujin", "nicoletv", "p0_2", "ronaldlopes", "daveardito", "valenrewah", "mikasalamanca", "eodriozola1", "iamferv", "steveharvey", "alejandro.villamizar", "scottkress_", "rorrovidios", "pongamoslo_a_prueba", "baimwong", "salokaarya27", "jesusortizpaz", "jalals", "foodie_chineses", "lucaspopan", "taina", "mahmoudalhasanat09", "everett", "zanfilms", "wuesilva", "tooturnttony", "juanacollet", "lilihayes", "chris", "vhackerr", "rucenuenda1", "libardoisaza", "_dieulinh16_", "gordonramsayofficial", "txt.bighitent", "minecraftgarage", "gbandme", "mlp.officiel", "mdmotivator", "keniaos", "numericaltiktok", "sucss.s", "shayvise", "nobleknightadventures", "dominguezbrii", "lu.s.cas", "labellachanel12", ".klooner", "ayyucekamit", "virginiafonseca", "mohaimen.alaa", "lexibrookerivera", "lilnasx", "domelipa", "rauwalejandro", "somi_official_", "just_dt", "kimberly.loaiza", "soysuco_ff", "jlamaru", "iamkevingates", "witch_hazel_x", "sergistwins", "francis.bourgeois", "jasonderulo", "jwaltonnn", "cookingwithlynja", "dunkmvp", "audreyteguh", "nilered", "dearra", "ameliadimz", "jimena.jimenezr", "gehadhassann", "therealcalebmclaughlin", "fhd.artz", "tamarajessica", "rosssmith", "bottleofdjinn", "caleb.finn", "laurahfritz", "jehianps", "ladyyasmina1", "zachdubs", "conorcregan", "yoongitea2", "mads.yo", "tuckot", "ibepds", "corvii_ff", "vlad.hoshin", "kadaltiga", "chefbjs", "brunodiferente2022", "soymildredcastro", "quincylk", "odalysanddafnne", "matheusevitoriaofc", "kaliuchis", "nada_m7amed", "its.michhh", "ff_shannn", "ibarrechejavier", "anthonnyswagg3", "thestradman", "previarda.arg", "jbdjebb", "thatlittlepuff", "dixiedamelio", "lucasmariano", "astarbarbers", "siscakohl", "zowloficial", "emibarbosam", "chrisbrownofficial", "zanoxplay", "incorrectlyroce", "ongsquad", "nashawnabi", "rafaellatuma", "caioceu", "aurikatariina", "forrestsautoreviews", "nandaarsyinta", "valestok", "ty.funnyfunny", "camimendes", "savanahmosss", "jessechrisss", "el.belda", "ewl.dsa", "adamshawn99", "mndiaye_97", "dualienhernandez", "montpantoja", "kirbyquimado", "owen.han", "armasmys", "milos.guzel", "brushzo.wannam", "a.samarcev", "nilskue", "carloandsarah", "cindycandy_", "iansanity_", "cat.valdezf", "austinzajurlife", "bigbeaubrown", "hardjeon", "wisdm8", "oyesebastien", "kikakiim", "trybyl.trybyl", "icdmcry", "paupelaez_", "the.historical", "kunaguero", "itssassagurl", "bintangemontersenyum", "travque", "jack_papho69", "thebrandonrobert", "jonahpedro", "cats.territory", "luisvelody", "vanessalopesr", "civan.ibrahim99", "daviddobrik", "vivianlinhares_", "liamsilk", "mckekell", "mo_vlogs", "komskomskoms", "the.lightseeker", "meshopd", "marlinykevin", "thallyssonsb", "dl940", "ratuauliaa22", "michou_yt", "eyavanana", "kallmewhateveryouwant", "tsezy", "onwardwanna", "littlejem4", "kevindebruyne", "fatihyasin", "frankielapenna", "janeydm", "adammilardovicc", "howridiculous", "iammrbanks", "miketoks", "rus.alien", "jasminechiswell", "olisboa", "hat590", "bilal.hd91", "shanielleroy", "romanlolo", "cuhpcakee", "noahbeck", "daddyyankee", "rebeccazamolo", "ayutingting", "gameboytok", "pam_a_cake", "benjaminmaissecret", "thejoeyswoll", "realmadrid", "ferchugimenez", "esperansagrasia", "cegielski_twins", "emilymariko", "posterised", "steveotv", "chrissymetz", "bdylanhollis", "someasianontiktok", "peterbuiii", "ofumii", "daz_black", "popokbolong", "trastornocturno95", "marisol.viola", "kienreview90", "euro2024", "snarkymarky", "lqlvmrb", "pissingoffmydad", "ireneswnd", "tommyinnit", "carloscastroes", "chef_le3roubi", "rikyoli", "anna..paull", "thehuskyfam", "capricongirl05", "alwishihab234", "jennifer_aplicano", "jypestraykids", "bellafoodie", "thedonato", "quanh__102", "kaylamalecc", "billyandchet", "lilireinhart", "cbum", "williesalim", "cjay011", "mmmjoemele", "thatmartinkid", "itsjojosiwa", "roccotnl", "meosimmyyt", "sofiaalcastro", "mrvisprettyrad", "nikkietutorials", "isaac.h.p.karaoke.backup", "trainee_a", "sillyghillie", "jakeandrich", "sofarsabi", "ngoc.matcha", "joe.bartolozzi", "duolingo", "cardncyn", "dewiperssik_real", "eduardbaka", "dez.thelez", "addisonre", "nickandcarrie", "codenamejesse", "anitta", "ngikuttrendaja", "daryltufekci", "nashvibes", "fujiiian", "elbobby_yt", "tropa_do_adm1", "camotoofunny", "gzfoodqood", "7iprast", "hoaa.hanassii", "jdpantoja", "livvy", "ramcofero1", "dylanjamesmulvaney", "julioangelmunozpr", "cesarpantoja.n", "viki_tory88", "hunterprosper", "kyliejenner", "mieayamthebstt"]).run()
