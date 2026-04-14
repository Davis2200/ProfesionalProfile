import pandas as pd
from sqlalchemy import text
import sys
import os

# Configuración de ruta para database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import engine

def clean_duplicate_games():
    print("🧹 Iniciando limpieza profunda de la tabla 'games'...")
    
    with engine.begin() as conn:
        # 1. Identificar juegos duplicados (versión corta vs versión con ceros)
        # Traemos todos los IDs para procesar en memoria y no saturar SQL
        query_games = "SELECT game_id FROM games"
        all_ids = pd.read_sql(query_games, conn)['game_id'].tolist()
        
        # Diccionario para mapear ID corto -> ID largo (00...)
        mapping = {}
        for gid in all_ids:
            long_id = str(gid).zfill(10)
            if str(gid) != long_id and long_id in all_ids:
                mapping[str(gid)] = long_id

        if not mapping:
            print("✨ No se encontraron duplicados lógicos (corto vs largo).")
        else:
            print(f"found {len(mapping)} juegos con IDs duplicados. Corrigiendo referencias...")

            # 2. Desactivar restricciones temporalmente (opcional en algunas configuraciones, 
            # pero mejor lo hacemos mediante updates directos)
            
            tables_to_fix = [
                'players_stats', 
                'mean_players', 
                'player_advanced_metrics', 
                'team_defense_history',
                'game_lineups'
            ]

            for old_id, new_id in mapping.items():
                # Actualizar cada tabla dependiente para que use el ID de 10 dígitos
                for table in tables_to_fix:
                    conn.execute(text(f"""
                        UPDATE {table} 
                        SET game_id = :new_id 
                        WHERE game_id = :old_id
                    """), {"new_id": new_id, "old_id": old_id})
                
                # Una vez actualizadas las referencias, borrar el ID corto de la tabla maestra
                conn.execute(text("DELETE FROM games WHERE game_id = :old_id"), {"old_id": old_id})

            print(f"✅ Se eliminaron {len(mapping)} registros duplicados y se actualizaron las dependencias.")

        # 3. Estandarización final: Asegurar que TODO lo que quedó tenga 10 dígitos
        print("📏 Asegurando formato de 10 dígitos en todos los registros restantes...")
        
        # Lista de tablas para aplicar el LPAD final
        all_tables = ['games', 'players_stats', 'mean_players', 'player_advanced_metrics']
        
        for table in all_tables:
            conn.execute(text(f"""
                UPDATE {table} 
                SET game_id = LPAD(game_id::text, 10, '0') 
                WHERE LENGTH(game_id::text) < 10
            """))
            
        print("🚀 Limpieza completada con éxito.")

if __name__ == "__main__":
    clean_duplicate_games()