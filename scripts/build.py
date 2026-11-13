import json, os
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=json.load(open(f'{OUT}/data/rates.json'))
T=11.664
SITE='https://goldsilverrate.pk'
DATE=D.get('updated_iso','2026-11-13')[:10]
ps,pb=D['silver']['psl_tola_sell'],D['silver']['psl_tola_buy']
rs,rb=D['silver']['rawa_tola_sell'],D['silver']['rawa_tola_buy']
g24s,g24b=D['gold']['24k_tola_sell'],D['gold']['24k_tola_buy']
g22s,g21s=D['gold']['22k_tola_sell'],D['gold']['21k_tola_sell']
ratio=g24b/g24s
g22b,g21b=g22s*ratio,g21s*ratio
g18s,g18b=g24s*.75,g24b*.75
UP=D['last_updated']
def pk(n): return f"Rs {round(n):,}"
def row(label,f,s,b): return (label,pk(s*f),pk(b*f))
G=1/T
def table(cap,rows,id_=None):
    h=f'<div class="tablebox"><table><caption>{cap}</caption><thead><tr><th scope="col">Weight / Unit</th><th scope="col">Selling Price (PKR)</th><th scope="col">Buying Price (PKR)</th></tr></thead><tbody>'
    for a,b,c in rows: h+=f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>'
    return h+'</tbody></table></div>'
def silver_rows(s,b,kind):
    return [row(f'1 Tola ({kind})',1,s,b),row(f'5 Tola ({kind})',5,s,b),row(f'10 Tola ({kind})',10,s,b),
            row(f'1 Gram ({kind})',G,s,b),row(f'10 Gram ({kind})',10*G,s,b),row(f'1 KG ({kind})',1000*G,s,b)]
def gold_rows():
    r=[]
    for k,s,b in(('24K',g24s,g24b),('22K',g22s,g22b),('21K',g21s,g21b),('18K',g18s,g18b)):
        r.append(row(f'{k} Gold - 1 Tola',1,s,b))
        r.append(row(f'{k} Gold - 10 Gram',10*G,s,b))
    return r
PSLT=table('PSL silver bar rates today',silver_rows(ps,pb,'PSL'))
RAWAT=table('Rawa (local refine) silver rates today',silver_rows(rs,rb,'Rawa'))
GOLDT=table('Gold rates today by karat',gold_rows())
NOTE_G='<p class="note">Selling price is what a dealer asks when you buy. Buying price is what a dealer pays when you sell. The 24K buying and selling rates and the 22K and 21K selling rates come from the market sheet. The other buying prices are worked out from the 24K gap, and 18K is 75% of 24K. Always confirm the final price at the counter.</p>'
NOTE_S='<p class="note">Selling price is what a dealer asks when you buy. Buying price is what a dealer pays when you sell. Prices are for metal only and do not include making charges, tax or packing.</p>'

NAV=[('/','Home'),('/silver-rate-pakistan','Silver'),('/psl-silver-rate-pakistan','PSL Bars'),('/gold-rate-pakistan','Gold'),('/gold-rate-today-karachi','Karachi'),('/silver-rate-lahore','Lahore'),('/gold-silver-calculator','Calculator')]
def rel(slugs):
    return '<div class="links">'+''.join(f'<a href="/{s}">{PAGES[s]["short"]}</a>' for s in slugs)+'</div>'

def faq_html(faqs):
    return '<h2>Common questions</h2>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)

def calc_widget():
    return '''<div class="card"><h2>Gold and silver price calculator</h2><p class="note">Pick the metal, the unit and the amount. You get the selling and buying price right away.</p>
<div class="fields"><div><label for="calc-metal">Metal</label><select id="calc-metal"><option value="psl">Silver - PSL bar</option><option value="rawa">Silver - Rawa</option><option value="g24">Gold 24K</option><option value="g22">Gold 22K</option><option value="g21">Gold 21K</option><option value="g18">Gold 18K</option></select></div>
<div><label for="calc-unit">Unit</label><select id="calc-unit"><option value="tola">Tola</option><option value="gram">Gram</option><option value="masha">Masha</option><option value="ratti">Ratti</option><option value="kg">Kilogram</option></select></div>
<div><label for="calc-qty">Amount</label><input id="calc-qty" type="number" inputmode="decimal" min="0" step="any" value="10"></div></div>
<div class="out" id="calc-out" aria-live="polite"></div></div>'''

def full_calc():
    return '''<div class="grid two"><div class="card"><h2 style="margin-top:0">Weight converter</h2><p class="note">1 Tola = 12 Masha. 1 Masha = 8 Ratti. 1 Tola = 11.664 Grams.</p>
<div class="fields two"><div><label for="cv-val">Amount</label><input id="cv-val" type="number" inputmode="decimal" min="0" step="any" value="1"></div>
<div><label for="cv-unit">Unit</label><select id="cv-unit"><option value="tola">Tola</option><option value="masha">Masha</option><option value="ratti">Ratti</option><option value="gram">Gram</option><option value="kg">Kilogram</option></select></div></div>
<div class="out" id="cv-out" aria-live="polite"></div></div>
<div class="card"><h2 style="margin-top:0">Jewellery cost estimator</h2><p class="note">Shops add kaat (wastage) and mazdoori (making charge) on top of the metal price. Ask your jeweller for his numbers and enter them here.</p>
<div class="fields two"><div><label for="jw-metal">Metal</label><select id="jw-metal"><option value="g22">Gold 22K</option><option value="g21">Gold 21K</option><option value="g24">Gold 24K</option><option value="g18">Gold 18K</option><option value="psl">Silver - PSL</option><option value="rawa">Silver - Rawa</option></select></div>
<div><label for="jw-wt">Weight (tola)</label><input id="jw-wt" type="number" inputmode="decimal" min="0" step="any" value="2"></div>
<div><label for="jw-kaat">Kaat (masha per tola)</label><input id="jw-kaat" type="number" inputmode="decimal" min="0" step="any" value="0.5"></div>
<div><label for="jw-maz">Mazdoori (Rs per tola)</label><input id="jw-maz" type="number" inputmode="decimal" min="0" step="any" value="5000"></div></div>
<div class="out" id="jw-out" aria-live="polite"></div></div></div>'''

PAGES={}
def add(slug,**k): PAGES[slug]=k

