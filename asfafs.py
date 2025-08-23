<?php
// futbolcu_bilgi_kutusu_cevirici.php
// İngilizce futbolcu bilgi kutusunu Türkçe'ye çeviren ve giriş metni ile kategorileri oluşturan araç

// Parametre eşlemeleri (İngilizce → Türkçe)
$param_map = [
    "name" => "ad",
    "full_name" => "tamadı",
    "image" => "resim",
    "image_size" => "resimboyutu",
    "caption" => "altyazı",
    "birth_name" => "doğumadı",
    "birth_date" => "doğumtarihi",
    "birth_place" => "doğumyeri",
    "death_date" => "ölümtarihi",
    "death_place" => "ölümyeri",
    "height" => "boy",
    "position" => "mevki",
    "currentclub" => "bulunduğukulüp",
    "clubnumber" => "numarası",
    "youthyears1" => "altyapıyıl1",
    "youthclubs1" => "altyapıkulübü1",
    "youthyears2" => "altyapıyıl2",
    "youthclubs2" => "altyapıkulübü2",
    "youthyears3" => "altyapıyıl3",
    "youthclubs3" => "altyapıkulübü3",
    "youthyears4" => "altyapıyıl4",
    "youthclubs4" => "altyapıkulübü4",
    "youthyears5" => "altyapıyıl5",
    "youthclubs5" => "altyapıkulübü5",
    "youthyears6" => "altyapıyıl6",
    "youthclubs6" => "altyapıkulübü6",
    "youthyears7" => "altyapıyıl7",
    "youthclubs7" => "altyapıkulübü7",
    "youthyears8" => "altyapıyıl8",
    "youthclubs8" => "altyapıkulübü8",
    "youthyears9" => "altyapıyıl9",
    "youthclubs9" => "altyapıkulübü9",
    "youthyears10" => "altyapıyıl10",
    "youthclubs10" => "altyapıkulübü10",
    "youthyears11" => "altyapıyıl11",
    "youthclubs11" => "altyapıkulübü11",
    "youthyears12" => "altyapıyıl12",
    "youthclubs12" => "altyapıkulübü12",
    "years1" => "kulüpyıl1",
    "clubs1" => "kulüp1",
    "caps1" => "maç1",
    "goals1" => "gol1",
    "years2" => "kulüpyıl2",
    "clubs2" => "kulüp2",
    "caps2" => "maç2",
    "goals2" => "gol2",
    "years3" => "kulüpyıl3",
    "clubs3" => "kulüp3",
    "caps3" => "maç3",
    "goals3" => "gol3",
    "years4" => "kulüpyıl4",
    "clubs4" => "kulüp4",
    "caps4" => "maç4",
    "goals4" => "gol4",
    "years5" => "kulüpyıl5",
    "clubs5" => "kulüp5",
    "caps5" => "maç5",
    "goals5" => "gol5",
    "years6" => "kulüpyıl6",
    "clubs6" => "kulüp6",
    "caps6" => "maç6",
    "goals6" => "gol6",
    "years7" => "kulüpyıl7",
    "clubs7" => "kulüp7",
    "caps7" => "maç7",
    "goals7" => "gol7",
    "years8" => "kulüpyıl8",
    "clubs8" => "kulüp8",
    "caps8" => "maç8",
    "goals8" => "gol8",
    "years9" => "kulüpyıl9",
    "clubs9" => "kulüp9",
    "caps9" => "maç9",
    "goals9" => "gol9",
    "years10" => "kulüpyıl10",
    "clubs10" => "kulüp10",
    "caps10" => "maç10",
    "goals10" => "gol10",
    "years11" => "kulüpyıl11",
    "clubs11" => "kulüp11",
    "caps11" => "maç11",
    "goals11" => "gol11",
    "years12" => "kulüpyıl12",
    "clubs12" => "kulüp12",
    "caps12" => "maç12",
    "goals12" => "gol12",
    "years13" => "kulüpyıl13",
    "clubs13" => "kulüp13",
    "caps13" => "maç13",
    "goals13" => "gol13",
    "years14" => "kulüpyıl14",
    "clubs14" => "kulüp14",
    "caps14" => "maç14",
    "goals14" => "gol14",
    "years15" => "kulüpyıl15",
    "clubs15" => "kulüp15",
    "caps15" => "maç15",
    "goals15" => "gol15",
    "years16" => "kulüpyıl16",
    "clubs16" => "kulüp16",
    "caps16" => "maç16",
    "goals16" => "gol16",
    "years17" => "kulüpyıl17",
    "clubs17" => "kulüp17",
    "caps17" => "maç17",
    "goals17" => "gol17",
    "years18" => "kulüpyıl18",
    "clubs18" => "kulüp18",
    "caps18" => "maç18",
    "goals18" => "gol18",
    "years19" => "kulüpyıl19",
    "clubs19" => "kulüp19",
    "caps19" => "maç19",
    "goals19" => "gol19",
    "years20" => "kulüpyıl20",
    "clubs20" => "kulüp20",
    "caps20" => "maç20",
    "goals20" => "gol20",
    "years21" => "kulüpyıl21",
    "clubs21" => "kulüp21",
    "caps21" => "maç21",
    "goals21" => "gol21",
    "years22" => "kulüpyıl22",
    "clubs22" => "kulüp22",
    "caps22" => "maç22",
    "goals22" => "gol22",
    "years23" => "kulüpyıl23",
    "clubs23" => "kulüp23",
    "caps23" => "maç23",
    "goals23" => "gol23",
    "years24" => "kulüpyıl24",
    "clubs24" => "kulüp24",
    "caps24" => "maç24",
    "goals24" => "gol24",
    "years25" => "kulüpyıl25",
    "clubs25" => "kulüp25",
    "caps25" => "maç25",
    "goals25" => "gol25",
    "years26" => "kulüpyıl26",
    "clubs26" => "kulüp26",
    "caps26" => "maç26",
    "goals26" => "gol26",
    "years27" => "kulüpyıl27",
    "clubs27" => "kulüp27",
    "caps27" => "maç27",
    "goals27" => "gol27",
    "years28" => "kulüpyıl28",
    "clubs28" => "kulüp28",
    "caps28" => "maç28",
    "goals28" => "gol28",
    "years29" => "kulüpyıl29",
    "clubs29" => "kulüp29",
    "caps29" => "maç29",
    "goals29" => "gol29",
    "years30" => "kulüpyıl30",
    "clubs30" => "kulüp30",
    "caps30" => "maç30",
    "goals30" => "gol30",
    "years31" => "kulüpyıl31",
    "clubs31" => "kulüp31",
    "caps31" => "maç31",
    "goals31" => "gol31",
    "years32" => "kulüpyıl32",
    "clubs32" => "kulüp32",
    "caps32" => "maç32",
    "goals32" => "gol32",
    "years33" => "kulüpyıl33",
    "clubs33" => "kulüp33",
    "goals33" => "gol33",
    "years34" => "kulüpyıl34",
    "clubs34" => "kulüp34",
    "goals34" => "gol34",
    "years35" => "kulüpyıl35",
    "clubs35" => "kulüp35",
    "goals35" => "gol35",
    "years36" => "kulüpyıl36",
    "clubs36" => "kulüp36",
    "goals36" => "gol36",
    "years37" => "kulüpyıl37",
    "clubs37" => "kulüp37",
    "goals37" => "gol37",
    "years38" => "kulüpyıl38",
    "clubs38" => "kulüp38",
    "goals38" => "gol38",
    "years39" => "kulüpyıl39",
    "clubs39" => "kulüp39",
    "goals39" => "gol39",
    "years40" => "kulüpyıl40",
    "clubs40" => "kulüp40",
    "goals40" => "gol40",
    "years41" => "kulüpyıl41",
    "clubs41" => "kulüp41",
    "goals41" => "gol41",
    "years42" => "kulüpyıl42",
    "clubs42" => "kulüp42",
    "goals42" => "gol42",
    "years43" => "kulüpyıl43",
    "clubs43" => "kulüp43",
    "goals43" => "gol43",
    "years44" => "kulüpyıl44",
    "clubs44" => "kulüp44",
    "goals44" => "gol44",
    "years45" => "kulüpyıl45",
    "clubs45" => "kulüp45",
    "goals45" => "gol45",
    "years46" => "kulüpyıl46",
    "clubs46" => "kulüp46",
    "goals46" => "gol46",
    "years47" => "kulüpyıl47",
    "clubs47" => "kulüp47",
    "goals47" => "gol47",
    "years48" => "kulüpyıl48",
    "clubs48" => "kulüp48",
    "goals48" => "gol48",
    "years49" => "kulüpyıl49",
    "clubs49" => "kulüp49",
    "goals49" => "gol49",
    "years50" => "kulüpyıl50",
    "clubs50" => "kulüp50",
    "goals50" => "gol50",
    "years51" => "kulüpyıl51",
    "clubs51" => "kulüp51",
    "goals51" => "gol51",
    "years52" => "kulüpyıl52",
    "clubs52" => "kulüp52",
    "goals52" => "gol52",
    "medaltemplates" => "madalyalar",
    "club-update" => "güncelleme",
    "totalcaps" => "toplammaç",
    "totalgoals" => "toplamgol",
    // Milli takım kariyeri
"nationalyears1" => "milliyıl1",
"nationalteam1" => "millitakım1",
"nationalcaps1" => "milli_maç1",
"nationalgoals1" => "milli_gol1",
"nationalyears2" => "milliyıl2",
"nationalteam2" => "millitakım2",
"nationalcaps2" => "milli_maç2",
"nationalgoals2" => "milli_gol2",
"nationalyears3" => "milliyıl3",
"nationalteam3" => "millitakım3",
"nationalcaps3" => "milli_maç3",
"nationalgoals3" => "milli_gol3",
"nationalyears4" => "milliyıl4",
"nationalteam4" => "millitakım4",
"nationalcaps4" => "milli_maç4",
"nationalgoals4" => "milli_gol4",
"nationalyears5" => "milliyıl5",
"nationalteam5" => "millitakım5",
"nationalcaps5" => "milli_maç5",
"nationalgoals5" => "milli_gol5",
"nationalyears6" => "milliyıl6",
"nationalteam6" => "millitakım6",
"nationalcaps6" => "milli_maç6",
"nationalgoals6" => "milli_gol6",
"nationalyears7" => "milliyıl7",
"nationalteam7" => "millitakım7",
"nationalcaps7" => "milli_maç7",
"nationalgoals7" => "milli_gol7",
"nationalyears8" => "milliyıl8",
"nationalteam8" => "millitakım8",
"nationalcaps8" => "milli_maç8",
"nationalgoals8" => "milli_gol8",
"nationalyears9" => "milliyıl9",
"nationalteam9" => "millitakım9",
"nationalcaps9" => "milli_maç9",
"nationalgoals9" => "milli_gol9",
    // ... bu örnek yapı, numaralandırmayı ihtiyaca göre devam ettir
    // Teknik direktörlük kariyeri (manageryears ve managerclubs)
"manageryears1" => "çalıştığıyıl1",
"managerclubs1" => "çalıştığıkulüp1",
"manageryears2" => "çalıştığıyıl2",
"managerclubs2" => "çalıştığıkulüp2",
"manageryears3" => "çalıştığıyıl3",
"managerclubs3" => "çalıştığıkulüp3",
"manageryears4" => "çalıştığıyıl4",
"managerclubs4" => "çalıştığıkulüp4",
"manageryears5" => "çalıştığıyıl5",
"managerclubs5" => "çalıştığıkulüp5",
"manageryears6" => "çalıştığıyıl6",
"managerclubs6" => "çalıştığıkulüp6",
"manageryears7" => "çalıştığıyıl7",
"managerclubs7" => "çalıştığıkulüp7",
"manageryears8" => "çalıştığıyıl8",
"managerclubs8" => "çalıştığıkulüp8",
"manageryears9" => "çalıştığıyıl9",
"managerclubs9" => "çalıştığıkulüp9",
"manageryears10" => "çalıştığıyıl10",
"managerclubs10" => "çalıştığıkulüp10",
"manageryears11" => "çalıştığıyıl11",
"managerclubs11" => "çalıştığıkulüp11",
"manageryears12" => "çalıştığıyıl12",
"managerclubs12" => "çalıştığıkulüp12",
"manageryears13" => "çalıştığıyıl13",
"managerclubs13" => "çalıştığıkulüp13",
"manageryears14" => "çalıştığıyıl14",
"managerclubs14" => "çalıştığıkulüp14",
"manageryears15" => "çalıştığıyıl15",
"managerclubs15" => "çalıştığıkulüp15",
"manageryears16" => "çalıştığıyıl16",
"managerclubs16" => "çalıştığıkulüp16",
"manageryears17" => "çalıştığıyıl17",
"managerclubs17" => "çalıştığıkulüp17",
"manageryears18" => "çalıştığıyıl18",
"managerclubs18" => "çalıştığıkulüp18",
"manageryears19" => "çalıştığıyıl19",
"managerclubs19" => "çalıştığıkulüp19",
"manageryears20" => "çalıştığıyıl20",
"managerclubs20" => "çalıştığıkulüp20",
"manageryears21" => "çalıştığıyıl21",
"managerclubs21" => "çalıştığıkulüp21",
"manageryears22" => "çalıştığıyıl22",
"managerclubs22" => "çalıştığıkulüp22",
"manageryears23" => "çalıştığıyıl23",
"managerclubs23" => "çalıştığıkulüp23",
"manageryears24" => "çalıştığıyıl24",
"managerclubs24" => "çalıştığıkulüp24",
"manageryears25" => "çalıştığıyıl25",
"managerclubs25" => "çalıştığıkulüp25",
"manageryears26" => "çalıştığıyıl26",
"managerclubs26" => "çalıştığıkulüp26",
"manageryears27" => "çalıştığıyıl27",
"managerclubs27" => "çalıştığıkulüp27",
"manageryears28" => "çalıştığıyıl28",
"managerclubs28" => "çalıştığıkulüp28",
"manageryears29" => "çalıştığıyıl29",
"managerclubs29" => "çalıştığıkulüp29",
"manageryears30" => "çalıştığıyıl30",
"managerclubs30" => "çalıştığıkulüp30",
"manageryears31" => "çalıştığıyıl31",
"managerclubs31" => "çalıştığıkulüp31",
"manageryears32" => "çalıştığıyıl32",
"managerclubs32" => "çalıştığıkulüp32",
"manageryears33" => "çalıştığıyıl33",
"managerclubs33" => "çalıştığıkulüp33",
"manageryears34" => "çalıştığıyıl34",
"managerclubs34" => "çalıştığıkulüp34",
"manageryears35" => "çalıştığıyıl35",
"managerclubs35" => "çalıştığıkulüp35",
"manageryears36" => "çalıştığıyıl36",
"managerclubs36" => "çalıştığıkulüp36",
"manageryears37" => "çalıştığıyıl37",
"managerclubs37" => "çalıştığıkulüp37",
"manageryears38" => "çalıştığıyıl38",
"managerclubs38" => "çalıştığıkulüp38",
"manageryears39" => "çalıştığıyıl39",
"managerclubs39" => "çalıştığıkulüp39",
"manageryears40" => "çalıştığıyıl40",
"managerclubs40" => "çalıştığıkulüp40",
"manageryears41" => "çalıştığıyıl41",
"managerclubs41" => "çalıştığıkulüp41",
"manageryears42" => "çalıştığıyıl42",
"managerclubs42" => "çalıştığıkulüp42",
"manageryears43" => "çalıştığıyıl43",
"managerclubs43" => "çalıştığıkulüp43",
"manageryears44" => "çalıştığıyıl44",
"managerclubs44" => "çalıştığıkulüp44",
"manageryears45" => "çalıştığıyıl45",
"managerclubs45" => "çalıştığıkulüp45",
"manageryears46" => "çalıştığıyıl46",
"managerclubs46" => "çalıştığıkulüp46",
"manageryears47" => "çalıştığıyıl47",
"managerclubs47" => "çalıştığıkulüp47",
"manageryears48" => "çalıştığıyıl48",
"managerclubs48" => "çalıştığıkulüp48",
"manageryears49" => "çalıştığıyıl49",
"managerclubs49" => "çalıştığıkulüp49",
"manageryears50" => "çalıştığıyıl50",
"managerclubs50" => "çalıştığıkulüp50",
    // Buraya diğer parametreleri ekleyebilirsin
];

