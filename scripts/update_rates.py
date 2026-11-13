#!/usr/bin/env python3
"""Update data/rates.json from world gold/silver prices and the USD-PKR rate,
then rebuild every page. Uses only the Python standard library.

Safe by design: if anything looks wrong (no data, old data, a jump bigger than
max_change_pct) it keeps the old rates and exits without changing files.
"""
import json, os, sys, subprocess, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATES = os.path.join(ROOT, 'data', 'rates.json')
CONF = os.path.join(ROOT, 'scripts', 'config.json')
OZ = 31.1034768
TOLA = 11.664

def get(url):
    mock = os.environ.get('RATES_MOCK_DIR')
    if mock:  # used only for testing
        name = 'spot.json' if 'xaus' in url else 'fx.json'
        with open(os.path.join(mock, name)) as f:
            return json.load(f)
    req = urllib.request.Request(url, headers={'User-Agent': 'goldsilverrate-updater/1.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def rebuild():
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'build.py')], check=True)

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

def save(p, d):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')

def rnd(x, step):
    return int(round(x / step) * step)

def world_prices():
    spot = get('https://xaus.com/api/v1/spot?currency=PKR')
    ds = spot.get('data_state') or {}
    if spot.get('stale') or (ds.get('status') not in (None, 'fresh') and ds.get('age_seconds', 0) > 3600):
        raise ValueError('price data is old')
    gold = float(spot['spot_usd_oz'])
    silver = float(spot['silver_usd_oz'])
    fx = (spot.get('fx_rates') or {}).get('PKR')
    if not fx and spot.get('fx_rate') not in (None, 1, 1.0):
        fx = spot['fx_rate']
    if not fx:
        fx = get('https://open.er-api.com/v6/latest/USD')['rates']['PKR']
    fx = float(fx)
    if not (500 < gold < 30000 and 5 < silver < 500 and 50 < fx < 1000):
        raise ValueError(f'values out of range: gold={gold} silver={silver} fx={fx}')
    return gold, silver, fx

def main():
    conf = load(CONF)
    # Scheduled runs happen every hour, but only update on even Pakistan hours
    # (every 2 hours) to save Cloudflare builds. Manual runs always update.
    if os.environ.get('GITHUB_EVENT_NAME') == 'schedule' and conf.get('every_hours', 2) > 1:
        if datetime.now(ZoneInfo('Asia/Karachi')).hour % conf.get('every_hours', 2) != 0:
            print('Skipping this hour (updates every', conf.get('every_hours', 2), 'hours)')
            return 0
    if conf.get('mode') == 'manual':
        print('manual mode: rebuilding pages only')
        rebuild()
        return 0
    old = load(RATES)
    try:
        gold, silver, fx = world_prices()
    except Exception as e:
        print('SKIP: could not get good prices:', e)
        return 0

    world_gold_tola = gold / OZ * TOLA * fx
    world_silver_tola = silver / OZ * TOLA * fx

    # first run: learn the Sarafa premium from the rates already in the file
    changed_conf = False
    if conf.get('gold_premium_pct') is None:
        conf['gold_premium_pct'] = round((old['gold']['24k_tola_sell'] / world_gold_tola - 1) * 100, 3)
        changed_conf = True
    if conf.get('silver_premium_pct') is None:
        conf['silver_premium_pct'] = round((old['silver']['psl_tola_sell'] / world_silver_tola - 1) * 100, 3)
        changed_conf = True
    if conf.get('rawa_to_psl_ratio') is None:
        conf['rawa_to_psl_ratio'] = round(old['silver']['rawa_tola_sell'] / old['silver']['psl_tola_sell'], 5)
        changed_conf = True

    g24 = rnd(world_gold_tola * (1 + conf['gold_premium_pct'] / 100), conf['gold_round_to'])
    psl = rnd(world_silver_tola * (1 + conf['silver_premium_pct'] / 100), conf['silver_round_to'])
    rawa = rnd(psl * conf['rawa_to_psl_ratio'], conf['silver_round_to'])

    for new, prev, name in ((g24, old['gold']['24k_tola_sell'], 'gold'), (psl, old['silver']['psl_tola_sell'], 'silver')):
        if abs(new / prev - 1) * 100 > conf['max_change_pct']:
            print(f'SKIP: {name} moved more than {conf["max_change_pct"]}% ({prev} -> {new}). Check the source and config.')
            return 0

    now = datetime.now(ZoneInfo('Asia/Karachi'))
    new = {
        'last_updated': now.strftime('%d %b %Y, %I:%M %p PKT').lstrip('0'),
        'updated_iso': now.strftime('%Y-%m-%dT%H:%M:%S+05:00'),
        'silver': {
            'psl_tola_sell': psl,
            'psl_tola_buy': psl - conf['silver_psl_spread'],
            'rawa_tola_sell': rawa,
            'rawa_tola_buy': rawa - conf['silver_rawa_spread'],
        },
        'gold': {
            '24k_tola_sell': g24,
            '24k_tola_buy': g24 - conf['gold_24k_spread'],
            '22k_tola_sell': rnd(g24 * 22 / 24, 1),
            '21k_tola_sell': rnd(g24 * 21 / 24, 1),
        },
    }
    if changed_conf:
        save(CONF, conf)
    if new['silver'] == old.get('silver') and new['gold'] == old.get('gold'):
        print('Prices unchanged: nothing to publish.')
        if changed_conf:
            save(RATES, old)
        return 0
    save(RATES, new)
    rebuild()
    print('Updated:', new['last_updated'], '| gold 24K', g24, '| silver PSL', psl)
    return 0

if __name__ == '__main__':
    sys.exit(main())