# ---------- PAGE CONTENT ----------
add('silver-rate-pakistan',short='Silver Rate',
 title='Silver Rate in Pakistan Today (999 Fine, Rawa & PSL Bar) | GoldSilverRate.pk',
 urdu='آج کا چاندی کا ریٹ پاکستان میں۔',
 desc='Silver rate in Pakistan today per tola, 10 gram and 1 kg for pure 999 silver, local Rawa and PSL bars.',
 h1='Silver Rate in Pakistan Today',
 lead=f'Today silver sells at {pk(ps)} per tola for PSL bars and {pk(rs)} per tola for local Rawa. Here is the full list for tola, gram and kilo, so you can see your exact weight without doing any sums.',
 product=('Silver per tola in Pakistan',ps),
 body=lambda:PSLT+RAWAT+NOTE_S+'''
<h2>Three kinds of silver you will hear about</h2>
<h3>Pure 999 fine silver</h3><p>This is silver that is 99.9% pure. It is sold as sealed bars and bullion pieces, and it is the form most people use to save money in silver. Dealers pay a little less when you sell it back, which is why you see two prices.</p>
<h3>Local Rawa silver</h3><p>Rawa is the silver sold loose in the Sarafa Bazar by weight. It is cheaper per tola than a sealed bar because there is no bar premium, but you need a dealer you trust to test the purity.</p>
<h3>PSL sealed bars</h3><p>These come in sealed packs with a QR code. Because the weight and purity are already marked, they are easy to resell. See our <a href="/psl-silver-rate-pakistan">PSL silver bar page</a> for the buying checklist.</p>
<h2>What moves the silver price in Pakistan</h2>
<ul><li>The international silver price, which changes through the day.</li><li>The dollar to rupee rate. When the dollar goes up, silver costs more rupees.</li><li>Demand from factories, since silver is used in electronics and solar panels.</li><li>Local demand and supply in the big Sarafa markets.</li></ul>
<p>Because of these four things the rate can change more than once in a day. We show one benchmark rate with the time it was updated, so you always know how fresh it is. We do not keep a past rate archive on this page yet, so check the update time before you decide.</p>
<h2>Check other weights</h2>'''+rel(['1-tola-silver-price-pakistan','10-tola-silver-price-pakistan','52-tola-chandi-price-pakistan','1-kg-silver-bar','10-gram-silver-price-pakistan']),
 faqs=[('What is the silver rate in Pakistan today?',f'The PSL bar rate today is {pk(ps)} per tola selling and {pk(pb)} per tola buying. Local Rawa is {pk(rs)} selling and {pk(rb)} buying. Last updated: {UP}.'),
       ('Why is Rawa cheaper than a PSL bar?','A PSL bar carries a premium for the sealed pack, the QR code and the easy resale. Rawa is sold loose by weight, so the price per tola is lower.'),
       ('How many grams are in one tola of silver?','One tola is 11.664 grams. Ten tola is 116.64 grams.')],
 faq_schema=True)

add('psl-silver-rate-pakistan',short='PSL Bar Rate',
 title='PSL Silver Rate in Pakistan Today (10 Tola QR Bar Price) | GoldSilverRate.pk',
 urdu='پی ایس ایل چاندی بار کا آج کا ریٹ۔',
 desc='PSL silver rate in Pakistan today. 10 tola QR bar buying and selling price, plus a simple guide to check the seal.',
 h1='PSL Silver Rate in Pakistan Today',
 lead=f'A PSL 10 tola silver bar costs {pk(ps*10)} to buy today. If you sell it back, a dealer pays about {pk(pb*10)}. The bar weighs 116.64 grams.',
 product=('PSL 10 Tola Silver Bar',ps*10),
 body=lambda:table('PSL bar prices today',[row('1 Tola PSL bar',1,ps,pb),row('5 Tola PSL bar',5,ps,pb),row('10 Tola PSL bar (116.64 g)',10,ps,pb),row('1 KG PSL silver (85.73 tola)',1000*G,ps,pb)])+NOTE_S+'''
<h2>How to check a PSL bar before you pay</h2>
<ol><li><strong>Look at the seal.</strong> The pack should be closed, with no cuts, glue marks or loose corners.</li>
<li><strong>Scan the QR code.</strong> Compare the details you see with the printed weight and serial number on the pack and on the bar.</li>
<li><strong>Match the serial number.</strong> The number on the bar, the pack and the bill should be the same.</li>
<li><strong>Weigh it.</strong> Ask the dealer to put it on a digital scale in front of you. A 10 tola bar should read close to 116.64 grams.</li>
<li><strong>Take a proper bill.</strong> Write the date, weight and rate on it. Keep it with the original pack.</li></ol>
<h2>Why people choose sealed bars</h2>
<p>With loose silver you must trust the shop to test it every time. A sealed bar already has the weight and purity written on it, so the next buyer can check it quickly. That makes it easier to sell later, and usually at a clear rate.</p>
<h2>Selling your bar back</h2>
<p>Keep the pack and the bill. A bar in its original seal usually gets a better buying price than a bar with a broken pack. Ask two or three dealers for their buying rate before you decide.</p>
<h2>More bar guides</h2>'''+rel(['10-tola-silver-price-pakistan','ary-kbe-gold-silver-bars','silver-rate-pakistan']),
 faqs=[('What is the PSL 10 tola silver bar price today?',f'The selling price is {pk(ps*10)} and the buying price is {pk(pb*10)}. Last updated: {UP}.'),
       ('How much does a PSL 10 tola bar weigh?','10 tola equals 116.64 grams.'),
       ('How can I tell if a PSL bar is real?','Check that the seal is unbroken, scan the QR code, match the serial number on the pack and the bar, and weigh it at the shop before you pay. Buy only from a dealer you know.')],
 faq_schema=True)