// Kulüp parametreleri
for($i=1;$i<=20;$i++){
    $param_map["years$i"]="kulüpyıl$i";
    $param_map["clubs$i"]="kulüp$i";
}

// Parametre değerlerini çevir (pozisyon ve milli takımlar)
$value_map = [
    "[[Forward (association football)|Striker]]" => "[[Forvet (futbol)|Forvet]]",
    "[[Forward]]" => "[[Forvet (futbol)|Forvet]]",
    "[[Defence]]" => "[[Defans]]",
    "[[Defender]]" => "[[Defans]]",
    "[[Midfielder]]" => "[[Orta saha]]",
    "[[Goalkeeper]]" => "[[Kaleci (futbol)|Kaleci]]",
    "[[Goalkeeper (association football)|Goalkeeper]]" => "[[Kaleci (futbol)|Kaleci]]",
    "[[Winger]]" => "[[Kanat]]",
    "[[Attacking midfielder]]" => "[[Ofansif orta saha]]",
    "[[Defensive midfielder]]" => "[[Defansif orta saha]]",
    // Milli takımlar
    "national under-15 football team" => "15 yaş altı millî futbol takımı",
    "national under-16 football team" => "16 yaş altı millî futbol takımı",
    "national under-17 football team" => "17 yaş altı millî futbol takımı",
    "national under-18 football team" => "18 yaş altı millî futbol takımı",
    "national under-19 football team" => "19 yaş altı millî futbol takımı",
    "national under-20 football team" => "20 yaş altı millî futbol takımı",
    "national under-21 football team" => "21 yaş altı millî futbol takımı",
    "men's national football team" => "millî futbol takımı",
    // Ülkeler
 "Afghanistan" => "Afganistan", "Albania" => "Arnavutluk", "Algeria" => "Cezayir", "Andorra" => "Andorra", "Angola" => "Angola", "Antigua and Barbuda" => "Antigua ve Barbuda", "Argentina" => "Arjantin", "Armenia" => "Ermenistan", "Australia" => "Avustralya", "Austria" => "Avusturya", "Azerbaijan" => "Azerbaycan", "Bahamas" => "Bahamalar", "Bahrain" => "Bahreyn", "Bangladesh" => "Bangladeş", "Barbados" => "Barbados", "Belarus" => "Beyaz Rusya", "Belgium" => "Belçika", "Belize" => "Belize", "Benin" => "Benin", "Bhutan" => "Butan", "Bolivia" => "Bolivya", "Bosnia and Herzegovina" => "Bosna-Hersek", "Botswana" => "Botsvana", "Brazil" => "Brezilya", "Brunei" => "Brunei", "Bulgaria" => "Bulgaristan", "Burkina Faso" => "Burkina Faso", "Burundi" => "Burundi", "Cambodia" => "Kamboçya", "Cameroon" => "Kamerun", "Canada" => "Kanada", "Cape Verde" => "Yeşil Burun", "Central African Republic" => "Orta Afrika Cumhuriyeti", "Chad" => "Çad", "Chile" => "Şili", "China" => "Çin", "Colombia" => "Kolombiya", "Comoros" => "Komorlar", "Costa Rica" => "Kosta Rika", "Côte d'Ivoire" => "Fildişi Sahili", "Croatia" => "Hırvatistan", "Cuba" => "Küba", "Cyprus" => "Kıbrıs", "Czechia" => "Çekya", "Democratic Republic of the Congo" => "Demokratik Kongo Cumhuriyeti", "Denmark" => "Danimarka", "Djibouti" => "Cibuti", "Dominica" => "Dominika", "Dominican Republic" => "Dominik Cumhuriyeti", "Ecuador" => "Ekvador", "Egypt" => "Mısır", "El Salvador" => "El Salvador", "Equatorial Guinea" => "Ekvator Ginesi", "Eritrea" => "Eritre", "Estonia" => "Estonya", "Eswatini" => "Svaziland", "Ethiopia" => "Etiyopya", "Fiji" => "Fiji", "Finland" => "Finlandiya", "France" => "Fransa", "Gabon" => "Gabon", "Gambia" => "Gambiya", "Georgia" => "Gürcistan", "Germany" => "Almanya", "Ghana" => "Gana", "Greece" => "Yunanistan", "Grenada" => "Grenada", "Guatemala" => "Guatemala", "Guinea" => "Gine", "Guinea-Bissau" => "Gine-Bisau", "Guyana" => "Guyana", "Haiti" => "Haiti", "Honduras" => "Honduras", "Hungary" => "Macaristan", "Iceland" => "İzlanda", "India" => "Hindistan", "Indonesia" => "Endonezya", "Iran" => "İran", "Iraq" => "Irak", "Ireland" => "İrlanda", "Israel" => "İsrail", "Italy" => "İtalya", "Jamaica" => "Jamaika", "Japan" => "Japonya", "Jordan" => "Ürdün", "Kazakhstan" => "Kazakistan", "Kenya" => "Kenya", "Kiribati" => "Kiribati", "Kuwait" => "Kuveyt", "Kyrgyzstan" => "Kırgızistan", "Laos" => "Laos", "Latvia" => "Letonya", "Lebanon" => "Lübnan", "Lesotho" => "Lesoto", "Liberia" => "Liberya", "Libya" => "Libya", "Liechtenstein" => "Lihtenştayn", "Lithuania" => "Litvanya", "Luxembourg" => "Lüksemburg", "Madagascar" => "Madagaskar", "Malawi" => "Malavi", "Malaysia" => "Malezya", "Maldives" => "Maldivler", "Mali" => "Mali", "Malta" => "Malta", "Marshall Islands" => "Marşal Adaları", "Mauritania" => "Moritanya", "Mauritius" => "Mauritius", "Mexico" => "Meksika", "Micronesia" => "Mikronezya", "Moldova" => "Moldova", "Monaco" => "Monako", "Mongolia" => "Moğolistan", "Montenegro" => "Karadağ", "Morocco" => "Fas", "Mozambique" => "Mozambik", "Myanmar" => "Myanmar", "Namibia" => "Namibya", "Nauru" => "Nauru", "Nepal" => "Nepal", "Netherlands" => "Hollanda", "New Zealand" => "Yeni Zelanda", "Nicaragua" => "Nikaragua", "Nijeria" => "Nijerya", "Niger" => "Nijer", "Nigeria" => "Nijerya", "North Korea" => "Kuzey Kore", "North Macedonia" => "Kuzey Makedonya", "Norway" => "Norveç", "Oman" => "Umman", "Pakistan" => "Pakistan", "Palau" => "Palau", "Palestine" => "Filistin", "Panama" => "Panama", "Papua New Guinea" => "Papua Yeni Gine", "Paraguay" => "Paraguay", "Peru" => "Peru", "Philippines" => "Filipinler", "Poland" => "Polonya", "Portugal" => "Portekiz", "Qatar" => "Katar", "Republic of the Congo" => "Kongo Cumhuriyeti", "Romania" => "Romanya", "Russia" => "Rusya", "Rwanda" => "Ruanda", "Saint Kitts and Nevis" => "Saint Kitts ve Nevis", "Saint Lucia" => "Saint Lucia", "Saint Vincent and the Grenadines" => "Saint Vincent ve Grenadinler", "Samoa" => "Samoa", "San Marino" => "San Marino", "São Tomé and Príncipe" => "São Tomé ve Príncipe", "Saudi Arabia" => "Suudi Arabistan", "Senegal" => "Senegal", "Serbia" => "Sırbistan", "Seychelles" => "Seyşeller", "Sierra Leone" => "Sierra Leone", "Singapore" => "Singapur", "Slovakia" => "Slovakya", "Slovenia" => "Slovenya", "Solomon Islands" => "Solomon Adaları", "Somalia" => "Somali", "South Africa" => "Güney Afrika", "South Korea" => "Güney Kore", "South Sudan" => "Güney Sudan", "Spain" => "İspanya", "Sri Lanka" => "Sri Lanka", "Sudan" => "Sudan", "Suriname" => "Surinam", "Sweden" => "İsveç", "Switzerland" => "İsviçre", "Syria" => "Suriye", "Tajikistan" => "Tacikistan", "Tanzania" => "Tanzanya", "Thailand" => "Tayland", "Timor-Leste" => "Doğu Timor", "Togo" => "Togo", "Tonga" => "Tonga", "Trinidad and Tobago" => "Trinidad ve Tobago", "Tunisia" => "Tunus", "Turkey" => "Türkiye", "Turkmenistan" => "Türkmenistan", "Tuvalu" => "Tuvalu", "Uganda" => "Uganda", "Ukraine" => "Ukrayna", "United Arab Emirates" => "Birleşik Arap Emirlikleri", "United Kingdom" => "Birleşik Krallık", "United States of America" => "Amerika Birleşik Devletleri", "Uruguay" => "Uruguay", "Uzbekistan" => "Özbekistan", "Vanuatu" => "Vanuatu", "Venezuela" => "Venezuela", "Vietnam" => "Vietnam", "Yemen" => "Yemen", "Zambia" => "Zambiya", "Zimbabwe" => "Zimbabve",
   // Terimler
    "Men's" => "Erkekler",
    "[[Association football|football]]" => "[[futbol]]",
    "Team" => "Takım",
];

