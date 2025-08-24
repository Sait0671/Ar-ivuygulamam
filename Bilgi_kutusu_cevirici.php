<?php
// Gelişmiş Vikipedi Futbolcu Bilgi Kutusu Çeviri Asistanı v4.1 (Nihai Sürüm)
ini_set('display_errors', 0);
error_reporting(E_ALL);

// =============================================================================
// PARAMETRE VE DEĞER HARİTALARI
// =============================================================================
$param_map = [ "name" => "ad", "full_name" => "tamadı", "image" => "resim", "image_size" => "resimboyutu", "caption" => "altyazı", "birth_name" => "doğumadı", "birth_date" => "doğumtarihi", "birth_place" => "doğumyeri", "death_date" => "ölümtarihi", "death_place" => "ölümyeri", "height" => "boy", "position" => "mevki", "currentclub" => "bulunduğukulüp", "clubnumber" => "numarası", "club-update" => "güncelleme", "nationalteam-update" => "millitakımgüncelleme", "totalcaps" => "toplammaç", "totalgoals" => "toplamgol", "medaltemplates" => "madalyalar", "upright" => "resim_ölçek", ];
$loop_params = [ 'youthyears' => 'altyapıyıl', 'youthclubs' => 'altyapıkulübü', 'years' => 'kulüpyıl', 'clubs' => 'kulüp', 'caps' => 'maç', 'goals' => 'gol', 'nationalyears' => 'milliyıl', 'nationalteam' => 'millitakım', 'nationalcaps' => 'milli_maç', 'nationalgoals' => 'milli_gol', 'manageryears' => 'çalıştığıyıl', 'managerclubs' => 'çalıştığıkulüp' ];
for ($i = 1; $i <= 50; $i++) { foreach ($loop_params as $eng => $tr) { $param_map[$eng . $i] = $tr . $i; } }
$value_map = [ 
    "[[Striker (association football)|Striker]]" => "[[Forvet (futbol)|Forvet]]", "[[Forward (association football)|Striker]]" => "[[Forvet (futbol)|Forvet]]", "[[Forward (association football)|Forward]]" => "[[Forvet (futbol)|Forvet]]", "[[Forward]]" => "[[Forvet (futbol)|Forvet]]", "[[Striker]]" => "[[Forvet (futbol)|Forvet]]", "[[Centre-forward]]" => "[[Santrfor]]", "[[Winger (association football)|Winger]]" => "[[Kanat (futbol)|Kanat]]", "[[Winger]]" => "[[Kanat (futbol)|Kanat]]", "[[Midfielder]]" => "[[Orta saha]]", "[[Attacking midfielder]]" => "[[Ofansif orta saha]]", "[[Defensive midfielder]]" => "[[Defansif orta saha]]", "[[Defender (association football)|Defender]]" => "[[Defans (futbol)|Defans]]", "[[Defender]]" => "[[Defans (futbol)|Defans]]", "[[Centre-back]]" => "[[Stoper]]", "[[Goalkeeper (association football)|Goalkeeper]]" => "[[Kaleci (futbol)|Kaleci]]", "[[Goalkeeper]]" => "[[Kaleci (futbol)|Kaleci]]",
    "(loan)" => "(kiralık)", "(manager)" => "(teknik direktör)", "(player-manager)" => "(oyuncu-teknik direktör)", "(caretaker)" => "(geçici teknik direktör)",
    "–" => "-", "[[Association football|football]]" => "[[futbol]]", "Men's" => "Erkekler", "Team" => "Takım", 
    "West Germany" => "Batı Almanya", "Norway" => "Norveç", "England" => "İngiltere", "Spain" => "İspanya", "Germany" => "Almanya", "Turkey" => "Türkiye", "Brazil" => "Brezilya", "Argentina" => "Arjantin", "France" => "Fransa", "Italy" => "İtalya", "Portugal" => "Portekiz", "Netherlands" => "Hollanda", ];