add('10-tola-silver-price-pakistan',short='10 Tola Silver',
 title='10 Tola Silver Price in Pakistan Today (Biscuit & Bar) | GoldSilverRate.pk',
 urdu='10 تولہ چاندی کی قیمت آج۔',
 desc='10 tola silver price in Pakistan today for PSL bars and local Sarafa biscuits, with buyback rates.',
 h1='10 Tola Silver Price in Pakistan Today',
 lead=f'10 tola silver is {pk(ps*10)} as a PSL bar and {pk(rs*10)} as local Rawa today. That is the price for 116.64 grams.',
 product=('10 Tola Silver',ps*10),
 body=lambda:table('10 tola silver price today',[row('10 Tola PSL bar',10,ps,pb),row('10 Tola Rawa (local biscuit)',10,rs,rb)])+NOTE_S+f'''
<h2>Bar or biscuit: which one to buy</h2>
<p>A silver biscuit is a flat cast piece sold in the Sarafa Bazar. A sealed bar from a brand such as PSL or KBE comes in a pack. Both are 10 tola if marked so, but the price is different.</p>
<div class="tablebox"><table><caption>Bar versus local biscuit</caption><thead><tr><th scope="col">Weight / Unit</th><th scope="col">Selling Price (PKR)</th><th scope="col">Buying Price (PKR)</th></tr></thead><tbody>
<tr><td>Gap on 10 tola (Bar minus Rawa)</td><td>{pk((ps-rs)*10)}</td><td>{pk((pb-rb)*10)}</td></tr></tbody></table></div>
<p>The gap is what you pay for the sealed pack and easier resale. For long saving, many people like the sealed bar. For gifting or jewellery work, local biscuits are fine.</p>
<h2>Buyback margin</h2>
<p>The difference between the selling and buying price is the dealer margin. Today on a PSL 10 tola bar it is {pk((ps-pb)*10)}. Keep the margin in mind: silver should rise by at least that much before you break even.</p>
<h2>Tips before you buy</h2>
<ul><li>Ask for the weight on a digital scale.</li><li>Get a bill with date, weight and rate.</li><li>Keep the original pack for the PSL bar.</li><li>Compare two shops before you pay.</li></ul>'''+rel(['psl-silver-rate-pakistan','1-tola-silver-price-pakistan','52-tola-chandi-price-pakistan']),
 faqs=[('What is 10 tola silver price today?',f'{pk(ps*10)} for a PSL bar and {pk(rs*10)} for local Rawa. Last updated: {UP}.'),
       ('How many grams is 10 tola?','10 tola is 116.64 grams.'),
       ('What is a silver biscuit?','It is a flat piece of cast silver sold by weight in the Sarafa Bazar, usually 5 or 10 tola.')])

add('52-tola-chandi-price-pakistan',short='52 Tola Chandi',
 title='52 Tola Chandi Price in Pakistan Today (52.5 Tola Silver Rate) | GoldSilverRate.pk',
 urdu='52 تولہ چاندی کی قیمت آج۔',
 desc='52 tola and 52.5 tola chandi price in Pakistan today. Bulk silver rates for 50, 52, 52.5 and 55 tola.',
 h1='52 Tola Chandi Price in Pakistan Today',
 lead=f'52 tola of local Rawa silver costs {pk(rs*52)} today, and 52.5 tola costs {pk(rs*52.5)}. The same weight in PSL silver costs {pk(ps*52)} and {pk(ps*52.5)}.',
 product=('52 Tola Silver (Rawa)',rs*52),
 body=lambda:table('Bulk silver price today (Local Rawa)',[row(f'{w} Tola Rawa',w,rs,rb) for w in (50,52,52.5,55)])+table('Bulk silver price today (999 Fine, PSL rate)',[row(f'{w} Tola 999 Fine',w,ps,pb) for w in (50,52,52.5,55)])+NOTE_S+'''
<h2>Why 52 and 52.5 tola?</h2>
<p>Bulk silver is often quoted in lots of about 52 tola. Some pieces come slightly heavier, so you will also see 52.5 tola. Always weigh the piece on a scale and pay for the actual weight.</p>
<h2>Buying bulk silver safely</h2>
<ul><li>Fix the weight and the rate in writing before payment.</li><li>Ask for a purity test in front of you for Rawa.</li><li>Check if the price is per tola or for the whole lot.</li><li>Do not pay the full amount in cash without a signed bill.</li></ul>
<h2>Fine silver or Rawa?</h2>
<p>999 fine silver is purer and easier to sell later. Rawa costs less per tola but its purity depends on the refiner. For large amounts, a small purity gap becomes a big money gap, so test it.</p>'''+rel(['silver-rate-pakistan','1-kg-silver-bar','10-tola-silver-price-pakistan']),
 faqs=[('What is the 52 tola chandi price today?',f'{pk(rs*52)} in local Rawa and {pk(ps*52)} at the PSL rate. Last updated: {UP}.'),
       ('How many grams is 52 tola?','52 tola is 606.53 grams.'),
       ('Why is 52.5 tola priced higher?','It is half a tola more, so it costs half a tola of silver extra.')])

add('1-kg-silver-bar',short='1 KG Silver',
 title='1 KG Silver Price in Pakistan Today (Chandi Rate per KG) | GoldSilverRate.pk',
 urdu='1 کلو چاندی کی قیمت آج۔',
 desc='1 kg silver price in Pakistan today. Chandi rate per kg for PSL bars and Rawa, 85.73 tola.',
 h1='1 KG Silver Price in Pakistan Today',
 lead=f'One kilogram of silver costs {pk(ps*1000*G)} at the PSL rate and {pk(rs*1000*G)} at the Rawa rate today. One kilo is about 85.73 tola.',
 product=('1 KG Silver Bar',ps*1000*G),
 body=lambda:table('1 KG silver price today',[row('1 KG PSL silver',1000*G,ps,pb),row('1 KG Rawa silver',1000*G,rs,rb),row('500 Gram PSL silver',500*G,ps,pb),row('100 Gram PSL silver',100*G,ps,pb)])+NOTE_S+'''
<h2>How we work out the kilo price</h2>
<p>1 kg is 1000 grams. One tola is 11.664 grams, so 1 kg equals 1000 divided by 11.664, which is about 85.73 tola. We multiply that by the tola rate.</p>
<h2>Where 1 kg bars are used</h2>
<ul><li><strong>Savings:</strong> a single large bar is easier to store than many small pieces.</li><li><strong>Factories:</strong> silver is used in electronics, solar panels and parts that need to conduct electricity well.</li><li><strong>Jewellery makers:</strong> large casting orders are bought by the kilo.</li></ul>
<h2>What to check on a kilo bar</h2>
<p>Look for the purity stamp (999), the weight mark and a serial number. Ask for an assay or purity slip if the bar is not from a sealed brand. For big money, test the bar at a second shop before you pay.</p>'''+rel(['52-tola-chandi-price-pakistan','silver-rate-pakistan','ary-kbe-gold-silver-bars']),
 faqs=[('What is 1 kg silver price in Pakistan today?',f'{pk(ps*1000*G)} at the PSL rate and {pk(rs*1000*G)} at the Rawa rate. Last updated: {UP}.'),
       ('How many tola are in 1 kg?','About 85.73 tola.'),
       ('Is silver cheaper per gram in a big bar?','The metal price is the same per gram. Some dealers give a small discount on large orders, so ask.')])