$input_text = "";
$translated_text = "";
$intro_text = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $input_text = $_POST["source_text"];
    $translated_text = $input_text;

    // 1. Şablon adını çevir
    $translated_text = preg_replace("/\{\{\s*Infobox football biography/i","{{Futbolcu bilgi kutusu",$translated_text);

    // 2. Karakterleri çevir
    $translated_text = str_replace(["–","(loan)"],["-","(kiralık)"],$translated_text);

    // 3. Parametreleri çevir
    foreach ($param_map as $eng => $tr) {
        $translated_text = preg_replace("/\|\s*$eng\s*=/i", "| $tr =", $translated_text);
    }

    // 4. Parametre değerlerini çevir
    foreach ($value_map as $eng_val => $tr_val) {
        $translated_text = str_replace($eng_val, $tr_val, $translated_text);
    }

    // -------------------------
    // Giriş cümlesi ve kategoriler
    // -------------------------
    $intro = "";
    $categories = [];

    // Ad
    preg_match("/\|\s*ad\s*=\s*(.*)/i",$translated_text,$m);
    $name = trim($m[1]??'');
    $intro .= "'''$name'''";

    // Doğum tarihi ve yeri
    preg_match("/\|\s*doğumtarihi\s*=\s*(.*)/i",$translated_text,$m);
    $birth = trim($m[1]??'');
    preg_match("/\|\s*doğumyeri\s*=\s*(.*)/i",$translated_text,$m);
    $birthplace = trim($m[1]??'');

    // Doğum tarihi formatı ve kategorisi
    $birth_year = '';
    if($birth!=''){
        if(preg_match('/(\d+)\|(\d+)\|(\d+)/',$birth,$dateparts)){
            $months_tr = ["January"=>"Ocak","February"=>"Şubat","March"=>"Mart","April"=>"Nisan","May"=>"Mayıs","June"=>"Haziran","July"=>"Temmuz","August"=>"Ağustos","September"=>"Eylül","October"=>"Ekim","November"=>"Kasım","December"=>"Aralık"];
            $birth_day = intval($dateparts[3]);
            $birth_month = $months_tr[date("F", mktime(0,0,0,intval($dateparts[2]),1))];
            $birth_year = intval($dateparts[1]);
            $birth = "$birth_day $birth_month $birth_year";

            $categories[] = "[[Kategori:{$birth_year} doğumlular]]";
        }
    }

    if($birth!='' || $birthplace!=''){
        $intro .= " (d. $birth, $birthplace)";
    }

