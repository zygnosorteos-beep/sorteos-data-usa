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

def procesar_sorteos_usa():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(BASE_DIR, 'raw_csv_usa')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'docs')

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Procesar Texas Cash Five
    csv_texas = os.path.join(INPUT_DIR, 'texas_cash_five.csv')
    if os.path.exists(csv_texas):
        try:
            records = []
            with open(csv_texas, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or len(row) < 9:
                        continue
                    
                    # Detectar si es cabecera
                    if 'FECHA' in str(row[0]).upper() or 'CONCURSO' in str(row[0]).upper():
                        continue
                    
                    # Formato oficial Texas Lottery: Cash Five,Month,Day,Year,N1,N2,N3,N4,N5
                    try:
                        month = int(row[1])
                        day = int(row[2])
                        year = int(row[3])
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

            print(f"[OK] Generado correctamente: {out_tx} ({len(json_texas)} sorteos)")
        except Exception as e:
            print(f"[ERROR] Error procesando Texas Cash Five: {e}")
    else:
        print(f"[AVISO] No se encontro: {csv_texas}")

    # 2. Procesar Powerball
    csv_pb = os.path.join(INPUT_DIR, 'powerball.csv')
    if os.path.exists(csv_pb):
        try:
            records = []
            with open(csv_pb, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or len(row) < 10:
                        continue
                    
                    # Detectar cabecera
                    if 'FECHA' in str(row[0]).upper() or 'CONCURSO' in str(row[0]).upper():
                        continue

                    # Formato oficial Texas Lottery: Powerball,Month,Day,Year,N1,N2,N3,N4,N5,PB,PowerPlay
                    try:
                        month = int(row[1])
                        day = int(row[2])
                        year = int(row[3])
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

            print(f"[OK] Generado correctamente: {out_pb} ({len(json_pb)} sorteos)")
        except Exception as e:
            print(f"[ERROR] Error procesando Powerball: {e}")
    else:
        print(f"[AVISO] No se encontro: {csv_pb}")

if __name__ == '__main__':
    procesar_sorteos_usa()