add('1-tola-silver-price-pakistan',short='1 Tola Silver',
 title='1 Tola Silver Price in Pakistan Today (Chandi Rate per Tola) | GoldSilverRate.pk',
 urdu='1 تولہ چاندی کا ریٹ آج۔',
 desc='1 tola silver price in Pakistan today. Chandi rate per tola for PSL bars and Rawa.',
 h1='1 Tola Silver Price in Pakistan Today',
 lead=f'One tola of silver is {pk(ps)} at the PSL bar rate and {pk(rs)} at the Rawa rate today. One tola is 11.664 grams.',
 product=('1 Tola Silver',ps),
 body=lambda:table('1 tola silver price today',[row('1 Tola PSL bar',1,ps,pb),row('1 Tola Rawa',1,rs,rb),row('Half Tola PSL',.5,ps,pb),row('1 Masha PSL',1/12,ps,pb)])+NOTE_S+f'''
<h2>Rawa and bar: why two prices</h2>
<p>Today the PSL bar rate is {pk(ps-rs)} higher per tola than Rawa. That extra amount pays for the sealed pack, the marked weight and easier resale. If you only need silver metal, for example to make a small piece, Rawa is the cheaper way to buy.</p>
<h2>Small weights</h2>
<p>1 Tola = 12 Masha and 1 Masha = 8 Ratti. So 1 Masha of PSL silver is about {pk(ps/12)}. For anything else use the <a href="/gold-silver-calculator">calculator</a>.</p>
<h2>Good to know</h2>
<ul><li>Small pieces often cost more per tola because of packing and handling.</li><li>The dealer buying price is lower than the selling price. The gap today is {pk(ps-pb)} per tola on PSL.</li><li>Rates change during the day, so check the update time above.</li></ul>'''+rel(['10-tola-silver-price-pakistan','10-gram-silver-price-pakistan','silver-rate-pakistan']),
 faqs=[('What is the chandi rate per tola today?',f'{pk(ps)} for a PSL bar and {pk(rs)} for Rawa. Last updated: {UP}.'),
       ('How many grams is 1 tola?','11.664 grams.'),
       ('How many masha in one tola?','12 masha.')])

add('10-gram-silver-price-pakistan',short='10 Gram Silver',
 title='10 Gram Silver Price in Pakistan Today (999 & 925 Sterling) | GoldSilverRate.pk',
 urdu='10 گرام چاندی کی قیمت آج۔',
 desc='10 gram silver price in Pakistan today for 999 pure silver and 925 sterling silver, per gram rates.',
 h1='10 Gram Silver Price in Pakistan Today',
 lead=f'10 grams of pure silver is {pk(10*G*ps)} at the PSL rate and {pk(10*G*rs)} at Rawa. One gram is about {pk(G*ps)}.',
 product=('10 Gram Silver',10*G*ps),
 body=lambda:table('Silver price by gram today',[row('10 Gram 999 (PSL rate)',10*G,ps,pb),row('10 Gram Rawa',10*G,rs,rb),row('1 Gram 999 (PSL rate)',G,ps,pb),row('1 Gram Rawa',G,rs,rb),row('10 Gram 925 Sterling (metal value)',10*G*.925,ps,pb),row('1 Gram 925 Sterling (metal value)',G*.925,ps,pb)])+NOTE_S+'''
<h2>What is 925 sterling silver?</h2>
<p>Sterling silver is 92.5% pure silver mixed with 7.5% other metal, usually copper. The mix makes it harder, so it holds shape better in rings, chains and cutlery. 999 silver is almost pure and softer.</p>
<p>The sterling figures above are the value of the silver inside, worked out as 92.5% of the 999 price. A jeweller will add making charges on top, so a finished sterling piece costs more.</p>
<h2>Buying small silver for gifts</h2>
<ul><li>Look for a "925" stamp on the piece.</li><li>Ask the weight in grams and the making charge separately.</li><li>Small pieces sell back at the metal price only, without the making charge.</li></ul>'''+rel(['1-tola-silver-price-pakistan','gold-silver-calculator','silver-rate-pakistan']),
 faqs=[('What is 10 gram silver price today?',f'{pk(10*G*ps)} at the PSL rate and {pk(10*G*rs)} at the Rawa rate. Last updated: {UP}.'),
       ('What is 925 silver?','It is sterling silver, made of 92.5% pure silver and 7.5% other metal.'),
       ('Is 925 silver cheaper than 999?','Per gram, yes, because it has less pure silver in it. Making charges can make a finished piece cost more.')])

add('gold-rate-pakistan',short='Gold Rate',
 title='Gold Rate in Pakistan Today (24K, 22K, 21K Per Tola) | GoldSilverRate.pk',
 urdu='آج کا سونے کا ریٹ پاکستان میں۔',
 desc='Gold rate in Pakistan today per tola and 10 gram for 24K, 22K, 21K and 18K gold.',
 h1='Gold Rate in Pakistan Today',
 lead=f'24K gold is {pk(g24s)} per tola today. 22K gold is {pk(g22s)} per tola and 21K gold is {pk(g21s)} per tola. Last updated: {UP}.',
 product=('24K Gold per Tola',g24s),
 body=lambda:GOLDT+NOTE_G+'''
<h2>What the karat number means</h2>
<p>Karat tells you how much of the piece is pure gold. 24K is pure. 22K is 22 parts gold out of 24, so about 91.6%. 21K is 87.5% and 18K is 75%. The rest is another metal such as copper that makes the gold harder.</p>
<h2>Which karat is used for what</h2>
<ul><li><strong>24K:</strong> gold bars and coins, because it is pure.</li><li><strong>22K:</strong> most jewellery sets in Pakistan.</li><li><strong>21K:</strong> everyday jewellery that needs to be a bit stronger.</li><li><strong>18K:</strong> light and designer pieces, often with stones.</li></ul>
<h2>Buying gold: simple rules</h2>
<ol><li>Fix the karat and the weight before you talk about price.</li><li>Ask for the rate of the day and compare it with this page.</li><li>For jewellery, ask the kaat (wastage) and mazdoori (making) separately.</li><li>Take a bill that shows the karat, weight, rate and making charge.</li><li>Keep the bill. When you sell, the shop will ask for it.</li></ol>
<p>Work out jewellery cost with our <a href="/gold-silver-calculator">jewellery cost estimator</a>.</p>'''+rel(['gold-rate-today-karachi','gold-silver-calculator','ary-kbe-gold-silver-bars']),
 faqs=[('What is gold rate in Pakistan today?',f'24K gold is {pk(g24s)} per tola. Last updated: {UP}.'),
       ('How many grams in one tola of gold?','One tola is 11.664 grams.'),
       ('Why is 22K cheaper than 24K?','22K has about 91.6% gold, so it contains less pure gold than 24K.')])

def cityrates(city,market):
    return f'''<p class="note">We show one benchmark rate for the whole country. Counter prices in {market} can be a little different from shop to shop, mostly in the buying price. Ask two shops before you decide.</p>'''