// Ölüm tarihi kontrolü
preg_match("/\|\s*ölümtarih\s*=\s*(.*)/i",$translated_text,$death_match);
$death_date = trim($death_match[1] ?? '');

if($death_date == '') {
    // Ölüm tarihi girilmemişse
    $categories[] = "[[Kategori:Yaşayan insanlar]]";
}

    // Ölüm tarihi ve kategorisi
    preg_match("/\|\s*ölümtarihi\s*=\s*(.*)/i",$translated_text,$m);
    $death = trim($m[1]??'');
    preg_match("/\|\s*ölümyeri\s*=\s*(.*)/i",$translated_text,$m);
    $deathplace = trim($m[1]??'');

    if($death!=''){
        if(preg_match('/(\d+)\|(\d+)\|(\d+)/',$death,$dateparts)){
            $death_year = intval($dateparts[1]);
            $categories[] = "[[Kategori:{$death_year} yılında ölenler]]";
        }
        $intro .= "; ö. $death";
    }

    // Pozisyon
    preg_match("/\|\s*mevki\s*=\s*(.*)/i",$translated_text,$m);
    $position = trim($m[1]??'');
    if($position!='') $intro .= ", $position pozisyonunda görev yapan futbolcudur.";
    else $intro .= " pozisyonunda görev yapan futbolcudur.";

    // Kulüpler
    $clubs = [];
    for($i=1;$i<=5;$i++){
        preg_match("/\|\s*kulüp$i\s*=\s*(.*)/i",$translated_text,$m);
        $c = trim($m[1]??'');
        if($c!='') $clubs[] = $c;
    }
    if(count($clubs)>0){
        $intro .= " Profesyonel kariyerine ".$clubs[0]." kulübünde başladı.";
        if(count($clubs)>1){
            $intro .= " Daha sonra sırasıyla ".implode(", ",array_slice($clubs,1))." takımlarda oynadı.";
        }
    }