// =============================================================================
// Ana Çeviri Fonksiyonu
// =============================================================================
function perform_translation($infobox_text, &$infobox_part, &$intro_part, &$categories_part) {
    global $param_map, $value_map;
    $data = parse_infobox($infobox_text); $translated_data = []; $skip_value_translation_keys = ['resim', 'altyazı'];
    foreach ($data as $key => $value) {
        $value = strip_comments($value); $translated_key = $param_map[strtolower($key)] ?? $key;
        if (in_array($translated_key, $skip_value_translation_keys)) { $translated_value = $value; } 
        else {
            $value = translate_complex_values($value); $value = translate_templates($value);
            $translated_value = str_replace(array_keys($value_map), array_values($value_map), $value);
            $translated_value = format_club_name($translated_value);
            if (strpos($translated_key, 'güncelleme') !== false) { $translated_value = translate_date_string($translated_value); }
        }
        $translated_data[$translated_key] = $translated_value;
    }
    $infobox_lines = []; foreach ($translated_data as $key => $value) { $infobox_lines[] = "| $key = $value"; }
    $infobox_part = trim("{{Futbolcu bilgi kutusu\n" . implode("\n", $infobox_lines) . "\n}}");
    $intro_part = trim(generate_intro($translated_data));
    $categories_part = trim(implode("\n", generate_categories($translated_data)));
}

// =============================================================================
// FORM İŞLEMLERİ
// =============================================================================
$error_message = ""; $infobox_part = ""; $intro_part = ""; $categories_part = ""; $english_source_part = "";
$input_url = ""; $input_text = ""; $active_tab = 'urlTab'; // Varsayılan aktif sekme

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if (isset($_POST['submit_url']) && !empty($_POST["source_url"])) {
        $active_tab = 'urlTab';
        $input_url = trim($_POST["source_url"]);
        $path = parse_url($input_url, PHP_URL_PATH); $parts = explode('/', $path); $page_title = end($parts);
        if (!$page_title) { $error_message = "Geçersiz Vikipedi URL'si."; } 
        else {
            $raw_content_url = "https://en.wikipedia.org/w/index.php?title=" . urlencode($page_title) . "&action=raw";
            $wikitext = fetch_url($raw_content_url);
            if ($wikitext === false) { $error_message = "Vikipedi sayfasının içeriği alınamadı."; } 
            else {
                $infobox_text = find_and_extract_infobox($wikitext, 'Infobox football biography');
                if ($infobox_text === false) { $error_message = "Sayfada 'Infobox football biography' şablonu bulunamadı."; } 
                else { $english_source_part = $infobox_text; perform_translation($infobox_text, $infobox_part, $intro_part, $categories_part); }
            }
        }
    }
    elseif (isset($_POST['submit_text']) && !empty($_POST["source_text"])) {
        $active_tab = 'textTab';
        $input_text = $_POST["source_text"]; $english_source_part = $input_text;
        perform_translation($input_text, $infobox_part, $intro_part, $categories_part);
    }
}