add('gold-rate-today-karachi',short='Karachi Gold',
 title='Gold Rate Today in Karachi (Sarafa Bazar 24K, 22K Per Tola) | GoldSilverRate.pk',
 urdu='کراچی میں آج سونے کا ریٹ۔',
 desc='Gold rate today in Karachi. Bolton Market and Saddar Sarafa benchmark for 24K, 22K and 21K gold per tola.',
 h1='Gold Rate Today in Karachi',
 lead=f'In Karachi today, 24K gold is {pk(g24s)} per tola and 22K gold is {pk(g22s)} per tola. These are benchmark rates used by the Sarafa Bazar.',
 product=('24K Gold per Tola - Karachi',g24s),
 body=lambda:GOLDT+cityrates('Karachi','Bolton Market and Saddar')+NOTE_G+'''
<h2>Where Karachi buys and sells gold</h2>
<p>Karachi has two well-known gold areas. Bolton Market is the old wholesale centre, where dealers trade in bulk. Saddar has many retail jewellers, so most families buy there. Retail shops add their own margin on top of the wholesale price.</p>
<h2>Tips for buyers in Karachi</h2>
<ul><li>Visit at least two shops and ask the same question: rate for your karat and weight.</li><li>Ask what the shop pays if you sell back the same day.</li><li>Get a written bill with the shop name and address.</li><li>For big purchases, prefer a shop that has been in the market for years.</li></ul>'''+rel(['gold-rate-pakistan','silver-rate-karachi','gold-silver-calculator']),
 faqs=[('What is gold rate in Karachi today?',f'24K gold is {pk(g24s)} per tola. Last updated: {UP}.'),
       ('Is gold cheaper in Bolton Market?','Wholesale dealers sell in bulk and retail shops add their own margin, so the price you pay depends on the shop.'),
       ('Does the rate change during the day?','Yes. It follows the world gold price and the dollar rate, so it can move several times a day.')])

add('silver-rate-karachi',short='Karachi Silver',
 title='Silver Rate in Karachi Today (10 Tola Price at Sarafa Bazar) | GoldSilverRate.pk',
 urdu='کراچی میں آج چاندی کا ریٹ۔',
 desc='Silver rate in Karachi today. Sarafa Bazar counter price for 1 tola, 10 tola and 10 gram silver.',
 h1='Silver Rate in Karachi Today',
 lead=f'In Karachi today, silver is {pk(ps)} per tola at the PSL rate and {pk(rs)} per tola at the Rawa rate. A 10 tola silver bar is {pk(ps*10)}.',
 product=('Silver per Tola - Karachi',ps),
 body=lambda:PSLT+RAWAT+cityrates('Karachi','the Karachi Sarafa Bazar')+NOTE_S+'''
<h2>Buying silver in Karachi</h2>
<p>Most silver in Karachi is traded in the Sarafa Bazar. Dealers sell both sealed bars and loose Rawa. If you want the easiest resale later, choose the sealed bar. If you want the lowest cost per tola, choose Rawa and get it tested.</p>
<ul><li>Bring your own weight in mind: 10 tola is 116.64 grams.</li><li>Check the scale reading before paying.</li><li>Ask for a bill that shows weight, purity and rate.</li></ul>'''+rel(['10-tola-silver-price-pakistan','gold-rate-today-karachi','silver-rate-lahore']),
 faqs=[('What is silver rate in Karachi today?',f'{pk(ps)} per tola (PSL) and {pk(rs)} per tola (Rawa). Last updated: {UP}.'),
       ('What is 10 tola silver price in Karachi today?',f'{pk(ps*10)} for a PSL bar and {pk(rs*10)} for Rawa.'),
       ('Where is silver sold in Karachi?','Mainly in the Sarafa Bazar, including Bolton Market and Saddar.')])

add('silver-rate-lahore',short='Lahore Silver',
 title='Silver Rate in Lahore Today (Sarafa Bazar, Suha Bazar Chandi Rate) | GoldSilverRate.pk',
 urdu='لاہور میں آج چاندی کا ریٹ۔',
 desc='Silver rate in Lahore today. Suha Bazar and Rang Mahal counter prices for chandi per tola and 10 tola.',
 h1='Silver Rate in Lahore Today',
 lead=f'In Lahore today, silver is {pk(ps)} per tola at the PSL rate and {pk(rs)} at the Rawa rate. A 10 tola silver bar is {pk(ps*10)}.',
 product=('Silver per Tola - Lahore',ps),
 body=lambda:PSLT+RAWAT+cityrates('Lahore','Suha Bazar and Rang Mahal')+NOTE_S+'''
<h2>Lahore Sarafa markets</h2>
<p>Suha Bazar and the lanes around Rang Mahal are the old centre of Lahore's gold and silver trade. Many wholesale dealers sit here, and small shops buy their stock from them. Prices are close to the national benchmark, with small differences by shop.</p>
<h2>Tips for buyers in Lahore</h2>
<ul><li>Ask for the rate per tola and the total for your weight, then check it yourself.</li><li>Compare a sealed bar and Rawa side by side.</li><li>Ask the shop what it pays to buy back, so you know your margin.</li><li>Keep your bill and the original pack of any sealed bar.</li></ul>'''+rel(['silver-rate-karachi','silver-rate-islamabad-rawalpindi','silver-rate-pakistan']),
 faqs=[('What is silver rate in Lahore today?',f'{pk(ps)} per tola (PSL) and {pk(rs)} per tola (Rawa). Last updated: {UP}.'),
       ('Where do people buy silver in Lahore?','Mainly Suha Bazar and the Rang Mahal area.'),
       ('Is Lahore silver price different from Karachi?','Usually only by a small amount that depends on the shop.')])

add('silver-rate-islamabad-rawalpindi',short='Islamabad Silver',
 title='Silver Rate in Islamabad & Rawalpindi Today (Chandi Rate per Tola) | GoldSilverRate.pk',
 urdu='اسلام آباد اور راولپنڈی میں آج چاندی کا ریٹ۔',
 desc='Silver rate in Islamabad and Rawalpindi today. F-7 Markaz and Rawalpindi Sarafa Bazar counter prices per tola.',
 h1='Silver Rate in Islamabad and Rawalpindi Today',
 lead=f'In Islamabad and Rawalpindi today, silver is {pk(ps)} per tola at the PSL rate and {pk(rs)} at the Rawa rate. A 10 tola silver bar is {pk(ps*10)}.',
 product=('Silver per Tola - Islamabad & Rawalpindi',ps),
 body=lambda:PSLT+RAWAT+cityrates('Islamabad','F-7 Markaz and the Rawalpindi Sarafa Bazar')+NOTE_S+'''
<h2>Two cities, two kinds of market</h2>
<p>In Islamabad, F-7 Markaz has modern jewellery shops with fixed price boards. In Rawalpindi, the main Sarafa Bazar near Raja Bazar is the older trading centre, where dealers sell to shops across the region. The base price is the same, but retail margins differ.</p>
<h2>Tips for buyers</h2>
<ul><li>Margins can differ between a modern shop and a bazar dealer for the same weight. Compare both.</li><li>Ask the buying price before you buy.</li><li>For large silver, test the purity at a second shop.</li></ul>'''+rel(['silver-rate-lahore','silver-rate-karachi','silver-rate-pakistan']),
 faqs=[('What is silver rate in Islamabad today?',f'{pk(ps)} per tola (PSL) and {pk(rs)} per tola (Rawa). Last updated: {UP}.'),
       ('Is silver cheaper in Rawalpindi?','It can be, depending on the shop. Compare a bazar dealer and a modern shop before you buy.'),
       ('How much is 10 tola silver in Islamabad?',f'{pk(ps*10)} for a PSL bar.')])