// Milli takımlar ve kategoriler
$national_teams = [];
for($i=1;$i<=7;$i++){
    preg_match("/\|\s*millitakım$i\s*=\s*(.*)/i",$translated_text,$m);
    $team = trim($m[1]??'');
    if($team!='') {

        // Kategori için bağlantısız düz yazı lazım
        $team_display = preg_replace('/\[\[.*\|(.*)\]\]/','$1',$team);
        $team_display = str_replace(['[[',']]'],'',$team_display);

        $age_category = '';
        if(preg_match('/U-?(\d+)/i',$team_display,$age_match)){
            $age_category = $age_match[1]." yaş altı ";
        }
        $country = preg_replace('/U-?\d+/i','',$team_display);
        $country = trim($country);

        // Kategoriye düz yazıyı ekle
        $categories[] = "[[Kategori:$country {$age_category}millî futbol takımı futbolcuları]]";

        // Giriş cümlesi için bağlantılı haliyle ekle
        $national_teams[] = $team;
    }
}
if(count($national_teams)==1) {
    $intro .= " Aynı zamanda {$national_teams[0]} millî takımının formasını giydi.";
} elseif(count($national_teams)>1){
    $last = array_pop($national_teams);
    $intro .= " Aynı zamanda ".implode(", ",$national_teams)." ve $last millî takımlarının formasını giydi.";
}

    // Pozisyon kategorisi
    if($position!=''){
        $pos_clean = preg_replace('/\[\[.*\|(.*)\]\]/', '$1', $position);
        $pos_clean = str_replace(['[[',']]'],'',$pos_clean);
        $categories[] = "[[Kategori:$pos_clean futbolcular]]";
    }

    $intro_text = $intro."\n\n".implode("\n",$categories);
}
?>