// =============================================================================
// YARDIMCI FONKSİYONLAR
// =============================================================================
function fetch_url($url) { if (!function_exists('curl_init')) { return false; } $ch = curl_init(); curl_setopt($ch, CURLOPT_URL, $url); curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true); curl_setopt($ch, CURLOPT_USERAGENT, 'VikipediCeviriAraci/4.1 (lütfen kendi bilgilerinizle güncelleyin)'); curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false); $output = curl_exec($ch); if (curl_errno($ch)) { $output = false; } curl_close($ch); return $output; }
function find_and_extract_infobox($wikitext, $infobox_name) { $start_pos = stripos($wikitext, '{{' . $infobox_name); if ($start_pos === false) { return false; } $brace_count = 0; $len = strlen($wikitext); $infobox_start = 0; for ($i = $start_pos; $i < $len - 1; $i++) { if ($wikitext[$i] == '{' && $wikitext[$i+1] == '{') { if ($brace_count == 0) { $infobox_start = $i; } $brace_count += 2; $i++; } elseif ($wikitext[$i] == '}' && $wikitext[$i+1] == '}') { $brace_count -= 2; $i++; if ($brace_count == 0) { return substr($wikitext, $infobox_start, ($i - $infobox_start) + 1); } } } return false; }
function parse_infobox($text) { $data = []; $pattern = '/\|\s*([^=]+?)\s*=\s*([\s\S]*?)(?=\n\s*\||\n\}\})/s'; preg_match_all($pattern, $text, $matches, PREG_SET_ORDER); foreach ($matches as $match) { $key = trim($match[1]); $value = trim($match[2]); if (!empty($key)) { $data[$key] = $value; } } return $data; }
function strip_comments($text) { return preg_replace('//', '', $text); }
function format_club_name($text) { return str_replace([' F.C.', ' A.F.C.'], [' FC', ' AFC'], $text); }
function get_wikilink_target($text) { if (preg_match('/\[\[([^|\]]+)/', $text, $matches)) { return trim($matches[1]); } return clean_wikilink($text); }
function format_list_with_and($items) { if (empty($items)) return ''; if (count($items) < 2) { return implode('', $items); } $last_item = array_pop($items); return implode(', ', $items) . ' ve ' . $last_item; }
function add_nationality_suffix($country) { $demonyms = [ 'Batı Almanya' => 'Batı Alman', 'Almanya' => 'Alman', 'Fransa' => 'Fransız', 'Türkiye' => 'Türk', 'İspanya' => 'İspanyol', 'İtalya' => 'İtalyan', 'Rusya' => 'Rus' ]; if (isset($demonyms[$country])) { return $demonyms[$country]; } $vowels = ['a', 'ı', 'o', 'u', 'e', 'i', 'ö', 'ü']; $last_vowel = ''; for ($i = mb_strlen($country, 'UTF-8') - 1; $i >= 0; $i--) { $char = mb_substr($country, $i, 1, 'UTF-8'); if (in_array(mb_strtolower($char, 'UTF-8'), $vowels)) { $last_vowel = mb_strtolower($char, 'UTF-8'); break; } } $suffix = in_array($last_vowel, ['a', 'ı', 'o', 'u']) ? 'lı' : 'li'; return $country . $suffix; }
function translate_date_string($date_string) { $months_en = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']; $months_tr = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']; return str_ireplace($months_en, $months_tr, $date_string); }
function translate_complex_values($value) { $value = preg_replace_callback('/^([a-zA-Z\s]+?)\s+(U-?)(\d+)$/i', function($matches) { global $value_map; $country = trim($matches[1]); $age = $matches[3]; $translated_country = $value_map[$country] ?? $country; return "[[$translated_country {$age} yaş altı millî futbol takımı|{$country} U{$age}]]"; }, $value); $value = preg_replace_callback('/\[\[(.*?)\s+national\s+(?:under|u)-?(\d+)\s+football\s+team\|(.*?)\]\]/i', function($matches) { global $value_map; $country = $matches[1]; $age = $matches[2]; $translated_country = $value_map[$country] ?? $country; return "[[$translated_country {$age} yaş altı millî futbol takımı|{$matches[3]}]]"; }, $value); $value = preg_replace_callback('/\[\[(.*?)\s+national\s+football\s+team\|(.*?)\]\]/i', function($matches) { global $value_map; $country = $matches[1]; $translated_country = $value_map[$country] ?? $country; return "[[$translated_country millî futbol takımı|{$matches[2]}]]"; }, $value); return $value; }
function translate_templates($value) { $value = preg_replace('/\{\{birth date and age\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)[^}}]*\}\}/i', '{{doğum tarihi ve yaşı|$1|$2|$3}}', $value); $value = preg_replace('/\{\{death date and age\s*\|\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})\s*\|\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})[^}}]*\}\}/i', '{{ölüm tarihi ve yaşı|$1|$2|$3|$4|$5|$6}}', $value); $value = preg_replace('/\{\{height\s*\|\s*m\s*=\s*([\d\.]+)\s*\}\}/i', '$1 m', $value); $value = preg_replace('/\{\{convert\s*\|\s*([\d\.]+)\s*\|\s*m\s*\|.*\}\}/i', '$1 m', $value); return $value; }
function clean_wikilink($text) { $text = preg_replace('/\[\[[^|\]]+\|([^\]]+)\]\]/', '$1', $text); $text = str_replace(['[[', ']]'], '', $text); $text = preg_replace('/<br\s*\/?>/i', ', ', $text); $text = preg_replace('/\s*\([^)]*\)/', '', $text); return trim($text); }
function get_nationality($data) {
    global $value_map; $country_name = clean_wikilink($data['doğumyeri'] ?? ''); $parts = explode(',', $country_name); $country_name = trim(end($parts)); return $value_map[$country_name] ?? $country_name;
}
function generate_intro($data) {
    $is_player = !empty($data['kulüp1']); $is_manager = !empty($data['çalıştığıkulüp1']); $role = 'unknown';
    if ($is_player && !$is_manager) $role = 'player'; if (!$is_player && $is_manager) $role = 'manager'; if ($is_player && $is_manager) $role = 'player_then_manager';
    $name = isset($data['ad']) ? clean_wikilink($data['ad']) : ''; if (!$name && isset($data['tamadı'])) { $name = clean_wikilink($data['tamadı']); }
    $birth_date_raw = $data['doğumtarihi'] ?? ''; $birth_place_linked = strip_comments($data['doğumyeri'] ?? ''); $birth_date_formatted = '';
    if(preg_match('/\{\{doğum tarihi ve yaşı\|(\d+)\|(\d+)\|(\d+)/', $birth_date_raw, $m)) { $months_tr = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]; $birth_date_formatted = (int)$m[3] . ' ' . $months_tr[(int)$m[2]] . ' ' . $m[1]; }
    $intro = "'''" . $name . "'''" . " (d. " . trim($birth_date_formatted . ", " . $birth_place_linked, ", ") . ")";
    $nationality_clean = get_nationality($data); $nationality_with_suffix = add_nationality_suffix($nationality_clean);
    if ($role === 'player' || $role === 'player_then_manager') { $position_linked = $data['mevki'] ?? ''; $intro .= ", " . $position_linked . " pozisyonunda görev yapmış " . $nationality_with_suffix . " eski millî futbolcu ve teknik direktördür."; } 
    elseif ($role === 'manager') { $intro .= ", " . $nationality_with_suffix . " teknik direktördür."; }
    $current_club_linked = $data['bulunduğukulüp'] ?? '';
    if(!empty($current_club_linked)) { 
        $current_club_clean = preg_replace('/\s*\([^)]*\)/', '', $current_club_linked);
        $action = (strpos($current_club_linked, 'teknik direktör') !== false) ? "takımını çalıştırmaktadır" : "takımında forma giymektedir"; 
        $intro .= " Günümüzde " . $current_club_clean . " " . $action . "."; 
    }
    if ($role === 'player' || $role === 'player_then_manager') {
        $prof_clubs = []; for ($i = 1; $i <= 30; $i++) { if (!empty($data['kulüp' . $i])) { $prof_clubs[] = $data['kulüp' . $i]; } }
        if (count($prof_clubs) > 0) { $intro .= " Profesyonel futbolculuk kariyerine " . $prof_clubs[0] . " kulübünde başladı."; if (count($prof_clubs) > 1) { $other_clubs = array_slice($prof_clubs, 1); $intro .= " Daha sonra sırasıyla " . format_list_with_and($other_clubs) . " kulüplerinde oynadı."; } }
    }
    $national_teams = []; for ($i = 1; $i <= 20; $i++) { if (!empty($data['millitakım' . $i])) { $national_teams[] = $data['millitakım' . $i]; } }
    if (count($national_teams) > 0) { $intro .= " " . format_list_with_and($national_teams) . " millî takımlarında forma giydi."; }
    if ($role === 'manager' || $role === 'player_then_manager') {
        $manager_clubs = []; for ($i = 1; $i <= 30; $i++) { if (!empty($data['çalıştığıkulüp' . $i])) { $manager_clubs[] = $data['çalıştığıkulüp' . $i]; } }
        if(count($manager_clubs) > 0) { if ($role === 'player_then_manager') { $intro .= " Futbolculuk kariyerinin ardından teknik direktörlüğe başlamıştır."; } $intro .= " Sırasıyla " . format_list_with_and($manager_clubs) . " takımlarını çalıştırdı."; }
    }
    return $intro;
}
function generate_categories($data) {
    $categories = [];
    if (isset($data['doğumtarihi']) && preg_match('/\|(\d{4})\|/', $data['doğumtarihi'], $m)) { $categories[] = "[[Kategori:{$m[1]} doğumlular]]"; }
    if (isset($data['ölümtarihi']) && !empty($data['ölümtarihi'])) { if (preg_match('/\|(\d{4})\|/', $data['ölümtarihi'], $m)) { $categories[] = "[[Kategori:{$m[1]} yılında ölenler]]"; } } else { $categories[] = "[[Kategori:Yaşayan insanlar]]"; }
    if(!empty($data['doğumyeri'])) { $birth_city_target = get_wikilink_target($data['doğumyeri']); $categories[] = "[[Kategori:{$birth_city_target} doğumlular]]"; }
    $nationality_clean = get_nationality($data); $nationality_with_suffix = add_nationality_suffix($nationality_clean);
    if(!empty($data['çalıştığıkulüp1'])) { $categories[] = "[[Kategori:{$nationality_with_suffix} teknik direktörler]]"; }
    for ($i = 1; $i <= 30; $i++) { if (isset($data['kulüp' . $i])) { $club_name = get_wikilink_target($data['kulüp' . $i]); $club_name = trim(preg_replace('/\s*\([^)]*\)/', '', $club_name)); $categories[] = "[[Kategori:{$club_name} futbolcuları]]"; } }
    for ($i = 1; $i <= 20; $i++) { if (!empty($data['millitakım' . $i])) { $team_name_target = get_wikilink_target($data['millitakım' . $i]); $categories[] = "[[Kategori:{$team_name_target} futbolcuları]]"; } }
    for ($i = 1; $i <= 30; $i++) { if (!empty($data['çalıştığıkulüp' . $i])) { $club_name = clean_wikilink(get_wikilink_target($data['çalıştığıkulüp' . $i])); $club_name = trim(preg_replace('/\s*\([^)]*\)/', '', $club_name)); $categories[] = "[[Kategori:{$club_name} teknik direktörleri]]"; } }
    $position_clean = clean_wikilink($data['mevki'] ?? '');
    if ($position_clean) { $categories[] = "[[Kategori:" . ucfirst($position_clean) . " futbolcular]]"; }
    return array_unique($categories);
}
?>
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Gelişmiş Vikipedi Futbolcu Çeviri Asistanı</title>
<style>
    body { font-family: 'Montserrat', sans-serif; margin: 0; background: #f0f0f0; display: flex; flex-direction: column; min-height: 100vh; }
header {
    background: linear-gradient(to right, #2E4826, #315424); /* Koyu ve şık bir gradyan */
    color: white;
    padding: 25px 30px; /* Boşlukları artırarak daha ferah bir görünüm verdik */
    text-align: center;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16); /* Altına yumuşak bir gölge ekledik */
    border-bottom: 4px solid #eaeaea; /* Canlı mavi rengi altta ince bir çizgi olarak koruduk */
}

header h1 {
    margin: 0;
    font-size: 26px;
    font-weight: 300; /* Yazıyı daha ince ve zarif yaptık */
    letter-spacing: 1px; /* Harflerin arasını biraz açtık */
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2); /* Yazıya çok hafif bir derinlik hissi verdik */
}

    main { padding: 20px; max-width: 900px; margin: 20px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 95%; }
    .tab-container { display: flex; border-bottom: 2px solid #dee2e6; margin-bottom: 20px; }
    .tab-button { padding: 10px 20px; cursor: pointer; background: transparent; border: 0; border-bottom: 2px solid transparent; color: #6c757d; font-size: 16px; margin-bottom: -2px; }
    .tab-button:hover { color: #0056b3; }
    .tab-button.active { color: #007bff; font-weight: bold; border-bottom: 2px solid #007bff; }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    .form-group { margin-bottom: 20px; }
    label { display: block; margin-bottom: 8px; font-weight: 600; }
    input[type="url"], textarea { width: 100%; padding: 12px; font-size: 13px; border-radius: 8px; border: 1px solid #ccc; box-sizing: border-box; }
    textarea { height: 250px; font-family: Montserrat; }
    .output-container { border-top: 2px dashed #ccc; margin-top: 20px; padding-top: 20px; }
    .output-area { width: 100%; height: 500px; padding: 10px; font-family: Montserrat; font-size: 13px; border: 1px solid #ccc; box-sizing: border-box; background: #f9f9f9; white-space: pre-wrap; overflow-y: auto; }
    .button-container, .options-container { display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap; }
    .options-container { border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #fcfcfc; }
    .options-container label { display: flex; align-items: center; gap: 5px; cursor: pointer; }
    button { padding: 9px 13px; font-size: 14px; font-weight: bold; cursor: pointer; border-radius: 8px; border: none; color: white; transition: background-color 0.2s ease, transform 0.1s ease; }
    button:active { transform: scale(0.98); }
    .submit-btn { background-color: #007bff; } .submit-btn:hover { background-color: #0056b3; }
    .copy-btn { background-color: #456838; } .copy-btn:hover { background-color: #315424; }
    .clear-btn { background-color: #dc3545; } .clear-btn:hover { background-color: #c82333; }
    #toggleSourceBtn { background-color: #6c757d; } #toggleSourceBtn:hover { background-color: #5a6268; }
    .error-box { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    footer { text-align: center; padding: 20px; margin-top: auto; font-size: 14px; color: #666; }
</style>
</head>
<body>
<header><h1>Gelişmiş Vikipedi Futbolcu Çeviri Asistanı</h1></header>
<main>
    <div class="tab-container">
        <button class="tab-button <?= ($active_tab === 'urlTab') ? 'active' : '' ?>" onclick="openTab('urlTab')">URL ile Çevir</button>
        <button class="tab-button <?= ($active_tab === 'textTab') ? 'active' : '' ?>" onclick="openTab('textTab')">Metin ile Çevir</button>
    </div>

    <div id="urlTab" class="tab-content <?= ($active_tab === 'urlTab') ? 'active' : '' ?>">
        <form method="post">
            <div class="form-group">
                <label for="source_url">İngilizce Vikipedi Futbolcu Sayfası URL'si:</label>
                <input type="url" name="source_url" id="source_url" placeholder="https://en.wikipedia.org/wiki/Erling_Haaland" value="<?= htmlspecialchars($input_url) ?>" required>
            </div>
            <button type="submit" name="submit_url" class="submit-btn">Getir ve Çevir</button>
        </form>
    </div>

    <div id="textTab" class="tab-content <?= ($active_tab === 'textTab') ? 'active' : '' ?>">
        <form method="post">
            <div class="form-group">
                <label for="source_text">İngilizce Bilgi Kutusu Metni:</label>
                <textarea name="source_text" id="source_text" placeholder="{{Infobox football biography...}}"><?= htmlspecialchars($input_text) ?></textarea>
            </div>
            <button type="submit" name="submit_text" class="submit-btn">Çevir</button>
        </form>
    </div>

    <?php if ($error_message || $infobox_part): ?>
    <div class="output-container">
        <?php if ($error_message): ?>
            <div class="error-box"><?= htmlspecialchars($error_message) ?></div>
        <?php endif; ?>

        <?php if ($infobox_part): ?>
        <div class="form-group">
            <label>Dahil Etme Seçenekleri:</label>
            <div class="options-container">
                <label><input type="checkbox" id="includeInfobox" checked> Bilgi Kutusu</label>
                <label><input type="checkbox" id="includeIntro" checked> Giriş Metni</label>
                <label><input type="checkbox" id="includeCategories" checked> Kategoriler</label>
            </div>
        </div>
        <div class="form-group">
            <label for="output_wikitext">Oluşturulan Türkçe Vikimetin:</label>
            <div id="output_wikitext" class="output-area"><?php
                $parts = [];
                if (!empty($infobox_part)) $parts[] = $infobox_part;
                if (!empty($intro_part)) $parts[] = $intro_part;
                if (!empty($categories_part)) $parts[] = $categories_part;
                $full_text = implode("\n\n", $parts);
                echo "<span id='infobox_span' style='display:none;'>" . htmlspecialchars($infobox_part) . "</span>";
                echo "<span id='intro_span' style='display:none;'>" . htmlspecialchars($intro_part) . "</span>";
                echo "<span id='categories_span' style='display:none;'>" . htmlspecialchars($categories_part) . "</span>";
                echo "<span id='english_source_span' style='display:none;'>" . htmlspecialchars($english_source_part) . "</span>";
                echo htmlspecialchars($full_text);
            ?></div>
        </div>
        <div class="button-container">
            <button type="button" class="copy-btn" data-target="all">Tümünü Kopyala</button>
            <button type="button" class="copy-btn" data-target="infobox">Kutuyu Kopyala</button>
            <button type="button" class="copy-btn" data-target="intro">Metni Kopyala</button>
            <button type="button" class="copy-btn" data-target="categories">Kategorileri Kopyala</button>
            <button type="button" id="toggleSourceBtn">Kaynağı Göster</button>
            <button type="button" class="clear-btn">Temizle</button>
        </div>
        <?php endif; ?>
    </div>
    <?php endif; ?>
</main>
<footer><p>Bu araç, Vikipedi düzenlemelerini kolaylaştırmak amacıyla oluşturulmuştur.</p></footer>
<script>
document.addEventListener('DOMContentLoaded', function() {
    window.openTab = function(tabName) {
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        document.getElementById(tabName).classList.add('active');
        event.currentTarget.classList.add('active');
    }
    const outputContainer = document.querySelector('.output-container');
    if (outputContainer) {
        const outputBox = document.getElementById('output_wikitext');
        const checkboxes = { infobox: document.getElementById('includeInfobox'), intro: document.getElementById('includeIntro'), categories: document.getElementById('includeCategories') };
        const spans = { infobox: document.getElementById('infobox_span'), intro: document.getElementById('intro_span'), categories: document.getElementById('categories_span'), english_source: document.getElementById('english_source_span') };
        const toggleBtn = document.getElementById('toggleSourceBtn');
        const copyButtons = document.querySelectorAll('.copy-btn');
        let isSourceVisible = false;
        function updateOutputVisibility() {
            const parts = [];
            if (checkboxes.infobox.checked && spans.infobox.innerText) parts.push(spans.infobox.innerText);
            if (checkboxes.intro.checked && spans.intro.innerText) parts.push(spans.intro.innerText.trim());
            if (checkboxes.categories.checked && spans.categories.innerText) parts.push(spans.categories.innerText.trim());
            outputBox.innerText = parts.join('\n\n').trim();
        }
        Object.values(checkboxes).forEach(cb => cb.addEventListener('change', () => { if (!isSourceVisible) { updateOutputVisibility(); } }));
        toggleBtn.addEventListener('click', () => {
            if (!spans.english_source.innerText) return;
            isSourceVisible = !isSourceVisible;
            if (isSourceVisible) {
                outputBox.innerText = spans.english_source.innerText;
                toggleBtn.innerText = 'Çeviriyi Göster';
                copyButtons.forEach(btn => btn.style.display = 'none');
                Object.values(checkboxes).forEach(cb => cb.disabled = true);
            } else {
                updateOutputVisibility();
                toggleBtn.innerText = 'Kaynağı Göster';
                copyButtons.forEach(btn => btn.style.display = 'inline-block');
                Object.values(checkboxes).forEach(cb => cb.disabled = false);
            }
        });
        function copyToClipboard(text, button) {
            if (!text) return;
            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.innerText;
                button.innerText = 'Kopyalandı!';
                button.style.backgroundColor = '#2E4826';
                setTimeout(() => {
                    button.innerText = originalText;
                    button.style.backgroundColor = '#2E4826';
                }, 2000);
            }).catch(err => console.error('Kopyalama başarısız: ', err));
        }
        copyButtons.forEach(button => {
            button.addEventListener('click', () => {
                const target = button.dataset.target;
                let textToCopy = '';
                if (target === 'all') { textToCopy = outputBox.innerText; } 
                else if (spans[target]) { textToCopy = spans[target].innerText.trim(); }
                copyToClipboard(textToCopy, button);
            });
        });
        document.querySelector('.clear-btn').addEventListener('click', () => {
            window.location.href = window.location.pathname;
        });
    }
});
</script>
</body>
</html>