add('ary-kbe-gold-silver-bars',short='ARY, PSL, KBE Bars',
 title='ARY, PSL, KBE & PAMP Gold Silver Bar Price in Pakistan | GoldSilverRate.pk',
 urdu='اے آر وائی، پی ایس ایل اور کے بی ای بار کی قیمت۔',
 desc='ARY gold bar and KBE silver bar price in Pakistan. Compare sealed bars from ARY, PSL, KBE and Swiss PAMP.',
 h1='ARY, PSL, KBE and PAMP Gold & Silver Bar Price in Pakistan',
 lead=f'Sealed bars are priced close to the day rate plus a small premium. Today the PSL silver bar benchmark is {pk(ps)} per tola, and 24K gold is {pk(g24s)} per tola.',
 product=('Sealed Silver Bar (PSL benchmark, 10 tola)',ps*10),
 body=lambda:table('Benchmark bar prices today',[row('10 Tola Silver bar (PSL benchmark)',10,ps,pb),row('1 Tola 24K Gold bar (benchmark)',1,g24s,g24b),row('10 Gram 24K Gold bar (benchmark)',10*G,g24s,g24b)])+'''<p class="note">Brand bars from ARY, KBE and PAMP can carry a different premium from the benchmark. We do not have a separate price sheet for every brand, so use these as your reference and ask the dealer for the exact brand price.</p>
<h2>Sealed bar brands you will see</h2>
<p>ARY, PSL and KBE are well-known names in Pakistan's bullion market. PAMP is a Swiss refiner whose bars are sold in a sealed assay card. All four sell bars that come in a sealed pack with the weight and purity marked on it.</p>
<div class="tablebox"><table><caption>What to check on any sealed bar</caption><thead><tr><th scope="col">Check</th><th scope="col">What to look for</th><th scope="col">Why it matters</th></tr></thead><tbody>
<tr><td>Seal</td><td>Closed pack, no cuts or glue marks</td><td>A broken seal lowers the buyback price</td></tr>
<tr><td>Purity mark</td><td>999 for silver, 999.9 or 995 for gold</td><td>Shows the metal content</td></tr>
<tr><td>Weight mark</td><td>Weight printed on bar and pack</td><td>You can match it on a scale</td></tr>
<tr><td>Serial number</td><td>Same on bar, pack and bill</td><td>Proves the bar is the one you paid for</td></tr>
<tr><td>QR code or card</td><td>Scan it or read the assay card</td><td>Quick way to check the details</td></tr>
<tr><td>Bill</td><td>Date, weight, rate, shop name</td><td>You need it to resell</td></tr></tbody></table></div>
<h2>Buying tips</h2>
<ul><li>Buy from a shop that has a fixed place and a name you can trace.</li><li>Do not buy a bar with a pack that looks opened or re-sealed.</li><li>Ask what the shop pays to buy the same bar back.</li><li>Keep the pack, bill and bar together in a safe place.</li></ul>'''+rel(['psl-silver-rate-pakistan','1-kg-silver-bar','gold-rate-pakistan']),
 faqs=[('What is the price of a gold bar in Pakistan today?',f'Pure 24K gold benchmark is {pk(g24s)} per tola. A brand bar may add a small premium.'),
       ('How do I check a KBE or PSL silver bar?','Check the seal, scan the code if there is one, match the serial number and weigh it before paying.'),
       ('Which bar is easiest to resell?','Bars in their original sealed pack with the bill are easiest to resell.')])

add('gold-silver-calculator',short='Calculator',
 title='Gold & Silver Calculator Pakistan (Tola, Masha, Ratti to Gram) | GoldSilverRate.pk',
 urdu='سونا چاندی کیلکولیٹر: تولہ، ماشہ، رتی سے گرام۔',
 desc='Gold and silver calculator for Pakistan. Convert tola, masha and ratti to gram and work out jewellery cost with mazdoori and kaat.',
 h1='Gold and Silver Calculator for Pakistan',
 lead='Turn tola, masha, ratti and gram into each other, then see the price at today\'s rate. The jewellery estimator adds kaat and mazdoori so you know the full cost before you go to the shop.',
 product=('Gold and silver calculator',ps),
 body=lambda:calc_widget()+full_calc()+'''
<h2>Weight table</h2>
<div class="tablebox"><table><caption>Common conversions</caption><thead><tr><th scope="col">Unit</th><th scope="col">In grams</th><th scope="col">In tola</th></tr></thead><tbody>
<tr><td>1 Tola</td><td>11.664 g</td><td>1</td></tr><tr><td>1 Masha</td><td>0.972 g</td><td>0.0833</td></tr><tr><td>1 Ratti</td><td>0.1215 g</td><td>0.0104</td></tr><tr><td>10 Gram</td><td>10 g</td><td>0.857</td></tr><tr><td>1 KG</td><td>1000 g</td><td>85.73</td></tr></tbody></table></div>
<h2>What are kaat and mazdoori?</h2>
<p><strong>Kaat</strong> is the wastage the jeweller keeps for metal lost while making the piece. It is usually counted in masha or ratti per tola. <strong>Mazdoori</strong> is the making charge, usually a fixed amount per tola or a percentage. Both are on top of the metal price, so ask your jeweller to tell you each number clearly.</p>
<h2>Example</h2>
<p>A 2 tola 22K gold set with 0.5 masha kaat per tola and Rs 5,000 mazdoori per tola costs the metal value, plus the kaat in gold, plus Rs 10,000 making. Put your own numbers into the estimator to see the total.</p>'''+rel(['gold-rate-pakistan','silver-rate-pakistan']),
 faqs=[('How many masha in one tola?','12 masha.'),('How many ratti in one masha?','8 ratti.'),('How many grams in one tola?','11.664 grams.')])

