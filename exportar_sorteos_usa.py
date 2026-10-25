import os
import sys
import json
import csv
from datetime import datetime

# Configurar salida UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def parse_date(date_str):
    if not date_str:
        return None
    date_str = str(date_str).strip()
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return None

def procesar_todos_sorteos():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_USA = os.path.join(BASE_DIR, 'raw_csv_usa')
    INPUT_MEX = os.path.join(BASE_DIR, 'raw_csv')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'docs')

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ==========================================
    # 1. Procesar Texas Cash Five (USA)
    # ==========================================
    csv_texas = os.path.join(INPUT_USA, 'texas_cash_five.csv')
    if os.path.exists(csv_texas):
        try:
            records = []
            with open(csv_texas, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or len(row) < 9:
                        continue
                    if 'FECHA' in str(row[0]).upper() or 'CONCURSO' in str(row[0]).upper():
                        continue
                    try:
                        month, day, year = int(row[1]), int(row[2]), int(row[3])
                        d_obj = datetime(year, month, day)
                        date_iso = d_obj.strftime('%Y-%m-%d')
                        id_concurso = int(d_obj.strftime('%Y%m%d'))
                        nums = sorted([int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8])])
                        records.append({
                            'date_obj': d_obj,
                            'data': {
                                'idConcurso': id_concurso,
                                'fecha': date_iso,
                                'numeros': nums
                            }
                        })
                    except Exception:
                        continue

            records.sort(key=lambda x: x['date_obj'], reverse=True)
            json_texas = [r['data'] for r in records]
            out_tx = os.path.join(OUTPUT_DIR, 'resultados_texas_cash_five.json')
            with open(out_tx, 'w', encoding='utf-8') as f:
                json.dump(json_texas, f, ensure_ascii=False, indent=2)
            print(f"[OK] Generado: {out_tx} ({len(json_texas)} sorteos)")
        except Exception as e:
            print(f"[ERROR] Error procesando Texas Cash Five: {e}")

    # ==========================================
    # 2. Procesar Powerball (USA)
    # ==========================================
    csv_pb = os.path.join(INPUT_USA, 'powerball.csv')
    if os.path.exists(csv_pb):
        try:
            records = []
            with open(csv_pb, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or len(row) < 10:
                        continue
                    if 'FECHA' in str(row[0]).upper() or 'CONCURSO' in str(row[0]).upper():
                        continue
                    try:
                        month, day, year = int(row[1]), int(row[2]), int(row[3])
                        d_obj = datetime(year, month, day)
                        date_iso = d_obj.strftime('%Y-%m-%d')
                        id_concurso = int(d_obj.strftime('%Y%m%d'))
                        nums = sorted([int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8])])
                        pb = int(row[9])
                        records.append({
                            'date_obj': d_obj,
                            'data': {
                                'idConcurso': id_concurso,
                                'fecha': date_iso,
                                'numeros': nums,
                                'adicional': pb
                            }
                        })
                    except Exception:
                        continue

            records.sort(key=lambda x: x['date_obj'], reverse=True)
            json_pb = [r['data'] for r in records]
            out_pb = os.path.join(OUTPUT_DIR, 'resultados_powerball.json')
            with open(out_pb, 'w', encoding='utf-8') as f:
                json.dump(json_pb, f, ensure_ascii=False, indent=2)
            print(f"[OK] Generado: {out_pb} ({len(json_pb)} sorteos)")
        except Exception as e:
            print(f"[ERROR] Error procesando Powerball: {e}")

    # ==========================================
    # 3. Procesar Chispazo (México)
    # ==========================================
    csv_chispazo = os.path.join(INPUT_MEX, 'Chispazo.csv')
    if os.path.exists(csv_chispazo):
        try:
            items = []
            with open(csv_chispazo, 'r', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        concurso = int(r['CONCURSO'])
                        d_obj = parse_date(r['FECHA'])
                        fecha_iso = d_obj.strftime('%Y-%m-%d') if d_obj else str(r['FECHA'])
                        nums = [int(r['R1']), int(r['R2']), int(r['R3']), int(r['R4']), int(r['R5'])]
                        items.append({
                            "idConcurso": concurso,
                            "fecha": fecha_iso,
                            "numeros": nums
                        })
                    except Exception:
                        continue

            items.sort(key=lambda x: x['idConcurso'], reverse=True)
            out_ch = os.path.join(OUTPUT_DIR, 'resultados_chispazo.json')
            with open(out_ch, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"[OK] Generado: {out_ch} ({len(items)} sorteos)")
        except Exception as e:
            print(f"[ERROR] Error procesando Chispazo: {e}")

    # ==========================================
    # 4. Procesar Melate Retro (México)
    # ==========================================
    csv_retro = os.path.join(INPUT_MEX, 'melate_retro.csv')
    if os.path.exists(csv_retro):
        try:
            items = []
            with open(csv_retro, 'r', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        concurso = int(r['CONCURSO'])
                        d_obj = parse_date(r['FECHA'])
                        fecha_iso = d_obj.strftime('%Y-%m-%d') if d_obj else str(r['FECHA'])
                        nums = [int(r['F1']), int(r['F2']), int(r['F3']), int(r['F4']), int(r['F5']), int(r['F6'])]
                        adicional = int(r['F7'])
                        items.append({
                            "idConcurso": concurso,
                            "fecha": fecha_iso,
                            "numeros": nums,
                            "adicional": adicional
                        })
                    except Exception:
                        continue

            items.sort(key=lambda x: x['idConcurso'], reverse=True)
            out_retro = os.path.join(OUTPUT_DIR, 'resultados_melate.json')
            with open(out_retro, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"[OK] Generado: {out_retro} ({len(items)} sorteos)")
        except Exception as e:
            print(f"[ERROR] Error procesando Melate Retro: {e}")

    # ==========================================
    # 5. Procesar Melate Tradicional (Principal - México)
    # ==========================================
    csv_melate = os.path.join(INPUT_MEX, 'Melate.csv')
    if os.path.exists(csv_melate):
        try:
            items = []
            with open(csv_melate, 'r', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        concurso = int(r['CONCURSO'])
                        d_obj = parse_date(r['FECHA'])
                        fecha_iso = d_obj.strftime('%Y-%m-%d') if d_obj else str(r['FECHA'])
                        nums = [int(r['R1']), int(r['R2']), int(r['R3']), int(r['R4']), int(r['R5']), int(r['R6'])]
                        adicional = int(r['R7'])
                        items.append({
                            "idConcurso": concurso,
                            "fecha": fecha_iso,
                            "numeros": nums,
                            "adicional": adicional
                        })
                    except Exception:
                        continue

            items.sort(key=lambda x: x['idConcurso'], reverse=True)
            out_melate = os.path.join(OUTPUT_DIR, 'resultados_melate_principal.json')
            with open(out_melate, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"[OK] Generado: {out_melate} ({len(items)} sorteos)")
        except Exception as e:
            print(f"[ERROR] Error procesando Melate Principal: {e}")

if __name__ == '__main__':
    procesar_todos_sorteos()