<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Vikipedi Futbolcu Bilgi Kutusu Çeviri Aracı</title>
<style>
    body { font-family: 'Segoe UI', sans-serif; margin: 20px; background: #f0f0f0; }
    h2 { text-align: center; }
    .container { display: flex; justify-content: space-between; gap: 20px; /* Sütunlar arasına boşluk ekledik */ }
    
    /* Her bir sütun için stil */
    .column {
        width: 50%; /* Genişliği esnek hale getirdik */
        display: flex;
        flex-direction: column;
    }

    /* Başlıklar için stil */
    .column h4 {
        margin-top: 0;
        margin-bottom: 8px;
        color: #333;
        font-weight: 600;
    }

    /* Metin kutuları için ortak stiller */
    .text-box {
        width: 100%;
        height: 800px;
        padding: 10px;
        font-family: monospace;
        font-size: 14px;
        border: 1px solid #ccc;
        box-sizing: border-box; /* Padding ve border'ın genişliğe dahil olmasını sağlar */
    }

    /* Çıktı kutusu için ek stiller */
    #translated_with_intro {
        background: #fff;
        white-space: pre-wrap;
        overflow-y: auto; /* İçerik taşarsa kaydırma çubuğu çıkar */
    }
    
    /* Ana Çevir Butonu */
    #main_submit_button {
        display: block; 
        width: 200px;
        margin: 20px auto;
    }

    /* Butonlar için ortak stil */
    button {
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 8px;
        border: none;
        background-color: #007bff;
        color: white;
        transition: background-color 0.2s ease;
    }

    /* Fare butonun üzerine geldiğinde çalışacak stil */
    button:hover {
        background-color: #0056b3;
    }

    /* YENİ: Temizle butonu için farklı stil */
    #clearBtn {
        background-color: #dc3545; /* Kırmızı renk */
    }
    #clearBtn:hover {
        background-color: #c82333; /* Koyu kırmızı */
    }

    /* YENİ: Buton grubu için stil (sağa hizalamak için) */
    .button-group {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    
    .button-group.align-right {
        justify-content: flex-end; /* İçindeki butonları sağa yaslar */
    }

    .button-group.align-left {
        justify-content: flex-start; /* İçindeki butonları sola yaslar (varsayılan) */
    }
</style>
</head>
<body>

<h2>Futbolcu Bilgi Kutusu Çevirici</h2>
<form method="post" id="translationForm">
    <div class="container">
        <div class="column">
            <h4>İngilizce Kaynak Şablon</h4>
            <textarea name="source_text" id="source_text" class="text-box" placeholder="İngilizce şablon buraya..."><?= htmlspecialchars($input_text ?? '') ?></textarea>
            
            <div class="button-group align-left">
                <button type="button" id="clearBtn">Temizle</button>
            </div>
        </div>

        <div class="column">
            <h4>Türkçe Çıktı</h4>
            <div id="translated_with_intro" class="text-box"><?= htmlspecialchars(($translated_text ?? '')."\n\n".($intro_text ?? '')) ?></div>
            
            <div class="button-group align-right">
                <button type="button" id="selectAllBtn">Tümünü Seç</button>
                <button type="button" id="copyBtn">Metni Kopyala</button>
            </div>
        </div>
    </div>
    <button type="submit" id="main_submit_button">Çevir</button>
</form>

<script>
// Gerekli HTML elemanlarını seçiyoruz
const selectAllButton = document.getElementById('selectAllBtn');
const copyButton = document.getElementById('copyBtn');
const clearButton = document.getElementById('clearBtn'); // Yeni buton
const outputBox = document.getElementById('translated_with_intro');
const sourceBox = document.getElementById('source_text'); // Yeni kaynak kutusu

// "Tümünü Seç" butonuna tıklandığında çalışacak kod
selectAllButton.addEventListener('click', () => {
    const range = document.createRange();
    range.selectNodeContents(outputBox);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
});

// "Metni Kopyala" butonuna tıklandığında çalışacak kod
copyButton.addEventListener('click', () => {
    const textToCopy = outputBox.innerText;
    if (!textToCopy) return;

    navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = copyButton.innerText;
        copyButton.innerText = 'Kopyalandı!';
        setTimeout(() => {
            copyButton.innerText = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Metin kopyalanamadı: ', err);
    });
});

// YENİ: "Temizle" butonuna tıklandığında çalışacak kod
clearButton.addEventListener('click', () => {
    sourceBox.value = ''; // Soldaki metin kutusunu temizle
    outputBox.innerText = ''; // Sağdaki metin kutusunu temizle
});
</script>

</body>
</html>