TRUST={
'about':('About GoldSilverRate.pk','About Us','Who we are and how we work.',
'''<p>GoldSilverRate.pk is a simple website that shows daily gold and silver rates for Pakistan. We built it because most people cannot find the exact price for the weight they want to buy, such as 10 tola, 52 tola or 1 kilo, in one clear place.</p>
<h2>What we do</h2><p>We take the day's benchmark rate from the Sarafa Bazar and use one fixed formula to work out every weight: 1 tola = 11.664 grams. All pages use the same numbers, so rates never differ from page to page.</p>
<h2>How often we update</h2><p>Rates are updated on working days. The time of the last update is shown at the top of every rate page.</p>
<h2>What we are not</h2><p>We do not buy or sell gold or silver. We only share rates and simple guides. The price at your shop is the final price.</p>'''),
'contact':('Contact Us','Contact','How to reach GoldSilverRate.pk.',
'''<p>Found a wrong rate or have a question? Write to us by email and we will reply as soon as we can.</p>
<p><strong>Email:</strong> <a href="mailto:contact@goldsilverrate.pk">contact@goldsilverrate.pk</a></p>
<p>When you write about a rate, please tell us the page, the weight and the shop price you saw, so we can check it.</p>'''),
'privacy-policy':('Privacy Policy','Privacy Policy','How this site handles visitor information.',
'''<p>Last updated: 13 November 2026.</p>
<h2>What we collect</h2><p>This site does not ask visitors for names, phone numbers or any personal details. The calculators run in your browser and the numbers you type are not sent to us.</p>
<h2>Cookies and ads</h2><p>We may use basic analytics to see which pages are read. If we show ads in future, ad partners such as Google may use cookies to show ads based on earlier visits to this and other websites. You can turn off personalised ads in your Google ad settings.</p>
<h2>Links to other sites</h2><p>Some pages may link to other websites. We are not responsible for what those sites do with your information.</p>
<h2>Changes</h2><p>We may update this policy. The date at the top shows the latest change.</p>
<h2>Questions</h2><p>Write to <a href="mailto:contact@goldsilverrate.pk">contact@goldsilverrate.pk</a>.</p>'''),
'disclaimer':('Disclaimer','Disclaimer','Please read before you use the rates.',
'''<p>The rates on this website are for information only. They are benchmark rates and may differ from the price at your jeweller or dealer, and they can change during the day.</p>
<ul><li>We do not buy or sell gold or silver.</li><li>Prices do not include making charges, tax or packing.</li><li>Buying prices for some karats are estimated from the 24K gap and are marked as such.</li><li>Gold and silver prices can fall as well as rise. Nothing here is financial advice.</li><li>Confirm the final price, weight and purity with your dealer before you pay.</li></ul>'''),
}

SVGICON="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='15' fill='%23f59e0b'/%3E%3Ccircle cx='16' cy='16' r='9' fill='none' stroke='%230b0d10' stroke-width='2'/%3E%3C/svg%3E"
RATES_JSON=json.dumps(D,separators=(',',':'))

def head(title,desc,url,schemas):
    title=title.replace('&','&amp;'); desc=desc.replace('&','&amp;')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b0d10">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="GoldSilverRate.pk">
<link rel="icon" href="{SVGICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Playfair+Display:wght@600;700&display=swap">
<link rel="stylesheet" href="/css/style.css">
'''+''.join(f'<script type="application/ld+json">{json.dumps(s,ensure_ascii=False)}</script>\n' for s in schemas)+'</head>\n'

def shell(path,body_inner,ticker=''):
    nav=''.join(f'<a href="{h}"{" class=on" if h==path else ""}>{t}</a>' for h,t in NAV)
    return f'''<body>
<header><div class="wrap bar"><a class="logo" href="/">Gold<b>Silver</b><span>Rate</span>.pk</a><nav aria-label="Main">{nav}</nav></div></header>
{ticker}<main class="wrap">{body_inner}</main>
<footer><div class="wrap"><div class="cols">
<div><h3>GoldSilverRate.pk</h3><p>Daily gold and silver rates for Pakistan, worked out from one Sarafa Bazar benchmark. 1 Tola = 11.664 Grams.</p><p>Rates are for information. Confirm the final price with your dealer.</p></div>
<div><h3>Silver</h3><a href="/silver-rate-pakistan">Silver rate in Pakistan</a><a href="/psl-silver-rate-pakistan">PSL silver rate</a><a href="/10-tola-silver-price-pakistan">10 tola silver</a><a href="/52-tola-chandi-price-pakistan">52 tola chandi</a><a href="/1-kg-silver-bar">1 KG silver</a><a href="/1-tola-silver-price-pakistan">1 tola silver</a><a href="/10-gram-silver-price-pakistan">10 gram silver</a><a href="/silver-rate-karachi">Silver Karachi</a><a href="/silver-rate-lahore">Silver Lahore</a><a href="/silver-rate-islamabad-rawalpindi">Silver Islamabad</a></div>
<div><h3>Gold and more</h3><a href="/gold-rate-pakistan">Gold rate in Pakistan</a><a href="/gold-rate-today-karachi">Gold rate Karachi</a><a href="/ary-kbe-gold-silver-bars">ARY, KBE, PSL bars</a><a href="/gold-silver-calculator">Calculator</a><a href="/about">About</a><a href="/contact">Contact</a><a href="/privacy-policy">Privacy Policy</a><a href="/disclaimer">Disclaimer</a></div>
</div><p class="copy">&copy; 2026 GoldSilverRate.pk. All rights reserved.</p></div></footer>
<script type="application/json" id="rates">{RATES_JSON}</script>
<script src="/js/main.js" defer></script>
</body></html>'''

def crumbs(items):
    return '<nav class="crumbs" aria-label="Breadcrumb">'+' &rsaquo; '.join(f'<a href="{h}">{t}</a>' if h else t for h,t in items)+'</nav>'
def bc_schema(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"item":SITE+(h if h!='/' else '/')} for i,(h,t) in enumerate(items)]}
def product_schema(name,price,url):
    return {"@context":"https://schema.org","@type":"Product","name":name,"description":f"{name} price in Pakistan. Last updated: {UP}.","url":url,
      "offers":{"@type":"Offer","price":str(round(price)),"priceCurrency":"PKR","availability":"https://schema.org/InStock","url":url}}
def faq_schema(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
def write(name,html):
    open(f'{OUT}/{name}','w',encoding='utf-8').write(html)

urls=[('/','1.0')]
for slug,p in PAGES.items():
    path='/'+slug; url=SITE+path
    items=[('/','Home'),(path,p['short'])]
    desc=f"{p['desc']} {p['urdu']}"
    sch=[bc_schema(items),product_schema(p['product'][0],p['product'][1],url)]
    if p.get('faq_schema'): sch.append(faq_schema(p['faqs']))
    inner=crumbs(items)+f'<section class="hero"><span class="stamp"><i></i>Updated: {UP}</span><h1>{p["h1"]}</h1><p class="lead">{p["lead"]}</p></section>'+p['body']()+faq_html(p['faqs'])
    write(slug+'.html',head(p['title'],desc,url,sch)+shell(path,inner))
    urls.append((path,'0.9'))

# trust pages
for slug,(h1,short,desc,body) in TRUST.items():
    path='/'+slug;url=SITE+path
    items=[('/','Home'),(path,short)]
    inner=crumbs(items)+f'<section class="hero"><h1>{h1}</h1></section><div class="card">{body}</div>'
    write(slug+'.html',head(f'{h1} | GoldSilverRate.pk',desc,url,[bc_schema(items)])+shell(path,inner))
    urls.append((path,'0.3'))

# homepage
ticker=f'<div class="ticker"><div><span class="g">GOLD 24K <b>{pk(g24s)}</b> /tola</span><span class="g">22K <b>{pk(g22s)}</b></span><span class="s">SILVER PSL <b>{pk(ps)}</b> /tola</span><span class="s">RAWA <b>{pk(rs)}</b></span><span>10 Tola PSL bar <b>{pk(ps*10)}</b></span></div></div>'
home_title='Silver & Gold Rate in Pakistan Today (Live Sarafa Market & PSL 10 Tola Bar) | GoldSilverRate.pk'
home_desc='Live Gold and Silver Rate in Pakistan today. پاکستان میں آج سونے اور چاندی کا ریٹ. Check 24K Gold, PSL 10 Tola Silver Bar & Rawa rates.'
hf=[('What is the gold rate in Pakistan today?',f'24K gold is {pk(g24s)} per tola. Last updated: {UP}.'),
    ('What is the silver rate in Pakistan today?',f'PSL silver is {pk(ps)} per tola and Rawa is {pk(rs)} per tola.'),
    ('How many grams are in one tola?','One tola is 11.664 grams. Ten grams is about 0.857 tola.')]
hb=f'''<section class="hero"><span class="stamp"><i></i>Updated: {UP}</span><h1>Silver &amp; Gold Rate in Pakistan Today</h1><p class="lead">Simple daily rates for gold and silver, with the exact price for the weight you want. Tola, 10 gram, 10 tola, 52 tola and 1 kilo are all here.</p></section>
<div class="grid two">
<div class="card gold"><h2>Gold - 24K</h2><div class="price-row"><div class="price"><small>Selling (per tola)</small><strong>{pk(g24s)}</strong></div><div class="price"><small>Buying (per tola)</small><strong>{pk(g24b)}</strong></div></div><p class="note">22K: {pk(g22s)} &middot; 21K: {pk(g21s)} per tola</p><a href="/gold-rate-pakistan">See all gold rates &rarr;</a></div>
<div class="card silver"><h2>Silver - PSL Bar</h2><div class="price-row"><div class="price"><small>Selling (per tola)</small><strong>{pk(ps)}</strong></div><div class="price"><small>Buying (per tola)</small><strong>{pk(pb)}</strong></div></div><p class="note">Rawa: {pk(rs)} selling &middot; {pk(rb)} buying per tola</p><a href="/silver-rate-pakistan">See all silver rates &rarr;</a></div></div>
<h2>Calculator</h2>{calc_widget()}
<h2>All weights at a glance</h2>{PSLT}{RAWAT}{GOLDT}{NOTE_G}
<h2>Pick your page</h2>
<div class="grid three">
<div class="card"><h3>Silver by weight</h3><p><a href="/1-tola-silver-price-pakistan">1 tola</a> &middot; <a href="/10-gram-silver-price-pakistan">10 gram</a> &middot; <a href="/10-tola-silver-price-pakistan">10 tola</a> &middot; <a href="/52-tola-chandi-price-pakistan">52 tola</a> &middot; <a href="/1-kg-silver-bar">1 kg</a></p></div>
<div class="card"><h3>City rates</h3><p><a href="/gold-rate-today-karachi">Karachi gold</a> &middot; <a href="/silver-rate-karachi">Karachi silver</a> &middot; <a href="/silver-rate-lahore">Lahore</a> &middot; <a href="/silver-rate-islamabad-rawalpindi">Islamabad &amp; Rawalpindi</a></p></div>
<div class="card"><h3>Bars and tools</h3><p><a href="/psl-silver-rate-pakistan">PSL bars</a> &middot; <a href="/ary-kbe-gold-silver-bars">ARY, KBE, PAMP</a> &middot; <a href="/gold-silver-calculator">Tola, masha, ratti calculator</a></p></div></div>
<h2>Why Sarafa Bazar rates differ from news rates</h2>
<p>News sites often show only the 24K gold rate, or the world price changed into rupees. When you walk into a Sarafa Bazar shop, you see something else: a rate for the bar, a rate for loose Rawa, a selling price and a lower buying price. This site shows all of them together, so you know what to expect at the counter.</p>
<h2>How to use these rates</h2>
<ol><li>Find your weight in the tables above.</li><li>Check the update time at the top.</li><li>Visit two shops and ask for the same karat or bar.</li><li>Take a bill with date, weight and rate.</li></ol>
<p>The difference between selling and buying price is the dealer margin. It is the amount the price has to rise before you break even, so keep it in mind.</p>'''
hitems=[('/','Home')]
inner=hb+faq_html(hf)
hsch=[bc_schema(hitems),{"@context":"https://schema.org","@type":"WebSite","name":"GoldSilverRate.pk","url":SITE+"/"},product_schema('24K Gold per Tola in Pakistan',g24s,SITE+'/'),product_schema('PSL Silver per Tola in Pakistan',ps,SITE+'/')]
write('index.html',head(home_title,home_desc,SITE+'/',hsch)+shell('/',inner,ticker))

write('404.html',head('Page not found | GoldSilverRate.pk','This page could not be found.',SITE+'/404',[])+shell('',f'<section class="hero"><h1>Page not found</h1><p class="lead">This page is not here. Go back to the <a href="/">home page</a> for today\'s rates.</p></section>'))

sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p,pr in urls: sm+=f'<url><loc>{SITE}{p}</loc><lastmod>{DATE}</lastmod><changefreq>daily</changefreq><priority>{pr}</priority></url>\n'
write('sitemap.xml',sm+'</urlset>\n')
write('robots.txt',f'User-agent: *\nAllow: /\nDisallow: /scripts/\n\nSitemap: {SITE}/sitemap.xml\n')
write('_headers','/css/*\n  Cache-Control: public, max-age=86400\n/js/*\n  Cache-Control: public, max-age=86400\n/data/*\n  Cache-Control: public, max-age=300\n')
print(len(urls),'urls')
